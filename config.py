# -*- coding: utf-8 -*-

# Kategori Tanımları (Anahtar kelime tabanlı)
CATEGORIES = {
    "Düğün Mekanı": [
        "mekan", "salon", "lokasyon", "düğün yeri", "mekan ara", 
        "salon bak", "reception", "wedding venue", "yer sor"
    ],
    "Gelinlik": [
        "gelinlik", "kıyafet", "elbise", "wedding dress", "bridal",
        "gelin elbisesi", "kostüm", "tören kıyafeti"
    ],
    "Fotoğrafçı": [
        "fotoğraf", "çekim", "kamera", "fotoğrafçı", "photographer",
        "video", "albüm", "pre-wedding", "resim"
    ],
    "Nişan": [
        "nişan", "yüzük", "engagement", "pırlanta", "alyans",
        "tören", "nişanlık", "ring"
    ],
    "Kına": [
        "kına", "kına gecesi", "henna", "henne night", 
        "kına organizasyon", "gelin kınası"
    ],
    "Davetiye": [
        "davetiye", "kart", "invitation", "davet", 
        "card", "basım", "tasarım"
    ],
    "Catering": [
        "yemek", "menü", "catering", "ikram", "kokteyl",
        "servis", "aşçı", "menu"
    ]
}

# Niyet (Intent) Tanımları
INTENTS = {
    "Mekan Arıyor": [
        "mekan ara", "salon bak", "düğün yeri sor", "venue", 
        "yer arıyorum", "lokasyon sor", "mekan önerisi"
    ],
    "Ürün Arıyor": [
        "fiyat sor", "ücret öğren", "ne kadar", "price",
        "tutar nedir", "bütçe", "fiyat listesi", "cost"
    ],
    "Bilgi Soruyor": [
        "nedir", "nasıl", "bilgi ver", "information",
        "açıklama", "detay", "help", "yardım"
    ],
    "Randevu Alıyor": [
        "randevu", "tarih sor", "rezervasyon", "appointment",
        "ayırtmak", "booking", "tarih belirle"
    ],
    "Şikayet": [
        "problem", "şikayet", "complaint", "memnuniyetsiz",
        "kötü", "beğenmedim", "hatalı", "disappointed"
    ],
    "Övgü": [
        "teşekkür", "harika", "mükemmel", "thanks",
        "awesome", "perfect", "beğendim", "süper"
    ]
}

# Türkçe Duygu Analizi için Ekstra Kelimeler
SENTIMENT_WORDS = {
    "pozitif": {
        "mükemmel": 4.0, "harika": 4.0, "muhteşem": 4.0,
        "memnun": 3.5, "süper": 3.0, "kaliteli": 3.0,
        "hızlı": 2.5, "uygun": 2.0, "tavsiye": 3.0
    },
    "negatif": {
        "berbat": -4.0, "kötü": -3.5, "fahiş": -3.0,
        "pahalı": -3.0, "kalitesiz": -3.5, "hayal kırıklığı": -3.0,
        "gecikme": -2.5, "problem": -2.0, "şikayet": -3.0
    }
}

# Özel Ayarlar
SETTINGS = {
    "timezone": "Europe/Istanbul",
    "default_language": "tr",
    "max_response_time_hours": 24,
    "min_text_length": 3
}

def get_all_categories():
    """Kategorileri liste olarak döndürür"""
    return list(CATEGORIES.keys())

def get_all_intents():
    """Niyetleri liste olarak döndürür"""
    return list(INTENTS.keys())
