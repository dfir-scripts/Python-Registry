#!/usr/bin/python
# Parse BAM DAM registry keys and output evidence of program execution as TLN or csv
# https://www.sans.org/security-resources/posters/windows-forensic-analysis/170/download
# Based on python-registry samples and bamparser.py written by Patrick Olsen
# https://www.linkedin.com/pulse/alternative-prefetch-bam-costas-katsavounidis/  
# https://github.com/williballenthin/python-registry
# https://github.com/prolsen/bam/blob/master/bamparser.py
# According the the Forensic Wiki: TLN is a timeline format (as far known) introduced in a blog post by Harlan Carvey. 
# http://windowsir.blogspot.com/2009/02/timeline-analysis-pt-iii.html
import sys
import time
def usage():
    return "USAGE:\n  %s <Windows System Registry File> -c (Outputs csv and date)\n\n Search BAM key for evidence of file execution\n Requires Python 3 and Python Registy\n" % sys.argv[0]
def main():
    #Requirements check
    try:
        assert sys.version_info >= (3,0)
        assert len(sys.argv) >= 2
        from Registry import Registry
    except:
        print(usage())
        sys.exit(-1)
    try:
        registry = Registry.Registry(sys.argv[1])
        select = registry.open("Select")
        current = select.value("Current").value()
        testopen = registry.open("ControlSet00%d\\Services\\bam\\UserSettings" % (current))
    except:
        print("\n*** Unable to open Registry Hive or Key ***\n\n" + usage())
        sys.exit(-1)
    try:
        cname_key = registry.open("ControlSet00%d\\Control\\ComputerName\\ComputerName" % (current))
        for cname in cname_key.values():
            if cname.name() == "ComputerName":
                compname = (cname.value())
    except:
        pass
    #Get computer Name
    try:
        cname_key = registry.open("ControlSet00%d\\Control\\ComputerName\\ComputerName" % (current))
        for cname in cname_key.values():
            if cname.name() == "ComputerName":
                compname = (cname.value())
    except:
        pass
    try:
        bamdam = ["bam", "dam"]
        for moderator in bamdam:
            registry = Registry.Registry(sys.argv[1])
            bamdam_key = registry.open("ControlSet00%d\\Services\\%s\\UserSettings" % (current, moderator))
    except:
        pass
    for profile in bamdam_key.subkeys():
        try:
            profile_name = profile.name()
        except:
            print("error")
        for value in profile.values():
            file_path = value.name()
            data_type = value.value_type()
            if data_type == 3:
                data_as_regbin = value.raw_data()[0:16]
                data_as_integer = int.from_bytes(data_as_regbin, byteorder='little', signed='False')
                data_as_epoch = int(float(data_as_integer/10000000-11644473600))
                timestamp = (data_as_epoch)
                delim = "|"
                if len(sys.argv) == 3:
                    if sys.argv[2] == "-c":
                        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(int(timestamp)))
                        delim = ","
                print("%s%sBAM%s%s%s%s%s%s" % (timestamp, delim, delim, compname, delim, profile_name, delim, file_path))
if __name__ == '__main__':
    main()
