from Turkishnlp import TurkishNLP
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pandas as pd

class TurkishSentimentAnalyzer:
    def __init__(self):
        self.tr_nlp = TurkishNLP()
        self.tr_nlp.download()
        self.en_analyzer = SentimentIntensityAnalyzer()
        
        # Türkçe özel kelime listesi
        self.custom_lexicon = {
            'mükemmel': 4.0, 'harika': 4.0, 'müthiş': 4.0,
            'berbat': -4.0, 'kötü': -3.0, 'fahiş': -3.0,
            'pahalı': -2.5, 'kalitesiz': -3.0
        }
        self.en_analyzer.lexicon.update(self.custom_lexicon)
    
    def analyze(self, text):
        try:
            # Önce Türkçe analiz
            tr_result = self.tr_nlp.sentiment_analysis(text)
            
            # İngilizce analiz (destek için)
            en_scores = self.en_analyzer.polarity_scores(text)
            
            # Kombine sonuç
            if tr_result['overall'] != 'neutral':
                return tr_result['overall'].capitalize()
            elif en_scores['compound'] >= 0.05:
                return "Pozitif"
            elif en_scores['compound'] <= -0.05:
                return "Negatif"
            return "Nötr"
        except:
            # Fallback to VADER
            scores = self.en_analyzer.polarity_scores(text)
            if scores['compound'] >= 0.05:
                return "Pozitif"
            elif scores['compound'] <= -0.05:
                return "Negatif"
            return "Nötr"
