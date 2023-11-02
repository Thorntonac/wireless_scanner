import socket
import sys
import keyboard

def get_platform_code():
	platform = sys.platform
	if platform == 'win32':
		return 0
	if platform == 'linux':
		return 1
	if platform == 'darwin':
		return 2


class client:
	def __init__(self, ip, server_os, port=24810):
		self.server_ip = ip
		self.server_port = port
		self.server_os = server_os
		self.local_OS = get_platform_code()

		self.server_socket = (ip, int(port))

	def start_client(self):
		print(f'[*] Connecting to server at {self.server_ip}:{self.server_port}')

		self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.client_socket.sendto("0x0000x0000".encode('utf-8'), self.server_socket)

		self.run_client()

	def run_client(self):
		keyboard.hook(self.key_dump)

		while True:
			(command, client)  = self.client_socket.recvfrom(1024)
			command = command.decode('utf-8')
			print(f'[*] Received: {command}')
			if command == '753677510005':
				self.close_client()
			self.type_input(command)

	def type_input(self, input):
		for key in input:
			keyboard.send(key, do_press=True, do_release=False)
			keyboard.send(key, do_press=False, do_release=True)
		keyboard.send('enter', do_press=True, do_release=False)
		keyboard.send('enter', do_press=False, do_release=True)

	def close_client(self):
		keyboard.stash_state()
		keyboard.unhook(self.key_dump)
		print('[-] SHUTTING DOWN')
		exit()

	def key_dump(self, key):
		pass

if __name__ == '__main__':
	try:
		Client = client(sys.argv[1], sys.argv[2])
		Client.start_client()
	except IndexError:
		print('OS CODES')
		print('Windows = 0')
		print('Linux = 1')
		print('MacOS =2')
