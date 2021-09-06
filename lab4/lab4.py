import serial

serialPort = "COM3"  # 串口
baudRate = 9600  # 波特率
ser = serial.Serial(serialPort, baudRate, timeout=0.5) # 连接串口
print("参数设置：串口=%s ，波特率=%d" % (serialPort, baudRate))

demo0 = b"0"  # 将0转换为bytes类型的ASCII码方便发送
demo1 = b"1"  # 同理
count = 0     #计数

# demo0 = 0b0
# demo1 = 0b1
state = 0
while 1:
    ser.flushInput()
    str = ser.read() # 接收下位机上传的
    #print(str)
    if str == b'1':
        if state == 0:
            state = 1
    else:
        if  state == 1:
            state = 0
            count += 1
            print(count)
            if count%10 == 0:
                ser.write(demo1)
                ser.write(demo1)
    # print("是否有障碍物",str)
    # x = int(input("请输入0 or 1："))
    # if(x == 1):
    #     ser.write(demo1) # 发送字节1
    # else:
    #     ser.write(demo0) # 发送字节0

ser.close()
