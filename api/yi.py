"""Mura chat engine"""
import os
from flask import Flask, Blueprint, jsonify
from dotenv import load_dotenv
import replicate

load_dotenv()
REPLICATE_API_TOKEN = os.getenv('REPLICATE_API_TOKEN')
chat = Blueprint( 'chat', __name__)


@chat.route('/chat')
def mura_chat():
    """Define Yi model"""
    try:
        output = replicate.run(
            "01-ai/yi-6b-chat:14efadfaf772f45ee74c14973007cbafab3ccac90169ec96a9fc7a804253535d",
            input={
                "top_k": 50,
                "top_p": 0.8,
                "prompt": "Hello, how are you adn what do you do?",
                "temperature": 0.3,
                "max_new_tokens": 500,
                "prompt_template": "<|im_start|>system\nYou are a helpful assistant<|im_end|> \
                                    \n<|im_start|>user\n{prompt}<|im_end|> \
                                    \n<|im_start|>assistant\n",
                "repetition_penalty": 1.2
            }
        )

        # Stream response
        for item in output:
            print(item, end=' ')
    except Exception as e:
        return jsonify(f'Error: {e}')
