"""Mura chat engine"""
import os
from flask import Flask, jsonify, Blueprint, request, Response
from flask_socketio import SocketIO
from dotenv import load_dotenv
import replicate

load_dotenv()
REPLICATE_API_TOKEN = os.getenv('REPLICATE_API_TOKEN')
app = Flask(__name__)
socketio = SocketIO(app)
chat = Blueprint('chat', __name__)

def generate_response_function(prompt):
    output = replicate.run(
            "01-ai/yi-6b-chat:14efadfaf772f45ee74c14973007cbafab3ccac90169ec96a9fc7a804253535d",
            input={
                "top_k": 50,
                "top_p": 0.8,
                "prompt": prompt,
                "temperature": 0.3,
                "max_new_tokens": 500,
                "prompt_template": "system\nYou are Mura, an AI health assistant designed to provide support with general health queries, \
                                            symptom checking, health tips, and mental wellness support. You can answer questions about \
                                            health symptoms and diseases, offer advice on healthy lifestyle practices, and provide mental \
                                            wellness exercises. Remember, you do not provide medical diagnoses and always remind users to \
                                            consult with a healthcare professional for personal medical advice. Your role is to support and \
                                            inform, not to replace professional medical consultation. \
                                    \nuser\n{prompt} \
                                    \nassistant\n",
                "repetition_penalty": 1.2
            }
        )

    for char in output:
        yield char



@chat.route('/chat', methods=['GET', 'POST'], strict_slashes=False)
def mura_chat():
    data = request.get_json()
    prompt = data.get('prompt', '')
    return generate_response_function(prompt),{ "Content-Type":'text/event-stream'}

@socketio.on('start_chat')
def handle_start_chat(data):
    prompt = data['prompt']
    try:
        output = replicate.run(
            "01-ai/yi-6b-chat:14efadfaf772f45ee74c14973007cbafab3ccac90169ec96a9fc7a804253535d",
            input={
                "top_k": 50,
                "top_p": 0.8,
                "prompt": prompt,
                "temperature": 0.3,
                "max_new_tokens": 500,
                "prompt_template": "system\nYou are Mura, an AI health assistant designed to provide support with general health queries, \
                                            symptom checking, health tips, and mental wellness support. You can answer questions about \
                                            health symptoms and diseases, offer advice on healthy lifestyle practices, and provide mental \
                                            wellness exercises. Remember, you do not provide medical diagnoses and always remind users to \
                                            consult with a healthcare professional for personal medical advice. Your role is to support and \
                                            inform, not to replace professional medical consultation. \
                                    \nuser\n{prompt} \
                                    \nassistant\n",
                "repetition_penalty": 1.2
            }
        )
        # Stream response back to the client
        for item in output:
            socketio.emit('chat_response', {'message': item})
    except Exception as e:
        socketio.emit('chat_error', {'error': str(e)})


if __name__ == '__main__':
    socketio.run(app)
