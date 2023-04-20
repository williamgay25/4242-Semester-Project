import os
from sklearn.cluster import OPTICS
import numpy as np
import pandas as pd
import time


def cluster(seed_song = None, artist = None, year = None, length = 35):
    data_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data.csv')
    big_data = pd.read_csv(data_file_path, index_col=0)
    data = big_data.sample(frac = 0.02).reset_index(drop=True)
    
    #Inputs here Please
    inputs = {"Seed Song": seed_song, "Artist": artist, "Year": year, "Length": length*60}
    
    artists = []
    decades = []
    
    seed_existence = False
    #Manipulates data based on presence of a seed song
    if (inputs["Seed Song"] != None):
        seed_row = big_data.loc[big_data["song_title"] == inputs["Seed Song"]]
        #print(len(seed_row))
        if(len(seed_row) > 0):
            seed_existence = True
            data = pd.concat([data, seed_row], ignore_index=True)
            data = data.drop_duplicates()
            
            artists.append(seed_row["artist_name"].iloc[0])
            decades.append(seed_row["year"].iloc[0])
            
            data["key"] = np.where(data["key"] == seed_row["key"].iloc[0], 1, 0)
            data["time_signature"] = np.where(data["time_signature"] == seed_row["time_signature"].iloc[0], 1, 0)
    #Default settings for no seed song
    else:
        data["key"] = 0
        data["time_signature"] = 0
        
    if (inputs["Artist"] != None):
        artists.append(inputs["Artist"])
        
    #Sets up artist feature
    data["norm_artist_name"] = np.where(data["artist_name"].isin(artists), 1, 0)
    
    
    #Sets up year feature
    if (inputs["Year"] != None):
        decades.append(inputs["Year"])
    
    decades = [int(np.floor(x/10.0)*10) for x in decades]
    
    data["year"] = ((data["year"]/10.0).apply(np.floor)*10).astype('int')
    data["year"] = np.where(data["year"].isin(decades), 1, 0)
    
    #Normalizes data
    data["norm_duration"] = data["duration"]/data["duration"].max()
    data["loudeness"] = data["loudeness"]/data["loudeness"].max()
    data["tempo"] = data["tempo"]/data["tempo"].max()
    
    
    #Runs CLustering Algorithm. Uses OPTICS instead of DBSCAN Due to Memory Issues
    #print("Its Clusterin Time")
    t1 = time.time()
    
    data = data.dropna()
    #print(data.columns)
    clustering = OPTICS(max_eps = 3, min_samples=10).fit(data.iloc[:,np.r_[2, 4:14]])
    
    t2 = time.time()
    #print('Clustering Completed In:', str(datetime.timedelta(seconds=t2-t1)))
    
    data["Cluster"] = clustering.labels_
    
    #Identifies points in the same cluster as the seed song
    #If no seed song is selected then select smallest cluster
    if (inputs["Seed Song"] != None and seed_existence):
        chosen_label = data.loc[data["song_title"] == inputs["Seed Song"]]["Cluster"].iloc[0]
        eligible_songs = data.loc[data["Cluster"] == chosen_label]
    else:
        min_index = np.bincount(clustering.labels_+1).argmin()-1
        eligible_songs = data.loc[data["Cluster"] == min_index]
    
    eligible_songs = eligible_songs.sort_values(by=["duration"], ascending = False)
    
    #Randomly sample songs out of cluster while keeping within the time limit
    playlist = []
    remaining_time = inputs["Length"]
    while (remaining_time > 0 and len(eligible_songs) > 0):
        eligible_songs = eligible_songs.sample(frac = 1).reset_index(drop=True)
        if (eligible_songs["duration"].iloc[0] <= remaining_time):
            playlist.append([eligible_songs["song_title"].iloc[0], eligible_songs["artist_name"].iloc[0], eligible_songs["duration"].iloc[0]])
            remaining_time -= eligible_songs["duration"].iloc[0]
            
        eligible_songs = eligible_songs.drop(0)
        
    print(playlist)
    return playlist