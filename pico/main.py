from connections import connect_mqtt, connect_internet
from time import sleep

def cb(topic, msg):
    if topic == b"text":
        print(msg.decode())

def main():
    try:
        connect_internet("",password="")
        client = connect_mqtt("5cb09e3e4832406fa9e58d96b387c192.s1.eu.hivemq.cloud", "LukeB", "Luke122604!?")

        client.set_callback(cb)
        client.subscribe("text")

        counter=0
        while True:
            client.check_msg()
            sleep(0.1)
            counter+=1
            if (counter == 100):
                client.publish("message", "Hello from the pico!")
    except KeyboardInterrupt:
        print('keyboard interrupt')
        
        
if __name__ == "__main__":
    main()



