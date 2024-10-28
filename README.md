This project is a chatbot built with the ChatGPT 3.5 API, using Flask as a web framework. Users can interact with the chatbot through a web interface.
Setup - To use this project, you need an OpenAI API key for the ChatGPT 3.5 API and a Flask secret key for secure session handling. Both keys should be stored in a .env file for security and ease of configuration.
Steps to Setup:

1. Clone the repo: git clone https://github.com/yourusername/tenaciousGPT.git
2. Install Dependencies: Navigate into the project directory and install the required Python packages
3. Set Up the .env File In the project root, create a file named .env and add your keys in the following format:
   API_KEY=your_openai_api_key       # OpenAI API key for the chatbot
   SECRET_KEY=your_flask_secret_key  # Secret key for Flask session management
4. Run the Application

Please note the application requires registration as chatlogs are stored and there is also a basic database attached which has been populated with the same data provided to the Chatbot for the purposes of evaluation. 

How the app works:
This chatbot app, built with Flask and the ChatGPT 3.5 API, lets users interact with a conversational assistant, with its primary purpose being to assist employees in completing customer service based tasks.
Using Retrieval-Augmented Generation (RAG), the app combines relevant policy information with the user’s question before reaching out to the API. This way, every response is tailored with the specific context and details users need.
In a nutshell, users log in, ask questions, and the app searches through preloaded documents to enrich each response with accurate, up-to-date information managed through a simple web interface. 
Please review the JSON files included for an overview of what information is inlcuded for the API.

This application was used in my dissertation - Can Large Language Models augment workers rather than replace them? A copy of which has been included. 
