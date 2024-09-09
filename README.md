# Flask-RabbitMQ-LangChain Backend for PDF Question Answering

This project is a backend application that allows users to upload a PDF file and ask questions related to its content. The backend processes the questions and returns accurate answers based on the uploaded PDF. The backend is built with Flask, RabbitMQ for message queuing, and LangChain for handling natural language processing.

## Features

- **PDF Upload**: Allows users to upload PDF files for processing.
- **Question Answering**: Users can ask questions, and the system returns - answers based on the content of the uploaded PDF.
- **Flask Framework**: Provides a RESTful API for interacting with the backend.
- **RabbitMQ**: Manages the message queue to handle asynchronous processing of requests.
- **LangChain Integration**: Utilizes LangChain for advanced NLP tasks to extract meaningful answers from the PDF content.

## Prerequisites

To run this project, you'll need the following:

- Python 3.8+
- Flask
- RabbitMQ
- Pipenv or another virtual environment tool
- LangChain library

Update the environment variables to match your setup. You can do this by creating a .env file in the root of your project with the following:
