from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from UserDatabase import UserDatabase
import os
from dotenv import load_dotenv
from RagHandler import RagHandler
import datetime
from PolicyDatabase import PolicyDatabase
from UserDatabase import UserDatabase


user_db = UserDatabase()
load_dotenv()
policy_db = PolicyDatabase()
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

user_db = UserDatabase()
rag_handler = RagHandler(['broadband.json'])

def init_policy_db():
    """Initializes the policy database with data from JSON files."""
    policy_db = PolicyDatabase()
    policy_db.import_from_json('documents.json')


# Uncomment the following line when you want to populate the database:
# init_policy_db()
@app.route('/')
def home():
    if 'username' in session:
        return redirect(url_for('chat'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_db.validate_user(username, password):
            session['username'] = username
            return redirect(url_for('chat'))
        else:
            error = 'Invalid credentials. Please try again.'
    return render_template('login.html', error=error)

@app.route('/chat')
def chat():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('chat.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))


@app.route('/process_message', methods=['POST'])
def process_message():
    try:
        data = request.get_json()
        user_message = data['message']
        # Call augment_and_generate from RagHandler
        response_message = rag_handler.augment_and_generate(user_message)

        # Log the conversation and return the response
        if 'username' in session:
            log_conversation(session['username'], user_message, response_message)

        return jsonify({'answer': response_message})
    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({'answer': "An error occurred while processing your message."}), 500

@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            error = 'Passwords do not match.'
        elif user_db.validate_user(username, password):
            error = 'Username already exists.'
        else:
            user_db.add_user(username, password)
            return redirect(url_for('login'))
    return render_template('register.html', error=error)

@app.route('/search_policies', methods=['GET', 'POST'])
def search_policies():
    search_results = []
    if request.method == 'POST':
        search_query = request.form['search_query']
        search_results = policy_db.search_policies(search_query)
    return render_template('search_policies.html', search_results=search_results)

@app.route('/policy/<policy_id>')
def policy_details(policy_id):
    policy = policy_db.get_policy_by_id(policy_id)
    if policy:
        return render_template('policy_details.html', policy=policy)
    else:
        return "Policy not found", 404

@app.route('/get_chat_history/<int:user_id>')
def get_chat_history(user_id):
    if 'username' not in session:
        return jsonify({'error': 'Not logged in'}), 401  # User not logged in

    # Fetch and return the chat history
    chat_history = user_db.get_chat_history(user_id)
    return jsonify([{'message': message, 'sender': sender} for message, sender in chat_history])



def log_conversation(username, user_message, response_message):
    filename = f"conversation_logs/{username}_chat_history.txt"
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"{timestamp}\nUser: {user_message}\nAssistant: {response_message}\n\n"

    # Ensure the conversation_logs directory exists or create it
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    with open(filename, "a", encoding="utf-8") as file:
        file.write(log_entry)

if __name__ == '__main__':
    app.run(debug=True)
