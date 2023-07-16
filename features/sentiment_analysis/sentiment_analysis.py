import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.stem import WordNetLemmatizer
from textblob import TextBlob 

mcd_file = "cleaned_reviews.csv"

nltk.download('punkt')
nltk.download('wordnet')
nltk.download('stopwords')
nltk.download('vader_lexicon')

stop_words = set(stopwords.words('english'))
stop_words.add('wa')
stop_words.add('get')
lemmatizer = WordNetLemmatizer()

def preprocess_text(text):
    tokens = word_tokenize(text.lower())
    tokens = [lemmatizer.lemmatize(token) for token in tokens if token.isalpha()]
    tokens = [token for token in tokens if token not in stop_words]
    return tokens

def getPolarity(text):
   return TextBlob(text).sentiment.polarity

def sentiment_analysis(input_file):
    #get dataset
    df = pd.read_csv(input_file, encoding='ISO-8859-1')
    reviews = df["review"]
    
    #preprocess reviews
    preprocessed_rvws = []
    for i, review in reviews.iteritems():
        tokens = preprocess_text(review)
        preprocessed_rvws.append(tokens)

    sia = SentimentIntensityAnalyzer()
    compound_scores = []
    polarity_scores = []
    
    #calculating polarity score
    for review in preprocessed_rvws:
        #calculating polarity score
        polarity_score = review.apply(getPolarity)
        polarity_scores.append(polarity_score)
        
        #calculating compound score    
        compound_score = sia.polarity_scores(review)['compound']
        compound_scores.append(compound_score)
            
    #calculating "super score"
    num_reviews = len(preprocessed_rvws)
    super_scores = []
    
    for i in range(num_reviews):
        super_scores[i] = polarity_score[i] * compound_score[i]
        
    #create new dataset
    sentiment_df = pd.DataFrame(list(zip(polarity_scores, compound_scores, super_scores)), 
                          columns = ['polarity_score', 'compound_score', 'super_score'])
    new_df = pd.concat([df, sentiment_df], axis=1)
    
    #save result to file
    new_df.to_csv('df_sentiment_analysis.csv', index=False)
    
df_sentiment_analysis = sentiment_analysis(mcd_file)