import os
import pandas as pd

def get_artists():
    data_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data.csv')
    data = pd.read_csv(data_file_path)
    column_data = data['artist_name'].unique().tolist()
    
    return column_data