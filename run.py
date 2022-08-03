import json
import os
import sys
import ast
import time
from functools import wraps
from tkinter import Tk, filedialog, Button
from flask_login import login_required
import tkinter.ttk as ttk
from tkinter.filedialog import askdirectory
import win32api, pywintypes, win32wnet
from ldap3 import Server, Connection, ALL, NTLM
from ldap3.core.exceptions import LDAPBindError
import ldap3
from forms import LoginForm
from stubs import STALE
# from STALE import getListOfFiles, getCount, getListOfFilesOneLevel
from flask import Flask, render_template, url_for, redirect, send_from_directory, request, jsonify, session, flash, \
    Response

app = Flask(__name__, template_folder='templates', static_url_path='', static_folder='static')
cls = STALE()
app.config['SECRET_KEY']='91a52a9fdbb83c1762f518c62c9b8924'

driveIndexes = [];
def showDrives():
    drives = win32api.GetLogicalDriveStrings()
    drives = drives.split('\000')[:-1]
    for i in drives:
        driveIndexes.append(i)
    
    ##driveIndexes = drives
    return drives


# drivesDict = {};
# def showDrives():
#     drives = win32api.GetLogicalDriveStrings()
#     drives = drives.split('\000')[:-1]
#     count = 0;
#     getNetworkDrives(0, len(drives), drives, drivesDict)
#     print("driveslist", drivesDict)
#     return drivesDict

# def getNetworkDrives(count, len, drives, drivesDict):
#     try:
#         if count == len: 
#             return
#         else:
#             d = win32wnet.WNetGetUniversalName(drives[count])
#             drivesDict.update({drives[count]: d})
#             # list.append(d);
#             # print(d);s
#             getNetworkDrives(count+1, len, drives, drivesDict)
#     except pywintypes.error as e:
#         print("not a network drive")
#         getNetworkDrives(count+1, len, drives, drivesDict);

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            print("session")
            return f(*args, **kwargs)
        else:
            print("session not found")
            flash("You need to login first", "danger")
            return redirect(url_for('login'))
    return wrap

@app.route('/')
@login_required
def index():
    drives = showDrives();
    print("returned", drives);
    return render_template('home.html', msg='Archived Stubs', connected = drives)

@app.route('/get')
def get():
    return redirect(url_for('index'))
