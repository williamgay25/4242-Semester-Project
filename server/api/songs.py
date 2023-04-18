import os
import numpy as np
import pandas as pd

def get_songs():
    data_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data.csv')
    data = pd.read_csv(data_file_path)

    # Identify rows with invalid float values in the 'song_title' column
    invalid_rows = data['song_title'].apply(lambda x: isinstance(x, float) and not np.isfinite(x))

    # Remove rows with invalid float values
    data = data[~invalid_rows]

    column_data = data['song_title'].unique().tolist()
    
    return column_data