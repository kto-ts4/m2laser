import socket

def command(command, t_id, **parameters):
	msg = ''
	l = len(parameters)
	if l == 0:
		msg += f'{{"message":{{"transmission_id":[{t_id}],"op":"{command}"}}}}'
	else:
		keys = list(parameters.keys())
		str_param = '{'
		for j in range(l):
			key = keys[j]
			str_param += f'"{key}"'
			if type(parameters[key]) is str:
				str_param += f'"{parameters[key]}"'
			else:
				str_param += f'[{parameters[key]}]'

			if not j == l-1:
				str_param += ','
			else:
				str_param += '}'
		msg += f'{{"message":{{"transmission_id":[{t_id}],"op":"{command}","parameters":{str_param}}}}}'
		t_id += 1
	return msg

class Equipment:
	def __init__(self, ip, port):
		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.s.connect((ip, port))
		myip = self.s.getsockname()[0]
		init_msg = command("start_link", ip_address=myip)
		self.s.sendall(init_msg.encode())
		print(self.s.recv(1024))
		self.t_id = 0

class Solstis(Equipment):
	def __init__(self, ip, port):
		super().__init__(ip, port)

	def set_wavelength(self, wl):
		msg = command('move_wave_t',t_id=self.t_id, wavelength=wl)
		self.s.sendall(msg.encode())
		self.t_id += 1
		print(self.s.recv(1024))

	def etalon_lock(self, operation):
		if not (operation == 'on' or operation == 'off'):
			print('operation should be either "on" or "off"')
		else:
			msg = command('etalon_lock', operation=operation)
			self.s.sendall(msg.encode())
			self.t_id += 1
			print(self.s.recv(1024))

class Equinox(Equipment):
	def __init__(self, ip, port):
		super().__init__(ip, port)

	def laser_control(self, operation):
		if not (operation == 'start' or operation == 'stop'):
			print('operation should be either "start" or "stop"')
		else:
			msg = command('laser_control', operation=operation)
			self.s.sendall(msg.encode())
			self.t_id += 1
			print(self.s.recv((1024)))

	def set_power(self, power):
		msg = command('set_power', power=power)
		self.s.sendall(msg.encode())
		self.t_id += 1
		print(self.s.recv(1024))