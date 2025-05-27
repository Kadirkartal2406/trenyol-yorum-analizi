from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report, accuracy_score
import pandas as pd
import warnings
from collections import Counter

# Uyarıları kapatma
warnings.filterwarnings('ignore')

# Stopword listesi
turkish_stopwords = [
    've', 'bir', 'bu', 'da', 'de', 'için', 'ile', 'ama', 'fakat', 'çok', 'gibi', 'daha',
    'şu', 'mi', 'mı', 'mu', 'mü', 'ne', 'ya', 'ki', 'o', 'veya', 'hem', 'her', 'hiç', 'ben',
    'sen', 'biz', 'siz', 'onlar', 'çünkü', 'ancak', 'artık', 'en', 'bazı', 'sadece'
]

# Excel dosyasını oku
df = pd.read_excel("trendyol_yorumlari.xlsx")

# Yorumları boş olmayanlarla filtrele
df["Yorum"] = df["Yorum"].fillna("").astype(str)

# Yıldızlara göre 3 sınıflı etiketleme
def label_grup(y):
    if y in [1, 2]:
        return 0  # Olumsuz
    elif y == 3:
        return 1  # Nötr
    elif y in [4, 5]:
        return 2  # Olumlu
    else:
        return -1  # Diğer (varsa)

df['YildizGrup'] = df['Yıldız'].apply(label_grup)
df = df[df['YildizGrup'] != -1]  # Sadece 0,1,2 sınıflarını al

X = df["Yorum"]
y = df["YildizGrup"]

# Veriyi böl
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.5, random_state=42)

# TF-IDF vektörleme
vectorizer = TfidfVectorizer(stop_words=turkish_stopwords)
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

# Model oluştur ve eğit
model = MultinomialNB()
model.fit(X_train_vec, y_train)

# Tahmin yap
y_pred = model.predict(X_test_vec)

# Sonuçları yazdır
print("Doğruluk:", accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred, zero_division=1))

# En sık kelimeleri bulma fonksiyonu
def en_sik_kelimeler(yildiz_grup_num, n=10):
    yorumlar = df[df['YildizGrup'] == yildiz_grup_num]['Yorum'].str.cat(sep=' ')
    kelimeler = yorumlar.lower().split()
    kelimeler = [k for k in kelimeler if k not in turkish_stopwords and len(k) > 2]
    counter = Counter(kelimeler)
    return counter.most_common(n)

# Sınıflar için en sık kelimeleri yazdır
siniflar = {0: "Olumsuz (1-2 Yıldız)", 1: "Nötr (3 Yıldız)", 2: "Olumlu (4-5 Yıldız)"}
for k, v in siniflar.items():
    print(f"\n=== {v} için en sık kullanılan kelimeler ===")
    for kelime, sayi in en_sik_kelimeler(k):
        print(f"{kelime}: {sayi}")
import zeyrek
from collections import Counter

analyzer = zeyrek.MorphAnalyzer()

def yorumdan_sifat_ve_fiil_cek(yorum):
    sonuc = analyzer.analyze(yorum.lower())
    secilen_kelimeler = []
    for analizler in sonuc:
        for analiz in analizler:
            if analiz.pos in ['Adjective', 'Verb']:  # sadece sıfat ve fiil
                secilen_kelimeler.append(analiz.normalized_input)
                break  # ilk uygun analizi al
    return secilen_kelimeler

def kelime_frekansi(df, yildiz):
    yorumlar = df[df['YildizGrup'] == yildiz]['Yorum']
    kelimeler = []
    for yorum in yorumlar:
        kelimeler.extend(yorumdan_sifat_ve_fiil_cek(yorum))
    return Counter(kelimeler).most_common(10)

print("\n=== Sıfat ve Fiil Temelli Yorum Analizi ===")
for yildiz in sorted(df['YildizGrup'].unique()):
    print(f"\n=== {yildiz} yıldız için en sık geçen sıfat ve fiiller ===")
    for kelime, sayi in kelime_frekansi(df, yildiz):
        print(f"{kelime}: {sayi}")
