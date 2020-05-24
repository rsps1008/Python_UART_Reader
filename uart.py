#格式   P封包id,   RSSI,	clent端id
#	   packet[0] packet[1] packet[2] 

import serial  # 引用pySerial模組
import MySQLdb
from colorama import Fore, Back, Style

#SQL初始化
db = MySQLdb.connect("127.0.0.1","root","","cc1350")
cursor = db.cursor()
cursor.execute('DELETE FROM `1c00`')
cursor.execute('DELETE FROM `5884`')
db.commit()
fp = open("s.log", "w")
fp.truncate()

#PySerial初始化
COM_PORT = 'COM8'	# 指定通訊埠名稱
BAUD_RATES = 115200	# 設定傳輸速率
ser = serial.Serial(COM_PORT, BAUD_RATES)   # 初始化序列通訊埠
 
try:
	while True:
		while ser.in_waiting:	   # 若收到序列資料…
			data_raw = ser.readline()  # 讀取一行
			data = data_raw.decode().strip()   # 用預設的UTF-8解碼
			print(Fore.RED + 'logging:', data)
			fp.write(data+'\n');
			try:
				packet = data.split(';');
				#驗證資料封包
				if packet[1][0] == "P":
					#選擇相對應資料庫
					if packet[3]=="fd00::212:4b00:d2e:1c00":
						print("---已新增至資料庫1c00: ", packet[1]); #fp.write("已新增至資料庫1c00:", packet[1], "\n");
						commandline = "INSERT INTO `1c00`(`data`,`rssi`) VALUES (" + packet[1][1:] +','+ packet[2] + ")"
						cursor.execute(commandline); db.commit();
						
					elif packet[3]=="fd00::212:4b00:d2e:5884":
						print("---已新增至資料庫5884:" , packet[1]); #fp.write("已新增至資料庫5884:", packet[1], "\n");
						commandline = "INSERT INTO `5884`(`data`,`rssi`) VALUES (" + packet[1][1:] +','+ packet[2] + ")"
						cursor.execute(commandline); db.commit(); 
						
					else:
						print(packet[3])
						print("沒此指裝置對應的資料庫")

				#錯誤封包
				else:
					print("非訊息封包:",data)

			#封包包含不法字元
			except:
				pass;
				

 
except KeyboardInterrupt:
	ser.close() # 清除序列通訊物件
	fp.close()
	print('結束！')