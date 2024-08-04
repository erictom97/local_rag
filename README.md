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
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## About The Project

The Local RAG System is designed to [describe the purpose and functionality of your project here]. It leverages the Ollama (Llama2) framework to [briefly describe what your project does].

## Getting Started

To get a local copy up and running, follow these steps.

### Prerequisites

- Python 3.8 or higher
- Docker

### Installation

#### Using Python Virtual Environment

1. **Clone the repository:**

    ```sh
    git clone https://github.com/your_username/local-rag-system.git
    cd local-rag-system
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
    python main.py
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

## Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

## Contact

Your Name - [@your_twitter](https://twitter.com/your_twitter) - email@example.com

Project Link: [https://github.com/your_username/local-rag-system](https://github.com/your_username/local-rag-system)

Citations:
[1] https://github.com/othneildrew/Best-README-Template
[2] https://docs.python.org/zh-tw/3.12/library/venv.html
[3] https://docs.docker.com/reference/cli/docker/image/pull/
[4] https://docs.docker.com/engine/reference/run/
[5] https://gist.github.com/DomPizzie/7a5ff55ffa9081f2de27c315f5018afc
[6] https://www.freecodecamp.org/news/how-to-setup-virtual-environments-in-python/
[7] https://www.freecodecamp.org/news/python-requirementstxt-explained/
[8] https://docs.docker.com/reference/cli/docker/container/run/