@app.route('/login',methods=["POST","GET"])
def login():
    
    form = LoginForm()
    if form.validate_on_submit():
        if form.username.data == 'GBNN8A' and form.password.data == 'password':
            print("logged in")
            flash('You have been logged in!', 'success')
            session['logged_in'] = True
            return redirect(url_for('index'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)

# @app.route('/login',methods=["POST","GET"])
# def login():
#     form = LoginForm()
#     # server = Server('LDAP://LDAP-EMEA.zurich.uat/', use_ssl=True, get_info=ALL)
#     if form.validate_on_submit():
#         try: 
#             server = Server('LDAP://LDAP-EMEA.Zurich.uat', use_ssl=True, get_info=ALL)
#             conn = Connection(server, form.username.data, form.password.data, auto_bind=True)
#             print('LDAP Bind Successful.')
#             print("logged in")
#             flash('You have been logged in!', 'success')
#             session['logged_in'] = True
#             return redirect(url_for('index'))
            
#         except ldap3.core.exceptions.LDAPBindError:
#             print('LDAP Bind Failed: ')
#             print(form.username.data) 
#             print(form.password.data)
#             flash('Login Unsuccessful. Please check username and password', 'danger')
        
#     return render_template('login.html', title='Login', form=form)

@app.route('/logout')
def logout():
    session.pop('logged_in',None)
    return redirect(url_for('login'))

@app.route('/check')
@login_required
def checkindex():
    return render_template('check.html')

@app.route("/counter",methods=["POST","GET"])
@login_required
def ajaxfilecounter():
    if request.method == 'POST':
        data = request.form['data']
        res = ast.literal_eval(data)
        return render_template('prereport.html', rowdata=res)


@app.route("/ajaxmovestubs",methods=["POST","GET"])
@login_required
def ajaxmovestubs():
    if request.method == 'POST':
        
        folderPath = request.form['folderPath']
        optProc = request.form['optProc']
        try:
            noSubFolders = request.form['noSubFolders']#if we select checkbox as mark it will treat as 'yes' that means it will not include any subfolders
        except KeyError as e:
            noSubFolders = 'NO'
            
        # folderPath = 'C:\python\zurich\stubs\Destination'
        start = time.time()
        if noSubFolders == 'YES':
            FileData =  cls.getListOfFilesOneLevel(folderPath, optProc)#getListOfFilesOneLevel this is for it will read only one file and delete or separate unwanted data
        else:
            FileData =  cls.getListOfFiles(folderPath, optProc)
        end = time.time()
        processTime = end-start 
        s=round(processTime,1)
        print(s)
        # FileData =  getStubsStale(folderPath)
        CountData = cls.getCount(FileData, folderPath, optProc)
        CountData.update({'ptime' : s, 'noSubFolders' : noSubFolders})
        
        msg = f'{CountData}'
    return jsonify(msg)

##confirmation call
@app.route("/stubsconfirm",methods=["POST","GET"])
@login_required
def stubsconfirm():
    if request.method == 'POST':
        flash('processing pls wait','success')
        folderPath = request.form['folderPath']
        optProc = request.form['optProc']
        try:
            noSubFolders = request.form['noSubFolders']
        except KeyError as e:
            noSubFolders = 'NO'
            
        start = time.time()
        if noSubFolders == 'YES':
            CountData =  cls.getListOfFilesOneLevel(folderPath, optProc, 'Yes')#yes means for deletion confirmation will trigger,getListOfFilesOneLevel this is for it will read only one file and delete or separate unwanted data
        else:
            CountData =  cls.getListOfFiles(folderPath, optProc, 'Yes')
        msg = f'{CountData}'
    return jsonify(msg)

# @app.route("/opendialog/<driveIndex>",methods=["POST","GET"])
# def opendialog(driveIndex):
#     open_folder = 'Select Folder Path'
#
#     if request.method == 'POST':
#         content = request.get_json(silent=True)
#         # drivesList = list(drivesDict)
#         # selectedDrive = drivesList[int(driveIndex) - 1]
#         selectedDrive = driveIndexes[(int)(driveIndex) - 1]
#         print("the selected drive is -> ", selectedDrive);
#         root = Tk()
#         root.withdraw()
#         root.attributes('-topmost', True)
#         open_folder = filedialog.askdirectory(initialdir=selectedDrive)
#         root.iconify()
#         root.deiconify()
#         root.destroy()
#         root.mainloop()
#     return jsonify(open_folder)




#############################################################################

import os

listPath = []

def convert_path():
    temp_path = ""
    for i in listPath:
        temp_path = temp_path + i + "/"    
    return temp_path


@app.route("/initial_path/<selected_drive>",methods=["POST","GET"])
def initial_path(selected_drive):
   listPath.clear()
   selectedDrive = driveIndexes[(int)(selected_drive) - 1].replace("\\","")
   print("selected drive split",selectedDrive)
   updatedSelectedDrive = selectedDrive
   listPath.append(updatedSelectedDrive)
   return "path selected"+listPath[0]

@app.route("/get_folder_path/<selectedFolder>", methods=["POST", "GET"])
def get_folder_path(selectedFolder):
    folder_path = convert_path() + selectedFolder
    return folder_path

@app.route("/get_folders",methods=["POST","GET"])
def fetch_folders():
    tempPath = convert_path()
    if tempPath == "":
        try:
            tempPath = convert_path()
            r = os.listdir(tempPath)
            folders = []
            for each in r:
                if os.path.isdir(tempPath+"/"+each):
                    folders.append(each)     
        except FileNotFoundError:
            flash("Drive not selected", "danger")
            return redirect(url_for('index'))
    result = os.listdir(tempPath)
    folders = []
    for each in result:
        if os.path.isdir(tempPath+"/"+each):
            folders.append(each)
    print(folders)
    return render_template("file_dialog.html",path =convert_path(), selectedDrive = listPath[0], connected = showDrives(), folders = folders)

@app.route("/move_forward/<folder>")
def forward(folder):
    try:
        listPath.append(folder);
        tempPath = convert_path()
        print("inside forward"+tempPath)
        return redirect(url_for('fetch_folders'))
    except FileNotFoundError:
        flash("You cannot go level up.", "danger")
        return redirect(url_for('fetch_folders'))

@app.route("/move_back")
def backward():
    if(len(listPath) <= 1):
        flash("You cannot go level up. This is root directory", "danger")
        return redirect(url_for('fetch_folders'))
    else:
        listPath.pop()
        return redirect(url_for('fetch_folders'))


def main():
    app.run(debug=True, port=5000, host='127.0.0.1')

if __name__ == '__main__':
    main()