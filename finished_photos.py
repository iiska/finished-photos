#! /usr/bin/env python3

import os, re, sys
import argparse
import sqlite3

def digikam_db_path():
    ''' Finds sqlite database used by Digikam from the digikamrc '''
    # NOTE: Python's ConfigParser is unable to parse digikamrc because
    # it interprets [Section][Subsection] clauses as duplicate
    # sections
    #
    # TODO: Try to write ConfigParser subclass which could handle that
    # and nil starting section.
    pattern = re.compile('Database Name=(.*)')
    with open(os.path.expanduser('~/.kde/share/config/digikamrc'), 'r') as f:
        for line in f:
            m = pattern.match(line)
            if m:
                return os.path.join(m.group(1), 'digikam4.db')


def main():
    parser = argparse.ArgumentParser(description='Find processed photos for given tag name')
    parser.add_argument('tag', metavar='TAG', nargs=1,
                        help='Find photos matching this tag')
    parser.add_argument('-m', '--missing', action="store_true", help='Print photos missing processed copy')
    parser.add_argument('-e', '--existing', action="store_true", help='Print existing processed copies')

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
        finished = os.path.join(row[0].replace('original', 'finished'), row[1][1:],
                                row[2].replace('nef', 'jpg'))
        if args.missing and not os.path.exists(finished):
            print(original)
        if args.existing and os.path.exists(finished):
            print(finished)


if __name__ == '__main__':
    main()
