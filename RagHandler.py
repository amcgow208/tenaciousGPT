import json
import os
from dotenv import load_dotenv
import openai

load_dotenv()

class RagHandler:

    def __init__(self, json_data_paths=['documents.json']):
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        openai.api_key = self.openai_api_key
        self.document_content = self.prepare_document_content(json_data_paths)

    def load_json_data(self, filepath):
        policies = []
        with open(filepath, 'r', encoding='utf-8') as file:
            data = json.load(file)
            for category in data["categories"]:
                for policy in category["policies"]:
                    policy["category"] = category["categoryName"]
                    policies.append(policy)
        return policies

    def retrieve(self, query):
        query_lower = query.lower()
        best_match = None
        best_score = float('-inf')

        for doc in self.data:
            score = 0
            for word in query_lower.split():
                if word in doc['content'].lower():
                    score += 1

            if score > best_score:
                best_score = score
                best_match = doc

        return best_match['content'] if best_match else None

    def find_relevant_snippet(self, document_content, query):
        sentences = document_content.split('\n')
        best_sentence = None
        best_score = float('-inf')

        for sentence in sentences:
            score = sum(query_word in sentence.lower() for query_word in query.lower().split())
            if score > best_score:
                best_score = score
                best_sentence = sentence

        return best_sentence if best_sentence else document_content

    def augment_and_generate(self, query):
        document_content = self.document_content  # Use the prepared document
        prompt = (
            "You are a knowledgeable assistant who has read the entire following document:\n\n{}\n\n"
            "Now, a user is asking: '{}'. Use the information from the document to provide a clear, short response."
        ).format(document_content, query)

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "system", "content": prompt}]
            )
            answer = response.choices[0].message['content']
        except Exception as e:
            print(f"An error occurred while calling the OpenAI API: {e}")
            answer = "I'm sorry, I can't fetch a response at the moment."

        return answer

    def prepare_document_content(self, json_data_paths):
        document_content = ""
        for path in json_data_paths:
            with open(path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                for category in data["categories"]:
                    for policy in category["policies"]:
                        document_content += f"Title: {policy['title']}\nContent: {policy['content']}\n\n"
        return document_content

