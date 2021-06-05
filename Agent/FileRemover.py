import os

def fileRemove(remove_files):
    for filename in remove_files:
        os.remove(filename)