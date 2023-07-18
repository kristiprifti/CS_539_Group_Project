import streamlit as st
import pandas as pd
import pydeck as pdk # using pydeck to create the map
from streamlit_searchbox import st_searchbox



st.set_page_config(
    page_title="Home",
    page_icon="ALT+8962"
)

st.sidebar.success("Choose a Page")

st.title('McDonalds Guru')

# Load dataframes
map_df = pd.DataFrame(pd.read_csv('assets/cleaned_reviews.csv',  encoding='ISO-8859-1'),
                      columns=['reviewer_id', 'store_name', 'category',
                               'store_address', 'latitude', 'longitude',
                               'rating_count', 'review_time', 'review',
                               'rating'],
                      )
map_df['rating'] = map_df['rating'].str.extract('(\d+)').astype(float)
location_data = map_df.groupby(['latitude', 'longitude', 'store_address']).agg(
    {'rating': 'mean', 'review': 'count'}).reset_index()

map2_df = pd.DataFrame(pd.read_csv('assets/final_unique_locations.csv', encoding='utf_8', encoding_errors='replace'),
                       columns=['latitude', 'longitude', 'store_address']
                       )
map3_df_subway = pd.DataFrame(pd.read_csv('assets/subway_cleaned.csv', encoding='utf_8', encoding_errors='replace'),
                       columns=['latitude', 'longitude', 'store_address']
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
    zoom = 16

chosen_datasets = st.multiselect(
    "Choose which dataset(s) to display",
    options=["Original McDonald's", "All McDonald's Locations in the US", "All the Subway Locations in the US"],
    default=["Original McDonald's"]
)
layers = []
for dataset in chosen_datasets:
    if dataset == "Original McDonald's":
        df = location_data
        color = '[200, 30, 0, 160]'
    elif dataset == "All McDonald's Locations in the US":
        df = map2_df
        color = '[0, 200, 30, 160]'
    else:  # dataset == "Subway"
        df = map3_df_subway
        color = '[0, 0, 200, 160]'
    point_size = st.slider(f'Adjust point size for {dataset}', min_value=50,max_value=15000, value=50) if selected_address else st.slider(f'Adjust point size for {dataset}', min_value=50,max_value=15000, value=15000)
    layers.append(pdk.Layer(
        'ScatterplotLayer',
        df,
        get_position='[longitude, latitude]',
        get_fill_color=color,
        get_radius= point_size,
        pickable=True,
    ))

tooltips = {
    "html": "<b>Address:</b> {store_address}",
    "style": {"backgroundColor": "steelblue", "color": "white"},
}

r = pdk.Deck(
    layers=[layers],
    initial_view_state=pdk.ViewState(latitude=lat, longitude=lon, zoom=zoom),
    tooltip=tooltips,
)
st.pydeck_chart(r)
