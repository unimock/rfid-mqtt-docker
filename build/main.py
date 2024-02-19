import serial
import sys
import time
import signal
import random
import json
import os
#import syslog

from paho.mqtt import client as mqtt_client

rfidd_device = os.environ['DEVICE']
broker = os.environ['MQTT_NODE']
port =   int(os.environ['MQTT_PORT'])
topic =  os.environ['MQTT_TOPIC']
# Generate a Client ID with the publish prefix.
client_id = f'publish-{random.randint(0, 1000)}'
# username = 'emqx'
# password = 'public'
def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)
    client = mqtt_client.Client(client_id)
    # client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client
def publish(client, msg):
    result = client.publish(topic, msg)
    # result: [0, 1]
    status = result[0]
    if status == 0:
      print(f"Send `{msg}` to topic `{topic}`")
    else:
      print(f"Failed to send message to topic {topic}")

class GracefulKiller:
  kill_now = False
  signals = {
    signal.SIGINT: 'SIGINT',
    signal.SIGTERM: 'SIGTERM'
  }
  def __init__(self):
    signal.signal(signal.SIGINT, self.exit_gracefully)
    signal.signal(signal.SIGTERM, self.exit_gracefully)
  def exit_gracefully(self, signum, frame):
    print("\nReceived {} signal".format(self.signals[signum]))
    print("Cleaning up resources. End of the program")
    client.loop_stop()
    UART.close()
    #syslog.closelog()
    self.kill_now = True
    exit(0)

if __name__ == '__main__':
  killer = GracefulKiller()
  ID = ""
  Zeichen = 0
  Startflag = b'\x02'
  Endflag = b'\x03'
  UART = serial.Serial(
    port="%s" % rfidd_device,
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS
  )
  UART.isOpen()
  client = connect_mqtt()
  client.loop_start()
  # Kontinuierliches Lesen von Lesekopf einschalten
  #s='\x02'
  #s=s+"N1"
  #s=s+'\x04'
  #UART.write(s)
  while not killer.kill_now: # bringt hier nichts, da prg in read steckt
    ID = ""
    Zeichen = UART.read()
    #print ("Zeichen= " , str(Zeichen) )
    if Zeichen == Startflag:
      for Counter in range(13):
        Zeichen = UART.read() 
        ID = ID + Zeichen.decode("utf-8")
      #Endflag = Endflag.decode("utf-8")
      #ID = ID.replace(Endflag, "" );
      #print ("ID: ", ID[1:11])
      publish(client, ID[1:11])
      #syslog.syslog("detect rfid-id:")"



