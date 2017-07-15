from tornado.wsgi import WSGIContainer
from tornado.ioloop import IOLoop
from tornado.web import FallbackHandler, RequestHandler, Application
import tornado.websocket
import threading
import logging, time
import requests,json

from kafka import KafkaConsumer, KafkaProducer
import os,ast
from iothealthresources import *

subscribers=set()

class Producer(threading.Thread):
    daemon = True
    def run(self):
        producer = KafkaProducer(bootstrap_servers='localhost:9092')
        while True:
	    url = 'http://34.223.225.244:8080/heartratelive/webapi/heartrate?userId=20'
            resp = requests.get(url=url)
            if resp.status_code == 404:
                data = {"0","Server not Found"}
            else:
                data = json.loads(resp.text)
                producer.send('test-topic', b""+str(data))
            
            #time.sleep(5)

class Consumer(threading.Thread):
    daemon = True

    def run(self):
        try:
            consumer = KafkaConsumer(bootstrap_servers='localhost:9092',
                                 auto_offset_reset='earliest')
            consumer.subscribe(['test-topic'])
            
            for message in consumer:
                nb=ast.literal_eval(message.value)
                print("------------------------------------")
                print(nb['heartRate'])
                notificationUpdate['heartRate']=nb['heartRate']
                date, timeOfHeartRate = (nb['timestamp']).split()
                if nb['heartRate']=="":
                    obj1={"value": 0, "time": timeOfHeartRate}
                else:
                    obj1={"value": int(nb['heartRate']), "time": timeOfHeartRate}
                print("------------------------------------")
                if len(heartdata)>=450:
                    del heartdata[-1]
                heartdata.append(obj1)
                print(heartdata)
        except:
            print("error arrived!")

class WSocketHandler(tornado.websocket.WebSocketHandler): #Tornado Websocket Handler

    def check_origin(self, origin):
        return True

    def open(self):
        self.stream.set_nodelay(True)
        subscribers.add(self) #Join client to our league

    def on_close(self):
        if self in subscribers:
            subscribers.remove(self) #Remove client


tr = WSGIContainer(app)

application = Application([
(r'/ws', WSocketHandler), #For Sockets
(r".*", FallbackHandler, dict(fallback=tr)),
])

def pushNotifyFunction():
	try:
		for subscriber in subscribers:
                	subscriber.write_message(notificationUpdate)
	    		notificationUpdate['recommedation']=''
	    		notificationUpdate['calorieAvailable']=''
	    		notificationUpdate['calorieExceeds']=''
		threading.Timer(2, pushNotifyFunction).start()
    	except Exception as error : 
		    logging.exception("message")
def kafkaFunction():
    threads = [
        Producer(),
        Consumer()
    ]
    try:
        for t in threads:
            t.start()

        #time.sleep(50)
    finally:
            os.system('kafka-topics.sh --delete --zookeeper localhost:2181 --topic test-topic')

if __name__ == "__main__":
  application.listen(3000, address='0.0.0.0')
  print("Server Started...........")
  logging.basicConfig(
        format='%(asctime)s.%(msecs)s:%(name)s:%(thread)d:%(levelname)s:%(process)d:%(message)s',
        level=logging.INFO
        )
  #kafkaFunction()
  IOLoop.current().add_callback(pushNotifyFunction)
  IOLoop.instance().start()
 

