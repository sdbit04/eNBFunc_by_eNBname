import gzip
import argparse
import os

# root_dir = r"D:\D_drive_BACKUP\MENTOR\yubaraj\enbfunc_name_by_enbname\CM Files"


def get_orig_and_replacement_gz(path_CFG_gz_file):
    NENAME = None
    FUNCNAME = None
    FUNCNAME_tag = None
    with gzip.open(path_CFG_gz_file, 'rb') as cfg_file_ob:
        file_serial = cfg_file_ob.read()
        cfg_file_ob.seek(0)
        lines = cfg_file_ob.readlines()
        for line in lines:
            if b"<NENAME>" in line:
                NENAME = line.split(b">")[1].split(b"<")[0]
                print("NENAME={}".format(NENAME))
            elif b"<eNodeBFunctionName>" in line:
                FUNCNAME = line.split(b">")[1].split(b"<")[0]
                FUNCNAME_tag = "eNodeBFunctionName"
                print("FUNCNAME={}".format(FUNCNAME))
            if NENAME is not None and FUNCNAME is not None:
                break
            # print(line)
        return FUNCNAME, NENAME, FUNCNAME_tag, file_serial


def get_orig_and_replacement_xml(path_CFG_xml_file):
    NENAME = None
    FUNCNAME = None
    FUNCNAME_tag = None
    with open(path_CFG_xml_file, 'r') as cfg_xml_file_ob:
        file_serial = cfg_xml_file_ob.read()
        cfg_xml_file_ob.seek(0)
        lines = cfg_xml_file_ob.readlines()
        for line in lines:
            if "<NENAME>" in line:
                NENAME = line.split(">")[1].split("<")[0]
                print("NENAME={}".format(NENAME))
            elif "<eNodeBFunctionName>" in line:
                FUNCNAME = line.split(">")[1].split("<")[0]
                FUNCNAME_tag = "eNodeBFunctionName"
                print("FUNCNAME={}".format(FUNCNAME))
            if NENAME is not None and FUNCNAME is not None:
                break
    return FUNCNAME, NENAME, FUNCNAME_tag, file_serial


def replace_and_write_in_new_zip_file(path_CFG_gz_file):
    print("Updating {}".format(path_CFG_gz_file))
    try:
        funcname, nename, FUNCNAME_tag, file_serial = get_orig_and_replacement_gz(path_CFG_gz_file)
        # print("type of file-serial is {}".format(type(file_serial)))
        # print("NODEBFUNCTIONNAME is {}".format(funcname))
        # print("NENAME is {}".format(funcname))
        # FUNCNAME_tag = FUNCNAME_tag.encode()
        # print("functagname = {}".format(FUNCNAME_tag))
        funcname = funcname.decode()
        nename = nename.decode()
        file_serial = file_serial.decode()

        orig_func_tag = "<{0}>{1}</{0}>".format(FUNCNAME_tag, funcname)
        new_func_tag = "<{0}>{1}</{0}>".format(FUNCNAME_tag, nename)
        print("Orig =  {}".format(orig_func_tag))
        print("New = {}".format(new_func_tag))

        orig_func_tag = orig_func_tag
        new_func_tag = new_func_tag
        file_serial = file_serial.replace(orig_func_tag, new_func_tag)
        file_serial = file_serial.encode()
    except (TypeError, AttributeError):
        print("There was an unhandled exception, file was not updated, need to debug, please check and share the file {}".format(path_CFG_gz_file))
    else:
        with gzip.open(path_CFG_gz_file, 'wb') as cfg_xml_new_ob:
            cfg_xml_new_ob.write(file_serial)
            print("{} updated successfully ".format(path_CFG_gz_file))


def replace_and_write_in_new_file(path_CFG_xml_file):
    print("Updating {}".format(path_CFG_xml_file))
    try:
        funcname, nename, FUNCNAME_tag, file_serial = get_orig_and_replacement_xml(path_CFG_xml_file)
        orig_func_tag = "<{0}>{1}</{0}>".format(FUNCNAME_tag, funcname)
        new_func_tag = "<{0}>{1}</{0}>".format(FUNCNAME_tag, nename)
        file_serial = file_serial.replace(orig_func_tag, new_func_tag)
    except (TypeError, AttributeError):
        print(
            "There was an unhandled exception, file was not updated, need to debug, please check and share the file {}".format(path_CFG_xml_file))
    else:
        with open(path_CFG_xml_file, 'w') as CFG_xml_new_ob:
            CFG_xml_new_ob.write(file_serial)
            print("{} updated successfully ".format(path_CFG_xml_file))


def search_and_update(base_directory):
    root_path = os.path.abspath(base_directory)
    for present_dir, dirs, files in os.walk(top=root_path):
        # print(l, m, n)
        print("Present dir = {}".format(present_dir))
        for file in files:
            if str(file) == "CFGDATA.XML.gz":
                file_path = os.path.join(present_dir, file)
                try:
                    replace_and_write_in_new_zip_file(file_path)
                except:
                    print("Failed to update the file")

            elif str(file) == "CFGDATA.XML":
                file_path = os.path.join(present_dir, file)
                try:
                    replace_and_write_in_new_file(file_path)
                except:
                    print("Failed to update the file")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="provide input_dir, and reference file path")
    parser.add_argument("input_folder", help="Provide input folder path as first argument")
    print("Help contact : swapankumar.das@teoco.com")
    args = parser.parse_args()
    input_folder = args.input_folder
    search_and_update(input_folder)

