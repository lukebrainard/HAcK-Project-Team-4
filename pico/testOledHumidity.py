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

 
# Web server loop
while True: 
    try:
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
        oled.fill(0)
        oled.text(str(tempC) + "C" , 0, 0)
        oled.text(str(tempF) +  "F", 0, 10)
        oled.text(str(hum) + "%", 0, 20)
        oled.text(str(lumens) + " Lumens", 0, 30)
        oled.show()
    except Exception as e:
        # Print an error message if there's an issue with the sensor
        print("Failed to read from the sensor:", str(e))
 
    # Delay before the next read
    time.sleep(1)


