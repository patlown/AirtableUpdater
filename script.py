from pprint import pprint
from airtable import Airtable
import wmi
import psutil
import math
import cpuinfo
import arrow

def getSerial():
    with open("serial.txt",'rb') as file:
	    s = file.read().decode('utf-16')
	    serialfile = s.split('\n')
	    serialfile[1] = serialfile[1].strip()
    return serialfile[1]

def getTotalStorage():
    obj_Disk = psutil.disk_usage('/')
    total = obj_Disk.total / (1024.0 ** 3)
    return roundup(total)

def roundup(x):
	return int(math.ceil(x / 100.0)) * 100

def createFields(computer,cfgDict):
    fields = {'Name':'LSS-' + computer.serialNum, 'SN': computer.serialNum, 'Model':computer.model
	,'Make':computer.make, 'HD (GB)': computer.storage,
	'RAM (GB)':computer.ram, 'CPU': computer.cpu, 'Last Imaged':computer.date, 'OS': computer.os, 
	}

    return fields

def cfgToDict():
    f = open("clientsettings.cfg","r")

    s = f.read().strip()
    contents = dict(item.split("=") for item in s.split("\n"))


    if 'UW_Owner_or_Fiscal_Group' in contents:
        airtable = Airtable('app9og4P1Z4iet5fT','Departments','keybFjYyk9LuWpxNw')
        res = airtable.search('Name',contents['UW_Owner_or_Fiscal_Group'],fields = ['Name'])
        print(res)
        if len(res) == 0:
            del contents['UW_Owner_or_Fiscal_Group']
        else:
            contents['Department'] = [res['id']]
    if 'UW_Location' in contents:
        contents['Location'] = contents['UW_Location']
        del contents['UW_Location']
    if 'UW_NetID' in contents:
        contents['NetID'] = contents['UW_NetID']
        del contents['UW_NetID']
    if 'UW_PURCHASE_DATE' in contents:
        contents['Purchased'] = contents['UW_PURCHASE_DATE']
        del contents['UW_PURCHASE_DATE']
    



    return contents

    
        

    

class Computer:
    c = wmi.WMI()
    pcinfo = c.Win32_ComputerSystem()[0]
    osinfo = c.Win32_OperatingSystem()[0]   
    #given an airtable search call, this will create a computer object with the necessary info
    def __init__(self,serial,computer = {}):
        c = wmi.WMI()
        pcinfo = c.Win32_ComputerSystem()[0]
        osinfo = c.Win32_OperatingSystem()[0]   
        self.comp = computer
        self.make = pcinfo.Manufacturer.split(' ',1)[0]
        self.ram = math.ceil(int(pcinfo.TotalPhysicalMemory)/1024**3)
        self.cpu = cpuinfo.get_cpu_info()['brand']
        self.os = osinfo.Caption.split(' ',1)[1].strip()
        self.model = pcinfo.Model
        self.date = arrow.now().format('YYYY-MM-DD')
        self.serialNum = serial
        self.storage = getTotalStorage()


def main():
    serial = getSerial()
    airtable = Airtable('app9og4P1Z4iet5fT','Computers','keybFjYyk9LuWpxNw')
    computers = []
    
    records = airtable.search('SN',serial)
    print(records)
    cfgDict = cfgToDict()
    # print(cfgDict)

    if len(records) == 0:
        c = Computer(serial)
        airtable.insert(createFields(c,cfgDict))


    for record in records:
        curr = Computer(serial,record)
        computers.append(curr)

    for c in computers:
        airtable.update(c.comp.get('id'),createFields(c,cfgDict))

if __name__ == '__main__':
    main()


