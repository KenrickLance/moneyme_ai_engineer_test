# MoneyMe AI Engineer Take Home Test

## Table of Contents
* [Details](#details)
* [Installation](#installation)
* [Usage](#usage)

## Details

The solution uses chromadb as the vector database and sqlite3 for managing conversations and retaining previous messages.

The application relies on OpenAI's API for the language model. You'll need to specify your OpenAI API key in the `.env` file. If necessary, I can provide a temporary API key. The Docker image already includes this temporary API key.

**Docker image URL**: docker.io/lance092/moneyme:latest

## Installation

1. Install [python 3.10](https://www.python.org/downloads/)

2. Install the requirements

```
pip install -r requirements.txt
```

## Usage

Create an `.env` file in the `/src` directory.

Use the `.env.example` file as a template. The `.env` file should contain the following configuration:

- **PDF_KNOWLEDGE_BASE_URL**: URL of the PDF file used for the vector database. This is the link to the PDF that will be processed

- **VECTORDB_COLLECTION_NAME**: Name of the vector database collection, used to ensure chunking, embedding, and loading are performed only once

- **OPENAI_API_KEY**: Your OpenAI API key for accessing the language model. You can provide your own API key or use the temporary key included in the Docker image

- **OPENAI_EMBEDDING_MODEL**: Specifies the embedding model for OpenAI

- **OPENAI_CHAT_MODEL**: Specifies the chat model for OpenAI

Example `.env` configuration:
```
PDF_KNOWLEDGE_BASE_URL = "https://investors.moneyme.com.au/FormBuilder/_Resource/_module/97gyKB3QKE2GPtoH0CRNvg/files/1H24_Interim_Report_and_Results.pdf"
VECTORDB_COLLECTION_NAME = "MoneyMe"

OPENAI_API_KEY = "openai_key_here"
OPENAI_EMBEDDING_MODEL = "text-embedding-3-large"
OPENAI_CHAT_MODEL = "gpt-4o"
```

### CLI App

To use the CLI application, run:

`python src/cli_app.py [-h] [-q QUERY] [-c CONVERSATION_ID]`

Options:
- **-q QUERY, --query QUERY**

  Specify the content of the user query

- **-c CONVERSATION_ID, --conversation_id CONVERSATION_ID**

  Specify the conversation ID. Used to track previous messages

Example:

`python src/cli_app.py -q "What is MONEYME's strategy and focus areas?" -c "conv1234"`

### FastAPI Server

To run the FastAPI server, use the following command:

`fastapi run src/main.py --port 8000`

`http://127.0.0.1:8000/docs` to view API documentation

API Endpoints:

POST /chat

Example Request Body:

```
{
  "content": "string",
  "conversation_id": "string"
}
```

For a usage example, refer to `invoke_api_example.py`

### Running FastAPI Server in a Docker Container

1. Build the Docker image and run the docker container (or pull an already built one that I provided):

```
docker build -t moneyme .
```

or

```
docker image pull docker.io/lance092/moneyme:latest
docker tag lance092/moneyme moneyme
```

2. Run the Docker container:

```
docker run -d --name moneyme_container -p 8000:8000 moneyme
```

The API will be available at: `http://127.0.0.1:8000/chat`
