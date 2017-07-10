import paho.mqtt.client as mqtt

def on_connect(client,userdata,flags,rc): 
	print("Connected with result code"+" "+str(rc))
	client.subscribe("topic/test")

def on_message(client,userdata,message):
	print(str(message.payload))
	
  
    
client = mqtt.Client()
client.on_message = on_message
client.on_connect = on_connect
client.connect("localhost",1883)
client.loop_forever()

