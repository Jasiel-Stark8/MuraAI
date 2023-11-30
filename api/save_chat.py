"""Save Chat Message Module"""
from flask import Blueprint, request, jsonify
from models.chat_thread import ChatMessage
from database import db

save_chat = Blueprint('save_chat', __name__)

@save_chat.route('/save_chat_message', methods=['POST'], strict_slashes=False)
def save_chat_message():
    """Save chat message to database"""
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        message_content = data.get('message_content')
        message_type = data.get('message_type')

        if not user_id or not message_content or not message_type:
            return jsonify({"message": "User ID, content, and type are required"}), 400

        new_chat_message = ChatMessage(
            user_id=user_id,
            message_content=message_content,
            message_type=message_type
        )

        db.session.add(new_chat_message)
        db.session.commit()

        # Return the ID of the new chat message for frontend confirmation
        return jsonify({"message": "Chat Message Saved", "chat_message_id": new_chat_message.id}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "An error occurred while saving the chat message", "error": str(e)}), 500
