import os
import shutil#basically it performs with file operations,ability to copy files, move files,remove files this mainly occurrs in deletion confirmation sections copy for separation remove for deletion
import sys
from datetime import datetime
import logging
import csv

from PyQt5.QtWidgets import (QWidget, QPushButton, QLineEdit, QInputDialog, QApplication, QFileDialog)

class STALE():
    def __init__(self):
        super().__init__()

    # self.initUI()
    def remoteConnection():
        #remote connection between linux application and windows server
        pass
        # return listofserver
    
    def initUI(self):
        self.btn = QPushButton('Dialog', self)
        self.btn.move(20, 20)
        self.btn.clicked.connect(self.showDialog)

        self.le = QLineEdit(self)
        self.le.move(130, 22)

        self.setGeometry(300, 300, 450, 350)
        self.setWindowTitle('Input dialog')
        self.show()
    #text is read me file and .url is archive stub file
    def errHandle(self, filepathname):
        logging.basicConfig(filename=filepathname, level=logging.DEBUG, 
                        format='%(asctime)s %(levelname)s %(name)s %(message)s')
    
    def getListOfFiles(self, dirName, optProc, confirmAct='No'):
        self.errHandle('ArchivedError.log')
        
        # create a list of file and sub directories 
        # names in the given directory 
        listOfFile = os.listdir(dirName)
        allFiles = list()
        totalArch = 0
        totalReadme = 0
        num = 1
        
        ##creating CSV file for report
        '''
        today = datetime.today() 
        csvfilename = today.strftime('%d-%m-%Y') + "_Stub_Reports_.csv"
        fieldnames = ['S#','Path','File Name', 'Date and Time', 'File Type', 'Status', 'Size']
        file_exists = os.path.isfile(csvfilename)
        with open(csvfilename, 'a', newline='') as new_file:
            csv_writer = csv.DictWriter(new_file, fieldnames=fieldnames)
            if not file_exists:
                csv_writer.writeheader()
        ##end csv
        '''
        dict_counter = {'Archived_Stubs_Folders':0, 'Stub_Files': 0, 'ReadMe_Files' : 0, 'msg' : 'Stubs ARCHIVED, Read Me process completed', 'FolderPath': dirName, "optProc" : optProc}
        StubFolder_Count = 0
        StubFile_Count = 0
        ReadMe_Count = 0
        filenameColl = []
        # Iterate over all the entries
        for entry in sorted(listOfFile):
            # Delete Archived DIR
            if optProc == 'Delete' and confirmAct == 'Yes' and entry == 'Archived_File_Stubs':
                if os.path.exists(os.path.join(dirName, entry)):
                    shutil.rmtree(os.path.join(dirName, entry))
            # Create full path
            fullPath = os.path.join(dirName, entry)
            
            if entry == 'Archived_File_Stubs':
                StubFolder_Count +=1
            if ('ARCHIVE STUB' in entry.upper() or 'ARCHIVESTUB' in entry.upper()) and entry != 'Archived_File_Stubs' and entry.endswith('.url'):
                StubFile_Count +=1
            #if we take separation we will take this
            # If entry is a directory then get the list of files in this directory 
            if os.path.isdir(fullPath) and entry != 'Archived_File_Stubs':
                allFiles = allFiles + self.getListOfFiles(fullPath, optProc, confirmAct)
                if entry == 'Archived_File_Stubs':
                    allFiles.append(fullPath)
            else:#separation will come in this area               
                ##remove readme file
                filename = os.path.join(dirName, entry)
                allFiles.append(fullPath)
                if os.path.isfile(filename):
                    file_size = os.path.getsize(filename)/1024
                #and file_size <= 3
                if 'Archived_File_Stubs' in dirName:
                    StubFolder_Count +=1
                ##1)Remove archived stub file and read me file (.txt)
                if 'STALE DATA – PLEASE READ' in entry.upper() and entry.endswith('.txt'): 
                    if os.path.isfile(filename):
                        if optProc == 'Delete' and confirmAct == 'Yes':
                            os.remove(filename)
                        # fields={'S#':num,'Path':dirName,'File Name':entry, 'Date and Time':today.strftime('%d-%m-%Y %H:%M:%S'), 'File Type':'Readme File', 'Status': optProc, 'Size':file_size}
                        # # # csv_writer.writerow(fields)
                        num+=1
                        totalReadme +=1
                        ReadMe_Count +=1
                        # dict_counter.update({'ReadMe_Files':ReadMe_Count})
                
                ##Delete Existing archived folder and all its contents        
                if optProc == 'Delete' and confirmAct == 'Yes' and entry == 'Archived_File_Stubs':
                    if os.path.exists(os.path.join(dirName, entry)):
                        shutil.rmtree(os.path.join(dirName, entry))
                        
                ##Remove archived stub file and read me file (.url )
                if ('ARCHIVE STUB' in entry.upper() or 'ARCHIVESTUB' in entry.upper()) and 'Archived_File_Stubs' not in dirName and entry.endswith('.url'):
                    newDir = os.path.join(dirName, 'Archived_File_Stubs')
                    if (not os.path.exists(newDir) and optProc == 'Separate'):
                        os.mkdir(newDir)
                        # StubFolder_Count +=1
                    try:
                        if optProc == 'Delete' and confirmAct == 'Yes':
                            if os.path.isfile(os.path.join(dirName, entry)):
                                os.remove(os.path.join(dirName,entry ))
                                
                        if optProc == 'Separate':
                            shutil.move(os.path.join(dirName, entry), newDir)
                        
                            totalArch +=1     
                            # StubFile_Count +=1         
                            dict_counter.update({'Stub_Files':StubFile_Count})          
                            fields={'S#':num,'Path':dirName,'File Name':entry, 'Date and Time':today.strftime('%d-%m-%Y %H:%M:%S'), 'File Type':'Archive Stubs', 'Status':'Deleted', 'Size':'3KB'}
                            # # # csv_writer.writerow(fields)
                            num+=1           
                    except Exception as err:
                        errMsg = sys.exc_info().__str__()
                        logger = logging.getLogger(__name__)
                        logger.error(str(entry) + str(err))
                        print ('exception is raised for ' + str(entry), errMsg )
                        continue
                    # exit(0)
                
                    
            #  if type(fullPath) == int:
            
        # print(dict_counter)
        # dict_counter.update({'Stub_Files':StubFile_Count, 'Archived_Stubs_Folders':StubFolder_Count, 'Archived_Stubs_Folders':StubFolder_Count, 'all' : filenameColl})
        
        return allFiles

    def getListOfFilesOneLevel(self, dirName, optProc, confirmAct='No'):
        self.errHandle('ArchivedError.log')
        # create a list of file and sub directories 
        # names in the given directory 
        listOfFile = os.listdir(dirName)
        allFiles = list()
        totalArch = 0
        totalReadme = 0
        num = 1
            
        dict_counter = {'Archived_Stubs_Folders':0, 'Stub_Files': 0, 'ReadMe_Files' : 0, 'msg' : 'Stubs ARCHIVED, Read Me process completed', 'FolderPath': dirName, "optProc" : optProc}
        StubFolder_Count = 0
        StubFile_Count = 0
        ReadMe_Count = 0
        filenameColl = []
        # Iterate over all the entries
        for entry in sorted(listOfFile):
            # Delete Archived DIR
            if optProc == 'Delete' and confirmAct == 'Yes' and entry == 'Archived_File_Stubs':
                if os.path.exists(os.path.join(dirName, entry)):
                    shutil.rmtree(os.path.join(dirName, entry))
            # Create full path
            fullPath = os.path.join(dirName, entry)
            
            if entry == 'Archived_File_Stubs':
                StubFolder_Count +=1
            if ('ARCHIVE STUB' in entry.upper() or 'ARCHIVESTUB' in entry.upper()) and entry != 'Archived_File_Stubs' and entry.endswith('.url'):
                StubFile_Count +=1
            
            # If entry is a directory then get the list of files in this directory 
            
            ##remove readme file
            filename = os.path.join(dirName, entry)
            allFiles.append(fullPath)
            if os.path.isfile(filename):
                file_size = os.path.getsize(filename)/1024
            #and file_size <= 3
            if 'Archived_File_Stubs' in dirName:
                StubFolder_Count +=1
                
            if 'STALE DATA – PLEASE READ' in entry.upper() and entry.endswith('.txt'): 
                if os.path.isfile(filename):
                    if optProc == 'Delete' and confirmAct == 'Yes':
                        os.remove(filename)
                    # fields={'S#':num,'Path':dirName,'File Name':entry, 'Date and Time':today.strftime('%d-%m-%Y %H:%M:%S'), 'File Type':'Readme File', 'Status': optProc, 'Size':file_size}
                    # # # csv_writer.writerow(fields)
                    num+=1
                    totalReadme +=1
                    ReadMe_Count +=1
                    # dict_counter.update({'ReadMe_Files':ReadMe_Count})
            
            ##Delete Existing archived folder and all its contents        
            if optProc == 'Delete' and confirmAct == 'Yes' and entry == 'Archived_File_Stubs':
                if os.path.exists(os.path.join(dirName, entry)):
                    shutil.rmtree(os.path.join(dirName, entry))
                    
            ##Remove archived stub file and read me file (.url & .txt)
            if ('ARCHIVE STUB' in entry.upper() or 'ARCHIVESTUB' in entry.upper()) and 'Archived_File_Stubs' not in dirName and entry.endswith('.url'):
                newDir = os.path.join(dirName, 'Archived_File_Stubs')
                if (not os.path.exists(newDir) and optProc == 'Separate'):
                    os.mkdir(newDir)
                    # StubFolder_Count +=1
                try:
                    if optProc == 'Delete' and confirmAct == 'Yes':
                        if os.path.isfile(os.path.join(dirName, entry)):
                            os.remove(os.path.join(dirName,entry ))
                            
                    if optProc == 'Separate':
                        shutil.move(os.path.join(dirName, entry), newDir)
                    
                        totalArch +=1     
                        # StubFile_Count +=1         
                        dict_counter.update({'Stub_Files':StubFile_Count})          
                        fields={'S#':num,'Path':dirName,'File Name':entry, 'Date and Time':today.strftime('%d-%m-%Y %H:%M:%S'), 'File Type':'Archive Stubs', 'Status':'Deleted', 'Size':'3KB'}
                        # # # csv_writer.writerow(fields)
                        num+=1           
                except Exception as err:
                    errMsg = sys.exc_info().__str__()
                    logger = logging.getLogger(__name__)
                    logger.error(str(entry) + str(err))
                    print ('exception is raised for ' + str(entry), errMsg )
                    continue
                # exit(0)
                
                    
            #  if type(fullPath) == int:
            
        # print(dict_counter)
        # dict_counter.update({'Stub_Files':StubFile_Count, 'Archived_Stubs_Folders':StubFolder_Count, 'Archived_Stubs_Folders':StubFolder_Count, 'all' : filenameColl})
        
        return allFiles
    def getCount(self, FileListData, folderPath, optProc):
        StubFile_Count = 0
        ReadMe_Count = 0
        StubFolder_Count = 0
        dict_counter = {}
        
        for entry in FileListData:
            if 'Archived_File_Stubs' in entry:
                if (os.path.isdir(entry)):
                    StubFolder_Count +=1
                    
            if ('ARCHIVE STUB' in entry.upper() or 'ARCHIVESTUB' in entry.upper()) and entry.endswith('.url'):
                StubFile_Count +=1
                
            if 'STALE DATA – PLEASE READ' in entry.upper() and entry.endswith('.txt'):
                ReadMe_Count +=1
                
        dict_counter.update({'Stub_Files':StubFile_Count, 'ReadMe_Files':ReadMe_Count, 'Archived_Stubs_Folders':StubFolder_Count, 'all' : 'Jess', 'msg' : 'Stubs ARCHIVED, Read Me process completed', 'FolderPath': folderPath, 'optProc' : optProc})
        
        return dict_counter