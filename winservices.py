#!/usr/bin/python

from __future__ import print_function
from __future__ import unicode_literals

import sys
from Registry import Registry


def usage():
    return "  USAGE:\n\t%s <Windows SYSTEM Registry file> " % sys.argv[0]


def main():
    if len(sys.argv) != 2:
        print(usage())
        sys.exit(-1)

    registry = Registry.Registry(sys.argv[1])
    select = registry.open("Select")
    current = select.value("Current").value()
    services = registry.open("ControlSet00%d\\Services" % (current))
    print('TIME,NAME,START TYPE,SERVICE TYPE,DISPLAY NAME,IMAGE PATH,DLL,DESCRIPTION')
    for service in services.subkeys():
        try:
            servicename = (service.name().replace(",",";"))
        except:
            servicename = "-No_Service_Name-"
        try:
            timestamp = str(service.timestamp())
        except:
            timestamp = "-No_Timestamp-"
        try:
            display_name = (service.value("DisplayName").value().replace(",",";"))
        except:
            display_name = "-No_Display_Name-"
        try:
            description = (service.value("Description").value().replace(",",";"))
        except:
            description = "-No_Description-"
        try:
            image_path = (service.value("ImagePath").value().replace(",",";"))
        except:
            image_path = "-No_Image_Path-"
        try:
            dll = (service.subkey("Parameters").value("ServiceDll").value().replace(",",";"))
        except:
            dll = "-No_DLL-"
        try:
            start_type = service.value("Start").value()
            if str(start_type) == "0":
                start_type = "Start=Boot"
            if str(start_type) == "1":
                start_type = "Start=System"
            if str(start_type) == "2":
                start_type = "Start=AutoStart"
            if str(start_type) == "3":
                start_type = "Start=Manual"
            if str(start_type) == "4":
                start_type = "Start=Disabled"
        except:
            start_type = "Start=No_Info"
        try:
            svc_type = service.value("Type").value()
            if str(svc_type) == "1":
                svc_type = "Kernel_driver"
            if str(svc_type) == "2":
                svc_type = "File System_Driver"
            if str(svc_type) == "4":
                svc_type = "Adapter_Driver"
            if str(svc_type) == "8":
                svc_type = "File System_Driver"
            if str(svc_type) == "16":
                svc_type = "Own_Process"
            if str(svc_type) == "32":
                svc_type = "Share_Process"
            if str(svc_type) == "256":
                svc_type = "Interactive"
            if str(svc_type) == "272":
                svc_type = "Own_Process"
            if str(svc_type) == "288":
                svc_type = "Share_Process"
        except:
            svc_type = "-No_Service_Type-"
        
        print('%s, %s, %s, %s, %s, %s, %s, %s' % (timestamp, servicename, start_type, svc_type, display_name, image_path, dll, description))
if __name__ == '__main__':
    main()

