from pymavlink import mavutil,mavwp

adress= "127.0.0.1:14550"
iha = mavutil.mavlink_connection(adress,baudrate=115200,autoreconnect = True)
iha.wait_heartbeat()
print("baglanti basarili")


iha.set_mode("GUIDED")
iha.arducopter_arm()
iha.motors_armed()
iha.motors_armed_wait()
print("arm edildi")

wp = mavwp.MAVWPLoader()

def anlik_irtifa():
    message = iha.recv_match(type='GLOBAL_POSITION_INT', blocking= True)
    alt=message.relative_alt
    alt = alt/1000
    return alt

def takeoff(alt):
    iha.mav.command_long_send(iha.target_system, iha.target_component,mavutil.mavlink.MAV_CMD_NAV_TAKEOFF, 0, 0, 0, 0, 0, 0, 0, alt)
    while True: 
        current_alt= anlik_irtifa()
        if current_alt < alt:
            print(f"Anlik irtifa {current_alt}")
        elif current_alt >=  alt:
            print("Istenilen irtifaya ulasildi ")
            break

def add_mission(seq,lat,lon,alt):
    frame= mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT
    wp.add(mavutil.mavlink.MAVLink_mission_item_message(iha.target_system, iha.target_component,
    seq,
    frame,
    mavutil.mavlink.MAV_CMD_NAV_WAYPOINT,0,0,0,0,0,0,lat,lon,alt))

    iha.waypoint_clear_all_send()
    iha.waypoint_count_send(wp.count())
    for i in range (wp.count()):
        msg= iha.recv_match(type=["MISSION_REQUEST"], blocking= True)
        iha.mav.send(wp.wp(msg.seq))
        print("Sending waypoints {0}".format(msg.seq))

iha.set_mode("GUIDED")
iha.arducopter_arm()
takeoff(10)
add_mission(0, -35.36208860, 149.16523400, 20)
add_mission(1, -35.36183050, 149.16420400, 30)
add_mission(2, -35.36230730, 149.16314180, 35)
add_mission(3, -35.36350160, 149.16353880, 15)
add_mission(4, -35.36366780, 149.16447760, 10)
add_mission(5, -35.36328720, 149.16522320, 5)
iha.set_mode("RTL")