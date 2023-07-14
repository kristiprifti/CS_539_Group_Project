import pandas as pd
import numpy as np
import ast

md_df = pd.read_csv("McDonald_s_Reviews.csv", encoding='ISO-8859-1')
neighbors_df = pd.read_csv("neighbors.csv")
neighbors_df['coord'] = neighbors_df['coord'].apply(ast.literal_eval)

coords = []
for i, review in md_df.iterrows():
    lat = review["latitude "]
    long = review["longitude"]
    coord = (lat, long)
    coords.append(coord)

md_df["coord"] = coords

merged_df = pd.merge(md_df, neighbors_df, left_on='coord', right_on='coord', how='left')
merged_df.to_csv('md_plus_locations.csv', index=False)
