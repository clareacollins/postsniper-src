import os, re, shutil

### STRING PROCESSING ###
# Passed a tumblrfirst link, returns user and code
def extractUserAndCode(link):
    user = link.split("/")[3]
    code = link.split("/")[4]
    return user, code

# Passed file title and data, writes data to file at location
def write(title, data):
    csvText = ""
    if isinstance(data, str):
        csvText = data
    else:
        for tuple in data:
            if isinstance(tuple, str):
                csvText += tuple + "\n"
            else:
                csvText += "@".join(tuple) + "\n"
    os.chdir(REDACTED)
    FileObject = open(title, "w", encoding="utf-8")
    FileObject.write(csvText)
    FileObject.close()

### FILE READERS ###
# Passed file location, returns file text
def read(file_dir):
    if not os.path.exists(file_dir):
        return ""
    else:
        FileObject = open(file_dir, "r")
        FileText = FileObject.read()
        FileObject.close()
        return FileText

def readLines(file_dir):
    if not os.path.exists(file_dir):
        return []
    else:
        FileObject = open(file_dir, "r")
        FileLines = FileObject.readlines()
        FileObject.close()
        return [line.strip() for line in FileLines if line.strip() != ""]

def readCSV(file_dir):
    if not os.path.exists(file_dir):
        return []
    else:
        FileObject = open(file_dir, "r")
        FileText = FileObject.readlines()
        FileObject.close()
        return [line.split(",") for line in FileText]

# Read Derivative Process, returns lines in quotes for google search
def grabSearch(target_file):
    FileObject = open(target_file, "r", errors="ignore")
    searches = FileObject.read()
    searches = re.sub("\n", '"\n"', '"' + searches + '"')
    searches = searches.split("\n")
    FileObject.close()
    return searches

### FILE ACTIONS ###
def listFiles(dir, type):
    (REDACTED)
    write(f"Files{type}.txt", os.listdir(dir))

def moveFiles(file_dir, location, dest):
    file_ids = readLines(file_dir)
    for file in os.listdir(location):
        for file_id in file_ids:
            if file_id in file:
                print(f"Move {file}")
                try:
                    shutil.move(f"{location}\\{file}", f"{dest}\\{file}")
                except:
                    print(f"Failed to Move {file}")

def copyFiles(file_dir, location, dest):
    file_ids = readLines(file_dir)
    for file in os.listdir(location):
        for file_id in file_ids:
            if file_id in file:
                print(f"Copy {file}")
                shutil.copy(f"{location}\\{file}", f"{dest}\\{file}")

def renameFiles(location, sub_tups, file_tups=[]):
    if file_tups == []:
        for file in os.listdir(location):
            for sub_tup in sub_tups:

                if sub_tup[0] in file:
                    new_name = re.sub(f"{sub_tup[0]}", f"{sub_tup[1]}", file)
                    print(f"Rename {file} to {new_name}")
                    os.rename(f"{location}\\{file}", f"{location}\\{new_name}")
    else:
        for file in os.listdir(location):
            for file_tup in file_tups:
                if file_tup[0] == file:
                    new_name = file_tup[1]
                    print(f"Rename {file} to {new_name}")
                    os.rename(f"{location}\\{file}", f"{location}\\{new_name}")
