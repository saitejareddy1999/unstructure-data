import os
import ctypes

path = "C:/AWS"
# s=path.split('/')
# print(s)
listPath = []
# listPath.append('EC2')

# tempPath = ""
# for i in listPath:
#     tempPath = tempPath + i + "/"
# print(tempPath)

def initialPath(selectedPath):
   listPath.append(selectedPath)

def fetchFolders():
    tempPath = ""
    for i in listPath:
        tempPath = tempPath + i + "/"
    if tempPath == "":
        return "exception!! ";
    result = os.listdir(tempPath);
    folders = ();
    for each in result:
        if os.path.isdir(tempPath+"/"+each):
            folders(each);
    # print(folders);
    return folders;


def forward(folder):
    listPath.append(folder);
    tempPath = ""
    for i in listPath:
        tempPath = tempPath + i + "/"
    print("inside forward"+tempPath);
    return fetchFolders();


def backward():
    if(len(listPath) <= 1):
        print("cannot go up level")
        return False;
    else:
        listPath.pop();
        tempPath = ""
        for i in listPath:
            tempPath = tempPath + i + "/"
        fetchFolders();


# initialPath('C:')
# fetchFolders();
# forward('----------DOCUMENTS-------')

d = "C:\\".replace("\\","")
print(d)
# backward()
# forward('LPP')
# forward('Beauregard')
# print(listPath)
# print(os.path);

