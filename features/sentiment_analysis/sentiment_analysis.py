import pandas as pd
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

mcd_file = "CleanedData/cleaned_reviews.csv"

nltk.download('vader_lexicon')
nltk.download('omw-1.4')

def sentiment_analysis(input_file):
    #get dataset
    df = pd.read_csv(input_file, encoding="latin-1")
    reviews = df["review"]
    
    #preprocess ratings
    df['rating'] = df['rating'].str.replace(' star', '')
    df['rating'] = df['rating'].str.replace('s', '')
    df['rating'] = df['rating'].astype(int)
    ratings = df['rating']

    sia = SentimentIntensityAnalyzer()
    compound_scores = []
    idx = 0
    
    #calculating polarity score
    for review in reviews:
        #calculating compound score 
        if type(review) != str:
            rating_value = ratings[idx]
            compound_score = 2*((rating_value - 1) /4) - 1
            compound_scores.append(compound_score)
        else:
            compound_score = sia.polarity_scores(review)['compound']
            compound_scores.append(compound_score)
        idx += 1
        
    #create new dataset
    sentiment_df = pd.DataFrame(list(zip(compound_scores)), columns = ['compound_score'])
    new_df = pd.concat([df, sentiment_df], axis=1)
    
    #save result to file
    new_df.to_csv('features/sentiment_analysis/df_sentiment_analysis.csv', index=False)
    
df_sentiment_analysis = sentiment_analysis(mcd_file)