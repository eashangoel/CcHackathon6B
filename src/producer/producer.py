# import required libraries
import pika
import os
from flask import Flask
from flask import request

# Array to store new consumer
consumer_list = []

# read rabbitmq connection url from environment variable
amqp_url = os.environ['AMQP_URL']
url_params = pika.URLParameters(amqp_url)

# connect to rabbitmq
connection = pika.BlockingConnection(url_params)
chan = connection.channel()

# initialise queues
chan.queue_declare(queue='ride_match', durable=True)
chan.queue_declare(queue='database', durable=True)

# initialise app
app = Flask(__name__)


@app.route('/')
def hello():
    return "HELLO"

# ride matching 
@app.route('/new-ride', methods = ['POST'])
def new_ride():
    data = dict(request.args)
    time = str(data['time'])
    print("GOT DATA",data)

    chan.basic_publish(
        routing_key = 'ride_match', 
        body = time,
        exchange='',

    )
    chan.basic_publish(
        routing_key = 'database', 
        body = str(data),
        exchange='',

    )
    return "Success"

@app.route('/new_ride_matching_consumer')
def ride_matching():
    print(request.data)
    consumer_id = request.data.consumer_id
    consumer_ip = request.remote_addr
    consumer_list.append({
        "name": consumer_id,
        "ip": consumer_ip,
    })


print("Starting server")
app.run(port=5005, host='0.0.0.0')






