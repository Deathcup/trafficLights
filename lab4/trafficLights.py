import time
import random
from pyknow import *
import serial
exeTimes = 30  # time in second

serialPort = "COM3"  # 串口
baudRate = 9600  # 波特率
ser = serial.Serial(serialPort, baudRate, timeout=0.5)  # 连接串口
state = 0
we = 0
count = 0

class TrafficLights(KnowledgeEngine):

    # def __init__(self):
    #     self.serialPort = "COM3"  # 串口
    #     self.baudRate = 9600  # 波特率
    #     self.ser = serial.Serial(self.serialPort, self.baudRate, timeout=0.5)  # 连接串口
    #     self.demo0 = b"0"  # 将0转换为bytes类型的ASCII码方便发送
    #     self.demo1 = b"1"  # 同理

    @DefFacts()
    def _initial_action(self):
        yield Fact(Ticks = 0)
        yield Fact(Second = 0)
        yield Fact(ASecond = False)
        yield Fact(SwitchTime = 5)
        yield Fact(Period = 10)
        yield Fact(NSLight = 'GREEN')
        yield Fact(WELight = 'RED')
        yield Fact(NSCars = 0)
        yield Fact(WECars = 0)
    
    @Rule(AS.oldFact << Fact(Ticks = MATCH.times))
    def ticks(self,times,oldFact):
        self.retract(oldFact)
        self.declare(Fact(Ticks = times + 1))
        time.sleep(0.1)
        if times == exeTimes * 100:
            print('bye!')
            self.halt()
        else:
            if times%10 == 0:
                self.declare(Fact(ASecond = True))
            self.comm()

    @Rule(AS.fact1 << Fact(Second=MATCH.times),
          AS.fact2 << Fact(ASecond = True),
          salience= 1
    )
    def step(self,times,fact1,fact2):
        self.retract(fact1)
        self.retract(fact2)
        self.declare(Fact(Second= times + 1))
        print("{}-*-".format(times) )

    @Rule(AS.fact1 << Fact(Second=MATCH.times),
          Fact(Period = MATCH.period),
          TEST(lambda times,period: times == period),
          AS.fact2 << Fact(NSCars = MATCH.nsCars),
          AS.fact3 << Fact(WECars = MATCH.weCars),
          AS.fact4 << Fact(SwitchTime= MATCH.switchTime),
          salience = 2
         )
    def startSwitch1(self,fact1,fact2,fact3,fact4,nsCars,weCars,switchTime,period):
        self.retract(fact1)
        self.retract(fact2)
        self.retract(fact3)
        self.retract(fact4)
        self.decision(nsCars,weCars,switchTime,period)
        self.declare(Fact(Second = 0))
        self.declare(Fact(Switch = True))
        self.declare(Fact(NSCars = 0))
        self.declare(Fact(WECars = 0))



    
    @Rule(
          Fact(Second = MATCH.times),
          Fact(SwitchTime = MATCH.switchTime),
          TEST(lambda switchTime,times:times == switchTime),
          salience= 2
       )
    def startSwitch2(self):
        self.declare(Fact(Switch = True))
        
    @Rule(
        AS.oldSwtich << Fact(Switch = True),
        AS.oldNS << Fact(NSLight = 'RED'),
        AS.oldWE << Fact(WELight = 'GREEN'),
        salience = 2
      )
    def switch1(self,oldSwtich,oldNS,oldWE): 
        self.declare(Fact(NSLight = 'GREEN'))
        self.declare(Fact(WELight = 'RED'))
        self.retract(oldSwtich)
        self.retract(oldWE)
        self.retract(oldNS)
        global ser
        ser.write(b"1")
        ser.write(b"1")
        global we
        if we == 1:
            we = 0
        else:
            we = 1
        global count
        count = 0
        
    @Rule(
        AS.oldSwtich << Fact(Switch = True),
        AS.oldNS << Fact(NSLight = 'GREEN'),
        AS.oldWE << Fact(WELight = 'RED'),
        salience = 2
      )
    def switch2(self,oldSwtich,oldNS,oldWE):
        self.declare(Fact(NSLight = 'RED'))
        self.declare(Fact(WELight = 'GREEN'))
        self.retract(oldSwtich)
        self.retract(oldWE)
        self.retract(oldNS)
        global ser
        ser.write(b"1")
        ser.write(b"1")
        global we
        if we == 1:
            we = 0
        else:
            we = 1
        global count
        count = 0
        
    @Rule(
        Fact(NSLight = MATCH.NScolor),
        Fact(WELight = MATCH.WEcolor),
        salience = 2
      )
    def show(self,NScolor,WEcolor):
        #print('\n NS:WE={}:{} \n'.format(NScolor,WEcolor))
        if NScolor == 'RED':
            print('-X-  -V-')
        else:
            print('-V-  -X-')

    
    @Rule(
        AS.fact1 << Fact(NSSign = True),
        AS.fact2 << Fact(NSCars = MATCH.cars)
    )
    def countNS(self,fact1,fact2,cars):
        self.retract(fact1)
        self.retract(fact2)
        self.declare(Fact(NSCars = cars + 1 ))

    @Rule(
        AS.fact1 << Fact(WESign = True),
        AS.fact2 << Fact(WECars = MATCH.cars)
    )
    def countWE(self,fact1,fact2,cars):
        self.retract(fact1)
        self.retract(fact2)
        self.declare(Fact(WECars = cars + 1 ))

    def decision(self,nsCars,weCars,switchTime,period):
        if nsCars == 0:
            nsCars = 1
        if weCars == 0:
            weCars = 1
        newSwitchTime = int(nsCars/(nsCars+weCars)* period)
        if newSwitchTime == 0:
            newSwitchTime = 1
        if newSwitchTime == period:
            newSwitchTime = period -1

        print('nsCars ={} and weCars={},so we changed switch time from {} to {}'.format(nsCars,weCars,switchTime,newSwitchTime))
        self.declare(Fact(SwitchTime = newSwitchTime))

    def comm(self):
        global ser
        global state
        global we
        global count
        #print('debug')
        ser.flushInput()
        str = ser.read()  # 接收下位机上传的
        #print(we)
        #print(str)
        if str == b'1':
            if state == 0:
                state = 1
        else:
            if state == 1:
                state = 0
                count += 1
                print('通过{}辆车'.format(count))
                if we == 1:
                    self.declare(Fact(WESign=True))
                    #self.declare(Fact(NSSign = True))
                else:
                    self.declare(Fact(NSSign=True))
                    #self.declare(Fact(WESign=True))

        # if random.randint(0,5) == 0 :
        #     self.declare(Fact(NSSign = True))
        # if random.randint(0,5) == 0 :
        #     self.declare(Fact(WESign = True))

def main(args = None):
    engine =TrafficLights()
    engine.reset()  
    engine.run()  

if  __name__ == "__main__":
    main()