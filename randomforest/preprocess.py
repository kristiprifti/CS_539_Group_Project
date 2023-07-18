import pandas as pd

df = pd.read_csv('df.csv', encoding='ISO-8859-1')
original_n = len(df) #length of df

#remove unwanted rows from DF. 
bad_rows = []
for i, row in df.iterrows():
    if pd.isna(row["latitude"]) or pd.isna(row["longitude"]):
        bad_rows.append(i)
df = df.drop(bad_rows)
print(f"removed {len(bad_rows)} out of original {original_n} from dataframe")

#remove unwanted columns from DF:
unwanted = ["store_name", "category", "store_address", "latitude", "longitude",\
            "review_time", "review", "reviewer_id"]
df = df.drop(unwanted, axis=1)

#convert rating from string to numeric
for i, row in df.iterrows():
    df["rating"][i] = int(df["rating"][i][0])
    
#convert rating count from string to numeric
df["rating_count"] = df["rating_count"].str.replace(',','').astype(int)
df.to_csv('df_processed.csv', index=False)

