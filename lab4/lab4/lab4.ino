int R1= 13; //定义东西向红灯
int Y1= 12; //定义东西向黄灯
int G1= 11; //定义东西向绿灯
int R2= 6; //定义南北向红灯
int Y2= 5; //定义南北向黄灯
int G2= 4; //定义南北向绿灯
int state = 0;
int count = 0;
int buttonpin = 3; //定义避障传感器接口
int val; //定义避障传感器接口的数字变量val
char chr; //定义上位机的输入字符信号
void setup()
{
pinMode(R1, OUTPUT); //定义LED 为输出接口
pinMode(Y1, OUTPUT); //定义LED 为输出接口
pinMode(G1, OUTPUT); //定义LED 为输出接口
pinMode(R2, OUTPUT); //定义LED 为输出接口
pinMode(Y2, OUTPUT); //定义LED 为输出接口
pinMode(G2, OUTPUT); //定义LED 为输出接口
pinMode(buttonpin, INPUT); //定义避障传感器为输出接口
Serial.begin(9600); //连接上位机，波特率为960
digitalWrite(R1, LOW);
digitalWrite(Y1, LOW);
digitalWrite(G1, LOW);
digitalWrite(R2, LOW);
digitalWrite(Y2, LOW);
digitalWrite(G2, LOW);
}
void loop()
{
// 接收传感器信号然后发送给上位机
val = digitalRead(buttonpin); //将数字接口3的值读取赋给val
if (val == LOW) //当避障传感器检测低电平时，有障碍物，传输YES
{
Serial.print(B1);
}
else
{
Serial.print(B0);
}
// 接收上位机信号控制小灯开关
chr = Serial.read();
if (chr == '1') //当避障传感器检测低电平时，LED 灭
{
if(state == 0)
{
state = 1;
}
else if (state == 1)
{
state = 2;
}
else if (state == 2)
{
state = 3;
}
else
{
state = 0;
}
}
else
{
state = state;
}
if (state == 0)
{
digitalWrite(R1, HIGH);
digitalWrite(Y1, LOW);
digitalWrite(G1, LOW);
digitalWrite(R2, LOW);
digitalWrite(Y2, LOW);
digitalWrite(G2, HIGH);
}
else if (state == 2)
{
digitalWrite(R1, LOW);
digitalWrite(Y1, LOW);
digitalWrite(G1, HIGH);
digitalWrite(R2, HIGH);
digitalWrite(Y2, LOW);
digitalWrite(G2, LOW);

}
else
{
digitalWrite(R1, LOW);
digitalWrite(Y1, HIGH);
digitalWrite(G1, LOW);
digitalWrite(R2, LOW);
digitalWrite(Y2, HIGH);
digitalWrite(G2, LOW);
delay(500);
}
}

