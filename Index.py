import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image



st.title('McDonalds Guru')

def load_data(fastfood_data):
    pass

def analyze_the_data(working_data):
    pass

def make_recommnedations(analayzed_data):
    pass

map_image = Image.open('assets/mcdonalds_heatmap.jpg')

st.text_input("Search by Address to see our recommendation")

st.image(map_image, caption='Heatmap of Lower 48 US McDonalds Locations')

rec_category_labels = ["Verdict", "Fries Quality", "Bathroom Condition", "Service Quality", "Safe?"]

fake_data = ["Yes", "Crispy", "Clean", "Courteous", "Dangerous"]


recommendation_data = pd.DataFrame(
    [fake_data],
    columns=rec_category_labels
)

st.dataframe(data=recommendation_data, hide_index=True)

st.write(' *- Was thinking that we could maybe color code the above fields? I.e. green for positive, red for negative. '
         'This would result in an easier to read UI dashboard')

