#Project - CRUD Operations
"""
try
except
"""
from pathlib import Path
import os #Operating System

def readfileandfolder():
        try:
            p = Path('')
            items = list(p.rglob('*'))
            for index , file in enumerate(items):
                print(f'{index+1} - {file}')
        except Exception as e:
            print(e)


def create_file():
    try:
        readfileandfolder()
        # C:\Users\tanis\Desktop\File Handling\hello.txt
        file_name = input('Enter name of your file: ')
        p = Path(file_name)
        if p.exists():
            print('FILE ALREADY EXISTS')
        else:
            with open(file_name,'w') as file:
                content = input('Enter your file content: ')
                file.write(content)
                print('FILE ADDED!')
    
    except Exception as e:
        print(e)

def read_file():
    try:
        readfileandfolder()
        file_name = input('Enter name of your file: ')
        p = Path(file_name)
        if p.exists():
            with open(file_name,'r') as file:
                print(file.read())
        else:
            print('FILE NOT FOUND!')
    except Exception as e:
        print(e)











def update_file():
    try:
        readfileandfolder()
        file_name = input('Enter name of your file: ')
        p = Path(file_name)
        if p.exists():
            print('Press 1 to overwrite the content')
            print('Press 2 to append new content')
            
            option = int(input('Enter your choice for updating a file: '))
            if option == 1:
                with open(file_name,'w') as file:
                    content = input('Enter your content: ')
                    file.write(content)
                    print('CONTENT CHANGED...') 

            elif option == 2:
                with open(file_name,'a') as file:
                    content = input('Enter your content: ')
                    file.write(content)
                    print('CONTENT CHANGED...') 
            
            else:
                print("INVALID INPUT")
        else:
            print("FILE DOES NOT EXISTS!")
    
    except Exception as e:
        print(e)

def delete_file():
    readfileandfolder()
    file_name = input('Enter name of your file: ')
    p = Path(file_name)
    if p.exists():
        os.remove(p) #OS is removing path of that file completely from the system.
        print("FILE DELETED")
    else:
        print('FILE DOES NOT EXISTS!!')

def rename_file():
    readfileandfolder()
    file_name = input('Enter name of your file: ')
    p = Path(file_name)
    if p.exists():
       new_name=input('enter the new name of the file')
       p.rename(file_name)
       print('file renamed')
    else:
        print('FILE NOT FOUND!!')

def create_folder():
    readfileandfolder()
    folder_name = input('Enter name of your folder: ')
    p = Path(folder_name)
    if p.exists():
       print('folder already exists')
    else:
        p.mkdir('folder_name')
        print('folder created')

def delete_folder():
    readfileandfolder()
    folder_name = input('Enter name of your folder: ')
    p = Path(folder_name)
    if p.exists():
       p.rmdir()
       print('folder deleted')
    else:
        print('folder not found')

def create_file_in_folder():
    pass

while True:
    print("Press 1 for creating a file")
    print("Press 2 for reading a file")
    print("Press 3 for updating a file")
    print("Press 4 for deleting a file")
    print('press 5 for renaming a file')
    print("Press 6 for creating a folder ")
    print('press 7 for deleting a folder')
    print('press 0 for exiting')

    option = int(input("Enter your choice: "))
    if option ==1:
        create_file()

    if option ==2:
        read_file()

    if option == 3:
        update_file()

    if option == 4:
        rename_file()

    if option == 5:
        delete_folder()

    if option == 6:
        create_folder()
    
    if option == 0:
        break


