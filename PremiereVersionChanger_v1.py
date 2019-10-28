# Convert a Premiere Pro Project from version 37 to version 36
# User will enter the file version 37 of Premiere Pro with the full path
# and will get a folder with a project inside of version 36
# created by Jesus Panadero


# import tkinter as tk

from tkinter import *
import os
import gzip
import xml.etree.ElementTree as et
import shutil


def gunzip_shutil(source_filepath, dest_filepath, block_size=65536):
    with gzip.open(source_filepath, 'rb') as s_file, \
            open(dest_filepath, 'wb') as d_file:
        shutil.copyfileobj(s_file, d_file, block_size)

def convert(file):
    # file and path separation
    f = userInput.get()
    file2convert = f.split("\\")[-1]                # takes the file name with extension
    file2comvert_name = file2convert.split(".")[0]  # remove extension
    file2convert_ext = file2convert.split(".")[1]   # store the extension only
    path2file = os.path.dirname(os.path.abspath(f)) # takes the path to the file


    # _____ convertion begins____

    # step 1: create a new folder and copy the file to the folder renamed with sufix "_changed"
    # build the path
    path_1 = (path2file, file2comvert_name)         # the new directory is path + file name
    path_2 = "\\".join(path_1)                      # done
    path_3 = (path_2, "changed")                    # add the underscore "change" sufix to path
    new_dir = "_".join(path_3)                      # done

    xml2change_list = (new_dir, file2comvert_name)  # xml to convert
    xml2change = "\\".join(xml2change_list)         # name of xml file compressed

    # create folder
    try:
        os.makedirs(new_dir)
    except OSError:
        Label(mw, text="Creation of the directory %s failed" % new_dir).grid(row=6, column=3, sticky=W)
    else:
        Label(mw, text="Successfully created the directory %s " % new_dir).grid(row=6, column=3, sticky=W)

    # build the new file name
    new_name = (file2comvert_name, "changed")       # create name of new file with no extension just add sufix "_changed"
    new_file_name = "_".join(new_name)              # done - apply to the new xml name and new project name
    full_path = (new_dir, new_file_name)            # take the full path to the new files
    full_file_path = "\\".join(full_path)           # done - apply to the new xml name and new project name
    full_xml_path = full_file_path + ".xml"         # add ext .xml to the path. This is the xml file to be changed

    # copy file
    try:
        shutil.copy(f, xml2change)
    except OSError:
        Label(mw, text="Copy of the file %s failed" % xml2change).grid(row=7, column=3, sticky=W)
    else:
        Label(mw, text="Successfully copy of the file %s " % xml2change).grid(row=7, column=3, sticky=W)

    # step 2: unzip gz file to a xml file
    gunzip_shutil(xml2change, full_xml_path)            # extract the xml file to the directory to be changed

    # # step 3: change the version number
    with open(full_xml_path, encoding='UTF-8') as f:
        tree = et.parse(f)
        xml_file = tree.getroot()

    version = xml_file.find("./Project[@Version]")
    # v = version.attrib["Version"]
    # print(type(version))
    # print("Version >> ", version)
    # print(version.attrib)
    version.attrib["Version"] = '36'

    tree.write(full_xml_path)

    # # step 4: compress the file to a gz and rename to a premiere project
    fin = full_xml_path
    fout = full_file_path + ".prproj"
    with open(fin, 'rb') as f_in, gzip.open(fout, 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)
    Label(mw, text="Succesfully, PREMIERE PROJECT VERSION 36 CREATED.").grid(row=8, column=3, sticky=W)

    # cleaning files
    os.remove(xml2change)
    os.remove(full_xml_path)

def func(v):
    # check if userInput has the extension .prproj
    check = userInput.get()
    if check.endswith('.prproj'):
        Label(mw, text="Converting file to a previous version of premiere").grid(row=3, column=3, sticky=W)
        convert(check)
    else:
        Label(mw, text=" The file refered is not a Premiere Project.").grid(row=3, column=3, sticky=W)
    return check

if __name__ == '__main__':
    mw = Tk()
    mw.title("Premiere Pro Version Changer")
    mw.geometry("1000x150")

    userInput=StringVar()
    Label(mw, text=" ").grid(row = 1, column = 1)
    Label(mw, text=" Enter a premiere project file with full path: ").grid(row = 2, column = 1, sticky=W)
    Entry(mw, textvariable=userInput).grid(row = 2, column = 2)
    mw.bind('<Return>', func)

    mw.mainloop()