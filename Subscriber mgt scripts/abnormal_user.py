from jnpr.junos import Device
import multiprocessing
import getpass
from pprint import pprint
import csv
junos_username = input("Junos OS username: ")
junos_password = getpass.getpass("Junos OS password: ")

hosts=('R1', 'R2', 'R3', 'R4')
outPut = open('Collected_info.txt', 'w')                                    
def Src2Session(hostname, junos_username, junos_password):                      # Функция считывает инфо аналог "show ddos-protection protocols violations" "
	dev = Device(host=hostname, user=junos_username, passwd=junos_password)
	dev.open()
	src = dev.rpc.get_dhcp_server_binding_information()                         
	for i in src.findall('.//dhcp-binding'):	                                # Цикл по каждой строчке xml
		try:
			DataToFile = []  				 									# Лист с данными об устройстве								
			mac = i.xpath('./mac-address')[0].text  							# МАС адрес получателя IP
			address= i.xpath('./allocated-address')[0].text                   	# IP адрес																					
			interface = i.xpath('./interface-name')[0].text         			# Интерфейс откуда пришел запрос на получение адреса
			DataToFile.append(mac.strip())                                      # Интерфейс откуда пришел запрос на получение адреса
			DataToFile.append(address.strip())                                  # добавление данных в лист  
			DataToFile.append(interface.strip())	                              
			DataToFile = '#'.join(DataToFile)	                                  
			outPut.write(DataToFile+'\n')	                                    # Запись данных на файл
		except:
			print('ERORR!!!!')
	dev.close()

for hostname in hosts:
	Src2Session(hostname, junos_username, junos_password)
