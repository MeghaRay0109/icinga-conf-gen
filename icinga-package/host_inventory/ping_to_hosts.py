import subprocess
import sys
import json


def get_hosts(range):
	cmd = "fping "+str(range)
	host_list = ""
	process = subprocess.Popen(['fping', '-g', range], stdout=subprocess.PIPE)
	out, err = process.communicate()

	return out, err

def scann(range):
	print "Scanning.."
	ips = {}
	out, err =  get_hosts(sys.argv[1])
	if err != None:
		print "Error while running the script!"
	for line in out.split("\n"):
		if line.strip() == "":
			continue
		line = line.split("is")
		ip = line[0].strip()
		status = line[1].strip()
		if status in ips:
			ips[status].append(ip)
		else:
			ips[status]= [ip]

	return ips	


def write_to_file(ip_dict):
	file = open("ips.json", "wb+")
	file.write(json.dumps(ip_dict))
	file.close()
	print "Written to File!"


if __name__=="__main__":
	range = sys.argv[1]
	ip_dict = scann(range)
	write_to_file(ip_dict)
	print ip_dict
	print "Done!"



# nm = nmap.PortScanner()

# result = nm.scan('10.2.2.0/24', '22-443')

# print result