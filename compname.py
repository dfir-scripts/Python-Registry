#!/usr/bin/python
# https://github.com/williballenthin/python-registry
# From https://github.com/williballenthin/python-registry/tree/master/samples
# Returns the computer name from the Windows SYSTEM Registry Key
import sys
try:
    from Registry import Registry
except:
    print ("Python Registry Not Found")

def usage():
    return "\tUSAGE: %s <Windows SYSTEM Registry file and path>" % sys.argv[0]

def main():
    if len(sys.argv) !=2:
        print (usage())
        sys.exit(-1)
    try:
        registry = Registry.Registry(sys.argv[1])
        select =  registry.open("Select")
        current = select.value("Current").value()
        key =registry.open("ControlSet00%d\\Control\\ComputerName\\ComputerName" % (current))
    except:
        print("Unable to open registry hive or key")
        sys.exit(-1)
    for v in key.values():
        try:
            if v.name() == "ComputerName":
                compname = v.value()
                print ('%s' % (compname))
        except:
            print ("Computer Name Not Found!")
            print (usage())
if __name__ == '__main__':
    main()