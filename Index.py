import streamlit as st
import pandas as pd
import pydeck as pdk # using pydeck to create the map
from streamlit_searchbox import st_searchbox

st.title('McDonalds Guru')

# Load dataframes
map_df = pd.DataFrame(pd.read_csv('assets/McDonald_s_Reviews.csv', encoding='utf_8', encoding_errors='replace'),
                      columns=['reviewer_id', 'store_name', 'category',
                               'store_address', 'latitude', 'longitude',
                               'rating_count', 'review_time', 'review',
                               'rating'],
                      )
map_df['rating'] = map_df['rating'].str.extract('(\d+)').astype(float)
location_data = map_df.groupby(['latitude', 'longitude', 'store_address']).agg(
    {'rating': 'mean', 'review': 'count'}).reset_index()

map2_df = pd.DataFrame(pd.read_csv('assets/lat_lon.csv', encoding='utf_8', encoding_errors='replace'),
                       columns=['latitude', 'longitude']
                       )

def search_store_addresses(searchterm):
    if searchterm:
        matches = map_df[map_df['store_address'].str.contains(searchterm, case=False, na=False)].drop_duplicates(
            subset=['store_address'])
        return matches['store_address'].tolist()
    else:
        return []


if "selected_address" not in st.session_state:
    st.session_state.selected_address = None


selected_address = st_searchbox(search_store_addresses, 'Search by Address to see our recommendation')


lat = (location_data['latitude'].mean() + map2_df['latitude'].mean()) / 2
lon = (location_data['longitude'].mean() + map2_df['longitude'].mean()) / 2
zoom = 3

if selected_address:
    selected_data = map_df[map_df['store_address'] == selected_address]
    lat = selected_data.iloc[0]['latitude']
    lon = selected_data.iloc[0]['longitude']
    zoom = 11

if st.button('Add all the McDonalds in the US'):
    if 'use_first_dataset' not in st.session_state:
        st.session_state['use_first_dataset'] = True
    st.session_state['use_first_dataset'] = not st.session_state['use_first_dataset']

df = location_data if st.session_state.get('use_first_dataset', True) else map2_df



# Create a pydeck Layer
layer = pdk.Layer(
    'ScatterplotLayer',
    df,
    get_position='[longitude, latitude]',
    get_fill_color='[200, 30, 0, 160]' if st.session_state.get('use_first_dataset', True) else '[0, 200, 30, 160]',
    get_radius=1000,
    pickable=True,
)


r = pdk.Deck(layers=[layer], initial_view_state=pdk.ViewState(latitude=lat, longitude=lon, zoom=zoom))
st.pydeck_chart(r)
