from connections import connect_mqtt, connect_internet
import dht
import time
from machine import Pin, SoftI2C
from ssd1306 import SSD1306_I2C

i2c = SoftI2C(scl=Pin(5), sda=Pin(4))

oled = SSD1306_I2C(128, 64, i2c)
# DHT11 sensor setup
sensor_pin = Pin(9, Pin.IN, Pin.PULL_UP)
dht_sensor = dht.DHT11(sensor_pin)
photoresistor = machine.ADC(26)

#def cb(topic, msg):
#    oled.fill(0)
#    if topic == b"text":
#        lastText = msg.decode()
#        print(msg.decode())
#    elif topic == b"tempratureBack"
#        lastTemp = msg.decode()
#    elif topic == b"humidityBack"
#        lasthumidity = msg.decode()
#    oled.text(lastText, 0, 0)
#    oled.text(lastTemp, 10, 0)
#    oled.text(lasthumidity, 20, 0)
#    oled.show()


    
        

def main():
    try:
        connect_internet("HAcK-Project-WiFi-2",password="UCLA.HAcK.2024.Summer")
        client = connect_mqtt("5cb09e3e4832406fa9e58d96b387c192.s1.eu.hivemq.cloud", "LukeB", "Luke122604!?")
        while True: 
        # Read sensor
            
            dht_sensor.measure()
            tempC = dht_sensor.temperature()  # Access as property, not method
            hum = dht_sensor.humidity()      # Access as property, not method
            tempF = (tempC*1.8)+32
            light_value = photoresistor.read_u16()
            volts = light_value * 3.3/65535
        
            lumens= (-1/3.3)*volts + 1
            lumensAdj = lumens
        
            if lumens > 0.97:
                lumensAdj = 1
        
        # Print the values if the sensor is working
            print("Temperature:", tempC, "C")
            print("Temperature:", tempF, "F")
            print("Humidity:", hum, "%")
            print("Light Value", light_value)
            client.publish("light", str(lumens))
            client.publish("temp", str(tempF))
            client.publish("humidity", str(hum))
            oled.fill(0)
            oled.text(str(tempC) + "C" , 0, 0)
            oled.text(str(tempF) +  "F", 0, 10)
            oled.text(str(hum) + "%", 0, 20)
            oled.text(str(lumens) + " Lumens", 0, 30)
            oled.show()
            # Delay before the next read
            time.sleep(1)

    except KeyboardInterrupt:
        print('keyboard interrupt')
        
        
    
        
        
if __name__ == "__main__":
    main()



