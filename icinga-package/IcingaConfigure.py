
#parameter for dumping psutil collections

MONGO_CLIENT = '192.168.4.78'
MONGO_PORT = 27017
MONGO_DB = 'bee_hive'
MONGO_COLLECTION = 'host_details'



#Parameters for threshold 
THRESHOLD_COLLECTION = 'icinga_threshold'



# Parameters for confiuration

TEMPLATE_PATH = 'jinja_templates/'
ICINGA_HOST_TEMPLATE = 'icinga_host.j2'


SAVE_PATH = "conf_container/"

	
satellite_info = {
        "aws-produk" : {"name":"AWS_Prod_Satellite_UK","address":"10.30.2.4","servers":["^10.30.*"]},
        "aws-mntg" : {"name":"ip-10-22-3-11","address":"10.22.3.11","servers":["^10.22.*"]},
        "aws-uspartner" : {"name":"ip-10-40-5-108","address":"10.40.5.108","servers":["^10.40.*"]},
        "aws-us-devint" : {"name":"ip-10-42-4-201","address":"10.42.4.201","servers":["^10.42.*"]},
        "us-partner2" : {"name":"ip-10-50-2-10","address":"10.50.2.10","servers":["^10.50.*"]},
        "aws-staging" : {"name":"ip-10-52-4-47","address":"10.52.4.47","servers":["^10.52.*"]},
        "prod-navisite" : {"name":"NAVIAPP031","address":"10.2.2.31","servers":["^10.2.*","^172.17.*"]},
        "local-mumbai-dev" : {"name":"INMUZV-ICI-DEI03","address":"10.1.0.12","servers":["^10.70.*","^192.168.*","^10.10.*","^10.60.*"]},
        "aws-prodsgpr" : {"name":"SGAV-SJP-PRA","address":"10.80.0.13","servers":["^10.80.*"]},
        "local-speedy" : {"name":"INMUZV-ICI-DEI03","address":"10.1.0.12","servers":["^10.90.*"]},
        "aws-prodaus" : {"name":"ip-10-24-4-13.ap-southeast-2.compute.internal","address":"10.24.4.13","servers":["^10.24.*"]},
}



icinga_host = {'host_name' : None ,
					'satellite_name' : None ,
					 'address' : None,
					 'node_env' : None,
					 'os' : None,
					 'satellite_address' : None,
					 'service_tags' : None,
					 'mount_points' : None,
					 'thresholds':None}

icinga_services = {'activemq': [],'oracle' : [],'nginx' : [],'httpd' : [],'mongo':[],'redis':[],'tomcat':[],'jboss':[], 'python':[], 'java':[], 'zookeeper':[]}

activemq_dict = {'queues' : None,'tags' : None,'topics' : None,'port':None,'activemq_port':None,
				'activemq_admin_port':None,'app_name':None,'amq_warning':None,'amq_critical':None}
oracle_dict = {'oracle_tns_name' : None}

nginx_dict = {'port': None,'app_name': None,'tags': None}

httpd_dict = {'port': None,'app_name': None,'tags': None}

mongo_dict = {'mongo_db_name' : None}

mysql_dict = {'mysql_health_connect' : None}

redis_dict = {'port' : None,'tags':None,'app_name':None}

tomcat_dict = {'port':None,'app_name':None,'tags':None,'jmx_port':None}

jboss_dict = {'port':None,'app_name':None,'tags':None,'jmx_port':None}

python_dict = {'port':None,'app_name':None,'tags':None}

java_dict = {'port':None,'app_name':None,'tags':None}

zookeeper_dict = {'zookeeper_port':None,'app_name':None,'tags':None}


