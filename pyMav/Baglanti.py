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
# adres = serial.Serial('COM15', baudrate)
# adres = "/dev/ttyTHS1:115200"

# Specify only the address when creating the Serial object
# adres = serial.Serial('/dev/ttyUSB0', baudrate)
adres = serial.Serial('/dev/ttyACM0', baudrate)

# Connect to the mavlink device using the address and baudrate separately
baglanti = mavutil.mavlink_connection(
    device=adres.name,
    baud=baudrate
)

baglanti.wait_heartbeat()
print("Baglanti kuruldu")

while True:
    # mesaj = baglanti.recv_match() # Tüm mesajları al
    # if mesaj is not None: # mesaj varsa
    #     print(mesaj) # mesajı yazdır


    mesajPil = baglanti.recv_match(type='BATTERY_STATUS', blocking=True) # type ile sadece istenen mesajı al
    if mesajPil is not None: # mesaj varsa
        print(f"Batarya Yüzdesi: {mesajPil.battery_remaining}") # istenen mesajın istenen özelliğinin mesajını yazdır
    else :
        print("none")
        break
    
    mesajRollPitch = baglanti.recv_match(type='AHRS2', blocking=True) # type ile sadece istenen mesajı al
    if mesajRollPitch is not None: # mesaj varsa
        print(f"Roll: {mesajRollPitch.roll}, Pitch: {mesajRollPitch.pitch}") # istenen mesajın istenen özelliğinin mesajını yazdır
        break

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

    # IHA'nın konumunu yazdır
    mesajKonum = baglanti.recv_match(type='GLOBAL_POSITION_INT', blocking=True) # type ile sadece istenen mesajı al
    if mesajKonum is not None: # mesaj varsa
        print(f"Konum: {mesajKonum.lat}, {mesajKonum.lon}") # istenen mesajın istenen özelliğinin mesajını yazdır

    # IHA'nın yüksekliğini yazdır
    mesajYukseklik = baglanti.recv_match(type='GLOBAL_POSITION_INT', blocking=True) # type ile sadece istenen mesajı al
    if mesajYukseklik is not None: # mesaj varsa
        print(f"Yukseklik: {mesajYukseklik.relative_alt}") # istenen mesajın istenen özelliğinin mesajını yazdır
    
    # IHA'nın hızını yazdır
    mesajHiz = baglanti.recv_match(type='VFR_HUD', blocking=True) # type ile sadece istenen mesajı al
    if mesajHiz is not None: # mesaj varsa
        print(f"Hiz: {mesajHiz.airspeed}") # istenen mesajın istenen özelliğinin mesajını yazdır

    # IHA'nın yönünü yazdır
    mesajYon = baglanti.recv_match(type='VFR_HUD', blocking=True) # type ile sadece istenen mesajı al
    if mesajYon is not None: # mesaj varsa
        print(f"Yon: {mesajYon.heading}") # istenen mesajın istenen özelliğinin mesajını yazdır
    
    # IHA'nın arm durumunu yazdır
    mesajArm = baglanti.recv_match(type='HEARTBEAT', blocking=True) # HEARTBEAR ile IHA'nın arm durumunu öğren
    if mesajArm is not None: # mesaj varsa
        print(f"Arm: {mesajArm.base_mode}") # istenen mesajın istenen özelliğinin mesajını yazdır

    # IHA'nın yaw değerini yazdır
    mesajYaw = baglanti.recv_match(type='ATTITUDE', blocking=True) # type ile sadece istenen mesajı al
    if mesajYaw is not None: # mesaj varsa
        print(f"Yaw: {mesajYaw.yaw}") # istenen mesajın istenen özelliğinin mesajını yazdır

