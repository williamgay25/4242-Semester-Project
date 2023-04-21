import os
import pandas as pd
import numpy as np
# Load the data from the CSV file
data_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data.csv')
big_data = pd.read_csv(data_file_path)
in_list = ["Human", "Take My Breath Away", "The Heart Song"]
# Create an empty list to store the years of the requested songs
years = []

print(big_data)

# Loop through each song in the input list and find its year in the pandas database
for song_title in in_list:
    # Find the row in the pandas database that matches the requested song title
    song_row = big_data[big_data['song_title'] == song_title]
    
    # If there is no row that matches the requested song title, print an error message
    if len(song_row) == 0:
        print(f"Could not find year for song '{song_title}'")
    else:
        # Extract the year from the row and add it to the list of years
        year = song_row.iloc[0]['year']
        years.append(year)

print(years)
