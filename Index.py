import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
from streamlit_searchbox import st_searchbox
import folium
from streamlit_folium import st_folium
from folium.plugins import MarkerCluster


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
# Drop the whole row if there is any NaN in address column
map_df.dropna(subset=['store_address'], inplace=True)

# Drop duplicates from making the search box faster
def search_store_addresses(searchterm):
    if searchterm:
        matches = map_df[map_df['store_address'].str.contains(searchterm, case=False, na=False)].drop_duplicates(subset=['store_address'])
        return matches['store_address'].tolist()
    else:
        return []
selected_address = st_searchbox(search_store_addresses, 'Search by Address to see our recommendation')


lat = map_df['latitude'].mean()
lon = map_df['longitude'].mean()

#
if selected_address:

    selected_data = map_df[map_df['store_address'] == selected_address]
    lat = selected_data.iloc[0]['latitude']
    lon = selected_data.iloc[0]['longitude']

st.write('- Interactable map of mcdonalds with reviews in our dataset ')

map_df['rating'] = map_df['rating'].str.extract('(\d+)').astype(float) # extract the rating from the string
location_data = map_df.groupby(['latitude', 'longitude', 'store_address']).agg({'rating': 'mean', 'review': 'count'}).reset_index()

# Initialize
if "last_object_clicked" not in st.session_state:
    st.session_state["last_object_clicked"] = None
if "selected_address" not in st.session_state:
    st.session_state["selected_address"] = None

m_all = folium.Map(location=[map_df['latitude'].mean(), map_df['longitude'].mean()], zoom_start=3)
marker_cluster = MarkerCluster().add_to(m_all)

# The popups for the markers show the address and the number of reviews for that location
for _, row in location_data.iterrows():

    popup_text = f"{row['store_address']}<br>Number of reviews: {row['review']}"
    popup = folium.Popup(popup_text, max_width=300) # max_width to show the whole popup at once
    color = 'green' # color of the circle marker
    folium.Marker(location=[row['latitude'], row['longitude']], popup=popup,icon=folium.Icon(color=color)).add_to(marker_cluster)

# Display the selected address if search is used
if selected_address:
    folium.Marker([lat, lon], popup=selected_address).add_to(m_all)
    m_all.fit_bounds([[lat, lon], [lat, lon]]) # zoom to the selected address

out = st_folium(m_all)


if out["last_object_clicked"]:
    selected_address = None
    click_coordinates = tuple(out["last_object_clicked"].values())
    if click_coordinates != st.session_state["last_object_clicked"]:
        st.session_state["last_object_clicked"] = click_coordinates
        address = location_data[location_data['latitude'].between(click_coordinates[0] - 0.0001, click_coordinates[0] + 0.0001) &
                                location_data['longitude'].between(click_coordinates[1] - 0.0001, click_coordinates[1] + 0.0001)
                               ]['store_address'].values[0]
        st.session_state["selected_address"] = address
        st.experimental_rerun()

# Display the selected address if search is used
if selected_address:
    selected_data = map_df[map_df['store_address'] == selected_address]
    st.write('The selected store is currently: ', selected_address)

# Display the selected address if map is used
elif st.session_state["selected_address"]:
    selected_data = map_df[map_df['store_address'] == st.session_state["selected_address"]]
    st.write('The selected store is currently: ', st.session_state["selected_address"])





st.dataframe(data=map_df, hide_index=True)

st.write('Interactable map of all McDonalds locations in the USA ')

map2_df = pd.DataFrame(pd.read_csv('assets/lat_lon.csv', encoding='utf_8', encoding_errors='replace'),
                       columns=['latitude', 'longitude']
                       )
# The map of all McDonalds locations in the USA takes too long to load with folium.
st.map(map2_df)

st.dataframe(data=map2_df)
