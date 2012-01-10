#! /usr/bin/env python3
''' Find photos from Digikam db matching given tag'''

import os, re
import argparse
import shutil
import sqlite3

def digikam_db_path():
    ''' Finds sqlite database used by Digikam from the digikamrc '''
    # NOTE: Python's ConfigParser is unable to parse digikamrc because
    # it interprets [Section][Subsection] clauses as duplicate
    # sections
    pattern = re.compile('Database Name=(.*)')
    with open(os.path.expanduser('~/.kde/share/config/digikamrc'), 'r') as conf:
        for line in conf:
            match = pattern.match(line)
            if match:
                return os.path.join(match.group(1), 'digikam4.db')


def copy_photo(photo, dst_dir):
    ''' Copy photo to destination if it doesn't already exist there '''
    name = os.path.basename(photo)
    if not os.path.exists(os.path.join(dst_dir, name)):
        shutil.copy2(photo, dst_dir)


def main():
    ''' Parses commandline arguments and executes db query '''
    parser = argparse.ArgumentParser(
        description='Find processed photos for given tag name')
    parser.add_argument('tag', metavar='TAG', nargs=1,
                        help='Find photos matching this tag')
    parser.add_argument('-m', '--missing', action="store_true",
                        help='Print photos missing processed copy')
    parser.add_argument('-e', '--existing', action="store_true",
                        help='Print existing processed copies')
    parser.add_argument('--copy-to', metavar='DESTINATION',
                        help='Copy existing processed photos to this directory')

    args = parser.parse_args()

    # Query for determining absolute image paths for photos tagged
    # with certain tag name
    query = """ SELECT r.specificPath, a.relativePath, i.name FROM Images i
      JOIN Albums a ON a.id=i.album
      JOIN AlbumRoots r ON r.id=a.albumroot
      JOIN ImageTags it ON it.imageid=i.id
      JOIN Tags t ON t.id=it.tagid
      WHERE t.name LIKE ?
    """
    con = sqlite3.connect(digikam_db_path())
    for row in con.cursor().execute(query, args.tag):
        original = os.path.join(row[0], row[1][1:], row[2])
        finished = os.path.join(row[0].replace('original', 'finished'),
                                row[1][1:],
                                row[2].replace('nef', 'jpg'))

        if args.copy_to != None and os.path.exists(finished):
            if os.path.exists(args.copy_to):
                copy_photo(finished, args.copy_to)
            else:
                print("Destination directory %s doesn't exist" % (args.copy_to))
        else:
            if args.missing and not os.path.exists(finished):
                print(original)
            if args.existing and os.path.exists(finished):
                print(finished)


if __name__ == '__main__':
    main()
