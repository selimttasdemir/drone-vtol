# coding=utf-8
from pymavlink import mavutil
import serial , time

adres = "udpin:localhost:14550"
# adres = serial.Serial('/dev/ttyACM0')
# adres = "/dev/ttyTHS1:115200"

VTOLbrkt = mavutil.mavlink_connection(adres, baud=115200, autoreconnect=True)
VTOLbrkt.wait_heartbeat()
print("Baglanti kuruldu")

VTOLbrkt.set_mode("GUIDED")
print("GUIDED moduna gecildi")

VTOLbrkt.arducopter_arm() # IHA'y� arm et (kalk�� yap�labilir hale getir) fakat yaln�zca GUIDED modunda �al���r ve droneler i�in kullan�l�r
print("Arm edildi")

VTOLbrkt.motors_armed() # ayr�ca u�ak yada VTOL �halar kullan�lacaksa ekstradan bu komutu yazmak gereklidir. ��nk� bu komutlar aras�nda bir fark vard�r. 
# "motors_armed()"" komutu sadece motorlar� arm eder. Ancak "arducopter_arm()" komutu motorlar� arm eder ve ayn� zamanda kalk�� yap�labilir hale getirir.

VTOLbrkt.motors_armed_wait() # motorlar arm olana kadar bekler
print("Motorlar arm edildi")

def anlik_yukseklik():
    mesaj = VTOLbrkt.recv_match(type='GLOBAL_POSITION_INT', blocking=True)
    alt = mesaj.relative_alt/1000
    return alt

# takeoff komutu ile IHA'n�n kalk�� yapmas� sa�lan�r
# takeoff komutu 2 parametre al�r
# 1. parametre: kalk�� yap�lacak y�kseklik
# 2. parametre: kalk�� yap�lacak h�z
def takeoff(yukseklik, hiz):
    VTOLbrkt.mav.command_long_send(VTOLbrkt.target_system, VTOLbrkt.target_component, mavutil.mavlink.MAV_CMD_NAV_VTOL_TAKEOFF, 0,0,0,0,0,0,0,yukseklik, hiz)
    print("Kalkis yapiliyor")
    VTOLbrkt.motors_armed_wait() # motorlar arm olana kadar bekler
    print("Kalkis yapildi")
    



    while True:
        if anlik_yukseklik() >= yukseklik:
            print("Kalkis tamamlandi")
            break

takeoff(10, 0) # 10 metre y�kseklikte 0 h�zla kalk�� yap

# MAV_CMD_NAV_VTOL_TAKEOFF komutu ile IHA'n�n kalk�� yapmas� sa�lan�r
# MAV_CMD_NAV_VTOL_TAKEOFF komutu 11 parametre al�r
# 1. parametre: 0
# 2. parametre: 0
# 3. parametre: 0
# 4. parametre: 0
# 5. parametre: 0
# 6. parametre: 0
# 7. parametre: 0
# 8. parametre: 10 (kalk�� yap�lacak y�kseklik)
# 9. parametre: 0 (kalk�� yap�lacak h�z)
# 10. parametre: 0 (kalk�� yap�lacak h�z)
# yaz�lan rakamlardan bir tanesi onaylama i�in olmak �zere 7tane 0 yaz�ld� ard�ndan yukseklik ve h�z parametreleri yaz�ld�. 0,0,0,0,0,0,10,0 yaz�labilirdi.

VTOLbrkt.motors_armed_wait() # motorlar arm olana kadar bekler
print("Motorlar arm edildi")

# takeoff komutu ile IHA'n�n kalk�� yapmas� sa�lan�r
# takeoff komutu 2 parametre al�r
# 1. parametre: kalk�� yap�lacak y�kseklik
# 2. parametre: kalk�� yap�lacak h�z

time.sleep(10) # 10 saniye bekle

def land(yukseklik, hiz):
    VTOLbrkt.mav.command_long_send(VTOLbrkt.target_system, VTOLbrkt.target_component, mavutil.mavlink.MAV_CMD_NAV_VTOL_LAND, 0,0,0,0,0,0,0,yukseklik,hiz)
    print("Inis yapiliyor")
    VTOLbrkt.motors_armed_wait() # motorlar arm olana kadar bekler
    print("Inis yapildi")
    VTOLbrkt.arducopter_disarm() # IHA'y� disarm et (kalk�� yap�lamaz hale getir)
    print("Disarm edildi")

land(0, 0) # 0 metre y�kseklikte 0 h�zla ini� yap

# MAV_CMD_NAV_VTOL_LAND komutu ile IHA'n�n ini� yapmas� sa�lan�r