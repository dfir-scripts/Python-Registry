import sys
import time
from Registry import Registry

def usage():
    return "USAGE:\n  %s <Windows System Registry File> -c (Outputs csv and date)\n\n Search BAM key for evidence of file execution\n Requires Python 3 and Python Registry\n" % sys.argv[0]

def main():
    # Requirements check
    try:
        assert sys.version_info >= (3, 0)
        assert len(sys.argv) >= 2
    except:
        print(usage())
        sys.exit(-1)

    # Open the Registry file and retrieve the "Current" ControlSet
    try:
        registry = Registry.Registry(sys.argv[1])
        select = registry.open("Select")
        current = select.value("Current").value()
    except:
        # Silently handle missing "Select" key or "Current" value
        sys.exit(-1)

    # Retrieve the computer name
    compname = "Unknown"  # Default value if the key is not found
    try:
        cname_key = registry.open("ControlSet00%d\\Control\\ComputerName\\ComputerName" % (current))
        for cname in cname_key.values():
            if cname.name() == "ComputerName":
                compname = cname.value()
    except:
        pass  # Silently handle missing "ComputerName" key or value

    # Open BAM/DAM keys
    bamdam_key = None
    try:
        bamdam = ["bam", "dam"]
        for moderator in bamdam:
            try:
                bamdam_key = registry.open("ControlSet00%d\\Services\\%s\\UserSettings" % (current, moderator))
                break  # Exit the loop if the key is found
            except:
                pass  # Silently handle missing BAM/DAM keys
    except:
        pass

    # If no BAM/DAM key is found, exit silently
    if bamdam_key is None:
        sys.exit(0)

    # Process the BAM/DAM keys
    for profile in bamdam_key.subkeys():
        try:
            profile_name = profile.name()
        except:
            continue  # Silently skip profiles with errors
        for value in profile.values():
            try:
                file_path = value.name()
                data_type = value.value_type()
                if data_type == 3:  # Check if the value is REG_BINARY
                    data_as_regbin = value.raw_data()[0:16]
                    data_as_integer = int.from_bytes(data_as_regbin, byteorder='little', signed=False)
                    data_as_epoch = int(float(data_as_integer / 10000000 - 11644473600))
                    timestamp = data_as_epoch
                    delim = "|"
                    if len(sys.argv) == 3 and sys.argv[2] == "-c":
                        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(int(timestamp)))
                        delim = ","
                    print("%s%sBAM%s%s%sUser_Profile: %s;Path: %s" % (timestamp, delim, delim, compname, delim, profile_name, file_path))
            except:
                pass  # Silently skip values with errors

if __name__ == '__main__':
    main()
