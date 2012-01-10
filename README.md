Python script to support my photography workflow when searching raw
photos to process before ordering prints.

Script finds [Digikam](http://www.digikam.org/)'s SQLite database
according to config file ~/.kde/share/config/digikamrc and uses
Python's sqlite3 module to query photos tagged with given tag.

Raw photo paths for missing processed photos are printed when given
_--missing_ argument and existing paths for processed images are
printed when given _--existing_.

## TODO

* Better digikamrc parsing. Current one is quite a kludge. Maybe KDE
  project has some Python modules already.
