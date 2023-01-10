from netmiko import ConnectHandler
import pandas as pd
import progressbar
from datetime import datetime

def parsePing (variable):
    # Parsing выводы обычного пинга 
    intSearchStart = variable.find('packet loss')
    Pkt_lss=variable[intSearchStart-8:intSearchStart].strip()
    return (Pkt_lss)


# Открываем файл со списком eNodeB
f = open('eNodeB_list_IN.txt', 'r')
content = f.read().strip()
f.close
#Создание начальной Dict для заполнение результатов
Datatofile={'eNodb':[],'IP_eNodb':[],'Packet_loss':[]}
#Маршрутизатор откуда будет пинг до всех Базовых станции
Device_IP='10.15.x.x'#Router IP address 

USER = "username"
PASSWORD = "passwd"
DEVICE_PARAMS = {'device_type': 'huawei','ip': Device_IP, 'username': USER,'password': PASSWORD}
ssh = ConnectHandler( **DEVICE_PARAMS)
bar = progressbar.ProgressBar(maxval=len(content.split("\n"))).start()
i=0
print(datetime.now())
for row in content.split("\n"):
    eNodeB_Name = row.split(",")[0]
    eNodeB_IP = row.split(",")[1]
    Datatofile['eNodb'].append(eNodeB_Name)
    Datatofile['IP_eNodb'].append(eNodeB_IP)    
    # Sys name
    SSH_Command=parsePing(ssh.send_command(f'ping -i LoopBack 1000 -vpn-instance vpn-s1u -c 2 -m 10 {eNodeB_IP}'))
    Datatofile['Packet_loss'].append (SSH_Command)
    i+=1
    bar.update(i)
    print()
    print(eNodeB_Name+'--'+eNodeB_IP+'--'+SSH_Command)
ssh.disconnect()
# Create a Pandas dataframe from some data.
print()
print(datetime.now())
df = pd.DataFrame(Datatofile)

# Create a Pandas Excel writer using XlsxWriter as the engine.
writer = pd.ExcelWriter('Result_OUT.xlsx', engine='xlsxwriter')

# Convert the dataframe to an XlsxWriter Excel object.
df.to_excel(writer, sheet_name='Sheet1')

# Close the Pandas Excel writer and output the Excel file.
writer.save()