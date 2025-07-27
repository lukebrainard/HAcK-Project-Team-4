from connections import connect_mqtt, connect_internet
from machine import Pin, SoftI2C, time_pulse_us
import dht
import time
from ssd1306 import SSD1306_I2C

i2c = SoftI2C(scl=Pin(5), sda=Pin(4))

oled = SSD1306_I2C(128, 64, i2c)
# DHT11 sensor setup
sensor_pin = Pin(9, Pin.IN, Pin.PULL_UP)
dht_sensor = dht.DHT11(sensor_pin)
photoresistor = machine.ADC(26)


TRIGGER = Pin(16, Pin.OUT)
ECHO = Pin(17, Pin.IN)

SPEED_SOUND_CM_US = 0.034

lastMsg = ""
lastInfo = ""

def get_distance():
    TRIGGER.low()
    time.sleep_us(2)
    TRIGGER.high()
    time.sleep_us(10)
    TRIGGER.low()

    duration = time_pulse_us(ECHO, 1, 60000) 
    if duration < 0:
        return -1 
    distance = (duration * SPEED_SOUND_CM_US) / 2
    return distance

def cb(topic, msg):
    global lastMsg
    global lastInfo
    if topic == b"text":
        lastMsg = msg.decode()
    elif topic == b"data":
        lastInfo = msg.decode()
        

def main():
    try:
        connect_internet("HAcK-Project-WiFi-2",password="UCLA.HAcK.2024.Summer")
        client = connect_mqtt("5cb09e3e4832406fa9e58d96b387c192.s1.eu.hivemq.cloud", "LukeB", "Luke122604!?")
        client.set_callback(cb)
        client.subscribe("text")
        client.subscribe("data")
        while True: 
        # Read sensor
            
            dht_sensor.measure()
            client.check_msg()
            tempC = dht_sensor.temperature()  # Access as property, not method
            hum = dht_sensor.humidity()      # Access as property, not method
            tempF = (tempC*1.8)+32
            light_value = photoresistor.read_u16()
            volts = light_value * 3.3/65535
        
            lumens= (-1/3.3)*volts + 1
            lumensAdj = lumens
        
            if lumens > 0.97:
                lumensAdj = 1
            
            d = get_distance()
            # Print the values if the sensor is working
            # print("Temperature:", tempC, "C")
            # print("Temperature:", tempF, "F")
            # print("Humidity:", hum, "%")
            # print("Light Value", light_value)
            if d >= 0:
                print("Distance: " + "{:.2f}".format(d) + " cm")
            else:
                print("Out of Range")
                d = "Out of Range"
                
                
            oled.fill(0)
            
            client.publish("ultrasonic", str(d))
            client.publish("light", str(lumens))
            client.publish("temp", str(tempF))
            client.publish("humidity", str(hum))
            # oled.text(str(tempC) + "C" , 0, 0)
            # oled.text(str(tempF) +  "F", 0, 10)
            # oled.text(str(hum) + "%", 0, 20)
            # oled.text(str(lumens) + " Lumens", 0, 30)
            # oled.text(str(d) + " cm", 0, 40)
            oled.text(lastMsg, 0, 0)
            oled.text(lastData, 0, 10)
            oled.show()
            # Delay before the next read
            time.sleep(1)

    except KeyboardInterrupt:
        print('keyboard interrupt')
        
        
    
        
        
if __name__ == "__main__":
    main()



