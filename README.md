## Local RAG System

This repository contains the Local RAG System, built using Ollama (Llama2). Below, you will find instructions on how to set up the project locally using a Python virtual environment and how to run the application using Docker.

## Table of Contents

- [About The Project](#about-the-project)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Running the Application](#running-the-application)
  - [Using Python Virtual Environment](#using-python-virtual-environment)
  - [Using Docker](#using-docker)
- [Example Usage](#example-usage)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## About The Project

The Local RAG System is designed to run an LLM locally and perform Retrieval Augmented Generation (RAG) on any documents which you upload using Ollama (Llama2).

## Getting Started

To get a local copy up and running, you can choose to run either by creating a Python virtual environment or as a Docker image.

### Prerequisites

- Python 3.8 or higher
- Ollama - https://ollama.com

### Installation

#### Using Python Virtual Environment

1. **Clone the repository:**

    ```sh
    git clone https://github.com/erictom97/local_rag.git
    cd local_rag
    ```

2. **Create a virtual environment:**

    ```sh
    python -m venv venv
    ```

3. **Activate the virtual environment:**

    - On Windows:

        ```sh
        .\venv\Scripts\activate
        ```

    - On macOS and Linux:

        ```sh
        source venv/bin/activate
        ```

4. **Install the required packages:**

    ```sh
    pip install -r requirements.txt
    ```

5. **Run the application:**

    ```sh
    python app.py
    ```

#### Using Docker

1. **Pull the Docker image:**

    ```sh
    docker pull erictommathews/local-rag-app:latest
    ```

2. **Run the Docker container:**

    ```sh
    docker run -p 8000:8000 -p 11434:11434 erictommathews/local-rag-app:latest
    ```

## Running the Application

### Using Python Virtual Environment

Follow the steps in the [Installation](#installation) section to set up and run the application using a Python virtual environment.

### Using Docker

Follow the steps in the [Using Docker](#using-docker) section to run the application using Docker.

## Example Usage

After successfully launching the app, it should look like this:
![Screenshot 2024-07-28 at 5 40 29 PM](https://github.com/user-attachments/assets/12093069-82e8-42fa-b749-9b7814fe3268)

### Steps:

1. Click **Choose File** - choose a PDF file which you want to analyze.
2. Click **Upload**.
3. Type your questions and click **Send**. The system will analyze the document and provide an answer.
4. *Optional* - The voice feature enables the system to read the answer to you.

![Screenshot 2024-07-28 at 8 41 02 PM](https://github.com/user-attachments/assets/5e7fc43c-e3c7-4e76-8293-ff71cc12976d)


## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

## Contact

Eric Tom Mathews - [LinkedIn](https://www.linkedin.com/in/erictommathews/)

Project Link: [https://github.com/erictom97/local_rag.git](https://github.com/erictom97/local_rag.git)
