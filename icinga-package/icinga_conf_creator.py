from jinja2 import Environment
from jinja2 import FileSystemLoader
import IcingaConfigure
import sys
import os
import errno
import json
import traceback
import copy
import datetime
import re
import logging
import logging.handlers
from mongo_dao import NotificationDao
import requests

icinga_suffix = "_dict"
no_record_nodes = []
service_groups = set([])



now = datetime.datetime.now()
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setLevel(logging.INFO)
formatter = logging.Formatter("%(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)




def fetch_hosts():
	logger.info("Fetching hosts from swarm")
	Host_url="http://swarmapi.turbatio.zycus.com/hosts"
	hosts = initiateGetRequest(Host_url)
	return hosts

def initiateGetRequest(url,cred=None,headers=None):
	response = None
	logger.info("HITTING "+url)
	print "waiting...!"
	response  = requests.get(url,verify=False,auth=cred).json();
	print "received..."
	return response


def get_from_mongo(notification_obj,database,collection,query,lim):
	print "fetching"
	cursor =  notification_obj.database(database).collectn(collection).find(query,lim)
	print "iterating"
	docs = []
	if cursor.count()>0:
		logger.info("Fetched info from database.")
		for doc in cursor:
			docs.append(doc)
		return docs
	else:
		logger.warn("No record found...")
		pass

def fetch_and_modify(ip,data=None):
	notification_dao = NotificationDao(IcingaConfigure.MONGO_CLIENT,IcingaConfigure.MONGO_PORT)
	if data==None:
		data = get_from_mongo(notification_dao,IcingaConfigure.MONGO_DB,IcingaConfigure.MONGO_COLLECTION,{'ip':ip,'active':1},1)[0]
	if data:
		logger.info("Fetched info from database."+ip)
		docs = get_from_mongo(notification_dao,IcingaConfigure.MONGO_DB,IcingaConfigure.THRESHOLD_COLLECTION,{"hostaddress":ip},lim=1)
		thresholds = None
		if docs and len(docs)>0:
			temp = docs[0]
			validity = temp['validity']
			if datetime.datetime.strptime(validity, '%d/%m/%Y') >= now and temp['confirmed'] == True:
				thresholds = temp
				print "Printed"
		data["thresholds"] = thresholds
		return data

	else:
		no_record_nodes.append(ip)
		logger.exception("No record found on node"+ip)
		raise Exception("No records for the node:"+ip+" can be found in mongo")


def templating(machine):
	logger.info("Templating ")
	global_tags = set([])
	machine_info = machine['machine_info']
	host_name = machine_info['hostname']
	proc_info = machine['details']
	icinga_host = copy.deepcopy(IcingaConfigure.icinga_host)
	icinga_host['service_tags'] = global_tags
	icinga_host['thresholds'] = machine['thresholds']
	icinga_host = templatize_process(proc_info,icinga_host)
	icinga_host = templatize_machine(machine_info,icinga_host,machine['ip'],machine['env'])
	return icinga_host

def save_to_satellite(icinga_host):
	def my_finalize(thing):
		return thing if thing is not None else ''

	def create_list(var,temp_list):
		temp_list.append(str(var).encode("utf-8"))
		return json.dumps(temp_list)

	jinja_env = Environment(loader = FileSystemLoader([IcingaConfigure.TEMPLATE_PATH]),trim_blocks=True,lstrip_blocks=True,finalize=my_finalize)
	jinja_env.trim_blocks=True
	jinja_env.lstrip_blocks=True
	jinja_env.filters['getList'] = create_list
	icinga_template = jinja_env.get_template(IcingaConfigure.ICINGA_HOST_TEMPLATE)
	rendered_template = icinga_template.render(icinga_host=icinga_host)
	path = os.path.join(IcingaConfigure.SAVE_PATH, icinga_host['satellite_name'])
	try:
		if not os.path.exists(path):
			os.makedirs(path)

		file_name = os.path.join(path,icinga_host['host_name']+".conf")
		conf_file = open(file_name,'w')
		conf_file.write(rendered_template)
		conf_file.close()
		return os.path.exists(file_name),file_name
	except OSError as exception:
		if exception.errno != errno.EEXIST:
			logger.error("No configuration file can be generated at:"+str(path))
			raise Exception(exception.message())


def fetch_satellite_info(ip):
	satellite_info = IcingaConfigure.satellite_info
	p = re.compile(r'\b'+ip+r'\b',re.IGNORECASE)
	for k,v in satellite_info.iteritems():
		servers = v['servers']
		for s in servers:
			p = re.compile(r'\b'+s+r'\b',re.IGNORECASE)
			if p.search(ip):
				return v['address'],v['name'],k



def templatize_process(proc_info,icinga_host):
	logger.info("[INFO]:Templating Process")
	proc_details = {}
	icinga_services = copy.deepcopy(IcingaConfigure.icinga_services)
	icinga_service_keys = [x.lower() for x in  icinga_services.keys()]
	try:
		if proc_info:
			for pid in proc_info:
				if proc_info[pid]['tags']:
					proc_details[pid] = proc_info[pid]
		for proc in proc_details:
			connections = proc_details[proc]['connections']
			if connections: 
				port_list = list(set([conn[3][1] for conn in connections if conn[5]=="LISTEN"]))
				proc_details[proc]['port_list'] = port_list
				proc_details[proc]['port'] = port_list
			tags = [tag.encode("utf-8").lower() for tag in proc_details[proc]['tags']]
			icinga_host["service_tags"].update(tags)
			proc_details[proc]['app_name'] = tags[0]
			for tag in tags:
				service_groups.add(tag.encode("utf-8"))
				if tag in icinga_services.keys():
					var = tag+icinga_suffix
					exec("ser_dict = copy.deepcopy(IcingaConfigure.%s)" % (var))
					for k in ser_dict.keys():
						if k in proc_details[proc].keys():
							ser_dict[k] = proc_details[proc][k]
							if str(k) == 'tags':
								ser_dict[k] = json.dumps([s.encode("utf-8") for s in proc_details[proc][k]])

					if ser_dict not in icinga_services[tag]:
						icinga_services[tag].append(ser_dict)
					break
		for service in icinga_services:
			icinga_host[service] = icinga_services[service]
		return icinga_host
	except Exception ,e:
		raise Exception(e)
		



def templatize_machine(machine_info,icinga_host,ip,env):
	logger.info("[INFO]:Templating machine")
	satellite_info = copy.deepcopy(IcingaConfigure.satellite_info)
	sat_ip,sat_name,sat_env = fetch_satellite_info(ip)
	icinga_host['host_name'] = machine_info['hostname']
	icinga_host['address'] = machine_info['address']
	icinga_host['satellite_name'] = sat_name
	icinga_host['node_env'] = sat_env
	icinga_host['os'] = machine_info['os'].lower()
	icinga_host['satellite_address'] = sat_ip
	icinga_host['service_tags'].add(machine_info['linux_distribution'][0].encode("utf-8").lower())
	icinga_host['service_tags'].add(machine_info['system_manufacturer']);
	icinga_host['service_tags'] = list(icinga_host['service_tags'])
	icinga_host['service_tags'] = json.dumps(icinga_host['service_tags'])
	mount_points = []
	disk_partitions = machine_info['disk_partitions']
	for parts in disk_partitions:
		mounts = {}
		name = parts['part'][1]
		mounts['name'] = name
		mount_points.append(mounts)
	icinga_host['mount_points'] = mount_points
	return icinga_host

	 
def exec_auto(ip=None,host_type=None):
	nodes = []
	if ip:
		if host_type and host_type == 'node':
			logger.info('Generating configuration for single node: '+ip)
			nodes.append(ip)
		elif host_type and host_type == 'satellite':
			logger.info('Generating configuration for all nodes belonging to satellite: '+ip)
			logger.info('Fetching satellite info')
			sat_info = copy.deepcopy(IcingaConfigure.satellite_info)
			isSatellite = False
			for sat in sat_info:
				if sat_info[sat]['address'] == ip:
					split_ip = ip.split('.')
					prefix = split_ip[0]+'.'+split_ip[1]
					hosts = fetch_hosts()[0].keys()
					hosts = [h for h in hosts if h.startswith(prefix,0,len(h))]
					nodes = hosts
					print nodes
					isSatellite = True
					break
			if not isSatellite:
				logger.exception('No satellite of this kind '+ip)
				raise Exception('Not a satellite')
	else:
		logger.info('Fetching host from swarm api')
		hosts = fetch_hosts()[0].keys()
		nodes = hosts
	for h in nodes:
		try:
			server_info = fetch_and_modify(h)
			icinga_host = templating(server_info)
			logger.info("writing for "+str(icinga_host['address']))
			written,file_name = save_to_satellite(icinga_host)
			if written:
				logger.info("Successfully written to location:"+file_name)
		except Exception,e:
			logger.exception(e)
			no_record_nodes.append(ip)
			logger.error('error for ip: '+h)
			pass


def exec_manual(ip,data=None):
	try:
		logger.info('Manual mode on. Triggered from gatherer')
		icinga_host = templating(fetch_and_modify(ip,data))
		print icinga_host
		logger.info("Writing for "+str(icinga_host['address']))
		written,file_name = save_to_satellite(icinga_host)
		if written:
			logger.info("configuration file created at location:"+str(file_name))
			return written
		else:
			raise Exception('Could not write to file.')
	except Exception,e:
		no_record_nodes.append(ip)
		logger.exception(e)
		raise Exception(e.message)



if __name__=="__main__":
	# config-generator
	logger.info('Auto mode on')
	if len(sys.argv) == 3:
		exec_auto(sys.argv[1],sys.argv[2])
	else:
		exec_auto()
	print "non configurable nodes:"
	print no_record_nodes
	print "service_groups"



