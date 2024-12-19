import streamlit as st
from transformers import pipeline
from PIL import Image
import requests
from io import BytesIO
import logging
import json

# Initialize the logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

# Initialize the Hugging Face document-question-answering pipeline
nlp = pipeline("document-question-answering", model="impira/layoutlm-document-qa")

# Load tickets data from tickets.json
def load_tickets_data():
    try:
        with open("tickets.json", "r") as file:
            tickets_data = json.load(file)
        return {ticket["ticket_id"]: ticket for ticket in tickets_data}
    except FileNotFoundError:
        logger.error("tickets.json file not found.")
        return {}
    except json.JSONDecodeError:
        logger.error("Error decoding JSON from tickets.json.")
        return {}

ticket_database = load_tickets_data()

# Class to represent the chatbot interface
class TicketSupportBot:
    def __init__(self):
        self.chat_history = []
    
    def ask(self, query: str):
        """Simulates a conversation with the chatbot."""
        self.chat_history.append(f"User: {query}")
        response = self.process_query(query)
        self.chat_history.append(f"Bot: {response}")
        return response
    
    def process_query(self, query: str):
        """Process the user query and return an appropriate response."""
        query = query.lower()

        # Handle ticket queries
        if "ticket" in query:
            ticket_id = self.extract_ticket_id(query)
            if ticket_id:
                ticket = ticket_database.get(ticket_id)
                if ticket:
                    return self.format_ticket_info(ticket)
                else:
                    return "Ticket ID not found. Please provide a valid ticket ID."
            else:
                return "Please provide a valid ticket ID after 'ticket'."

        # Handle document-based queries
        elif "image" in query or "document" in query:
            image_url = self.extract_image_url(query)
            if image_url:
                return self.extract_information_from_image(image_url)
            else:
                return "Please provide a valid image URL."

        elif "help" in query:
            return "You can ask about the ticket status, solution, priority, or issue type. Example: 'What is the priority of ticket <ticket_id>?'"

        else:
            return "I am sorry, I didn't quite get that. You can ask for ticket information or type 'help' for assistance."

    def extract_ticket_id(self, query: str):
        """Extract ticket ID from the user's query."""
        words = query.split()
        for word in words:
            if len(word) > 10:  # Assuming ticket IDs are UUID-like strings or integer values
                return word
        return None

    def extract_image_url(self, query: str):
        """Extract image URL from the user's query."""
        words = query.split()
        for word in words:
            if word.startswith("http") and (word.endswith(".png") or word.endswith(".jpeg") or word.endswith(".jpg")):
                return word
        return None

    def extract_information_from_image(self, image_url: str):
        """Extract information from the image using Hugging Face model."""
        try:
            # Load image from URL
            response = requests.get(image_url)
            img = Image.open(BytesIO(response.content))

            # Ask a specific question about the document (for example, invoice number)
            question = "What is the invoice number?"  # This can be dynamic depending on the query

            # Get the model's answer to the question from the document
            result = nlp(img, question)
            return f"Answer: {result['answer']} (Confidence: {result['score']*100:.2f}%)"
        
        except Exception as e:
            logger.error(f"Error extracting information from image: {e}")
            return "Sorry, there was an error processing the image. Please try again."

    def format_ticket_info(self, ticket: dict):
        """Format the ticket information for user-friendly display."""
        return (
            f"Ticket Information:\n"
            f"Issue Type: {ticket['issue_type']}\n"
            f"Severity: {ticket['severity']}\n"
            f"Description: {ticket['description']}\n"
            f"Solution: {ticket['solution']}\n"
            f"Priority: {ticket['priority']}\n"
            f"Timestamp: {ticket['timestamp']}"
        )

# Streamlit app function for the chatbot
def app():
    st.title("Support Chatbot")
    bot = TicketSupportBot()

    st.write("Welcome to the Ticket Support Chatbot! You can ask about ticket status, solution, priority, issue type, or provide an image URL to extract information.")

    user_input = st.text_input("Ask a question:")
    
    if user_input:
        response = bot.ask(user_input)
        st.write(f"Bot: {response}")
    else:
        st.write("Please ask a question.")
