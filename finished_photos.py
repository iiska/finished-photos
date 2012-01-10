#! /usr/bin/env python3

import os
import configparser

def digikam_db_file():
    ''' Finds sqlite database used by Digikam from the digikamrc '''
    config = configparser.ConfigParser()
    config.read(os.path.expand_user('~/.kde/share/config/digikamrc'))
    db_path = config.get('Database Settings', 'Database Name')
    return os.path.join(db_path, 'digikam4.db')

def main():
    print digikam_db_file()


if __name__ == '__main__':
    main()
