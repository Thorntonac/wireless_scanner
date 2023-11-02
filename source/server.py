import socket
import sys
import json
import keyboard

class server:
	def __init__(self, ip, port=24810):
		self.ip = ip
		self.port = port
		self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.server_socket.bind((ip, port))
		self.typed_string: str = ''

		self.start_server()

	def start_server(self):
		print(f"[*] Server Started on {self.ip}:{self.port}")
		keyboard.hook(self.handle_server)

		while True:
			(data, client_socket) = self.server_socket.recvfrom(1024)
			command = data.decode('utf-8')

			if command == '0x0000x0000':
				self.client_socket = client_socket
				print(f'[*] Client Connected')

	def gather_string(self, keypress:str):
		if keypress != 'enter':
			self.typed_string += keypress
		else:
			print(f'[*] Scanned: {self.typed_string}')
			self.server_socket.sendto(self.typed_string.encode("utf-8"), self.client_socket)
			if self.typed_string == '753677510005':
				self.close_server()
			self.typed_string = ''

	def handle_server(self, key_event):
		key = (json.loads(key_event.to_json()))
		if key['event_type'] == 'down':
			self.gather_string(key['name'])

	def close_server(self):
		print('[-] SHUTTING DOWN')
		keyboard.stash_state()
		keyboard.unhook(self.handle_server)
		self.server_socket.close()
		exit()


if __name__ == '__main__':
	#  Args = IP
	Server = server(sys.argv[1])
	Server.start_server()