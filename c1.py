import serial  # 引用pySerial模組

COM_PORT = 'COM9'	# 指定通訊埠
BAUD_RATES = 115200	# 設定baud rate
ser = serial.Serial(COM_PORT, BAUD_RATES)   # 初始化序列通訊埠
fp = open("c1.txt", "r+")
fp.truncate()

try:
	while True:
		while ser.in_waiting:		  # 若收到序列資料
			data_raw = ser.readline()  # 讀取一行
			try:
				data = data_raw.decode().strip()   # UTF-8解碼
				#print('接收到的原始資料：', data_raw)
				print('UART資料：', data)
				fp.write(data)
				fp.write('\n')
			except:
				print('UART資料(含錯誤訊息)：', data)

except:
	ser.close()	# 清除序列通訊物件
	fp.close()
	print('再見！')