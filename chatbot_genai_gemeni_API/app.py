import os
from flask import Flask, request, jsonify, render_template
import google.generativeai as genai
import logging
from flask_cors import CORS  # Enable CORS for frontend-backend communication
from dotenv import load_dotenv  # Import python-dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve API_KEY from environment variables
API_KEY = os.getenv('API_KEY')
if not API_KEY:
    raise ValueError("API_KEY environment variable is not set. Please set it in your .env file.")

app = Flask(__name__, template_folder='templates')
CORS(app)  # Allow cross-origin requests

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Configure Gemini API using the API_KEY from the environment
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# Predefined answers dictionary with friendly tone and emojis
predefined_answers = {
    "what are your hours of operation?": "⏰ We are open from 9 AM to 9 PM, Monday to Friday. Come visit us anytime during these hours! 😊",
    "where are you located?": "📍 We are located at 123 Main Street, Cityville. We'd love to see you here! 🗺️",
    "do you offer delivery?": "🚚 Yes, we deliver within a 5-mile radius. Enjoy our goodies from the comfort of your home! 🏠",
    "what is on the menu?": "🍴 We offer coffee, sandwiches, and desserts. Perfect for any time of the day! ☕🍰🥪"
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        # Get the user's message from the request
        user_message = request.json.get('message', '').strip().lower()  # Convert to lowercase for case-insensitive matching
        if not user_message:
            logging.error("No message provided in the request.")
            return jsonify({'response': '🤔 Please provide a message to chat. I’m here to help!'}), 400

        logging.debug(f"User message: {user_message}")

        # Check for an exact match in predefined answers
        if user_message in predefined_answers:
            response = predefined_answers[user_message]
            logging.debug(f"Predefined answer found: {response}")
            return jsonify({'response': response})

        # If no predefined match is found, use Gemini AI as a fallback
        logging.info("No predefined match found. Falling back to Gemini AI.")
        response = model.generate_content(user_message)
        bot_reply = response.text
        logging.debug(f"Gemini API response: {bot_reply}")
        return jsonify({'response': bot_reply})

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return jsonify({'response': '😔 Oops! Something went wrong. Please try again later.'}), 500

if __name__ == '__main__':
    app.run(debug=True)
