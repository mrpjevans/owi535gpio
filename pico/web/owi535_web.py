from machine import Pin, PWM
from time import sleep
import network
import owi535

import WIFI_CONFIG
import socket
import _thread

# Connect to wifi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(WIFI_CONFIG.SSID, WIFI_CONFIG.PSK)
retry_count = 0
while wlan.isconnected() == False:
    print('Waiting for wifi connection...')
    retry_count += 1
    if retry_count > 10:
        print("Giving up")
        break
    sleep(1)
print('Wifi connected')
print('IP address:', wlan.ifconfig()[0])


led = Pin("LED", Pin.OUT)
led.on()

with open("index.html", "r") as f:
	html = f.read()

addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
s = socket.socket()
s.bind(addr)
s.listen(1)
print('Listening on', addr)

def serve_page(conn):
	conn.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
	conn.sendall(html)
	conn.close()

def web_server():
	while True:
		conn, addr = s.accept()
		print('Client connected from', addr)
		try:
			req = conn.recv(1024)
			request_line = req.decode().split('\r\n')[0]
			path = request_line.split(' ')[1] if len(request_line.split(' ')) > 1 else '/'
			if path == '/':
				serve_page(conn)
			elif path == '/stop':
				# Call all_stop on stop
				owi535.all_stop()
				conn.send('HTTP/1.0 200 OK\r\nContent-type: text/plain\r\n\r\n')
				conn.sendall(b'STOPPED')
				conn.close()
			else:
				# Expecting /motor/direction
				parts = path.lstrip('/').split('/')
				if len(parts) == 2:
					motor, direction = parts
					move_arm(motor, direction)
					conn.send('HTTP/1.0 200 OK\r\nContent-type: text/plain\r\n\r\n')
					conn.sendall(b'OK')
					conn.close()
				else:
					conn.send('HTTP/1.0 404 Not Found\r\nContent-type: text/plain\r\n\r\n')
					conn.sendall(b'Not Found')
					conn.close()
		except Exception as e:
			print('Error:', e)
			owi535.all_stop()
			conn.close()

def move_arm(motor, direction):
	owi535.all_stop()
	print(motor, direction)
	# Check if the motor is valid
	if motor not in owi535.motors:
		print(f"Unknown motor: {motor}")
		return
	if direction == 'forward':
		owi535.move(motor, forward=True)
	elif direction == 'reverse':
		owi535.move(motor, forward=False)
	else:
		print(f"Unknown direction: {direction}")

web_server()