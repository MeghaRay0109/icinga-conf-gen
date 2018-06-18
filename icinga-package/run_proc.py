import settings
import os
import datetime
from Hosts import Hosts
import sys
import requests
import json
import traceback
import logging
import logging.handlers
import mail
import subprocess
import time as tme
import icinga_conf_creator

now = datetime.datetime.now()


logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setLevel(logging.INFO)
formatter = logging.Formatter("%(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)


	
def get_hosts_from_ocs():
	# ocs_hosts = subprocess.check_output(settings.CMD,shell=True)
	# return ocs_hosts.split()
	return requests.get(settings.SWARM_API_ENDPOINT + "/hosts")

	

def get_hosts_info():
	return dao.database('bee_hive').collectn('temp_host_details').find({"active":1})


def get_setup_details(ip_to_swarm=None):
	logger.info(" [ INFO ] Gatherer Run Started.")
	run_time_start = datetime.datetime.now()
	time={}
 	i=0
 	fail_ip = {}
 	fail_ips = []
	h = Hosts()
	for ip in ip_to_swarm:
		fail_ip = {}
		try:
			st_time=datetime.datetime.now()
			product = "Hosts"
			print "Gather Details From {0} ".format(ip)
			
			if h:
				print "Fetching details"				
				setup_details = h.get_setup_details(ip)
				data = {
						"ip": ip,
						"details": setup_details["process_info"],
						"machine_info": setup_details["machine_info"],
						"active":1,
						"env": None,
						"last_run":str(now)
						}

				end_time=datetime.datetime.now()
				tot_time = end_time - st_time
				time[i]="{0} : time : {1}".format(ip,str(divmod(tot_time.total_seconds(),60)))
				i=i+1
				is_conf_created = icinga_conf_creator.exec_manual(ip,data)
				logger.info(str(is_conf_created))
		except Exception, e:
			errorMsg= "[ Gatherer Production ] Exception :: Running Gatherer on {0}".format(ip)
			fail_ip["ip"] = ip
			fail_ip["exception"] = str(e)
			fail_ips.append(fail_ip)
			logger.error(errorMsg)
			logger.exception(traceback.print_exc())
			raise Exception(e)


	logger.info("[ INFO ] Infra Run Ended.")
		
	logger.warn("FAILED_IP:"+str(fail_ips))
	error_file = None
	run_time_end = datetime.datetime.now()
	list_of_ip_to_report = ''
	report = ''
	if len(fail_ips) > 0:
		error_file =settings.ERROR_DIR+settings.ERROR_FILE
		list_of_ip_to_report = "Gatherer Report \n Fail Setups : \n"
		for failed_ip in fail_ips:
			list_of_ip_to_report += failed_ip["ip"]+"\n"
			report += failed_ip["ip"]+"\n"+"Cause:"+failed_ip["exception"]+"\n"+"----------------------------------------------------\n"
		exception_report_file = open(error_file,'w')
		exception_report_file.write(report)
		exception_report_file.close()

	if len(time) > 0:
		list_of_ip_to_report += "\nSuccess Setups : \n"
		for t in time:
			list_of_ip_to_report += time[t] + "\n"

	run_tot_time = run_time_end - run_time_start
	list_of_ip_to_report += "\nTotal Run Time : " + str(divmod(run_tot_time.total_seconds(),60))

	if len(fail_ips)>0:
		list_of_ip_to_report += "FAILURE RECORDED.PLEASE FIND FAILURE IN ATTACHMENT."

	mail.sendEmail(list_of_ip_to_report,error_file, settings.MAIL_FROM, settings.MAIL_TO, "Gatherer Run Report")
	for t in time :
		print time[t]

if __name__ == "__main__":
	logger.info("Initiating the process. Hold on.")
	if len(sys.argv) == 2:
		get_setup_details([sys.argv[1]])
	else:
		setups = json.loads(get_hosts().text)[0]
		get_setup_details(setups)
