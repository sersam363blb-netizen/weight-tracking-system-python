import sqlite3
from Bot_Projesi.Borsa_Botu_Kullanici_Arayuz import BorsaBotu
from Vucut_Kilo_Takip_Sistemi import Vucut_Takip
from Ev_Projesi import EvProjesi

class Sistem:
    def __init__(self):
        self.durum=True

    def sistem_calistir(self):
        print("Sistem başlatıldı.")
        self.admin_giris()
       
    def admin_giris(self):
        adminsifre=input("Admin şifresini giriniz:")
        
        if adminsifre=="123":
            self.kullanici_giris()
        else:
            print("Yanlış şifre!")
    
    def kullanici_giris(self):
        print("Admin girişi başarılı.")
        self.kullanici_sifresi_karsilastir()

    def kullanici_sifresi_karsilastir(self,):
        self.connect_db()
        self.kullanici_var_mi()
        kullaniciadi=input("Kullanıcı adınızı giriniz:")
        sifre=input("Şifrenizi giriniz:")
        self.cursor.execute("SELECT * FROM kullanicilar WHERE kullaniciad=? AND sifre=?",(kullaniciadi,sifre)) 
        kullanici=self.cursor.fetchone()
        if kullanici:
            print("Kullanıcı girişi başarılı.")
            self.aktif_kullanici=kullaniciadi
            self.menu_goster()
        else:
            print("Kullanıcı adı veya şifre yanlış.")
            self.durum=False  

    def kullanici_var_mi(self):
        self.cursor.execute("SELECT * FROM kullanicilar")
        kullanicilar=self.cursor.fetchall()
        if not kullanicilar:
            self.cursor.execute("INSERT INTO kullanicilar VALUES ('testuser','testpass')")
            self.connect.commit()    

    def menu_goster(self):
        
        print("****{} kullanıcısı olarak giriş yaptınız.****".format(self.aktif_kullanici))
        
        try: 
            while True:
                secim=int(input("Yapmak istediğiniz işlemi seçiniz:\n1) Kullanıcı İşlemlerini Aç\n2) Borsa Botunu Aç\n3) Vücut Takip Sistemi\n4) Ev Kontrol Sistemi\n5) Çıkış Yap"))
                if secim==1:
                    self.kullanici_islemleri(self.aktif_kullanici)
                    break
                if secim==2:
                    bot=BorsaBotu(self.aktif_kullanici)
                    bot.borsa_botu_calistir()
                    break
                if secim==3:
                    bot1=Vucut_Takip(self.aktif_kullanici)
                    bot1.vucut_takip_sistemi_calistir()
                    break
                if secim==4:
                    bot2=EvProjesi(self.aktif_kullanici)
                    bot2.ev_kontrol_sistemi_calistir()
                    break
                if secim==5:
                    self.cikis_yap()
                    break
        except ValueError:
            print("Lütfen sayı olarak bir seçim yapınız.")

    def kullanici_islemleri(self):
        try:
            while True:
                secim=int(input("Kullanıcı işlemlerinden yapmak istediğiniz işlemi seçiniz:\n1) Kullanıcı Ekle\n2) Kullanıcı Güncelle\n3) Kullanıcı Sil\n4) Geri Dön"))
                if secim==1:
                    self.kullanici_ekle()
                    break
                if secim==2:
                    self.kullanici_güncelle()
                    break
                if secim==3:
                    self.kullanici_sil()
                    break
                if secim==4:
                    self.menu_goster()
                    break
        except ValueError:
            print("Lütfen sayı olarak bir seçim yapınız.")

    def kullanici_ekle(self):
        self.connect_db()
        while True:
            eklenenkadi=input("Eklemek istediğiniz kullanıcı adını giriniz:")
            eklenensifre=input("Eklemek istediğiniz kullanıcının şifresini belirleyiniz:")
            try:
                if not eklenenkadi or not eklenensifre:
                    print("Lütfen eksik bırakmayınız")
                    continue
                self.cursor.execute("SELECT 1 FROM kullanicilar WHERE kullaniciad=?",(eklenenkadi,))
                var_mi= self.cursor.fetchone()
                if var_mi:
                    print("Belirlediğiniz kullanıcı adı özgün degildir. Lütfen kendinize göre bir kullanıcı adı veya şifre belirleyiniz")
                    continue
                self.cursor.execute("INSERT INTO kullanicilar(kullaniciad,sifre) VALUES (?,?)",(eklenenkadi,eklenensifre))
                self.connect.commit()
                print("Kullanıcı eklendi.")
                break
            except:
                print("Lütfen metin ve sayı olarak giriniz. Sadece sayı girmeyiniz.")
    
    def kullanici_güncelle(self):
        self.connect_db()
        self.cursor.execute("SELECT * FROM kullanicilar")
        kullanicilistesi= self.cursor.fetchall()
        print(kullanicilistesi)
        while True:
            try:
                kullanici=input("Lütfen güncellemek istediğiniz kullanıcı adını giriniz:")
                self.cursor.execute("SELECT * FROM kullanicilar WHERE kullaniciad=?",(kullanici,))
                var_mi= self.cursor.fetchone()
                if var_mi:
                    try:
                        while True:
                            secim= int(input("Lütfen güncellemek istediğiniz niteliği sayı olarak seçiniz\n1) Kullanıcı adı\n2) Şifre"))
                            if secim==1:
                                yenikulad=input("Lütfen değiştirmek istediğiniz yeni kullanıcı adı yazınız.")
                                self.cursor.execute("UPDATE kullanicilar SET kullaniciad=? where kullaniciad=?",(yenikulad,kullanici))
                                print("Kullanıcı adı istediğiniz gibi değiştirilmişitir.")
                                self.connect.commit()
                                return
                            elif secim==2:
                                yenisifre=input("Lütfen değiştirmek istediğiniz yeni şifreyi yazınız.")
                                self.cursor.execute("UPDATE kullanicilar SET sifre=? Where kullaniciad=?",(yenisifre,kullanici))
                                print("Yeni şifre işlemi gerçekleşmiştir.")
                                self.connect.commit()
                                return
                            else:
                                print("Lütfen 1 veya 2'yi seçiniz.")
                    except ValueError:
                        print("Lütfen sadece sayı giriniz")
                else:
                    print("Lütfen varolan bir kullanıcı adı yazınız.")
            except ValueError:
                print("Lütfen sadece sayı olarak bir yazı girmeyiniz")

    def kullanici_sil(self):
        self.connect_db()
        self.cursor.execute("SELECT * FROM kullanicilar")
        kullanicilistesi= self.cursor.fetchall()
        while True:
            try:
                secim= input("Lütfen silmek istediğiniz kullanıcının adını yazın")
                self.cursor.execute("Select 1 From kullanicilar WHERE kullaniciad=?",(secim,))
                var_mi= self.cursor.fetchone()
                if var_mi:
                    self.cursor.execute("Delete from kullanicilar where kullaniciad=?",(secim,))
                    print("İşleminiz gerçekleşmiştir.")
                    self.connect.commit()
                    break
                else:
                    print("Lütfen varolan bir kullanıcının adını giriniz.")
            except ValueError:
                print("Lütfen doğru şekile bir kullanıcı adı giriniz.")

    def connect_db(self):
        self.connect= sqlite3.connect("kullanici.db")
        self.cursor= self.connect.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS kullanicilar (kullaniciad TEXT, sifre TEXT)")
        
    def cikis_yap(self):
        print("Sistemden çıkış yapıldı.")
        self.durum=False


sistem=Sistem()
while sistem.durum:
    sistem.sistem_calistir()