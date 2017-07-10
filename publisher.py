import paho.mqtt.client as mqtt

# This is the Publisher

def on_connect(client,userdata,flags,rc): 
	print("Connected with result code"+" "+str(rc))
	client.publish("topic/test","hi",0,True)

client = mqtt.Client()
client.on_connect = on_connect
client.connect("localhost",1883)
client.loop_forever()

