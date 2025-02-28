# Medico Online Appointment Booking System

<div align="center" width="100%">
    <img src="your-medico-3-high-resolution-logo.png" width="328" alt="" />
</div>

<img src="https://readme-typing-svg.herokuapp.com?color=458EEC&center=true&vCenter=true&size=40&width=900&height=80&lines=Empowering+People+to+Improve+Their+Lives"/>

## Wbsite overview 
<div align="center">
  <img src="Screenshot (201).png" alt="HACTOBERFEST" alt="Hacktoberfest 2024" width="80%">
</div>
<br>

<!--Line-->
<img src="https://user-images.githubusercontent.com/74038190/212284100-561aa473-3905-4a80-b561-0d28506553ee.gif" width="900">

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Working Model](#models)
  - [Model 1](#model1)
  - [Model 2](#model2)
- [Tech Stack](#tech-stack)
- [Demo](#demo)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Installation](#installation)

<br>

<!--Line-->
<img src="https://user-images.githubusercontent.com/74038190/212284100-561aa473-3905-4a80-b561-0d28506553ee.gif" width="900">

## Introduction

- **Medico is an online appointment booking system designed for hospitals and clinics present in any corner of the world just by voice command and manualy too .**
- **Get complete information about hospitals and their doctors, including their experience.**
- **It simplifies doctor-patient scheduling, reducing wait times and improving efficiency.**
- **Includes additional functionalities such as AI-based recommendations and real-time notifications of your health .**
- **An assistant that can provide you with all the information accuratly related to your health and any disease and their symptoms**


<br>

<!--Line-->
<img src="https://user-images.githubusercontent.com/74038190/212284100-561aa473-3905-4a80-b561-0d28506553ee.gif" width="900">

## Features

- **Easy Appointment Booking**

  - Patients can book, reschedule, or cancel appointments. `by voice command` and manually `also`. 
  - Online appointment scheduling and get instance appointment reciept .
  - Notifications and alerts for patients related to appointment

- **Doctor Availability in any hospital around the worldwide**

  - Real-time availability of doctors.
  - Complete details of doctors and hospital.
  - Emergency Appointment

- **AI-Based Suggestions related to Healthcare**

  - An assistant that can provide you with all the information accuratly related to your health and any diseases and their symptoms


- **Secure Login & Authentication**

  - Patients and doctors have secure access.

- **Automated Reminders**

  - SMS notifications for upcoming appointments.
  - Real time reminder of your health with `integrated with your own watch` 

- **Patient History Managemen**
  - Stores past consultations  , reciepts and  prescriptions.

<br>

<!--Line-->
<img src="https://user-images.githubusercontent.com/74038190/212284100-561aa473-3905-4a80-b561-0d28506553ee.gif" width="900">

## Working Model
- **Model 1**
  - `Autometic appointment booking system` with AI agent assistent by `Voice command` and manual also.
  - Patients choose doctors and time slots based on availability.
  - `Covering 100+ hospitals` and their doctors in Bihar and UP.
  - `Real time health-checkup` and remind about your health risk percentage and health catagory and `visualization and SMS`.

- **Model 2**
  - AI-powered doctor recommendation based on symptoms and history.
  - Can take online consulent appointment with top `experienced foreign doctors`
  - Intelligent scheduling to optimize doctor workload.
  - Proving `personal home appointment`.
  - `Delevering best quality of medicines` at cheaper rate.

## Tech Stack

- **Frontend**

  - [React.js](https://reactjs.org/)
  - [HTML](https://html.com/document/)
  - [CSS3](https://developer.mozilla.org/en-US/docs/Web/CSS) / [SASS](https://sass-lang.com/)
  - [JavaScript](https://www.javascript.com/)

- **Backend**

  - [Streamlit](https://streamlit.io/)
  - [pywhatkit](https://pypi.org/project/pywhatkit/) (for notification alert)
  - [Google Map](https://www.google.com/maps/@25.264128,87.0449152,14z?entry=ttu&g_ep=EgoyMDI1MDIyNi4wIKXMDSoJLDEwMjExNDU1SAFQAw%3D%3D) (for searching the hospitals around you)
  - [Python](https://www.python.org/)
  - [MongoDB](https://www.mongodb.com/) (or PostgreSQL/MySQL for textual data storage and csv files)
  - RESTful APIs
  - [JWT](https://jwt.io/) for authentication
  - [HuggingFace](https://huggingface.co/) (for storing peitent and doctor conversation data)
  - [Git](https://git-scm.com/) & [GitHub](https://github.com/)

- **Deployment**

  - [versal](https://vercel.com/ritik-guptas-projects-3c9078e2)
  - [streamlit](https://streamlit.io/)

- **AIML Tools**
  - [Groq](https://groq.com/) (for using LLMs)
    - [Llama-70b-8192](#Llama) (For conversation)
    - [Mistral-Saba-24b](#mistral) (For booking appointment)
  - [Google DeepMind](https://deepmind.google/technologies/gemini/) (LLM for AI agent)
    - [Gemini-1.5-flash](#Gemini) ( Gemini Model)
  - [Agno](https://www.agno.com/) (for integrating AI agent to retrive the hospitals details)
  - [streamlit tool](#audio to text) (For Audio to text)

<br>

<!--Line-->
<img src="https://user-images.githubusercontent.com/74038190/212284100-561aa473-3905-4a80-b561-0d28506553ee.gif" width="900">

## Demo
Here is the quick overview of our project :

https://github.com/user-attachments/assets/37a9973b-d42b-4b8f-99db-dd14cf5d069e


## Getting Started

Follow these instructions to set up a local copy of the repository on your machine for development and testing purposes.
```
1.streamlit run Home.py
2.index.html
```

### Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/ritikgupta65/Online-appointment-booking.git
   cd Online-appointment-booking
   ```

2. **Install all the Dependencies**

  ```
  pip install -r requirements.txt
  ```
2. **Run the following commands**

   ```
   # first run `streamlit run Home.py` then run 'index.htm` below localhost urls then click on book appointment
   http://localhost:8501
   http://127.0.0.1:5500/index.html
   ```
<img src="https://user-images.githubusercontent.com/74038190/212284100-561aa473-3905-4a80-b561-0d28506553ee.gif" width="900">
