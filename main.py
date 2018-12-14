from pprint import pprint
from airtable import Airtable
import wmi
import psutil
import math
import cpuinfo
import arrow
 
def roundup(x):
	return int(math.ceil(x / 100.0)) * 100

def chooseDept():
	print("AAS - Asian American Studies")
	print("ACS - African Cultural Studies")
	print("AH - Art History")
	print("AIS - American Indian Studies")
	print("ALC - Asian Languages and Cultures")
	print("CANES - Classical and Near Eastern Studies")
	print("CJS - Center for Jewish Studies")
	print("CLFS - Comparative Literature and Folklore Studies")
	print("CLS - Chicano/a Latino/a Studies")
	print("EALL - East Asian Languages and Literature")
	print("FRIT - French and Italian")
	print("GNS - German, Nordic, and Slavic")
	dept = input("Input the 3-Letter Department Code")
	return dept

# get rounded up to nearest hundred disk space
obj_Disk = psutil.disk_usage('/')
total = obj_Disk.total / (1024.0 ** 3)
totalstorage = roundup(total)

# wmi gets computersystem information 
c = wmi.WMI()
pcinfo = c.Win32_ComputerSystem()[0]
osinfo = c.Win32_OperatingSystem()[0]



with open("serial.txt",'rb') as file:
	s = file.read().decode('utf-16')
	serialfile = s.split('\n')
	serialfile[1] = serialfile[1].strip()

airtable = Airtable('app9og4P1Z4iet5fT','Computers','keybFjYyk9LuWpxNw')
computer = airtable.search('SN',serialfile[1])
print(computer)

fmake = pcinfo.Manufacturer.split(' ',1)[0]
fram = math.ceil(int(pcinfo.TotalPhysicalMemory)/1024**3)
fcpu = cpuinfo.get_cpu_info()['brand']
fos = osinfo.Caption.split(' ',1)[1].strip()
fdate = arrow.now().format('YYYY-MM-DD')


if len(computer) == 0:
	print("Computer not in Airtable, creating new record")
elif len(computer) > 1:
	# print("Multiple records found with matching serial")
	#fdept = chooseDept().strip()
	# print(fdept)

	fields = {'Name':'LSS-' + serialfile[1], 'Model':pcinfo.Model
	,'Make':fmake, 'HD (GB)': totalstorage,
	'RAM (GB)':fram, 'CPU': fcpu, 'Last Imaged':fdate, 'OS': fos, 
	
	}
	for c in computer:
		# pprint(computer)
		airtable.update(c.get('id'),fields)	
else:
	print("Serial number matches unique record, updating")
	fields = {'Name':'LSS-' + serialfile[1], 'Model':pcinfo.Model
	,'Make':fmake, 'HD (GB)': totalstorage,
	'RAM (GB)':fram, 'CPU': fcpu, 'Last Imaged':fdate, 'OS': fos
	}
	airtable.update(computer[0].get('id'),fields)	


# # create fields to be updated
# fields = {'Name':'LSS-' + serialfile[1], 'Model':pcinfo.Model
# ,'Make':fmake, 'HD (GB)': totalstorage,
# 'RAM (GB)':fram, 'CPU': fcpu, 'Last Imaged':fdate, 'OS': fos
# }
# for c in computer:	
# 	airtable.update(c.get('id'),fields)
