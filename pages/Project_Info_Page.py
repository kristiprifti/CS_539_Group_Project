import streamlit as st
import pandas as pd
#import pydeck as pdk # using pydeck to create the map
#from streamlit_searchbox import st_searchbox
from urllib.error import URLError
from PIL import Image



st.set_page_config(
    page_title="Project Information",
    page_icon="ALT+8962"
)

st.title(":blue[Project Info & Discussion]")

st.markdown(" The Team has created a ML application to help users better evaluate a McDonalds")

st.markdown("The code for this project can be found at https://github.com/WillGodsey/CS_539_Group_Project")
st.markdown("""the public-facing github page for this project can be found at 
            https://willgodsey.github.io/CS_539_Group_Project/ ,
            which also contains the README information""")

st.markdown(""":red[What is exactly the function of your tool (or a method)? That is, what will it do?]""")

st.markdown("""
The goal and primary function of the team’s tool is to help users make well informed decisions regarding which fast-food
establishments to patronize and which to avoid. This can be done using reviews of that establishment and nationwide 
trends such as time of year, geographic location, and proximity to competitors.  The goal for this application is to act
as a “fast-food guru” using local and national information to help the user find the highest quality, safest, and 
cleanest dining options. """ )

st.markdown(":red[Why would we need such a tool (or a method) and who would you expect to use it and benefit from it?]")

st.markdown("""
Despite the best efforts of massive multi-national corporations, quality control and uniformity of user experience are 
major and persisting issues for fast food restaurants. The team hoped to aid in identifying these issues, whether that 
be simply identifying whether to stop at a particular McDonald’s, or to keep driving. The team also hopedto also inform users of 
the strengths and weaknesses of a particular establishment, i.e., the French fries are incredible, but the restrooms are
 horrendous. This level of thorough analysis would allow users to assess which establishments meet their desires and 
 needs while potentially aiding corporate entities in addressing lingering issues.  """)

st.markdown("""
:red[Does this kind of tool/method already exist? 
If similar tools/methods exist, how is your tool/method different from them? 
Would people care about the difference? How hard is it to build such a tool/algorithm? What is the challenge?]  """)

st.markdown(
    """
    Currently, the primary avenue through which users read review data is through simple aggregation tools such as “stars” 
ratings that average the ratings of users. These tools are useful for being concise and easily understandable, 
but they are greatly lacking in detail; if a user desired more elaboration, they would be required to comb through all 
the reviews themselves. Our tool’s goal is to highlight the important features of a successful fast-food chain 
and how it varies across the country. Not only could this tool be useful to a consumer, but also a fast-food chain 
corporation to better perform in locations identified as having poor sentiment by the tool. 

To build this tool, the team made use of a dataset containing store reviews across multiple locations, latitude and longitude 
positions of competing fast food chains, and census data to identify trends between an individual establishment and 
its location. Processing this data from different sources and performing feature extraction is crucial for the success 
of this tool, so that represented the main challenge for this project.  """)

st.markdown("""
:red[How do you plan to build it? You should mention the data you will use and the core algorithm that you will implement 
(either existing algorithm for tools or new algorithm for methods). ]  """)

st.markdown(
    """As mentioned previously, the team  collected fast-food chain store reviews, latitude and longitude positions 
of competing fast-food chains to gain understanding on what makes an individual establishment 
successful. For this tool, the fast-food chain we selected is McDonald’s, given its popularity across the 
United States. A robust dataset with McDonald’s store reviews can be found on Kaggle. It contains information such 
as a store’s address and latitude and longitude, the number of ratings/ reviews for each location, the review and its 
timestamp, and the rating value on a scale of one to five. Feature engineering for calculating the competition density 
and extracting demographic information for each store location will be performed to find trends and cluster on review 
topic and rating.  

The team preprocessed the text using NLP Python libraries like spaCy or NLTK, which will 
deal with the necessary preprocessing. Sentiment analysis gave us more insight into the customer's attitude going 
beyond their numerical star rating. We started with models like Naive Bayes, Logistic Regression, or SVM, then movef 
to more complex models for higher accuracy, like CNN with Word2Vec and RNNs for sentiment analysis. With the insight 
we gained from sentiment analysis, we usef NLP topic modeling to extract common topics and themes in the reviews. 
Topic modeling combined with sentiment analysis will narrow down the specific aspects of McDonald's that are positive 
or negative. Since the dataset includes location data, we usef sentiment analysis from the reviews to build a 
location sentiment heatmap. By mapping out the sentiment and using topic modeling, there is the potential to uncover 
any trends. For example, rural areas might have higher ratings due to less traffic, or urban stores have low ratings 
because they are busier with longer wait times. 

Our approach was to start with the simpler models, evaluate their performance, and then move towards more complex
models if needed. We will experiment with different models and hyperparameters that need to be tuned, 
like the number of topics.  
 
    """
)

st.markdown(""":red[Methodology & Process]""")

st.markdown("""The below flow chart gives us a broad-stroke overview of the team's workflow for this project."
         """)

methodology_diagram = Image.open('./assets/methodology_steps.JPG')
st.image(methodology_diagram, caption="Project Workflow")

st.markdown("""
    For this project, the first step was to clean the reviews dataset, to ensure that it did not contain any 
    unusable data. This cleaning consisted of filtering out punctuation and special characters, performing a spell
    check, and purging any reviews that were not tied to a particular establishment.  
    
    From here, the team began with exploratory dat analysis, which resulted in the finding shown in the two bar graphs 
    shown below. Respectively, they show the worst commonly found in :blue["5-Star"] reviews, and those most commonly 
    found in :blue["1-star"] reviews            
""")

rating_positive = Image.open('./assets/rating_5_common_words.png')
st.image(rating_positive, caption="The most common positive words about McDonalds found in the Review Dataset")

rating_negative = Image.open('./assets/rating_1_common_words.png')
st.image(rating_negative, caption="The most common negative words about McDonalds found in the Review Dataset")

st.markdown(""" WE NEED INFO ON TOPIC MODELING AND SENTIMENT ANALYSIS""")

st.markdown("""BUILDING AND TUNING A RANDOM FOREST""")

st.markdown("""APPLICATION DEVELOPMENT

The team chose to make use of Streamlit and Pydeck for the Ui and visualization elements of this application, as
both are relatively flexible and powerful. These tools allowed the team to easily integrate its work into an 
approachable and aesthetically pleasing user-experience. 
""")

st.markdown(""":red[Results]""")

st.markdown(""":red[Conclusions & Areas of Future Work]""")

st.markdown("""
    The team is pleased to say that it has created a an approachable and effective sentiment analysis tool, 
    that enables users to easily asses the key strengths and areas of concern for a particular McDonalds franchise. 
    As it stands the application is responsive, and able to provide succinct and poignant information, 
    but it unfortunately is limited in scope to only those franchises, whose reviews we have access to in our dataset.
    
    Given more time, the team would've liked to expand both the review database, as well as the overall 
    functionality of the application. The team had hoped to create some form of a predictive model, 
    that based upon available information and national trends, would be able to give insight and recommendations for
    franchises that it was not familiar with, but the team rapidly learned that such an application was beyond the 
    timeframe and scope of this course. 
    
    In addition, the team would want to explore alternative models to compare and contrast with the current product, 
    in hopes of finding an even better solution.
""")


