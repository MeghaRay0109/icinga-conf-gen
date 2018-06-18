
services_classifier = [
			[2,"iSource",{"tags":["isource","app_server","jboss","jmx","java"]},5],
			[3,"iSource",{"tags":["isource","app_server","jboss","jmx","java"]},2],
			[3,"^BRIDGE.*",{"tags":["ssobridge","app_server","tomcat","jmx","java"]},3],
			[2, "eProc",{"tags":["eproc","app_server","tomcat","jmx","java"]},None ],
			[2,"iContract",{"tags":["icontract","app_server","tomcat","jmx","java"]},3],
			[2,"SPM",{"tags":["spm","app_server","jboss","java"]},3],
			[2,"iCost",{"tags":["icost","app_server","jboss","jmx","java"]},None],
			[2,"CNS",{"tags":["cns","app_server","tomcat","java"]},None],
			[2,"ZyTrack",{"tags":["zytrack","app_server","tomcat","jmx","java"]},None],
			[2,"Dashboard",{"tags":["dashboard","app_server","tomcat","jmx","java"]},None],
			[2,"OneView",{"tags":["oneview","app_server","tomcat","jmx","java"]},3],
			[2,"iManage",{"tags":["imanage","app_server","jboss","jmx","java"]},None],
			[3,"CRMS",{"tags":["crms","app_server","tomcat","jmx","java"]},None],
			[2,"AutoClass",{"tags":["autoclass","app_server","jboss","java"]},3],
			[3,"^liferay-portal.*",{"tags":["supplier_portal","app_server","tomcat","jmx","java"]},5],
			[2,"SIM",{"tags":["sim","app_server","tomcat","jmx","java"]},3],
			[2,"TMS",{"tags":["tms","app_server","tomcat","jmx","java"]},3],
			[2,"iAnalyze",{"tags":["ianalyze","app_server","jboss","java"]},None],
			[2,"SupplierTMS",{"tags":["suppliertms","app_server","tomcat","jmx","java"]},3],
			[2,"Rainbow",{"tags":["rainbow","app_server","tomcat","jmx","java"]},5],
			[5,"H2",{"tags":["h2","middleware","java"]},None],
			[2,"FieldLibrary",{"tags":["fieldlibrary","flexiform","app_server","tomcat","jmx","java"]},None],
			[2,"^ZCS.*",{"tags":["zcs","inotify","imobile","app_server","tomcat","jmx","java"]},5],
			[2,"iRequest",{"tags":["irequest","app_server","tomcat","jmx","java"]},None],
			[2,"^iConsole.*",{"tags":["iconsole","app_server","tomcat","jmx","java"]},3],
			[2,"ZygrateSecurity",{"tags":["zygratesecurity","app_server","tomcat","jmx","java"]},3],
			[2,"Integration",{"tags":["integration","app_server","tomcat","jmx","java"]},3],
			[2,"ZooKeeper.*",{"tags":["zookeeper"]},2],
			[2,"iMonitor",{"tags":["imonitor","app_server","tomcat","jmx","java"]},3],
			[2,"ZSN",{"tags":["zsn","app_server","tomcat","jmx","java"]},3],
			[2,"QuickSearch",{"tags":["quicksearch","app_server","tomcat","jmx","java"]},None],
			[2,"Integration_Platform",{"tags":["integration_Platform","java"]},None],
			[2,"iSave",{"tags":["isave","app_server","tomcat","jmx","java"]},None],
			[2,"eCatalog",{"tags":["ecatalog","app_server","tomcat","jmx","java"]},3],
			[2,"eInvoice",{"tags":["einvoice","app_server","tomcat","jmx","java"]},3],
			[2,"SpendDashboard",{"tags":["spenddashboard","app_server","tomcat","jmx","java"]},None],
			[2,"IntegrationPlatform-2.*",{"tags":["integrationplatform-2"]},3],
			[2,"iMaster",{"tags":["imaster","app_server","tomcat","jmx","java"]},3],
			[2,"RuleManager",{"tags":["rulemanager"]},None],
			[2,"Bulk_Import",{"tags":["bulk_import"]},None],
			[2,"MAS",{"tags":["mas"]},None],
			[2,"Workflow",{"tags":["workflow","app_server","tomcat","jmx","java"]},None],
			[4,"Consul",{"tags":["consul"]},None],
			[2,"^Solr.*",{"tags":["solr"]},2],
			[2,"^ActiveMQ.*",{"tags":["activemq","middleware","java"]},3],
			[3,"httpd",{"tags":["apache","web_server","httpd"]},None],
			[3,"haproxy",{"tags":["ha"]},None],
			[3,"icinga2",{"tags":["icinga2"]},None],
			[3,"python",{"tags":["python"]},None],
			[6,"java",{"tags":["java"]},None],
			[1,"nginx",{"tags":["nginx","web_server"]},None],
			[1,"^redis.*",{"tags":["redis","middleware"]},None],
			[3,"^mongo.*",{"tags":["mongodb","database"]},None],
			[4,"^mongo.*",{"tags":["mongodb","database"]},None],
			[1,"^mongo.*",{"tags":["mongodb","database"]},None],
			]

service_component_classifier = {
	
		"eProc" : [[3,"service_node",{"tags":["service_node"]}],
					[3,"integration_node",{"tags":["integration_node"]}],
					[3,"reporting",{"tags":["reporting"]}]
				],
		"iAnalyze" :[
						[3,"iAnalyze_CARGILL",{"tags":["iAnalyze_CARGILL"]}]
				],



}

