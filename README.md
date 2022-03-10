#Austin Andres M220156
#Lab 5 - Understanding the Host's Integrity
This Program does the following
1. Walks through the entire file system, printing out the filenames with their paths and taking no action (but skipping) the unhashable directories.
2. Integrates SHA2 (SHA256) so that each file is hashed as it moves through the file system.
3. Stores the file and hash information so that it will be available for future runs. Stores the following data:
  filename with full path
  hash
  date/time file was observed
4. Runs and updates the hash information, upon completion it prints out summary information that includes all new files found, any missing files, and any file that was modified
5.  Detects that a file was moved, adds to summary section an output that documents where the file is now, and where it was, and the time of the last scan that saw it in the older location.

