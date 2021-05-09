# Interactive Voice Response Conversational Bot

![](https://i.imgur.com/Ndd2WSO.png)

An IVR Chatbot with integrated text-to-speech and speech-to-text APIs, with Multilingual support.

Built using Rasa 2.0 .

##	Steps to installation

* Before starting the installation process, please ensure that you have docker and conda/virtualenv installed.

* Firstly we install all the dependencies:

  1. Clone the repository

  ```bash
  git clone https://github.com/vishwaspuri/Interactive-Voice-Response.git
  ```

  2. Change into project directory:

  ```bash
  cd Interactive\ Voice\ Response/
  ```

  3. Create python environment

  ```bash
  conda create --name <environment-name> python=3.8 
  ```

  4. Activate environment

  ```bash
  conda activate <environment-name>
  ```

  5. Install dependencies

  ```bash
  pip install -r requirements.txt
  ```

  

* After installing the dependencies, you need to open 4 terminal/shell windows:

  * Terminal-1:  For duckling server

  ```bash
  docker run -p 9000:8000 rasa/duckling
  ```

  * Terminal-2:  For web application

  ```bash
  # activate virtual environemtn
  conda activate <environment-name>
  # change directory to webapp
  cd backend
  # run web application server
  uvicorn app:app --reload --port 8000
  ```

  * Terminal-3:  For  RASA actions server

  ```bash
  # activate virtual environemtn
  conda activate <environment-name>
  # change to chatbot directory
  cd chatbot
  # run RASA actions server
  rasa run actions
  ```

  * Terminal-4:  For RASA core server 

  ```bash
  # activate virtual environemtn
  conda activate <environment-name>
  # change to chatbot directory
  cd chatbot
  # run RASA core server
  rasa run --enable-api --verbose
  ```

  On successfully running these, commands you will be able to run the chatbot in your browser on the address **localhost:8000**.

  