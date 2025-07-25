# Düğün Sohbet Analiz Projesi

![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

DüğünBuketi platformundan alınan müşteri konuşmalarının analizi için geliştirilmiş Python tabanlı araç.

## 🌟 Özellikler

- JSON formatındaki sohbet geçmişlerini analiz eder
- Her mesaj için:
  - Yanıtlanma durumu (Evet/Hayır)
  - Duygu analizi (Pozitif/Negatif/Nötr)
  - Kategori sınıflandırması (Düğün mekanı, Gelinlik vb.)
  - Niyet analizi (Mekan arıyor, Fiyat soruyor vb.)
- CSV ve SQLite çıktı desteği
- Türkçe dil desteği

## 🛠 Kurulum

1. **Gereksinimler**:
   ```bash
   git clone https://github.com/kullaniciadiniz/dugun-analiz-projesi.git
   cd dugun-analiz-projesi
