from dronekit import connect, VehicleMode, LocationGlobalRelative
from pymavlink import mavutil,mavwp
import time

adress = "127.0.0.1:14550"
iha = mavutil.mavlink_connection(adress,baudrate=115200,autoreconnect = True)
iha.wait_heartbeat()
print("baglanti basarili")

#print(iha.is_armable)                                 # iha arm edilebilir mi edilemez mi kontrol edilir
#print(iha.armed)                                      # Şuanda ih aarm mı değl mi motorlar çalışıyor mu diye kontrol ediyor.


iha.set_mode("GUIDED")
iha.arducopter_arm()
iha.motors_armed()
iha.motors_armed_wait()
print("arm edildi")


#iha.mode = ihaMode("GUIDED")                      # İHA guıded mod ile dışarıdan komut alabilir duruma geçiyor.
#iha.armed = True                                      # İha arm ediliyor. motorlar artık çalışıyor.
#iha.simple_takeoff(10)                                # iha takeoff vererek 10 metre havalanacak

# def takeoff(irtifa):                                  # BU fonksiyon 
#     while iha.is_armable is not True:
#         print("İHA arm edilebilir durumda değil.")
#         time.sleep(1)


#     print("İHA arm edilebilir.")

#     iha.mode = ihaMode("GUIDED")

#     iha.armed = True

#     while iha.armed is not True:
#         print("İHA arm ediliyor...")
#         time.sleep(0.5)

#     print("İHA arm edildi.")

#     iha.simple_takeoff(irtifa)
    
#     while iha.location.global_relative_frame.alt < irtifa * 0.9:
#         print("İha hedefe yükseliyor.")
#         time.sleep(1)
    
# takeoff(10)

# konum = LocationGlobalRelative(-35.36223671, 149.16509335, 20)

# iha.simple_goto(konum)