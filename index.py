# usual imports
import os
import sys
import time
import glob
import datetime
import numpy as np  # get it at: http://numpy.scipy.org/
from dotenv import load_dotenv

# load the .env file
load_dotenv()

# path to the Million Song Dataset subset (uncompressed)
# CHANGE IT TO YOUR LOCAL CONFIGURATION
msd_subset_path = os.getenv('DATA_PATH')

# imports specific to the MSD
sys.path.append('./MSongsDB/PythonSrc/')
import hdf5_getters as GETTERS

# the following function simply gives us a nice string for
# a time lag in seconds
def strtimedelta(starttime, stoptime):
    return str(datetime.timedelta(seconds=stoptime-starttime))

# we define this very useful function to iterate the files
def apply_to_all_files(basedir, func=lambda x: x, ext='.h5'):
    """
    From a base directory, go through all subdirectories,
    find all files with the given extension, apply the
    given function 'func' to all of them.
    If no 'func' is passed, we do nothing except counting.
    INPUT
        basedir  - base directory of the dataset
        func     - function to apply to all filenames
        ext      - extension, .h5 by default
    RETURN
        number of files
    """
    cnt = 0
    # iterate over all files in all subdirectories
    for root, dirs, files in os.walk(basedir):
        files = glob.glob(os.path.join(root, '*' + ext))
        # count files
        cnt += len(files)
        # apply function to all files
        for f in files:
            func(f)
    return cnt

# we can now easily count the number of files in the dataset
print('number of song files:', apply_to_all_files(msd_subset_path))

# let's now get all artist names in a set(). One nice property:
# if we enter many times the same artist, only one will be kept.
all_artist_names = set()

# we define the function to apply to all files
def func_to_get_artist_name(filename):
    """
    This function does 3 simple things:
    - open the song file
    - get artist ID and put it
    - close the file
    """
    h5 = GETTERS.open_h5_file_read(filename)
    artist_name = GETTERS.get_artist_name(h5)
    all_artist_names.add(artist_name)
    h5.close()

# let's apply the previous function to all files
# we'll also measure how long it takes
t1 = time.time()
apply_to_all_files(msd_subset_path, func=func_to_get_artist_name)
t2 = time.time()
print('all artist names extracted in:', strtimedelta(t1, t2))

# let's see some of the content