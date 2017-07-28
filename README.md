# nus_serverless
# Project Title

Serverless IOT Platform using OPENWHISK and MQTT

## Getting Started

* Native Deployment of Openwhisk in Ubuntu 14.04
* Persistant Couch DB (for storage)
* Paho MQTT python 
* Node-Red 

### Installing Prerequisites

* Native Deployment of Openwhisk in Ubuntu 14.04

Download openwhisk from [here] (https://github.com/apache/incubator-openwhisk) and follow the instructions below for successful deployment or clone the repository using the below commands

```
# Install git if it is not installed
sudo apt-get install git -y
git clone https://github.com/apache/incubator-openwhisk
```
After downloading openwhisk run the following commands to install the pre-requsite tools required for installation of openwhisk 
```
# Change current directory to <openwhisk_home>
cd <openwhisk_home>

# Install all required software
cd tools/ubuntu-setup  //this is considering an Ubunutu operating system, for other operating system choose the setup file as required
sudo ./all.sh  // all.sh consists of a combined, pre-written set of installation commands required for installing different modules

```

* Persistent Couch DB - for storage 

This step needs to be done only once per development environment. It will generate configuration files based on  local settings which can be set up by following the below instructions.

```
# Install Couch DB if it is not installed
sudo apt-get install software-properties-common -y
sudo add-apt-repository ppa:couchdb/stable -y
sudo apt-get update
sudo apt-get install couchdb -y

```
To setup Couch DB for Openwhisk. 

```
# These env variables can also altered manually at db_local.ini file

export OW_DB=CouchDB
export OW_DB_USERNAME=<your couchdb user>
export OW_DB_PASSWORD=<your couchdb password>
export OW_DB_PROTOCOL=<your couchdb protocol> (http is most commonly used)
export OW_DB_HOST=<your couchdb host> 
export OW_DB_PORT=<your couchdb port> (5984 is most commonly used)

```

To deploy all the containers to support Openwhisk

```

cd ansible
sudo ansible-playbook -i environments/local setup.yml   //Initial setup
sudo ansible-playbook -i environments/local prereq.yml  //Pre-requisite for the containers


# Install Gradle if it is not installed 
sudo add-apt-repository ppa:cwchien/gradle
sudo apt-get update
sudo apt-get install gradle
```
Build openwhisk using gradle

```
cd <openwhisk_home>
sudo ./gradlew distDocker 

```
Setup the remaining containers

```
cd ansible
sudo ansible-playbook -i environments/local couchdb.yml
sudo ansible-playbook -i environments/local initdb.yml
sudo ansible-playbook -i environments/local wipe.yml
sudo ansible-playbook -i environments/local apigateway.yml
sudo ansible-playbook -i environments/local openwhisk.yml
sudo ansible-playbook -i environments/local postdeploy.yml

```

## Testing the deployment

```
#To check whether all the containers is running 
docker ps
```

The result should look like this:

```
|CONTAINER ID  |IMAGE                        |COMMAND                    |CREATED              | STATUS            |   PORTS,NAMES                             

| ------------ | --------------------------- |---------------------------| ------------------- |------------------ | --------------------------------------                                    |                                                                             
|87a6405b714e  |   whisk/dispatcher:latest   | "/startDispatcher.sh "    |  4 minutes ago      |   Up 4 minutes    |   0.0.0.0:12001->8080/tcp,invoker0                                          |                                                                                            
|cf1f1d0ed79a  |   whisk/loadbalancer:latest | "/startLoadBalancer.s"    |  4 minutes ago      |   Up 4 minutes    |   0.0.0.0:10003->8080/tcp,loadbalancer                                      |                                                                                              
|cfd15f5e26e3  |   whisk/dispatcher:latest   | "/startDispatcher.sh "    |  4 minutes ago      |   Up 4 minutes    |    0.0.0.0:12000->8080/tcp,activator                                         |                                                                                       
|cfd15f5e26e3  |   whisk/dispatcher:latest   | "/startDispatcher.sh "    |  4 minutes ago      |   Up 4 minutes    |   0.0.0.0:12000->8080/tcp,activator                                         |                                                                                       
|c5e96cc52cb1  |   whisk/controller:latest   |  "/startController.sh"    |  4 minutes ago      |   Up 4 minutes    |  0.0.0.0:10001->8080/tcp,controller                                        |                                                                                            
|e7d9ad87eeae  |   gliderlabs/registrator    |  "/bin/registrator -ip"   |  4 minutes ago	     |   Up 4 minutes 	 | tcp,                                                                                                                         0.0.0.0:8600->53/tcp,consulserver                                         |                                                                                                                 																													
|f85bf6923075  |   whisk/consul:latest       | "/startconsulserver.s"    |  4 minutes ago      |   Up 4 minutes    | 8000/tcp,      53/udp, 8080/tcp,8301-8302/ tcp, 8301-8302/udp, 8400/ 0.0.0.0:8500->8500  |                                                                                                                      	                                                                                                                        

|6298c63f8a03  |   whisk/kafka:latest        |  "/start.sh"              |  5 minutes ago      |   Up 5 minutes    | 7203/tcp, 0.0.0.0:9092->9092/tcp, 	                                                                                                                         0.0.0.0:9093->8080/tcp,kafka                                               |                                                                
|5ef6a2fcff67  |   whisk/zookeeper:latest    | "/opt/zookeeper/bin/z"    |  5 minutes ago      |   Up 5 minutes    | 2888/tcp, 3888/tcp, 8080/tcp,0.0.0.0:2181->2181/tcp,zookeeper                        |                                                                                                                                                                                            
|212271a5a939  |   nginx                     | "nginx -g 'daemon off"    |  5 minutes ago      |   Up 5 minutes    |   0.0.0.0:80->80/tcp, 0.0.0.0:443->443/tcp, 0.0.0.0:8443->8443/tcp,nginx     |                                                                                                                       
```
 

```
# To check openwhisk is working fine

cd <openwhisk-home>/bin
./wsk 

```

The result should look like this:

```       ____      ___                   _    _ _     _     _
       /\   \    / _ \ _ __   ___ _ __ | |  | | |__ (_)___| | __
  /\  /__\   \  | | | | '_ \ / _ \ '_ \| |  | | '_ \| / __| |/ /
 /  \____ \  /  | |_| | |_) |  __/ | | | |/\| | | | | \__ \   <
 \   \  /  \/    \___/| .__/ \___|_| |_|__/\__|_| |_|_|___/_|\_\
  \___\/ tm           |_|

Usage:
  wsk [command]

Available Commands:
  action           work with actions
  activation       work with activations
  package          work with packages
  rule             work with rules
  trigger          work with triggers
  sdk              work with the sdk
  property         work with whisk properties
  namespace        work with namespaces
  list             list entities in the current namespace
  api-experimental work with APIs (experimental)
  api              work with APIs

Flags:
      --apihost HOST         whisk API HOST
      --apiversion VERSION   whisk API VERSION
  -u, --auth KEY             authorization KEY
  -d, --debug                debug level output
  -h, --help                 help for wsk
  -i, --insecure             bypass certificate checking
  -v, --verbose              verbose output

Use "wsk [command] --help" for more information about a command.

```
Setting up of API host, namespace and auth token

```
cd <openwhisk-home>/bin
./wsk -i set property --apihost <host-ip>             // if its the same PC take IP address from <openwhisk-home>/ansible/environments/local
./wsk -i set property --auth <auth-token>            //  auth-token for the local namespace (whisk.system) will be available at <openwhisk-home>/ansible/files/auth.whisk.system

```
Make sure you get 'ok' messages after setting each property to proceed sucessfully

                                                   ```
## Creating web-actions which sends a message 

```
cd <openwhisk-home>/bin

```

Create a javascript file (<name>.js) inside the folder contains the intended message in the message payload

```
function main() 
{
    return {payload: '<message>'};
}

``` 

 Making the abpve javascript file as an action
 
```

./wsk -i action create <name of action> <name>.js --webtrue

```
 
 The result will look like:
```
 ok: created action <name of action>
```

```

 ./wsk -i action list

```

 The result should show list of actions in your system including the newly created one.


```
# Testing the action

./wsk -i invoke <name of action>

```

The result should look like:

```

{
"payload": "<message>"
}

```
 For more details regarding the operations with actions, refer here (https://github.com/apache/incubator-openwhisk/blob/master/docs/actions.md)

```
# Creating the API

./wsk -i api create <path> get <name of action> --response-type json

```
The result will look like:

```
ok: created API <path> GET for action /_/<name of action>
<api-url>     // something like " https://${APIHOST}:9001/api/21ef035/hello/world " will show up                 

```
```
# Testing the web-action

$ curl <api-url>

```
The result will look like:

```
{
"payload": "<message>"
}

```
## Paho MQTT python

```
# Installation

sudo pip install paho-mqtt

```

Subscriber and Publisher codes are available in subscribe.py and publish.py respectively.

### To setup local MQTT broker 

Login as root and change directory to where you want to download and install HiveMQ. By default  /opt.

```
cd /opt

```

Get the evaluation download here (http://www.hivemq.com/downloads/)
Copy the provided download link and download HiveMQ


Extract the files

```
unzip hivemq-<version>.zip
```

Create hivemq symlink
```
ln -s /opt/hivemq-<version> /opt/hivemq
```
Create HiveMQ user

```
useradd -d /opt/hivemq hivemq
```
Make scripts executable and change owner to hivemq user

```
chown -R hivemq:hivemq /opt/hivemq-<version>
chown -R hivemq:hivemq /opt/hivemq
cd /opt/hivemq
chmod +x ./bin/run.sh
```
Set up the configuration

```
cd /opt/hivemq/conf/examples/configuration

```

* Choose the appropriate setup file from the folder (by default use "config-sample-mqtt.xml")
* Copy the contents to the file to /opt/hivemq/conf/conf.xml
* Generally the conf.xml should look like this:

```
<?xml version="1.0"?>
<hivemq xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:noNamespaceSchemaLocation="hivemq-config.xsd">
    <listeners>
        <tcp-listener>
            <port>1883</port>
            <bind-address>0.0.0.0</bind-address>
        </tcp-listener>
    </listeners>
    <mqtt>
        <max-client-id-length>65535</max-client-id-length>
        <retry-interval>10</retry-interval>
    </mqtt>
    <throttling>
        <max-connections>-1</max-connections>
        <max-message-size>268435456</max-message-size>
        <outgoing-limit>0</outgoing-limit>
        <incoming-limit>0</incoming-limit>
  <mqtt>
        <max-client-id-length>65535</max-client-id-length>
        <retry-interval>10</retry-interval>
    </mqtt>
    <throttling>
        <max-connections>-1</max-connections>
        <max-message-size>268435456</max-message-size>
        <outgoing-limit>0</outgoing-limit>
        <incoming-limit>0</incoming-limit>
    </throttling>
    <general>
        <update-check-enabled>true</update-check-enabled>
    </general>

</hivemq>
```


Starting Hive-MQ after installation and change directory to HiveMQ directory

```
cd /opt/hivemq/bin

```
Execute startup script

```
sudo ./run.sh

```
The running Hive-MQ broker looks like this:

```

-------------------------------------------------------------------------

                  _    _  _              __  __   ____
                 | |  | |(_)            |  \/  | / __ \ 
                 | |__| | _ __   __ ___ | \  / || |  | |
                 |  __  || |\ \ / // _ \| |\/| || |  | |
                 | |  | || | \ V /|  __/| |  | || |__| |
                 |_|  |_||_|  \_/  \___||_|  |_| \___\_\

-------------------------------------------------------------------------

  HiveMQ Start Script for Linux/Unix v1.5

-------------------------------------------------------------------------

  HIVEMQ_HOME: /opt/hivemq-3.2.4

  JAVA_OPTS:  -Djava.net.preferIPv4Stack=true -XX:-UseSplitVerifier -noverify -Djava.security.egd=file:/dev/./urandom -XX:OnOutOfMemoryError='kill -9 %p' -XX:+HeapDumpOnOutOfMemoryError -XX:HeapDumpPath=/opt/hivemq-3.2.4/heap-dump.hprof

-------------------------------------------------------------------------

Java HotSpot(TM) 64-Bit Server VM warning: ignoring option UseSplitVerifier; support was removed in 8.0
2017-07-10 03:11:09,670 INFO  - Starting HiveMQ Server
2017-07-10 03:11:09,692 INFO  - HiveMQ version: 3.2.4
2017-07-10 03:11:09,692 INFO  - HiveMQ home directory: /opt/hivemq-3.2.4
2017-07-10 03:11:09,735 INFO  - Log Configuration was overridden by /opt/hivemq-3.2.4/conf/logback.xml
2017-07-10 03:11:32,640 INFO  - Loaded Plugin HiveMQ JVM Metrics Plugin - v3.1.0
2017-07-10 03:11:32,641 INFO  - Loaded Plugin HiveMQ MQTT Message Log Plugin - v3.0.0
2017-07-10 03:11:32,641 INFO  - Loaded Plugin HiveMQ JMX Metrics Reporting Plugin - v3.0.0
2017-07-10 03:11:32,711 INFO  - JMX Metrics Reporting started.
2017-07-10 03:11:32,755 INFO  - Starting TCP listener on address 0.0.0.0 and port 1883
2017-07-10 03:11:32,813 INFO  - Started TCP Listener on address 0.0.0.0 and on port 1883
2017-07-10 03:11:32,814 INFO  - Started HiveMQ in 23157ms
2017-07-10 03:11:32,829 INFO  - No valid license file found. Using evaluation license, restricted to 25 connections.

```

## Node-Red - Browser UI for configuring the flow

Installation

```
sudo apt-get install npm
sudo npm install node-red
```
Starting Node-Red

```
node-red  

```
The result will look similar to this:

```
Welcome to Node-RED
===================

6 Jul 08:33:29 - [info] Node-RED version: v0.16.2
6 Jul 08:33:29 - [info] Node.js  version: v7.10.0
6 Jul 08:33:29 - [info] Linux 3.19.0-25-generic x64 LE
6 Jul 08:33:31 - [info] Loading palette nodes
6 Jul 08:33:39 - [warn] nodes/core/io/lib/mqtt.js is deprecated and will be removed in a future release of Node-RED. Please report this usage to the Node-RED mailing list.
6 Jul 08:33:39 - [warn] nodes/core/io/lib/mqttConnectionPool.js is deprecated and will be removed in a future release of Node-RED. Please report this usage to the Node-RED mailing list.
6 Jul 08:33:41 - [info] Dashboard version 2.3.10 started at /ui
6 Jul 08:33:48 - [warn] ------------------------------------------------------
6 Jul 08:33:48 - [warn] [rpi-gpio] Info : Ignoring Raspberry Pi specific node
6 Jul 08:33:48 - [warn] ------------------------------------------------------
6 Jul 08:33:48 - [info] Starting flows
6 Jul 08:33:48 - [info] Started flows
6 Jul 08:33:48 - [info] Server now running at http://127.0.0.1:1880/

```

Now view Node-Red UI in any Internet Browser at http://127.0.0.1:1880/ or localhost:1880/

For installation of extra nodes you have to select Manage Palette from the menu (top right), and then select the install tab in the palette. You can now search for new nodes to install, and enable and disable existing nodes.



## Authors


## License


