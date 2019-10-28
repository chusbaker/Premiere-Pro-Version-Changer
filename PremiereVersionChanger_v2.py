'''
Adobe Premiere Pro Version Changer allows you to change the version in which a project has been created (any version of Premiere Pro)
to version 1, so it can be open in any version of Premiere, as far as the contents of the project allow that. To change the version, 
go to the line 110 of the code and change the version number there.
@ chusbaker 2019

'''
import os
import gzip
import xml.etree.ElementTree as et
import shutil
import sys
from PySide2.QtWidgets import (QApplication, QMainWindow, QLabel, QToolTip)


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowTitle('Premiere Pro Version Changer')

        self.label1 = QLabel('Drop your file here', self)
        self.label1.move(120, 90)

        QToolTip.setFont('Helvetica')
        self.setToolTip('Drag and Drop a <b>Premiere Project File</b> to be converted into this window. As soon as the file is dropped, you will find a folder named as the Project File with the extension "_changed" in the same location where the Project File that you dopped is located. Inside, you will find a <b>Converted Premiere Project File</b>.')


        self.setAcceptDrops(True)


    def greetings(self):
        print("Hello %s" % self.edit.text())

    def dragEnterEvent(self, e):
        if e.mimeData().hasUrls():
            e.acceptProposedAction()

    def dropEvent(self, e):
        for url in e.mimeData().urls():
            userInput = url.toLocalFile()
            print("Change Version on Project: " + userInput)
            func(userInput)
        return userInput


def gunzip_shutil(source_filepath, dest_filepath, block_size=65536):
    with gzip.open(source_filepath, 'rb') as s_file, \
            open(dest_filepath, 'wb') as d_file:
        shutil.copyfileobj(s_file, d_file, block_size)

def convert(userInput):
    # file and path separation
    print("value of userInput is: ", userInput)
    # convert the string to a path
    f = userInput
    file2convert = f.split("/")[-1]                # takes the file name with extension
    print("file2 convert: ", file2convert)
    file2comvert_name = file2convert.split(".")[0]  # remove extension
    # file2convert_ext = file2convert.split(".")[1]   # store the extension only
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
        label2 = QLabel('Creation of the directory %s failed' % new_dir)
        label2.move(120, 90)
    else:
        label3 = QLabel('Successfully created the directory %s ' % new_dir)
        label3.move(120, 90)

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
        label4 = QLabel("Copy of the file %s failed" % xml2change)
        label4.move(120, 100)
    else:
        label5 = QLabel("Successfully copy of the file %s " % xml2change)
        label5.move(120, 100)
    # step 2: unzip gz file to a xml file
    gunzip_shutil(xml2change, full_xml_path)            # extract the xml file to the directory to be changed

    # # step 3: change the version number
    with open(full_xml_path, encoding='UTF-8') as f:
        tree = et.parse(f)
        xml_file = tree.getroot()

    version = xml_file.find("./Project[@Version]")
    # change the number in next line so the version to which you want to move to
    version.attrib["Version"] = '1'

    tree.write(full_xml_path)

    # # step 4: compress the file to a gz and rename to a premiere project
    fin = full_xml_path
    fout = full_file_path + ".prproj"
    with open(fin, 'rb') as f_in, gzip.open(fout, 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)
    label6 = QLabel("Succesfully, PREMIERE PROJECT VERSION 36 CREATED.")
    label6.move(120, 110)
    # cleaning files
    os.remove(xml2change)
    os.remove(full_xml_path)

def func(userInput):
    # check if userInput has the extension .prproj
    check = userInput
    print(userInput)
    if check.endswith('.prproj'):
        label0 = QLabel("Converting file to a previous version of premiere")
        label0.move(120, 80)
        convert(check)
    else:
        label10 = QLabel(" The file refered is not a Premiere Project.")
        label10.move(120, 80)
    return check



def main():
    userInput = "glogal"

    app = QApplication(sys.argv)

    window = MainWindow()
    window.resize(350, 250)

    window.show()

    app.exec_()

if __name__ == '__main__':
    main()

