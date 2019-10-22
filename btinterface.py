import struct
import time

import bluetooth

import datefunction
import sqlite


def connect_to_usb_tester(bt_addr):
    try:
        sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        sock.connect((bt_addr, 1))
        sock.settimeout(1.0)
        for _ in range(10):
            try:
                read_data(sock)
            except bluetooth.BluetoothError as e:
                time.sleep(0.2)
            else:
                break
        return sock

    except Exception as e:
        print(e)


def read_data(sock):
    sock.send(bytes([0xF0]))
    d = bytes()
    while len(d) < 130:
        d += sock.recv(1024)
    assert len(d) == 130, len(d)
    return d


def read_measurements(sock):
    d = read_data(sock)
    assert d[0:2] == bytes([0x09, 0x63])
    assert d[-2:] == bytes([0xff, 0xf1])
    voltage, current, power = [x / 100 for x in struct.unpack('!HHI', d[2:10])]
    temp_celsius, temp_fahrenheit = struct.unpack('!HH', d[10:14])
    usb_data_pos_voltage, usb_data_neg_voltage = [x / 100 for x in struct.unpack('!HH', d[96:100])]
    charging_mode = d[100]
    del d
    del sock
    return locals()


def connect(bt_addr):
    while True:
        try:
            sock = connect_to_usb_tester(bt_addr)
            measurement = read_measurements(sock)
            volt = measurement["voltage"]
            temp = measurement["temp_celsius"]
            data = datefunction.nowToDatetimeHrString()
            print("Volt:" + str(volt) + " temp: " + str(temp))
            # sqlite.createDatabase()
            sqlite.insertValues(volt, temp, data)
        except KeyboardInterrupt:
            pass
        except Exception as e:
            print(e)
        finally:
            if not sock is None:
                sock.close()
                time.sleep(10)
