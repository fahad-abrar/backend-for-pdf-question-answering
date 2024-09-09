from flask import Flask, request, jsonify
from model import Question_and_Answer
from consumer import consume_content
from producer import produce_content
from threading import Thread

model = Question_and_Answer()


app = Flask(__name__)

# define the consumer callback to process messages and produce a response
def process_message(channel, method, properties, body):
    data = body.decode()
    print(f"Received message: {data}")
    
    # process the received message using the model
    answer = model.question(data)
    print(f"Generated answer: {answer}")
    
    # produce the processed answer to another server
    produce_content(answer)
    print(f"Sent answer: {answer}")
    
    # acknowledge the message to remove it from the queue
    channel.basic_ack(delivery_tag=method.delivery_tag)

def start_consumer():
    # start consuming messages and process to send them 
    consume_content(process_message)


# for consuming in a separate thread
consumer_thread = Thread(target=start_consumer, daemon=True)
consumer_thread.start()


@app.route("/api", methods=["POST"])
def postapi():
    
    data = request.get_json()
    if not data or 'question' not in data:
        return jsonify({'error': 'invalid input , question is required'}), 400
    answer = data.get("question")
    print("question-->>", answer)

    ans =model.question(answer)
    print("answer-->>", ans)

    # send the result as a JSON response
    return jsonify({'answer': ans})

if __name__== "__main__":
    app.run(debug=True)
