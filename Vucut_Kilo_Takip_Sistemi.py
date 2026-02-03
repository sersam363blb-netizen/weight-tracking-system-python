import sqlite3
import math
from datetime import date
from datetime import timedelta
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class Vucut_Takip:
    def __init__(self, aktif_kullanici):
        self.aktif_kullanici= aktif_kullanici
        self.durum=True
    def vucut_takip_sistemi_calistir(self):
        print("Vücut Kilo Takip Sistemi Modülü Başlatıldı.\n{} Sistemimize Hoşgeldiniz:D".format(self.aktif_kullanici))
        self.database_var_mi()
        self.menu_vucut()
    def database_var_mi(self):
        self.connect_db()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS Vucut_Kilo_Takip (kullaniciad TEXT, cinsiyet TEXT,boy INT,kilo INT,boyun INT, bel INT, omuz INT, kalca INT, Ideal_Kilo REAL, BMI REAL, Vucut_Yag_Orani REAL,tarih TEXT)")
        self.connect.commit()

    def menu_vucut(self):
        while True:
            try:
                secim=int(input("Yapmak istediğiniz işlemi seçiniz:\n1) Yeni Bilgilerimi Ekle \n2) Son Bilgilerime Göre Ölçümler \n3) Geçmiş Verilerim\n4) Geçmiş Verilerimi Düzenle\n5) Çıkış yap"))
                if secim==1:
                    self.yeni_bilgileri_ekle()
                    break
                elif secim==2:
                    self.son_bilgilerime_gore_olcumler()
                    break
                elif secim==3:
                    self.gecmis_verilerim()
                    break
                elif secim==4:
                    self.gecmis_verilerimi_duzenle()
                    break
                elif secim==5:
                    self.connect.close()
                    self.cikis_yap()

                    return
                else:
                    print("Lütfen 1 ila 5 arasında bir tamsayı seçiniz!")
            except ValueError:
                print("Lütfen Sadece Sayı giriniz!")
    def yeni_bilgileri_ekle(self):
        self.connect_db()
        while True:
            try:
                tarih=date.today().isoformat()
                boy_cm=int(input("Lütfen boyunuzu giriniz."))
                while boy_cm <140 or boy_cm > 235:
                    boy_cm=int(input("Lütfen boyunuzu cm olarak giriniz giriniz!"))
                boy_m=boy_cm/100
                kilo=int(input("Lütfen Kilonuzu giriniz."))
                while kilo <40 or kilo > 180:
                    kilo=int(input("Lütfen kilonuzu kg olarak giriniz!"))
                bmi= kilo/(boy_m**2)
                self.cursor.execute("SELECT cinsiyet FROM Vucut_Kilo_Takip WHERE kullaniciad=? AND cinsiyet IS NOT NULL ORDER BY tarih DESC LIMIT 1",(self.aktif_kullanici,))
                row = self.cursor.fetchone()
                cinsiyet = row[0] if row else None
                if cinsiyet is None:
                    cinsiyet = input("Cinsiyet (E/K): ").strip().upper()
                while cinsiyet not in ("E", "K"):
                    cinsiyet = input("Hatalı. Cinsiyet (E/K): ").strip().upper()
                if cinsiyet == "E":
                    ideal_kilo= 50+2.3*((boy_cm/2.54)-60)
                if cinsiyet == "K":
                    ideal_kilo= 45.5+2.3*((boy_cm/2.54)-60)
                

                secim=int(input("Diğer ölçülerinizi de girmek ister misiniz?\n1) Evet\n2) Hayır"))
                if secim==1:
                    print("Devam ediliyor.")
                    while True:
                        try:
                            bel=int(input("Bel Ölçünüzü Giriniz:"))
                            boyun=int(input("Boyun Ölçünüzü Giriniz:"))
                            while bel <= boyun:
                                print("Lütfen belinizi ve boynunuzu doğru giriniz! Boynunuz, belinizden büyük olamaz!")
                                bel=int(input("Bel Ölçünüzü Giriniz:"))
                                boyun=int(input("Boyun Ölçünüzü Giriniz:"))
                            omuz=int(input("Omuz Ölçünüzü Giriniz:"))
                            kalca=int(input("Kalça Ölçünüzü Giriniz:"))
                            if cinsiyet == "E":
                                vucut_yag= 495 / (1.0324 - 0.19077 * math.log10(bel - boyun) + 0.15456 * math.log10(boy_cm)) - 450
                            if cinsiyet == "K":
                                vucut_yag= 495 / (1.29579 - 0.35004 * math.log10(bel + kalca - boyun) + 0.22100 * math.log10(boy_cm)) - 450
                            self.cursor.execute("INSERT INTO Vucut_Kilo_Takip (cinsiyet,boy,kilo,bel,boyun,omuz,kalca,Ideal_Kilo,BMI,Vucut_Yag_Orani,tarih,kullaniciad) Values(?,?,?,?,?,?,?,?,?,?,?,?)",(cinsiyet,boy_cm,kilo,bel,boyun,omuz,kalca,ideal_kilo,bmi,vucut_yag,tarih,self.aktif_kullanici))
                            self.connect.commit()
                            
                            print("İşleminiz gerçekleşmiştir.\nBoyunuz=?,Kilonuz=?, Beliniz=?, Boyununuz=?, Omzunuz=?, Kalçanız=? olarak belirlenmiştir.",(boy_cm,kilo,bel,boyun,omuz,kalca))
                            return
                        except ValueError:
                            print("Lütfen tam sayı olarak girişlerinizi yapınız!")
                        
                elif secim==2:
                    self.cursor.execute("INSERT INTO Vucut_Kilo_Takip (cinsiyet,boy,kilo,tarih,kullaniciad) Values(?,?,?,?,?)",(cinsiyet,boy_cm,kilo,tarih,self.aktif_kullanici))
                    self.connect.commit()
                    
                    print("İşleminiz gerçekleşmiştir.\nBoyunuz=?, Kilonuz=? olarak belirlenmiştir.",(boy_cm,kilo))
                    return
                else:
                    print("Lütfen sadece 1 veya 2 sayılarını kullanınız!")
                
            except ValueError:
                print("Lütfen sadece tam sayı olarak girişleri yapınız!")

    def son_bilgilerime_gore_olcumler(self):
        self.connect_db()
        
        self.cursor.execute("SELECT * FROM Vucut_Kilo_Takip WHERE kullaniciad=? ORDER BY tarih DESC LIMIT 1",(self.aktif_kullanici,))
        sonuclar=self.cursor.fetchone()
        if not sonuclar:
            print("Bu kullanıcı için bir kayıt yok!")
            return
        print("Ölçümünüz yapılmıştır.Sonuçlar:")
        print(sonuclar)
        
        
    def gecmis_verilerim(self):
        self.connect_db()
        while True:
            try:
                
                secim=int(input("Lütfen ne kadarlık bir sürede inceleme yapmamızı istediğinizi seçiniz.1) 1 haftalık süre\n2) 1 aylık süre\n 3) 3 aylık süre:"))
                if secim==1:
                    baslangic=date.today()-timedelta(days=7)
                    break
                elif secim==2:
                    baslangic=date.today()-timedelta(days=30)
                    break
                elif secim==3:
                    baslangic=date.today()-timedelta(days=90)
                    break
                else:
                    print("Lütfen 1,2 veya 3 ten birini seçiniz!")
            except ValueError:
                print("Lütfen sayıyla ne kadarlık süreçteki halinizi görmek istediğinizi seçiniz!") 
        baslangic=baslangic.isoformat()
        self.cursor.execute("SELECT * FROM Vucut_Kilo_Takip WHERE kullaniciad=? AND tarih>=? ORDER BY tarih DESC",(self.aktif_kullanici,baslangic))
        sonuc=self.cursor.fetchall()
        if not sonuc:
            print("Bu aralıkta bir kayıt bulunamıştır.")
        else:
            print(sonuc)
            print("Grafikler gösteriliyor....")
            df = pd.DataFrame(sonuc, columns=["boy","kilo","boyun","bel","omuz","kalca","bmi","Vucut_Yag_Orani","tarih"])
            df = df.dropna(subset=["tarih"])
            df["tarih"] = pd.to_datetime(df["tarih"], errors="coerce")
            df = df.dropna(subset=["tarih"])
            print(df.to_string(index=False))
            self.grafikleri_goster(df)
           
    def grafikleri_goster(self,df):
        df_kilo = df.dropna(subset=["kilo"])
        if not df_kilo.empty:
            plt.figure(figsize=(8,4))
            plt.plot(df_kilo["tarih"], df_kilo["kilo"], marker="o")
            plt.xlabel("Tarih")
            plt.ylabel("Kilo (kg)")
            plt.title("Kilo Değişimi")
            plt.grid(True)
            plt.tight_layout()
            plt.show()
        df_bmi = df.dropna(subset=["bmi"])
        if not df_bmi.empty:
            plt.figure(figsize=(8,4))
            plt.plot(df_bmi["tarih"], df_bmi["bmi"], marker="o")
            plt.xlabel("Tarih")
            plt.ylabel("BMI")
            plt.title("BMI Değişimi")
            plt.grid(True)
            plt.tight_layout()
            plt.show()
        df_yag = df.dropna(subset=["yag"])
        if not df_yag.empty:
            plt.figure(figsize=(8,4))
            plt.plot(df_yag["tarih"], df_yag["yag"], marker="o")
            plt.xlabel("Tarih")
            plt.ylabel("Yağ Oranı (%)")
            plt.title("Vücut Yağ Oranı Değişimi")
            plt.grid(True)
            plt.tight_layout()
            plt.show()

    def gecmis_verilerimi_duzenle(self):
        self.connect_db()
        baslangic = (date.today() - timedelta(days=15)).isoformat()
        self.cursor.execute("SELECT rowid,kullaniciad,cinsiyet,boy,kilo,boyun,bel,omuz,kalca FROM Vucut_Kilo_Takip WHERE kullaniciad=? AND tarih>=? ORDER BY tarih DESC",(self.aktif_kullanici, baslangic))
        bilgiler = self.cursor.fetchall()
        if not bilgiler:
            print("Son 15 günde girilmiş bir bilginiz yoktur!")
            return
        print(bilgiler)
        rowid = int(input("Lütfen hangi günü değiştirmek istiyorsanız rowid giriniz: "))
        while True:
            try:
                secim = int(input("Değiştirmek istediğiniz veriyi sayı olarak seçin.\n1) boy,\n2) kilo,\n3) boyun,\n4) bel,\n5) omuz,\n6) kalca\n> "))
                operation = ["boy", "kilo", "boyun", "bel", "omuz", "kalca"]
                if 1 <= secim <= 6:
                    secilen = operation[secim - 1]
                    sql_select = f"SELECT {secilen} FROM Vucut_Kilo_Takip WHERE kullaniciad=? AND tarih>=? AND rowid=?"
                    self.cursor.execute(sql_select, (self.aktif_kullanici, baslangic, rowid))
                    eski = self.cursor.fetchone()
                    if not eski:
                        print("Bu rowid için kayıt bulunamadı.")
                        continue
                    print(f"Değiştirmek istediğiniz mevcut değer: {eski[0]}")
                    while True:
                        try:
                            degistiren = int(input("Lütfen yeni değeri yazınız: "))
                            break
                        except ValueError:
                            print("Lütfen bir sayı giriniz.")
                    sql_update = f"UPDATE Vucut_Kilo_Takip SET {secilen}=? WHERE kullaniciad=? AND tarih>=? AND rowid=?"
                    self.cursor.execute(sql_update, (degistiren, self.aktif_kullanici, baslangic, rowid))
                    self.connect.commit()

                    print("İşleminiz gerçekleşmiştir.")
                    break
                else:
                    print("Lütfen 1 ile 6 arasında bir tam sayı seçin!")

            except ValueError:
                print("Lütfen sayı olarak seçin!")
    def cikis_yap(self):
        print("Vücut Kilo sisteminden çıkılıyor.")
        self.durum=False
        

    def connect_db(self):
        self.connect= sqlite3.connect("Vucut_Kilo_Takip.db")
        self.cursor= self.connect.cursor()
        
        

