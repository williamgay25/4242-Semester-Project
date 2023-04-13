# usual imports
import os
import sys
import time
import glob
import datetime
import pandas as pd
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

# define a function to extract the data for each file
def func_to_get_data(filename):
    h5 = GETTERS.open_h5_file_read(filename)
    artist_name = GETTERS.get_artist_name(h5)
    song_title = GETTERS.get_title(h5)
    year = GETTERS.get_year(h5)
    tempo = GETTERS.get_tempo(h5)
    h5.close()
    return {'artist_name': artist_name,
            'song_title': song_title,
            'year': year,
            'tempo': tempo}

# create a list to hold the extracted data
data_list = []

# extract data for each file in the MSD subset
t1 = time.time()
apply_to_all_files(msd_subset_path, func=lambda x: data_list.append(func_to_get_data(x)))
t2 = time.time()
print('all artist names extracted in:', strtimedelta(t1, t2))

# create a Pandas dataframe from the list
df = pd.DataFrame(data_list)

# print the dataframe
print(df)