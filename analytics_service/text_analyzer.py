from shared.logger import get_logger
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

nltk.download('vader_lexicon', quiet=True)


class TextAnalyzer:
    def __init__(self):
        self.logger = get_logger('TextAnalyzer')
        self.analyzer = SentimentIntensityAnalyzer()

    def text_analyze(self, text):
        if not text:
            return 'Neutral'

        score = self.analyzer.polarity_scores(text)
        if score['compound'] >= 0.5000:
            return 'Positive'
        elif -0.4991 <= score['compound'] <= 0.4999:
            return 'Neutral'
        else:
            return 'Negative'

    def process_message(self, data):
        text_to_analyze = data.get('clean text', data.get('text', ''))
        sentiment = self.text_analyze(text_to_analyze)

        processed_data = {
            **data,
            "sentiment": sentiment,
            "status": "analyzed"
        }
        return processed_data
