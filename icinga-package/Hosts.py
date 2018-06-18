import datetime
import json
import settings
import re
import paramiko
from scp import SCPClient
from classification import services_classifier as services
from classification import service_component_classifier as components_classifer

class Hosts:
    def __init__(self):
        pass

    def get_setup_details(self,ip):
        infra_details = self.execute_on_host(ip)
        classified_infra_details=self.filter(infra_details)
        return classified_infra_details


    def execute_on_host(self,ip):
        ssh_client = paramiko.SSHClient()
        try:
            result = None
            ssh_client.load_system_host_keys()
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh_client.connect(hostname=ip,username=settings.USERNAME,password="")
            ssh_client._transport.window_size=2147483647
            #ftp_client = ssh_client.open_sftp()
            # ftp_client.put(settings.local_dir+settings.file_name,settings.remote_dir+settings.file_name)
            # ftp_client.close()
            scp = SCPClient(ssh_client.get_transport())
            scp.put(settings.local_dir+settings.file_name,settings.remote_dir+settings.file_name)
            scp.close()
            if self.exe_command(settings.CHECK_COMMAND,ssh_client):
                result = self.exe_command(settings.RUN_COMMAND,ssh_client)
                ssh_client.close()
                return result[0]
            else:
                ssh_client.close()
                raise Exception("Invalid output for CHECK_COMMAND:"+settings.CHECK_COMMAND+" on node:"+ip)
        except Exception,e:
            ssh_client.close()
            raise Exception("Exception detected",e)



    def exe_command(self,command,ssh_client):
        if ssh_client:
            print command
            ssh_client._transport.default_window_size=2147483647
            stdin, stdout, stderr = ssh_client.exec_command(command)
            exit_status = stdout.channel.recv_exit_status()
            if exit_status != 0:
                error = stderr.readlines()
                raise Exception(error)
            else:
                print str(exit_status)
                result = stdout.readlines()
            return result


    def filter(self,host_details):
        host_info = json.loads(host_details)
        host = host_info["process_info"]
        for process in host:
            tags = None
            cwd = host[process]["cwd"]
            cwd1 = host[process]["exe"]
            print "cwd:"+str(cwd)
            print "exe:"+str(cwd1)
            if cwd:
                print "in cwd"
                tags = self.set_tags(cwd.split("/"))
                print "for cwd:"+str(tags)
            if cwd1 and not tags:
                print "in exe"+str(cwd1)
                tags = self.set_tags(cwd1.split("/"))
                print "for exe:"+str(tags)
            if not tags:
                name = host[process]['name']
                print "for exe:["+name+"]"
                tags = self.set_tags([' ',name])
                print tags
            host[process]["tags"] = tags
        print host_info
        return host_info

    

    def fliter_component(self,cwd,tags):
        components = components_classifer[tags[0]]
        for component in components:
            p = re.compile(r'\b'+component[1]+r'\b',re.IGNORECASE)
            if p.search(cwd[component[0]]):
                tags.extend(component[2]["tags"])
                break
        return tags

    def set_tags(self,cwd):
        if "nginx" in cwd:
            print len(cwd)
        for service in services:
            p = re.compile(r'\b'+service[1]+r'\b',re.IGNORECASE)
            if service[0] and service[0]< len(cwd) and p.search(cwd[service[0]]):
                tags = []
                service_tags = service[2]["tags"]
                for tag in service_tags:
                    tags.append(tag)
                if service[3] and service[3] < len(cwd):
                    tags.append(cwd[service[3]])
                elif tags[0] in components_classifer:
                        tags = self.fliter_component(cwd,tags)
                return tags




if __name__ == '__main__':
    h = Hosts()
    h.get_setup_details("10.52.4.17")
