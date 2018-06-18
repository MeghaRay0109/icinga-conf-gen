import datetime

now = datetime.datetime.now()


SWARM_APP_PATH="/U01/TurbatIO/apps/swarm/app"
BEES_PATH=SWARM_APP_PATH+"/bees"
BASE_URL="http://192.168.5.50:8780/DBWebService/rest/query"
INSTALL_PATH=SWARM_APP_PATH+"/admin/install.py"
navisite=False
environment="Dev"
SWARM_API_ENDPOINT="http://swarmapi.turbatio.zycus.com"

#local and remote directory for psutil
USERNAME = "webtech"
local_dir = "psutil_container/"
remote_dir = "/tmp/"
file_name = "Machine_Info.py"
PYTHON_PATH = "/tmp/envs/sre_python/bin"
CHECK_COMMAND = "ls -l "+PYTHON_PATH
EXPORT_COMMAND= "export PATH="+PYTHON_PATH+":$PATH"
RUN_COMMAND=PYTHON_PATH+"/python "+remote_dir+file_name


#Exception file
ERROR_DIR=local_dir+"error_dir/"
ERROR_FILE="exception"+str(now)+".txt"
#to hit ocsinventory:
CMD = "java -Docs.location=/vagrant/psutil/execute/ocs.properties -jar /vagrant/psutil/execute/ocs-inventoryv1.2-jar-with-dependencies.jar"


#for mongoClient IP and PORT affects in file => checkap.py and dup.py
MongoClientIP = "192.168.4.78"
MongoClientPort = 27017


#fromadd => run_proc.py
MAIL_FROM="psutil.dev@zycus.com"
MAIL_PORT=25
MAIL_HOST= "devautomail.zycus.com"

#toaddr => LogMailer Change in run.py
MAIL_TO=['shashi.mishra@zycus.com']

#toaddr => run_dev.py
toaddrsDev=['shashi.mishra@zycus.com']

response = "http://goapi.zycus.com/api/notify"

