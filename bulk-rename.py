#! /usr/bin/env python3

# Script to rename multiple music or image files
# Only a few formats are supported (mp3, png, jpg, jpeg, the one I use)

import os
import sys
import argparse
import logging
import re


def natural_sort_key(s, _nsre=re.compile('([0-9]+)')):
    '''
    Sort keys in natural order
    See https://stackoverflow.com/a/16090640
    '''
    return [int(text) if text.isdigit() else text.lower()
            for text in _nsre.split(s)]


def rename_music(filepath: str, artist: str = ''):
    '''
    Rename all .mp3 files
    Remove underscores, change '---' to ' - ' and remove track numbers
    Replace the artist if one was specified with --artist
    '''

    for path, _, files in os.walk(filepath):

        for file in files:
            if file[-4:] != '.mp3':
                logger.warning(f'File {file} is not in mp3 format')
                continue

            if '___' in file:
                new_file = file.replace('___', ' - ')
            elif '---' in file:
                new_file = file.replace('---', ' - ')
            elif '_' in file:
                new_file = file.replace('_', ' ')
            else:
                new_file = file

            if new_file[:2].isdigit():
                # replace track numbers with the artist
                new_file = artist + new_file[2:]
            else:
                if artist:
                    # replace the old artist with the new one
                    split = new_file.split(' - ')
                    new_file = artist + ' - ' + split[1]

            if new_file == file:
                continue

            if args.dry_run:
                logger.info(f'DRY-RUN Renaming {file} to {new_file}')
            else:
                logger.info(f'Renaming {file} to {new_file}')
                if sys.platform == "linux" or sys.platform == "linux2":
                    os.rename(path + '/' + file, path + '/' + new_file)
                elif sys.platform == 'win32':
                    os.rename(path + '\\' + file, path + '\\' + new_file)


def rename_images(filepath: str):
    '''
    Rename all images in a directory in ascending order
    This assumes all images are in the desired order
    Filenames get changed to 1.png, 2.png, 3.jpg etc.
    '''

    for path, _, files in os.walk(filepath):
        files = sorted(files, key=natural_sort_key)

        for index, file in enumerate(files, start=1):
            # check file endings
            if file[-4:] == '.png':
                new_file = str(index) + '.png'
            elif file[-4:] == '.jpg':
                new_file = str(index) + '.jpg'
            elif file[-5:] == '.jpeg':
                new_file = str(index) + '.jpeg'
            else:
                logger.warning(f'Format of file {file} is not supported')
                continue

            if new_file == file:
                continue

            if args.dry_run:
                logger.info(f'DRY-RUN Renaming {file} to {new_file}')
            else:
                logger.info(f'Renaming {file} to {new_file}')
                if sys.platform == "linux" or sys.platform == "linux2":
                    os.rename(path + '/' + file, path + '/' + new_file)
                elif sys.platform == 'win32':
                    os.rename(path + '\\' + file, path + '\\' + new_file)


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--path',
        dest='filepath',
        type=str,
        help='Filepath to the files to rename',
        default=None
    )
    parser.add_argument(
        '--artist',
        dest='artist',
        type=str,
        help='Artist (when using --music)',
        default=None
    )
    parser.add_argument(
        '--music',
        dest='music',
        help='Rename music files (Remove userscores and track numbers)',
        action='store_true'
    )
    parser.add_argument(
        '--images',
        dest='images',
        help='Rename image files in ascending order (1.png, 2.png, etc.)',
        action='store_true'
    )
    parser.add_argument(
        '--dry-run',
        dest='dry_run',
        help='Perform a dry-run without changing anything',
        action='store_true'
    )
    args = parser.parse_args()

    logging.basicConfig(
        format=(
            '%(asctime)s %(levelname)-8s[%(lineno)s: %(funcName)s] '
            '%(message)s'
        )
    )
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    if not args.music and not args.images:
        logger.error('Please specify an action (--help for more info)')
        sys.exit(1)
    if not args.filepath:
        logger.error('Please state a filepath with --filepath')
        sys.exit(1)

    if args.music:
        rename_music(args.filepath, args.artist)

    if args.images:
        rename_images(args.filepath)
