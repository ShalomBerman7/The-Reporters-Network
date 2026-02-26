# נותן דירוג למשפטים
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
nltk.download('vader_lexicon')
tweet = 'love'
Score = SentimentIntensityAnalyzer().polarity_scores(tweet)
print(Score)


def check_text(text):
    score = SentimentIntensityAnalyzer().polarity_scores(text)
    if score['compound'] >= 0.5000:
        return 'חיובי'
    elif score['compound'] >= -0.4991 and score['compound'] <= 0.4999:
        return 'ניטרלי'
    else:
        return 'שלילי'

print(check_text(tweet))