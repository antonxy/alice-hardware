#!/usr/bin/env python3
import socket
from math import sqrt, pi
import time

# Receives GPS and Compass from the Sensorstream app via UDP and forwards it to alice via TCP
# Download app from here https://play.google.com/store/apps/details?id=de.lorenz_fenster.sensorstreamgps

last_gps = [-1.0, -1.0, -1.0]
last_angle = -1

def send(sock):
    global last_gps, last_angle
    sock.send("{} {} {} {} {} {}\n".format(last_gps[0], last_gps[1], last_gps[2], last_angle, -1, -1).encode("utf-8"))

def main():
    global last_gps, last_angle
    UDP_IP = "0.0.0.0"
    UDP_PORT = 5555

    sock = socket.socket(socket.AF_INET, # Internet
                         socket.SOCK_DGRAM) # UDP
    sock.bind((UDP_IP, UDP_PORT))

    OUTPUT_HOST = "localhost"
    OUTPUT_PORT = 2323


    while True:
        try:
            outs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            outs.connect((OUTPUT_HOST, OUTPUT_PORT))

            while True:
                data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
                data_str = data.decode("utf-8")
                #print(data_str)
                splitted = data_str.split(',')
                the_time = splitted[0]
                splitted_no_time = splitted[1:]
                #print('------')
                #print(splitted_no_time)
                i = 0
                while i < len(splitted_no_time):
                    num = int(splitted_no_time[i])
                    if num == 1:
                        data = list(map(float, splitted_no_time[i+1:i+4]))
                        print("GPS:", data)
                        last_gps = data
                        send(outs)
                    elif num == 8:
                        i += 2  # Number 8 is has only one data field
                        continue
                    elif num == 81:
                        data = list(map(float, splitted_no_time[i+1:i+4]))
                        angle_to_north = data[0]
                        if angle_to_north > 180.0:
                            angle_to_north -= 360.0
                        angle_to_north *= pi / 180.0
                        print("Angle to north:", angle_to_north)
                        last_angle = angle_to_north
                        send(outs)
                    '''
                    elif num == 84:
                        # https://developer.android.com/guide/topics/sensors/sensors_motion.html#sensors-motion-rotate
                        data = list(map(float, splitted_no_time[i+1:i+4]))
                        xyz = data
                        w = sqrt(1.0 - xyz[0] ** 2 - xyz[1] ** 2 - xyz[2] ** 2)  # Apparently wrong
                        quat = xyz + [w]
                        print(quat)
                    '''
                    i += 4
        except Exception as e:
            print("Error \"{}\", will try to reconnect".format(e))

        outs.close()
        time.sleep(2.0)

if __name__ == "__main__":
    main()
