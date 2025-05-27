# 📊 Trendyol Yorum Analizi – NLP Final Projesi

Bu proje, İstanbul Medeniyet Üniversitesi Bilgisayar Mühendisliği bölümünde **Doğal Dil İşleme (NLP)** dersi kapsamında gerçekleştirilmiştir. Amaç, Trendyol e-ticaret platformundan toplanan ürün yorumları üzerinden **duygu analizi** (sentiment analysis) yaparak, yorumları otomatik olarak olumlu, olumsuz ve nötr şeklinde sınıflandırmaktır.

## 👤 Geliştirici
**Kadir Kartal**  
Öğrenci No: 22120205079  
Ders Sorumlusu: Dr. Öğr. Üyesi Muhammet Sinan BAŞARSLAN  
📅 Mayıs 2025

---

## 📌 Proje Özeti

Trendyol’dan çekilen 1.000’den fazla ürün yorumu üzerinden veri işleme, metin ön işleme, TF-IDF vektörleştirme ve **Multinomial Naive Bayes** algoritması ile duygu analizi yapılmıştır. Ayrıca, **Zeyrek morfolojik analiz aracı** ile en sık kullanılan sıfat ve fiiller çıkarılmıştır. Eğitim/test veri oranları değiştirilerek model başarımı incelenmiştir.

---

## 🔍 Kullanılan Yöntemler ve Teknolojiler

- Python (Pandas, Scikit-learn, Selenium, Zeyrek, NLTK)
- TF-IDF vektörleme
- Multinomial Naive Bayes sınıflandırıcı
- Web scraping (Selenium ile Trendyol)
- Zeyrek ile morfolojik analiz
- Jupyter Notebook / Spyder IDE

---

## 🧪 Deneysel Sonuçlar

| Eğitim/Test Oranı | Doğruluk | Macro F1 Score |
|-------------------|----------|----------------|
| %10 / %90         | 92.6%    | 0.87           |
| %30 / %70         | 99.8%    | 1.00           |
| %50 / %50         | 99.8%    | 1.00           |

---

## 💬 Örnek Sonuçlar

**Olumsuz (1-2 Yıldız) İçin En Sık Kelimeler:**
- işe, kahve, etki, yok, abarta, asla, aldım...

**Nötr (3 Yıldız):**
- şöyle, iştahımı, açtııııı, anlamıyorum, susama...

**Olumlu (4-5 Yıldız):**
- kilo, tok, tutuyor, geldi, yardımcı...

---

## 🧠 Morfolojik Analiz (Zeyrek)

Zeyrek kullanılarak en sık geçen sıfat ve fiiller çıkarılmıştır. Örnek olarak:

| Sınıf     | Örnek Sıfatlar     | Örnek Fiiller       |
|-----------|--------------------|----------------------|
| Olumsuz   | kötü, gereksiz     | işe yaramıyor, bozuldu |
| Nötr      | orta, sıradan      | anlamıyorum, yapmadı |
| Olumlu    | kaliteli, tok      | tutuyor, yardımcı oldu |

---

## 📁 Dosyalar

- `veri_cekme.py` → Trendyol’dan yorumları çeker
- `yorumlama.py` → Veri analizi, model eğitimi ve yorum sınıflandırması
- `trendyol_yorumlari.xlsx` → Çekilen yorumların saklandığı dosya
- `Kadir_Kartal_NLP_Final.docx` → Proje raporunun Word formatı

---

## 📚 Kaynakça

- Bird, S., Klein, E., & Loper, E. (2009). *Natural Language Processing with Python*. O’Reilly Media.
- Jurafsky, D., & Martin, J. H. (2020). *Speech and Language Processing*.
- Manning, C. D., Raghavan, P., & Schütze, H. (2008). *Introduction to Information Retrieval*.
- McCallum, A., & Nigam, K. (1998). *Naive Bayes Text Classification*.
- Çakır, M. P., & Karaoğlan, B. (2018). *Türkçe metinlerde duygu analizi*.
- TDK (2023). *Güncel Türkçe Sözlük*. https://sozluk.gov.tr/

---

## 🛠️ Kurulum

```bash
git clone https://github.com/Kadirkartal2406/trenyol-yorum-analizi.git
cd trenyol-yorum-analizi
pip install -r requirements.txt
