from sentiment_tr import TurkishSentimentAnalyzer

analyzer = TurkishSentimentAnalyzer()
test_cases = [
    ("Harika bir mekan!", "Pozitif"),
    ("Fiyatlar çok pahalı", "Negatif"),
    ("Teslimat tarihini öğrenebilir miyim?", "Nötr"),
    ("Mükemmel bir organizasyondu", "Pozitif"),
    ("Berbat bir deneyim yaşadık", "Negatif")
]

for text, expected in test_cases:
    result = analyzer.analyze(text)
    print(f"Metin: {text} | Beklenen: {expected} | Sonuç: {result} | {'✅' if result == expected else '❌'}")
