from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re  # RegEx işlemleri için
import pandas as pd
import tkinter as tk
from tkinter import simpledialog

# Chrome seçenekleri
chrome_options = Options()
chrome_options.add_argument("--headless")  # Tarayıcıyı başsız modda çalıştır
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920,1080")

# ChromeDriver'ı otomatik indir ve kullan
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# Arayüz oluşturma
root = tk.Tk()
root.withdraw()  # Ana pencereyi gizle

# Kullanıcıdan link ve yorum sayısını alma
url = simpledialog.askstring("Link", "Lütfen Trendyol ürün yorum sayfasının linkini girin:")
comment_count = simpledialog.askinteger("Yorum Sayısı", "Lütfen çekilecek yorum sayısını girin:")

if url and comment_count:
    driver.get(url)

    # Sayfanın yüklenmesi için bekleme
    wait = WebDriverWait(driver, 40)
    wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'comment-text')]")))

    # Yorumları ve yıldızları çekme
    comments = []
    ratings = []
    previous_comment_count = 0  # Yorum sayısını takip et

    while len(comments) < comment_count:
        try:
            # Yorumları çeken XPath
            comment_elements = driver.find_elements(By.XPATH, "//div[contains(@class, 'comment-text')]")
            # Yıldızları çeken XPath
            rating_elements = driver.find_elements(By.XPATH, "//div[@class='comment-rating']")

            if not comment_elements or not rating_elements:
                print("Yorum veya yıldız öğesi bulunamadı.")
                break

            for comment, rating_element in zip(comment_elements, rating_elements):
                if len(comments) >= comment_count:
                    break
                comments.append(comment.text)

                # Yıldızları hesapla
                stars = rating_element.find_elements(By.XPATH, ".//div[@class='full']")
                total_rating = 0

                for star in stars:
                    style_attr = star.get_attribute("style")
                    match = re.search(r'width:\s*(\d+)', style_attr)
                    if match:
                        width_percentage = int(match.group(1))  # Yüzdelik değeri al (0-100)
                        total_rating += (width_percentage / 100)  # Tam yıldız hesapla

                ratings.append(total_rating)

            # Sayfa kaydırma (yeni yorumları yüklemek için)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(5)  # Yorumların yüklenmesi için bekleme

            # Yeni yorum eklenip eklenmediğini kontrol et
            if len(comments) == previous_comment_count:
                break  # Eğer yeni yorum eklenmediyse, durdur
            previous_comment_count = len(comments)

        except Exception as e:
            print(f"Hata oluştu: {e}")
            break

    driver.quit()

    # Verileri bir DataFrame'e çevirme
    df = pd.DataFrame({"Yorum": comments, "Yıldız": ratings})

    # Yıldız sayılarına göre değerlendirme ekleme
    def degerlendir(yildiz):
        if yildiz == 5:
            return "Çok İyi"
        elif yildiz == 4:
            return "İyi"
        elif yildiz == 3:
            return "Nötr"
        elif yildiz == 2:
            return "Kötü"
        else:
            return "Çok Kötü"

    df["Değerlendirme"] = df["Yıldız"].apply(degerlendir)

    # Excel dosyasına yazdırma
    excel_dosya = "trendyol_yorumlari.xlsx"
    df.to_excel(excel_dosya, index=False)

    print(f"{len(comments)} yorum ve yıldız bilgisi {excel_dosya} dosyasına yazıldı.")
else:
    print("Link veya yorum sayısı girilmedi.")