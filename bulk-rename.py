# script to rename multiple files

import os

def main():

    filepath = r'C:\Users\me\Music'
    #filepath = r'D:\Music'

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
            #new_file = 'Stand Atlantic' + new_file[2:]
        
            os.rename(path + '\\' + file, path + '\\' + new_file)


if __name__ == '__main__':
    main()