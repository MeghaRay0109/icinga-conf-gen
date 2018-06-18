import boto3
import os
import pprint, json

class AwsInventory:


	def __init__(self,aws_access_key,aws_secret_key,region_name):
		self.aws_access_key = aws_access_key
		self.aws_secret_key = aws_secret_key
		self.region = region

	def __init__(self):
		self.aws_access_key = os.environ["AWS_ACCESS_KEY"]
		self.aws_secret_key = os.environ["AWS_SECRET_KEY"]
		self.region = os.environ["region"]

	def get_regions(self):
		ec2_client = boto3.client('ec2',aws_access_key_id=self.aws_access_key,aws_secret_access_key=self.aws_secret_key,region_name=self.region)
		regions = []
		region_description = ec2_client.describe_regions()['Regions']
		for region in region_description:
			regions.append(region['RegionName'])
		return regions

		
	def get_hosts(self, regions):
		instances = []
		for region in regions:
		    instances.extend(self.get_instances(region))
		return instances


	def get_hosts_dict(self, regions):
		host_dict = {}
		for region in regions:
			host_dict[region] = self.get_instances(region)
		return host_dict

	def get_instances(self,region):
		instances = []
		ec2 = boto3.resource('ec2',aws_access_key_id=self.aws_access_key,aws_secret_access_key=self.aws_secret_key,region_name=region)
		result = ec2.instances.filter(Filters=[{'Name': 'instance-state-name', 'Values': ['*']}])
		for instance in result:
			instances.append(instance.private_ip_address)
		return instances

	def write_to_file(self,instances):
		file = open("aws_host_inventory","wb+")
		for inst in instances:
			file.write(inst+"\n")
		file.close()


if __name__=="__main__":
	awsInventory = AwsInventory()
	# print "getting regions"
	# regions = awsInventory.get_regions()
	# print "getting region wise host"
	# print awsInventory.get_hosts_dict(regions)
	instances = awsInventory.get_instances("ap-southeast-2")
	print instances
	awsInventory.write_to_file(instances)