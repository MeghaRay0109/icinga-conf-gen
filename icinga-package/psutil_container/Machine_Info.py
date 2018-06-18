import psutil
import datetime
import platform
import xml.etree.ElementTree as ET
import json
import os
import re
import sys
import socket
import subprocess



details = {}

def get_proc_info():
    proc_info = {}
    for proc in psutil.process_iter():
        #children = proc.children(recursive=True)
        childs = []
        try:
            pinfo = proc.as_dict()
            pinfo["create_time"] = datetime.datetime.fromtimestamp(pinfo["create_time"]).strftime("%Y-%m-%d %H:%M:%S")
            pinfo["cpu_utilization"] = proc.cpu_percent()/psutil.cpu_count()
            cwd = pinfo["cwd"]
            if cwd and pinfo['exe']!='/bin/bash':
                if re.compile(r'\b'+'.*tomcat.*'+r'\b',re.IGNORECASE).search(cwd):
                    jmx_port_check = "ps -ef | grep "+str(pinfo['pid'])+" | awk -F '-Dcom.sun.management.jmxremote.port=' '{print $2}' | awk '{print $1}' | tr -d '\n'"
                    jmx_port = subprocess.check_output(jmx_port_check,shell=True).strip('\'').strip('')
                    pinfo['jmx_port'] = int(jmx_port)


                p = re.compile(r'\b'+'.*activemq.*'+r'\b',re.IGNORECASE)
                if p.search(cwd):
                    queues = []
                    topics = []
                    activemq_admin = str(cwd)+"/activemq-admin"
                    cp = re.compile(r'\b'+'destinationName = '+r'\b',re.IGNORECASE)
                    queues_cmd = activemq_admin+' query -QQueue=* | egrep -i ^destinationName'
                    topics_cmd = activemq_admin+' query -QTopic=* | egrep -i ^destinationName'
                    try:
                        qucmd = cp.split(subprocess.check_output(queues_cmd,shell=True))
                        tocmd = cp.split(subprocess.check_output(topics_cmd,shell=True))
                        for qu in qucmd:
                            qu_tmp = qu.strip('\n')
                            if qucmd.index(qu)>0 and qu_tmp not in queues:
                                queues.append(qu_tmp)
                        for to in tocmd:
                            to_tmp = to.strip('\n')
                            if tocmd.index(to)>0 and to_tmp not in topics:
                                topics.append(to_tmp)
                    except subprocess.CalledProcessError as exc:
                        pass
                    pinfo["queues"] = queues
                    pinfo["topics"] = topics

                    activemq_port_check = "ps -ef | grep "+str(pinfo['pid'])+" | awk -F '-Dactivemq.jmxremote.port=' '{print $2}' | awk '{print $1}' | tr -d '\n'"
                    activemq_port = subprocess.check_output(activemq_port_check,shell=True).strip('\'').strip('')
                    pinfo['activemq_port'] = int(activemq_port)


                    keyword = "^apache-activemq-*"
                    p = re.compile(r'\b'+keyword+r'\b',re.IGNORECASE)
                    cwd_arr = cwd.split("/")
                    path = "";
                    for index in cwd_arr[1:]:
                        if p.match(index):
                            path=path+"/"+index
                            break
                        else:
                            path=path+"/"+index
                    
                    activemq_admin_port_check = "cat "+path+"/conf/jetty.xml | grep -3 rg.apache.activemq.web.WebConsolePort | egrep '\'port\'' | awk -F 'value=' '{print $2}' | cut -d '/' -f 1"

                    activemq_admin_port = subprocess.check_output(activemq_admin_port_check,shell=True).strip().strip('"')
                    pinfo['activemq_admin_port'] = int(activemq_admin_port)
                    length = len(pinfo["queues"])
                    if length>0:
                        pinfo['amq_warning'] = length-1
                        pinfo['amq_critical'] = length-2
                    else:
                        pinfo['amq_warning'] = 0
                        pinfo['amq_critical'] = 0

                p = re.compile(r'\b'+'.*zookeeper.*'+r'\b',re.IGNORECASE)
                if p.search(cwd):
                    connections = pinfo["connections"]
                    for conn in connections:
                        if conn[3][0]=="::":
                            pinfo["zookeeper_port"] = conn[3][1]

                if re.compile(r'\b'+'.*jboss.*'+r'\b',re.IGNORECASE).search(cwd):
                    cwd = cwd.strip("bin")
                    tree = ET.parse(cwd+'server/default/conf/bindingservice.beans/META-INF/bindings-jboss-beans.xml')
                    root = tree.getroot()
                    data = root.findall(".//*[@name='Ports01Bindings']/{urn:jboss:bean-deployer:2.0}constructor/{urn:jboss:bean-deployer:2.0}parameter[3]")
                    port1 = int(data[0].text)
                    data = root.findall(".//*[@name='StandardBindings']//{urn:jboss:bean-deployer:2.0}parameter//*")
                    port2 = 0
                    for n in data:
                        if n.text == "jboss.remoting:service=JMXConnectorServer,protocol=rmi":
                            port2 = int(data[data.index(n)+1].text)
                            break

                    pinfo["jmx_port"] = port1 + port2
                    print pinfo["jmx_port"]






            if pinfo['exe']!='/bin/bash':                    
                if not pinfo["connections"] or pinfo["connections"]=='[]':
                    name = pinfo['name']
                    connections = []
                    netstat_cmd = "sudo netstat -tulpn | grep "+name+"* | grep "+str(pinfo['pid'])+" | grep LISTEN"
                    try:
                        net_prc = subprocess.check_output(netstat_cmd,shell=True)
                        net_prc = (net_prc.strip('\n')).split("\n")
                        for np in net_prc:
                            conn = [3,2,1]
                            np =  re.split(r'\s+',np)
                            w_port = np[3].rsplit(':',1)
                            if w_port[1]!='':
                                w_port[1] = int(w_port[1])
                                conn.append(w_port)
                                conn.append(np[4].rsplit(':',1))
                                conn.append(np[5])
                                connections.append(list(conn))
                        pinfo['connections'] = connections
                    except subprocess.CalledProcessError as exc:
                        pass
        except psutil.NoSuchProcess:
            pass
        else:
            proc_info[pinfo["pid"]] = pinfo

    return proc_info


