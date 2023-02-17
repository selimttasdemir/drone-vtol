"""
Selim Taşdemir
github.com/selimttasdemir
Tarih : 02.14.2023

Açıklama : 
Bu dosyada IHA'nın mavlink ile bağlantı kurması
mesajların filtrelenmesi işlemleri yapılmıştır

"""



from pymavlink import mavutil
import serial

baudrate = 115200

# adres = "udpin:localhost:14550"
adres = serial.Serial('/dev/ttyACM0', baudrate, timeout=1)
# adres = "/dev/ttyTHS1:115200"

baglanti = mavutil.mavlink_connection(adres, source_system=1)
baglanti.wait_heartbeat()
print("Baglanti kuruldu")

# while True:
#     mesaj = baglanti.recv_match() # Tüm mesajları al
#     if mesaj is not None: # mesaj varsa
#         print(mesaj) # mesajı yazdır


mesajPil = baglanti.recv_match(type='BATTERY_STATUS', blocking=True) # type ile sadece istenen mesajı al
if mesajPil is not None: # mesaj varsa
    print(f"Batarya Yüzdesi: {mesajPil.battery_remaining}") # istenen mesajın istenen özelliğinin mesajını yazdır

mesajRollPitch = baglanti.recv_match(type='AHRS2', blocking=True) # type ile sadece istenen mesajı al
if mesajRollPitch is not None: # mesaj varsa
    print(f"Roll: {mesajRollPitch.roll}, Pitch: {mesajRollPitch.pitch}") # istenen mesajın istenen özelliğinin mesajını yazdır

mesajGSpeed = baglanti.recv_match(type='VFR_HUD', blocking=True) # type ile sadece istenen mesajı al
if mesajGSpeed is not None: # mesaj varsa
    print(f"Ground Speed: {mesajGSpeed.groundspeed}") # istenen mesajın istenen özelliğinin mesajını yazdır

mesajASpeed = baglanti.recv_match(type='VFR_HUD', blocking=True) # type ile sadece istenen mesajı al
if mesajASpeed is not None: # mesaj varsa
    print(f"Air Speed: {mesajASpeed.airspeed}") # istenen mesajın istenen özelliğinin mesajını yazdır

# Stabilize modunu yazdır
mesajMod = baglanti.recv_match(type='HEARTBEAT', blocking=True) # HEARTBEAR ile IHA'nın mode durumunu öğren
mode = mavutil.mode_string_v10(mesajMod)
if mesajMod is not None: # mesaj varsa
    print(f"Mod: {mode}") # istenen mesajın istenen özelliğinin mesajını yazdır

