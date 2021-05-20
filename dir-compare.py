'''
small utility to check if two directories contain the same files
'''

import os

path1 = r'D:\Music'
path2 = r'E:\Music'

path1_files = []
path2_files = []

# get all files from path1
for path, dirs, files in os.walk(path1):
    for file in files:
        path1_files.append(file)

# get all files from path2
for path, dirs, files in os.walk(path2):
    for file in files:
        path2_files.append(file)

# check, if the file exists in path1
for file in path2_files:
    if not file in path1_files:
        print(file)