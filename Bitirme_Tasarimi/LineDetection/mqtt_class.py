import paho.mqtt.client as paho_mqtt
class mqtt:
    __sub_topic = []
    __client=paho_mqtt.Client()
    __message=None
    def __init__(self,broker="localhost",port=1883,keepalive=120):
        self.host=broker
        self.port=port
        self.keepalive=keepalive
        self.__client.on_connect=self.__on_connect
        self.__client.on_message=self.__on_message
        self.__client.on_publish=self.__on_publish

    def add_topic(self,topic_name,qos=0):
        self.__sub_topic.append((topic_name,qos))

    def print_subtopics(self):
        print(self.__sub_topic)

    def connect(self,username="",password=""):
        self.username=username
        self.password=password
        self.__client.username_pw_set(self.username, password)
        self.__client.connect(self.host, self.port, self.keepalive)
        self.__client.subscribe(self.__sub_topic)
        self.__client.loop_start()

    def __on_connect(self,client, userdata, layoutFlags, rc):
        if rc == 0:
            print("Connected to Broker")
        else:
            print("Broker Connection is failed ")

    def publish(self,topic,message):
        self.__client.publish(topic,message)


    def __on_message(self,client, userdata, message):
        self.__message=message
        
    def __on_publish(self,client, userdata, mid):
        print("Mesaj gönderildi")

    def addsubscribefunc(self,function):
        self.__client.on_message=function

    def get_message(self):
        if self.__message == None:
            return
        else:
            payload=self.__message
            self.__message=None
            return payload