from __future__ import with_statement
from fabric.contrib import files
import sys
from fabric.api import local,settings,abort,run, cd, lcd,put, hosts, roles, env, parallel, execute, task
from fabric.contrib.console import confirm

custom_python = "sre_python.tar.gz"
local_python_path = "python_container/"


remote_path = "/tmp"
remote_extract_location = "/tmp/envs"
remote_user="webtech"

file_name = "Machine_Info.py"
local_machine_location = "psutil_container/"

#host_file = sys.argv[1]	
	
env.roledefs = {
	'role1' : [x.strip() for x in open('hosts1','r').readlines()]
}

def copy_extract():
	if not put(local_python_path+custom_python,remote_path).failed:
		with cd(remote_path):
			if not files.exists(remote_extract_location):
				run("mkdir "+remote_extract_location)
			if not run("tar -zxvf "+custom_python+" -C "+remote_extract_location).failed:
				print "successfully placed and extracted "+custom_python
			else:
				abort("Aborting on failed operation")
def copy_run():
	if not put(local_machine_location+file_name,remote_path).failed:
		if local("/home/webtech/envs/sre_python/bin/python run_proc.py "+env.host_string).failed:
			abort("Aborting due to psutil configuration error")

@task
@roles('role1')
@parallel
def deploy():
	with settings(colorize_errors=True,user=remote_user):
		copy_extract()
		copy_run()

execute(deploy)
		


			

		

		
			
