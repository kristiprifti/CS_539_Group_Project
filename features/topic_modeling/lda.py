#this code does topic modeling on the reviews of a pd data frame. User must enter the file path and number of topics
#and the code will add the probability of a review being part of a specific topic to a column. If there are
#30 topics then it will add 30 columns to the input dataframe.
#good resource https://towardsdatascience.com/end-to-end-topic-modeling-in-python-latent-dirichlet-allocation-lda-35ce4ed6b3e0

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.externals import joblib
import pandas as pd

nltk.download('punkt')
nltk.download('wordnet')
nltk.download('stopwords')

stop_words = set(stopwords.words('english'))
stop_words.add('wa')
stop_words.add('get')
lemmatizer = WordNetLemmatizer()

def preprocess_text(text):
    tokens = word_tokenize(text.lower())
    tokens = [lemmatizer.lemmatize(token) for token in tokens if token.isalpha()]
    tokens = [token for token in tokens if token not in stop_words]
    return tokens

def topic_modeling_train(input_file, n_topics):
    #get dataset
    df = pd.read_csv(input_file, encoding='ISO-8859-1')
    reviews = df["review"]
    reviews = reviews.fillna('') #fill na to solve a text.lower() errror in above func
    #preprocess the reviews
    preprocessed_rvws = []
    for i, review in reviews.iteritems():
        tokens = preprocess_text(review)
        preprocessed_rvws.append(tokens)

    #create document-term matrix
    vectorizer = CountVectorizer(ngram_range=(2,3))
    dtm = vectorizer.fit_transform([' '.join(review) for review in preprocessed_rvws])
    feature_names = vectorizer.get_feature_names()

    #train LDA:
    lda = LatentDirichletAllocation(n_components=n_topics, random_state=42)
    lda.fit(dtm)

    #topic probabilities for each review
    review_topic_probs = lda.transform(dtm)

    #make df with topic probabilities and add to existing df
    topic_columns = [f"Topic_{i+1}" for i in range(n_topics)]
    topic_df = pd.DataFrame(review_topic_probs, columns=topic_columns)
    new_df = pd.concat([df, topic_df], axis=1)

    #save result to file
    new_df.to_csv('df_topic.csv', index=False)

    #save the topic definitions to a text file
    with open('topic_definitions.txt', 'w') as f:
        for i, topic in enumerate(lda.components_):
            f.write(f"Topic {i+1}:\n")
            top_words_i = topic.argsort()[:-11:-1]  # Top 10 words
            top_words = [feature_names[i] for i in top_words_i]
            f.write(", ".join(top_words))
            f.write("\n\n")
    return new_df


#topic modeling on train set
df_train = topic_modeling_train('cleanlocDF.csv', n_topics=30)


