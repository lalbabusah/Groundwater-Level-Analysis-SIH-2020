#	|-------|     |	      |--------
#	|	|  ---|---    |
#	|	|     |	      |_______
#	|-------|     |	              |
#	|     \	      |		      |
#	|      \      |	      --------|

import os
import requests,json
from urllib import request,parse
opener=request.build_opener()
opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')] 
request.install_opener(opener)

def check_and_make(path):
	if not os.path.exists(path):
		os.makedirs(path);

def fetch_district(state_name,state_code):
	try:
		url="http://59.179.19.250/GWL/php/select_district.php"
		data=parse.urlencode({'Para1':state_code,'Para2':'get_district'}).encode()
		req=request.Request(url,data=data);
		response=str(request.urlopen(req).read());
		districts=[];temp="";ctr=0;
		for i in response:
			if i=='"':
				ctr+=1
				if ctr==2:
					if temp!="NA":
						districts.append(temp+"\n")
					temp=""
					ctr=0;
			elif ctr==1:
				temp+=i
		file = open("./districts/"+state_code+".txt","w+");
		file.writelines(districts);
		return 1
	except:
		return 0

def fetch_district_data(state_code,district_name):
	# http://59.179.19.250/GWL/php/exportAll_xls.php?Para1=AP&Para2=district_level&Para3=Chittoor
	try:
		data=parse.urlencode({'Para1':state_code,'Para2':'district_level','Para3':district_name}).encode();
		r=requests.get("http://59.179.19.250/GWL/php/exportAll_xls.php",params=data)
		if r.status_code == 200:
			with open("data/"+state_code+"/"+district_name+".csv", 'wb+') as local_file:
				for chunk in r.iter_content(chunk_size=128):
					local_file.write(chunk)
		return 1
	except:
		return 0


def fetch_all_district_names():
	try:
		with open("states.txt","r") as states:
			for i in states.readlines():
				i=i.strip()
				state_name,state_code=i[:-3],i[-2:]
				code=fetch_district(state_name,state_code)
				if code==1:
					print(state_name+" fetched");		
				else:
					print("Failed at "+state_name)
		return 1
	except:
		return 0

def fetch_all_district_data():
	check_and_make('districts')
	check_and_make('data')
	if fetch_all_district_names()==1:
		print("All District Names Fetched")
	else:
		print("Name Fetch Failed. Exiting")
		return 0
	try:
		for state in os.listdir('districts'):
			fullpath=os.path.join('districts',state)
			state_code=state.split('.')[0]
			check_and_make(os.path.join('data',state_code))
			with open(fullpath,'r') as district_list:
				for district in district_list.readlines():
					code=fetch_district_data(state_code,district.strip())
					if code==1:
						print(state_code+":"+district+" data fetched");
					else:
						print(state_code+":"+district+" FAILED");
		return 1
	except e:
		print(e)
		return 0

		
fetch_all_district_data()

