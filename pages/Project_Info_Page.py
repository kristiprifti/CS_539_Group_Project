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

The team preprocessed the text using NLP Python libraries like spaCy or NLTK. Sentiment analysis gave us more insight into the customer's
attitude going beyond their numerical star rating. With the insight we gained from sentiment analysis, we used NLP topic 
modeling to extract common topics and themes in the reviews. Topic modeling combined with sentiment analysis will narrow down the 
specific aspects of McDonald's that have a significant impact on the star rating. Since the dataset includes location data, we used sentiment analysis 
from the reviews to build a location sentiment heatmap. By mapping out the sentiment compound scorea and using topic modeling, there is the potential to uncover 
any trends. For example, rural areas might have higher ratings due to less traffic, or urban stores have low ratings 
because they are busier with longer wait times. Features created topic modeling and sentiment anyalsis was used to train a random forest model and find which features
had the most impact on a star rating.

Our approach was to start with a base model, evaluate its performance, and tune its hyperparameters.
 
    """
)

st.markdown(""":red[Methodology & Process]""")

st.markdown("""The below flow chart gives us a broad-stroke overview of the team's workflow for this project."
         """)

methodology_diagram = Image.open('./assets/methodology_steps.JPG')
st.image(methodology_diagram, caption="Project Workflow")

st.markdown("""
    For this project, the first step was to clean the McDonald's Reviews Kaggle dataset to ensure that it did not contain any 
    unusable data. This cleaning consisted of filtering out punctuation and special characters, performing a spell
    check, and purging any reviews that were not tied to a particular establishment.  The team preprocessed the text using NLP Python 
    libraries like spaCy and NLTK.
    
    From here, the team began with exploratory data analysis to evaluate the distribution of the reviews and word counts by each review. 
    The graphs below show the most common words found in reviews with :blue["5-Star"] ratings and :blue["1-star"] ratings. 
""")

rating_positive = Image.open('./assets/rating_5_common_words.png')
st.image(rating_positive, caption="The most common words found in 5-star reviews about McDonald's")

rating_negative = Image.open('./assets/rating_1_common_words.png')
st.image(rating_negative, caption="The most common words found in 1-star reviews about McDonald's")

st.markdown("""insert about topic modeling here""")

st.markdown(""" 
The third phase of the team's project largely centered around sentiment analysis, i.e. the process of reviewing digital 
text in the hopes of ascertaining the emotional tone of a message. A compound score can be extracted from this analysis to determine the degree 
of sentiment the message has. Its value can be between -1, indicating negative sentinment, and 1, indicating positive sentinment. 
This process was applied to all of the review data in the Kaggle dataset(https://www.kaggle.com/datasets/nelgiriyewithana/mcdonalds-store-reviews).
If there was no review, the star rating was normalized between -1 and 1 to fill in for the compound score. This compound score was added to our master dataset for training.

The team used a sentiment analysis package called VADER, which stands for :blue[V]alence :blue[A]ware :blue[D]ictionary and s:blue[E]ntiment :blue[R]easoner. 
VADER is a lexicon and rule-based sentiment analysis tool that is specifically attuned to sentiments expressed in social media and text from other domains.
""")

st.markdown("""The fourth phase of this project was the model development phase. The team chose to use a random forest since it performs well in a variety of 
contexts while being able to measure feature importance. We started with a base random forest model with 200 trees in the forest and some randomized bootstrapping
to predict the star rating. The team then tuned the model using a grid search on a variety of variables, and cross-validation was used to validate the results of each fit. After tuning the model, 
it produced a test R-squared value of around 0.62 as well as a list of important features in predicting the star rating.""")

st.markdown("""
The team chose to make use of Streamlit and Pydeck for the Ui and visualization elements of this application, as
both are relatively flexible and powerful. These tools allowed the team to easily integrate its work into an 
approachable and aesthetically pleasing user-experience. 

Streamlit is a simple-to-use, nearly all-in-one, data visualization tool, that allows for easy and quick 
web-application development, without having to make use of more traditional web-app coding langugaes, such as HTML or 
JavaScript.

Pydeck was used to create the  search bar, dataset toggles, and interactive map on the index page. 
Pydeck was chosen for its ease of use, as well as its relative stability when working with large datasets, a key factor
in the team's decision to make use of it over "shinier" options like Folium.

With the current application, users are able to make use of the model's functionality on the index/home page, as well as
find helpful links to the documentation and data that the team used, reach out to the team member's, and of course 
read this documentation and discussion. 
""")

st.markdown(""":red[Results]""")

st.markdown("""The final performance result for the teams model, was 
""")
st.latex("R^2 : 0.615")

st.markdown("""
Which was a major improvement over earlier results, largely due to refinements in sentiment analysis and 
iterative hyper-parameter tuning. The output of Feature importance metrics also demonstrates which 
characteristics had a significant impact on a particular McDonalds' net rating. 
""")

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


