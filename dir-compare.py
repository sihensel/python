#! /usr/bin/env python3

'''
Small utility to check if two directories contain the same files
Can be usefull when manually creating backups
'''

import os

source_dir = '/home/simon/music'
target_dir = '/home/simon/HDD/Music'

# When using Windows
source_dir = r'D:\Music'
target_dir = r'E:\Music'

source_dir_files = []
target_dir_files = []

# get all files from source_dir, ignoring file extensions
for _, _, files in os.walk(source_dir):
    for file in files:
        source_dir_files.append(file.split('.')[0])

# get all files from target_dir, ignoring file extensions
for _, _, files in os.walk(target_dir):
    for file in files:
        target_dir_files.append(file.split('.')[0])

print(f'The following files are NOT in the target dir {target_dir}\n')
# check if the file exists in target_dir
for file in source_dir_files:
    if file not in target_dir_files:
        print(file)

print(f'\nThe following files are NOT in the source dir {source_dir}\n')
# check if the file exists in source_dir
for file in target_dir_files:
    if file not in source_dir_files:
        print(file)
