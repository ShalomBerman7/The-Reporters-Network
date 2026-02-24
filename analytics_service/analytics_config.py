# Import dependencies
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
nltk.download('vader_lexicon')# Compute sentiment labels
tweet = 'Skillcate is a great Youtube Channel to learn Data Science'
Score = SentimentIntensityAnalyzer().polarity_scores(tweet)
