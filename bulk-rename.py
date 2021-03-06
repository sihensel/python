# script to rename multiple files

import os


filepath = r'C:\Users\me\Music'
#filepath = r'D:\Music'

'''
# 'walk' down the directory structure
for path, dirs, files in os.walk(filepath):
    for file in files:
        
        # replace all underscores with spaces
        if '___' in file:
            new_file = file.replace('___', ' - ')
        if '---' in file:
            new_file = file.replace('---', ' - ')
        if '_' in file:
            new_file = file.replace('_', ' ')
        else:
            new_file = file
        
        # replace track numbers with the artist
        new_file = 'Stand Atlantic' + new_file[2:]
    
        os.rename(path + '\\' + file, path + '\\' + new_file)
'''


# bulk rename images
i = 1
for path, dirs, files in os.walk(filepath):
    for file in files:
        # check file endings
        if file[-4:] == '.png':
            new_file = str(i) + '.png'
        elif file[-4:] == '.jpg':
            new_file = str(i) + '.jpg'
        elif file[-4:] == 'jpeg':
            new_file = str(i) + '.jpeg'
    
        os.rename(path + '\\' + file, path + '\\' + new_file)
        i += 1