def get_machine_info():
    machine_info = {}
    machine_info["fqdn"] = socket.getfqdn()
    machine_info["hostname"] = socket.gethostname()
    machine_info["address"] = get_ip()
    machine_info["platform"] = platform.platform() 
    machine_info["os"] =platform.system().lower()
    machine_info["architechture"] = platform.architecture()
    machine_info["machine"] = platform.machine()
    machine_info["version"] = platform.version()
    machine_info["linux_distribution"] = platform.linux_distribution()
    machine_info["release"] = platform.release()
    machine_info["uname"] = platform.uname()
    machine_info["processor"] = platform.processor()
    machine_info["ncpu"] = psutil.cpu_count()
    machine_info["cpu_times"] = psutil.cpu_times(percpu=False)
    machine_info["per_cpu_times"] = psutil.cpu_times(percpu=True)
    machine_info["cpu_percent"] = psutil.cpu_percent(interval=None, percpu=False)
    machine_info["per_cpu_percent"] = psutil.cpu_percent(interval=None, percpu=True)
    machine_info["cpu_stats"] = psutil.cpu_stats()
    # machine_info["cpu_freq"] = psutil.cpu_freq()
    # machine_info["per_cpu_freq"] = psutil.cpu_freq(percpu=True)
    machine_info["virtual_memory"] = psutil.virtual_memory()
    machine_info["swap_memory"] = psutil.swap_memory()
    disk_parts = psutil.disk_partitions()
    disk_partitions = []
    p = re.compile(r'\b'+'ext.*'+r'\b',re.IGNORECASE)
    for part in disk_parts:
        if part.mountpoint!='/root/admin': #and p.search(part.fstype):    
            usage = psutil.disk_usage(part.mountpoint)
            part_value = {}
            part_value["part"] = part
            part_value["usage"] = usage
            disk_partitions.append(part_value)

    machine_info["disk_partitions"] = disk_partitions
    machine_info["all_disk_io_counters"] = psutil.disk_io_counters(perdisk=False, nowrap=True)
    machine_info["per_disk_io_counters"] = psutil.disk_io_counters(perdisk=True, nowrap=True)
    machine_info["all_nic_io_counters"] = psutil.net_io_counters(pernic=False)
    machine_info["per_nic_io_counters"] = psutil.net_io_counters(pernic=True)
    machine_info["socket_connections"] = psutil.net_connections()
    machine_info["nic_addresses"] = psutil.net_if_addrs()
    machine_info["sensors_temperature"] = psutil.sensors_temperatures()
    machine_info["sensors_fans"] = psutil.sensors_fans()
    machine_info["sensors_battery"] = psutil.sensors_battery()
    machine_info["boot_time"] = datetime.datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S")
    machine_info["system_manufacturer"] = subprocess.check_output("dmidecode -s system-manufacturer",shell=True).strip()
    machine_info["bios_vendor"] = subprocess.check_output("dmidecode -s bios-vendor",shell=True).strip()


    return machine_info

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]


def pprint_ntuple(nt):
    for name in nt._fields:
        value = getattr(nt, name)
        if name != 'percent':
            value = bytes2human(value)
        return ('%-10s : %7s' % (name.capitalize(), value))


def bytes2human(n):
    ''' Have to see the conversion properly'''
    symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
    prefix = {}
    for i, s in enumerate(symbols):
        prefix[s] = 1 << (i + 1) * 10
    for s in reversed(symbols):
        if n >= prefix[s]:
            value = float(n) / prefix[s]
            return '%.1f%s' % (value, s)
    return "%sB" % n


def main():
    details["machine_info"] = get_machine_info()
    details["process_info"] = get_proc_info()
    print json.dumps(details)



main()





