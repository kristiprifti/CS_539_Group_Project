import streamlit as st
import pandas as pd
import pydeck as pdk # using pydeck to create the map
from streamlit_searchbox import st_searchbox



st.set_page_config(
    page_title="Home",
    page_icon="ALT+8962"
)

st.sidebar.success("Choose a Page")

st.title(":red[Grub Guru] :hamburger:")

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
website_df = pd.read_csv('assets/updated_websiteDF.csv')
website_df.set_index('coord', inplace=True)

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
def get_color(score):
    if score < -0.1:
        return '#0000FF'  # Blue
    elif score < 0.1:
        return '#ADD8E6'  # Light Blue
    elif score < 0.2:
        return '#800080'  # Purple
    elif score < 0.4:
        return '#FFA500'  # Orange
    else:
        return '#FF0000'  # Red


if selected_address:
    selected_data = map_df[map_df['store_address'] == selected_address]
    lat = selected_data.iloc[0]['latitude']
    lon = selected_data.iloc[0]['longitude']
    zoom = 16

    coord = f'({lat}, {lon})'

    features = website_df.loc[coord]

    features_container = st.container()

    features_container.title("Features")

    # 1. Customer Rating
    with features_container:
        st.markdown("**1. Customer Rating**")
        st.write(features['rating'])

    # 2. Sentiment Score
    with features_container:
        st.markdown("**2. Sentiment Score**")
        score = features['compound_score']
        st.markdown(f'<p style="color:{get_color(score)};">{score}</p>', unsafe_allow_html=True)
        with st.expander("Sentiment Score Color Coding"):
            st.info("The sentiment score is color-coded according to the following scheme:")
            st.markdown('<p style="color:#0000FF;">Blue: Score < -0.1 (Negative Sentiment)</p>', unsafe_allow_html=True)
            st.markdown('<p style="color:#ADD8E6;">Light Blue: -0.1 <= Score < 0.1 (Somewhat Negative Sentiment)</p>',
                        unsafe_allow_html=True)
            st.markdown('<p style="color:#800080;">Purple: 0.1 <= Score < 0.2 (Neutral Sentiment)</p>',
                        unsafe_allow_html=True)
            st.markdown('<p style="color:#FFA500;">Orange: 0.2 <= Score < 0.4 (Somewhat Positive Sentiment)</p>',
                        unsafe_allow_html=True)
            st.markdown('<p style="color:#FF0000;">Red: Score >= 0.4 (Positive Sentiment)</p>', unsafe_allow_html=True)

    # 3. Fast Service Related Sentiments (Topic 19)
    with features_container:
        st.markdown(f"**3. Quality experience and customer satisfaction (Topic 19)** : <span style='color:blue;'>{features['Topic_19']}</span>", unsafe_allow_html=True)
        topic19 = features['Topic_19']
        # Create a progress bar
        min_value = 0.0006
        max_value = 0.0518
        median_value = 0.0385
        range_value = max_value - min_value

        # Calculate the relative position of the topic19 score
        relative_position = (topic19 - min_value) / range_value

        st.progress(relative_position)
        st.info(f"Min Value: {min_value} | Max Value: {max_value} | Median Value: {median_value}")
        with st.expander("Info about Topic 19"):
            st.info(
                'Topic 19: fast service, customer service, service good, great food, great customer, great customer service, quick service, good food, food service, service great')

    # 4. Rating Count
    with features_container:
        st.markdown("**4. Rating Count**")
        st.write(features['rating_count'])

    # 5. Fast Friendly Service Related Sentiments (Topic 26)
    with features_container:
        st.markdown("**5.Fast and friendly service  (Topic 26)**")
        st.write(features['Topic_26'])
        with st.expander("Info about Topic 26"):
            st.info(
                'Topic 26: fast friendly, friendly service, fast friendly service, drive thru, customer service, take order, fast food, macdonald ever, hot food, service excellent')

    # 6. Nearby Subway Stations within 20 miles
    with features_container:
        st.markdown("**6. Nearby Subway Stations within 20 miles**")
        st.write(features['subway20'])






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
