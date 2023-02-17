# coding=utf-8
from pymavlink import mavutil
import serial , time

# adres = "udpin:localhost:14550"
adres = serial.Serial('/dev/ttyACM0')
# adres = "/dev/ttyTHS1:115200"

VTOLbrkt = mavutil.mavlink_connection(adres, baud=115200, autoreconnect=True)
VTOLbrkt.wait_heartbeat()
print("Baglanti kuruldu")

VTOLbrkt.set_mode("GUIDED")
print("GUIDED moduna gecildi")

VTOLbrkt.arducopter_arm() # IHA'yý arm et (kalkýþ yapýlabilir hale getir) fakat yalnýzca GUIDED modunda çalýþýr ve droneler için kullanýlýr
print("Arm edildi")

VTOLbrkt.motors_armed() # ayrýca uçak yada VTOL ýhalar kullanýlacaksa ekstradan bu komutu yazmak gereklidir. Çünkü bu komutlar arasýnda bir fark vardýr. 
# "motors_armed()"" komutu sadece motorlarý arm eder. Ancak "arducopter_arm()" komutu motorlarý arm eder ve ayný zamanda kalkýþ yapýlabilir hale getirir.

VTOLbrkt.motors_armed_wait() # motorlar arm olana kadar bekler
print("Motorlar arm edildi")

def anlik_yukseklik():
    mesaj = VTOLbrkt.recv_match(type='GLOBAL_POSITION_INT', blocking=True)
    alt = mesaj.relative_alt/1000
    return alt

# takeoff komutu ile IHA'nýn kalkýþ yapmasý saðlanýr
# takeoff komutu 2 parametre alýr
# 1. parametre: kalkýþ yapýlacak yükseklik
# 2. parametre: kalkýþ yapýlacak hýz
def takeoff(yukseklik, hiz):
    VTOLbrkt.mav.command_long_send(VTOLbrkt.target_system, VTOLbrkt.target_component, mavutil.mavlink.MAV_CMD_NAV_VTOL_TAKEOFF, 0,0,0,0,0,0,0,yukseklik, hiz)
    print("Kalkis yapiliyor")
    VTOLbrkt.motors_armed_wait() # motorlar arm olana kadar bekler
    print("Kalkis yapildi")
    



    while True:
        if anlik_yukseklik() >= yukseklik:
            print("Kalkis tamamlandi")
            break

takeoff(10, 0) # 10 metre yükseklikte 0 hýzla kalkýþ yap

# MAV_CMD_NAV_VTOL_TAKEOFF komutu ile IHA'nýn kalkýþ yapmasý saðlanýr
# MAV_CMD_NAV_VTOL_TAKEOFF komutu 11 parametre alýr
# 1. parametre: 0
# 2. parametre: 0
# 3. parametre: 0
# 4. parametre: 0
# 5. parametre: 0
# 6. parametre: 0
# 7. parametre: 0
# 8. parametre: 10 (kalkýþ yapýlacak yükseklik)
# 9. parametre: 0 (kalkýþ yapýlacak hýz)
# 10. parametre: 0 (kalkýþ yapýlacak hýz)
# yazýlan rakamlardan bir tanesi onaylama için olmak üzere 7tane 0 yazýldý ardýndan yukseklik ve hýz parametreleri yazýldý. 0,0,0,0,0,0,10,0 yazýlabilirdi.

VTOLbrkt.motors_armed_wait() # motorlar arm olana kadar bekler
print("Motorlar arm edildi")

# takeoff komutu ile IHA'nýn kalkýþ yapmasý saðlanýr
# takeoff komutu 2 parametre alýr
# 1. parametre: kalkýþ yapýlacak yükseklik
# 2. parametre: kalkýþ yapýlacak hýz

time.sleep(10) # 10 saniye bekle

def land(yukseklik, hiz):
    VTOLbrkt.mav.command_long_send(VTOLbrkt.target_system, VTOLbrkt.target_component, mavutil.mavlink.MAV_CMD_NAV_VTOL_LAND, 0,0,0,0,0,0,0,yukseklik,hiz)
    print("Inis yapiliyor")
    VTOLbrkt.motors_armed_wait() # motorlar arm olana kadar bekler
    print("Inis yapildi")
    VTOLbrkt.arducopter_disarm() # IHA'yý disarm et (kalkýþ yapýlamaz hale getir)
    print("Disarm edildi")

land(0, 0) # 0 metre yükseklikte 0 hýzla iniþ yap

# MAV_CMD_NAV_VTOL_LAND komutu ile IHA'nýn iniþ yapmasý saðlanýr