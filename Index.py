import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
from streamlit_searchbox import st_searchbox
import folium
from streamlit_folium import st_folium

st.title('McDonalds Guru')


def load_data(fastfood_data):
    pass


def analyze_the_data(working_data):
    pass


def make_recommnedations(analayzed_data):
    pass


map_image = Image.open('assets/mcdonalds_heatmap.jpg')

    #st.image(map_image, caption='Heatmap of Lower 48 US McDonalds Locations')

rec_category_labels = ["Verdict", "Fries Quality", "Bathroom Condition", "Service Quality", "Safe?"]

fake_data = ["Yes", "Crispy", "Clean", "Courteous", "Dangerous"]

recommendation_data = pd.DataFrame(
    [fake_data],
    columns=rec_category_labels
)

st.dataframe(data=recommendation_data, hide_index=True)



#df = pd.DataFrame(
    #np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
    #columns=['lat', 'lon'])

#st.map(df)

map_df = pd.DataFrame(pd.read_csv('assets/McDonald_s_Reviews.csv', encoding='utf_8', encoding_errors='replace'),
                      columns=['reviewer_id', 'store_name', 'category',
                               'store_address', 'latitude', 'longitude',
                               'rating_count', 'review_time', 'review',
                               'rating'],
                      )
def search_store_addresses(searchterm):
    if searchterm:
        matches = map_df[map_df['store_address'].str.contains(searchterm, case=False, na=False)]
        return matches['store_address'].tolist()
    else:
        return []
selected_address = st_searchbox(search_store_addresses, 'Search by Address to see our recommendation')

if selected_address:
    st.write('The selected store is currently', selected_address)

    selected_data = map_df[map_df['store_address'] == selected_address]
    lat = selected_data.iloc[0]['latitude']
    lon = selected_data.iloc[0]['longitude']

    m = folium.Map(location=[lat, lon], zoom_start=15)

    folium.Marker([lat, lon], popup=selected_address).add_to(m)
    
    st_folium(m)


st.write('- Interactable map of mcdonalds with reviews in our dataset ')
st.map(map_df.dropna(subset=["latitude", "longitude"]))


st.dataframe(data=map_df, hide_index=True)

st.write('Interactable map of all McDonalds locations in the USA ')

map2_df = pd.DataFrame(pd.read_csv('assets/lat_lon.csv', encoding='utf_8', encoding_errors='replace'),
                       columns=['latitude', 'longitude']
                       )

st.map(map2_df)

st.dataframe(data=map2_df)
