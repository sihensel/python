#! /usr/bin/env python3

'''
Converts Markdown files to Asciidoc

Not all quirks and expressions of Markdown are supported, but it is enough
to convert most run-of-the-mill documents

NOTE: The Regex expressions in this script are questionable at best,
      I'm still learning all of that stuff
'''

import argparse
import logging
import re
import sys
import os


def read_file(filename: str) -> list[str]:
    '''
    Read the specified file into memory

    Args:
        filename (str): the file to read

    Raises:
        FileNotFoundError: When the file cannot be found
        TypeError: When no file has been specified

    Returns:
        list: all lines of the file
    '''
    try:
        with open(filename, 'r') as fp:
            logging.info(f'Reading file {filename}')
            return fp.readlines()
    except FileNotFoundError:
        logging.error(f"File {filename} does not exist")
        sys.exit(1)
    except TypeError:
        logging.error("Please provide a filename with -f, -h for help")
        sys.exit(1)


def main(filename: str, delete: bool) -> None:
    '''
    Parse the Markdown file and convert it to Asciidoc

    Args:
        filename (str): the Markdown file to convert
        delete (bool): wether to delete the Markdown after conversion

    Returns:
        None
    '''

    if not filename.endswith('.md'):
        logging.error("The specified file is not a Markdown file")
        sys.exit(1)

    lines = read_file(filename)

    # build the Asciidoc header
    # use highlight.js for the source-highlighter as it is built-in
    new_file = ':source-highlighter: highlight.js\n'
    new_file += ':last-update-label!:\n'
    new_file += '\n'

    # parse the file
    table = False
    code_block = False
    for (index, line) in enumerate(lines):

        # titles
        if line.startswith('#'):
            if table or code_block:
                new_file += line
            else:
                if lines[index + 1] == '\n':
                    new_file += line.replace('#', '=')
                else:
                    new_file += line.replace('#', '=') + '\n'

        # code blocks
        elif line.startswith('```'):
            code_block = True if not code_block else False
            # add the code language, if it exists
            if line != '```\n':
                new_file += '[source,' + line[3:-1] + ']\n'
            new_file += '----\n'

        # explicit linebreaks
        elif line.endswith('  \n'):
            new_file += line[:-3] + ' +\n'
        elif line.endswith('<br>\n'):
            new_file += line[:-5] + ' +\n'

        # quotes
        # NOTE nested quotes are not supported, as they don't exist in Asciidoc
        elif line.startswith('> '):
            new_file += '[quote, author, source]\n____\n'
            new_file += line[2:] + '____\n'

        # tables
        # FIXME this can be switched out for a more robust regex
        elif '|' in line:
            if not table:
                new_file += '[options="header"]\n|====\n'
                table = True

            for elem in line.split('|'):
                # skip the '--- | ---' line
                if not all(char in ['-', ' ', '\n'] for char in elem):
                    new_file += f'|{elem}'

        # images
        elif re.match(r'.*!{1}\[.*?\]\(.*?\).*', line):
            images = re.findall(r'!{1}\[.*?\]\(.*?\)', line)
            new_line = ''
            for image in images:
                alt_text = image[image.find("[")+1:image.find("]")]
                path = image[image.find("(")+1:image.find(")")]
                if new_line:
                    new_line = re.sub(rf'!\[{alt_text}\]\({path}\)',
                                      f'image:{path}[{alt_text}]',
                                      new_line)
                else:
                    new_line = re.sub(rf'!\[{alt_text}\]\({path}\)',
                                      f'image:{path}[{alt_text}]',
                                      line)
            new_file += new_line

        # links
        elif re.match(r'.*\[.*?\]\(.*?\).*', line):
            links = re.findall(r'\[.*?\]\(.*?\)', line)
            new_line = ''
            for link in links:
                title = link[link.find("[")+1:link.find("]")]
                url = link[link.find("(")+1:link.find(")")]
                if new_line:
                    new_line = re.sub(rf'\[{title}\]\({url}\)',
                                      f'{url}[{title}]',
                                      new_line)
                else:
                    new_line = re.sub(rf'\[{title}\]\({url}\)',
                                      f'{url}[{title}]',
                                      line)
            new_file += new_line

        # checklists
        elif re.match(r'^- \[(x| )\] .*\n', line):
            new_file += line.replace('-', '*', 1)

        # unordered lists
        elif re.match(r'^(- | +- |\* | +\* ).*', line):
            # add an empty line above lists so it gets displayed properly
            if not re.match(r'^(- | +- |\* | +\* ).*', lines[index-1]):
                new_file += '\n'

            if line.startswith('- '):
                new_file += line.replace('-', '*', 1)
            elif line.startswith(' '):
                spaces = len(line) - len(line.lstrip(' '))
                if spaces >= 2:
                    new_file += int(spaces/2+1) * '*' + line[spaces+1:]
            else:
                new_file += line

        # ordered lists
        elif re.match(r'^ *?\d. .*', line):
            # add an empty line above lists so it gets displayed properly
            if not re.match(r'^ *?\d. .*', lines[index-1]):
                new_file += '\n'

            if line.startswith(' '):
                spaces = len(line) - len(line.lstrip(' '))
                new_file += int(spaces/4+1) * '.' + line[spaces+2:]
            else:
                new_file += re.sub(r'^\d', '', line)

        # horizontal lines
        elif line == '---\n':
            new_file += '\'\'\'\n'

        # empty lines, which also end table blocks
        elif line == '\n':
            if table:
                new_file += '|====\n\n'
                table = False
            else:
                new_file += '\n'

        # normal text and empty lines
        else:
            # italic and bold text
            # FIXME this only works when both the * or _ are on the same line
            if '*' in line or '__' in line or '~' in line:
                # do not format text in code blocks
                if code_block:
                    new_file += line
                    continue

                new_line = ''
                # replace *** and ___ with *_
                # FIXME the regex pattern below returs 3 groups,
                # one would be enough as only the complete element is needed
                matches = re.findall(r'((\*{3}|_{3}).*?(\*{3}|_{3}))', line)
                for match in matches:
                    match = match[0]
                    if new_line:
                        new_line = new_line.replace(match,
                                                    f'*_{match[3:-3]}_*')
                    else:
                        new_line = line.replace(match, f'*_{match[3:-3]}_*')

                # replace * with _
                matches = re.findall(r'[^\*]\*[^\*| ].+?\*', line)
                for match in matches:
                    # FIXME this regex is a bit hacky
                    match = match.replace(' ', '')
                    if new_line:
                        new_line = new_line.replace(match, f'_{match[1:-1]}_')
                    else:
                        new_line = line.replace(match, f'_{match[1:-1]}_')

                # replace __ with *
                matches = re.findall(r'((\*{2}|_{2}).*?(\*{2}|_{2}))', line)
                for match in matches:
                    match = match[0]
                    if new_line:
                        new_line = new_line.replace(match, f'*{match[2:-2]}*')
                    else:
                        new_line = line.replace(match, f'*{match[2:-2]}*')

                # replace strikethrough ~~text~~ with [.line-through]#<text>#
                matches = re.findall(r'~{2}.*?~{2}', line)
                for match in matches:
                    if new_line:
                        new_line = new_line.replace(
                            match,
                            f'[.line-through]#{match.replace("~~", "")}#'
                        )
                    else:
                        new_line = line.replace(
                            match,
                            f'[.line-through]#{match.replace("~~", "")}#'
                        )

                new_file += new_line

            # text without special formatting
            else:
                new_file += line

    logging.info('Conversion complete')

    # write final .asc file
    new_filename = filename[:-3] + '.asc'
    try:
        with open(new_filename, "w") as fp:
            logging.info(f"Writing file {new_filename}")
            fp.write(new_file)
    except Exception as e:
        logging.error(f"Error while writing file:\n{e}")
        sys.exit(1)

    # delete file after conversion
    if delete:
        try:
            os.remove(filename)
        except Exception as e:
            logging.error(f'Could not delete file:\n{e}')
            sys.exit(1)
        logging.info(f'Deleted original Markdown file {filename}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--file',
        '-f',
        dest='file',
        type=str,
        help='Markdown file to convert'
    )
    parser.add_argument(
        '--debug',
        dest='debug',
        help='Enable debug logging',
        action='store_true'
    )
    parser.add_argument(
        '--delete',
        dest='delete',
        help='Delete the original file after converting',
        action='store_true'
    )
    args = parser.parse_args()

    level = logging.DEBUG if args.debug else logging.INFO
    logging.basicConfig(format="%(asctime)s %(levelname)-8s[%(filename)s "
                        "%(funcName)s(): %(lineno)s] %(message)s",
                        level=level,
                        datefmt='%Y-%m-%d %H:%M:%S')

    main(args.file, args.delete)
