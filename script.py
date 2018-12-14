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

def createFields(computer):
    fields = {'Name':'LSS-' + computer.serialNum, 'SN': computer.serialNum, 'Model':computer.model
	,'Make':computer.make, 'HD (GB)': computer.storage,
	'RAM (GB)':computer.ram, 'CPU': computer.cpu, 'Last Imaged':computer.date, 'OS': computer.os, 
	}

    return fields
    

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

    if len(records) == 0:
        c = Computer(serial)
        airtable.insert(createFields(c))


    for record in records:
        curr = Computer(serial,record)
        computers.append(curr)

    for c in computers:
        airtable.update(c.comp.get('id'),createFields(c))

if __name__ == '__main__':
    main()


