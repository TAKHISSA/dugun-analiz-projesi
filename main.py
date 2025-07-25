#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import pandas as pd
import os
import sqlite3
from datetime import datetime
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from config import CATEGORIES, INTENTS
import nltk
import logging
from typing import List, Dict, Any, Optional, Union

# Log ayarları
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('wedding_analysis.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Türkçe NLP alternatifi
try:
    from turkishnlp import TurkishNLP
    TURKISH_NLP_AVAILABLE = True
    logger.info("TurkishNLP başarıyla yüklendi")
except ImportError:
    TURKISH_NLP_AVAILABLE = False
    logger.warning("TurkishNLP kütüphanesi bulunamadı, sadece VADER kullanılacak")

nltk.data.path.append('./nltk_data')

class TurkishSentimentAnalyzer:
    """Türkçe metinler için duygu analizi sınıfı"""
    
    def __init__(self):
        self.en_analyzer = SentimentIntensityAnalyzer()
        
        # Gelişmiş Türkçe kelime listesi
        self.custom_lexicon = {
            'mükemmel': 4.0, 'harika': 4.0, 'muhteşem': 4.0, 'şaheser': 4.0,
            'berbat': -4.0, 'kötü': -3.0, 'fahiş': -3.0, 'rezalet': -4.0,
            'pahalı': -2.5, 'kalitesiz': -3.0, 'memnun': 3.0, 'tavsiye': 2.0,
            'hayal kırıklığı': -3.0, 'müthiş': 4.0, 'korkunç': -4.0,
            'vasat': -1.0, 'orta': 0.5, 'idare eder': 1.0
        }
        self.en_analyzer.lexicon.update(self.custom_lexicon)
        
        if TURKISH_NLP_AVAILABLE:
            self.tr_nlp = TurkishNLP()
            try:
                if not os.path.exists('TurkishNLP'):
                    logger.info("TurkishNLP modelleri indiriliyor...")
                    self.tr_nlp.download()
            except Exception as e:
                logger.error(f"TurkishNLP model indirme hatası: {str(e)}")

    def analyze(self, text: str) -> str:
        """Metin için duygu analizi yapar
        
        Args:
            text: Analiz edilecek metin
            
        Returns:
            str: "Pozitif", "Negatif" veya "Nötr"
        """
        if not text or not isinstance(text, str):
            return "Nötr"
        
        # TurkishNLP ile analiz
        if TURKISH_NLP_AVAILABLE:
            try:
                tr_result = self.tr_nlp.sentiment_analysis(text)
                if tr_result['overall'] != 'neutral':
                    return tr_result['overall'].capitalize()
            except Exception as e:
                logger.error(f"TurkishNLP analiz hatası: {str(e)}")
        
        # VADER ile analiz
        scores = self.en_analyzer.polarity_scores(text)
        if scores['compound'] >= 0.05:
            return "Pozitif"
        elif scores['compound'] <= -0.05:
            return "Negatif"
        return "Nötr"

class WeddingChatAnalyzer:
    """Düğün sohbet analiz sınıfı"""
    
    def __init__(self):
        self.sentiment_analyzer = TurkishSentimentAnalyzer()
    
    def analyze_conversations(self, json_path: str) -> pd.DataFrame:
        """JSON dosyasındaki konuşmaları analiz eder
        
        Args:
            json_path: Analiz edilecek JSON dosya yolu
            
        Returns:
            pd.DataFrame: Analiz sonuçlarını içeren DataFrame
        """
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            logger.info(f"{json_path} başarıyla yüklendi")
        except Exception as e:
            logger.error(f"JSON okuma hatası: {str(e)}")
            return pd.DataFrame()
        
        results = []
        for conv in data:
            try:
                conv_results = self._process_conversation(conv)
                results.extend(conv_results)
            except Exception as e:
                logger.error(f"Konuşma işleme hatası: {str(e)}")
                continue
        
        return pd.DataFrame(results)
    
    def _process_conversation(self, conversation: Dict) -> List[Dict]:
        """Tek bir konuşmayı işler"""
        conv_id = conversation.get('conversation_id', '')
        messages = conversation.get('messages', [])
        return [self._analyze_message(msg, i, messages) 
                for i, msg in enumerate(messages)]
    
    def _analyze_message(self, msg: Dict, idx: int, messages: List) -> Dict:
        """Tek bir mesajı analiz eder"""
        try:
            text = self._extract_text(msg)
            return {
                'conversation_id': msg.get('conversation_id', ''),
                'message_id': msg.get('id', idx),
                'sender_id': msg.get('sender_id', ''),
                'text': text,
                'is_answered': self._check_if_answered(messages, idx),
                'sentiment': self.sentiment_analyzer.analyze(text),
                'category': self._detect_category(text),
                'intent': self._detect_intent(text),
                'type': msg.get('type', ''),
                'is_internal': msg.get('is_internal', False),
                'timestamp': msg.get('created_at', ''),
                'response_time': self._calculate_response_time(messages, idx, msg.get('created_at'))
            }
        except Exception as e:
            logger.error(f"Mesaj analiz hatası: {str(e)}")
            return {}
    
    def _extract_text(self, msg: Dict) -> str:
        """Mesajdan metni çıkarır"""
        content = msg.get('content', {})
        if isinstance(content, dict):
            if 'text' in content:
                return content['text']
            if 'options' in content:
                return " | ".join(opt.get('text', '') for opt in content.get('options', []))
        return ""
    
    def _check_if_answered(self, messages: List, current_idx: int) -> str:
        """Mesajın yanıtlanıp yanıtlanmadığını kontrol eder"""
        if current_idx + 1 >= len(messages):
            return "Hayır"
        current = messages[current_idx].get('sender_id')
        next_msg = messages[current_idx+1].get('sender_id')
        return "Evet" if current != next_msg and next_msg is not None else "Hayır"
    
    def _detect_category(self, text: str) -> str:
        """Mesajın kategorisini belirler"""
        if not text:
            return "Belirsiz"
        
        text_lower = text.lower()
        for category, keywords in CATEGORIES.items():
            if any(kw.lower() in text_lower for kw in keywords):
                return category
        return "Diğer"
    
    def _detect_intent(self, text: str) -> str:
        """Mesajın niyetini belirler"""
        if not text:
            return "Belirsiz"
        
        text_lower = text.lower()
        for intent, keywords in INTENTS.items():
            if any(kw.lower() in text_lower for kw in keywords):
                return intent
        return "Genel Sorgu"
    
    def _calculate_response_time(self, messages: List, idx: int, timestamp: str) -> Optional[str]:
        """Yanıt süresini hesaplar"""
        if idx == 0 or not timestamp:
            return None
        
        try:
            prev_time = datetime.fromisoformat(messages[idx-1].get('created_at'))
            curr_time = datetime.fromisoformat(timestamp)
            return str(curr_time - prev_time)
        except Exception as e:
            logger.debug(f"Zaman hesaplama hatası: {str(e)}")
            return None

def ensure_directory(path: str) -> None:
    """Dizin yoksa oluşturur"""
    os.makedirs(path, exist_ok=True)

def main():
    """Ana işlem fonksiyonu"""
    try:
        ensure_directory('outputs')
        analyzer = WeddingChatAnalyzer()
        
        json_files = [f for f in os.listdir('data') if f.endswith('.json')]
        if not json_files:
            logger.warning("'data' klasöründe JSON dosyası bulunamadı")
            return
        
        for json_file in json_files:
            logger.info(f"Analiz ediliyor: {json_file}")
            try:
                df = analyzer.analyze_conversations(f'data/{json_file}')
                
                if df.empty:
                    logger.warning(f"{json_file} işlendi ancak boş veri döndü")
                    continue
                
                # Çıktı dosya adları
                base_name = os.path.splitext(json_file)[0]
                csv_path = f'outputs/{base_name}_analysis.csv'
                db_path = f'outputs/{base_name}_analysis.db'
                
                # CSV kaydet
                df.to_csv(csv_path, index=False, encoding='utf-8-sig')
                
                # SQLite kaydet
                try:
                    with sqlite3.connect(db_path) as conn:
                        df.to_sql('conversation_analysis', conn, 
                                 if_exists='replace', index=False)
                    logger.info(f"Çıktılar kaydedildi: {csv_path}, {db_path}")
                except sqlite3.Error as e:
                    logger.error(f"Veritabanı kayıt hatası: {str(e)}")
                    
            except Exception as e:
                logger.error(f"{json_file} işlenirken hata: {str(e)}")
                continue
                
    except Exception as e:
        logger.critical(f"Beklenmeyen hata: {str(e)}", exc_info=True)
    finally:
        logger.info("Analiz süreci tamamlandı")

if __name__ == "__main__":
    main()
