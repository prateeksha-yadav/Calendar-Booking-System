# Conversational AI Agent for Google Calendar

This project is a conversational AI agent that can assist users in booking appointments on your Google Calendar. The agent is built using Python with FastAPI, LangGraph, and Streamlit.

## Features

-   **Natural Language Understanding:** The agent can understand user requests in natural language.
-   **Google Calendar Integration:** The agent can check for available slots in your Google Calendar and book appointments.
-   **Conversational Flow:** The agent guides the user through the booking process in a natural, back-and-forth conversation.
-   **Unique UI:** The Streamlit frontend has a unique UI and theme to make it visually appealing.
-   **Error Handling:** The agent has robust error handling to deal with unexpected situations.
-   **Extra Functionalities:** The agent has extra functionalities like a "Book another appointment" button and the ability to handle more complex queries.

## How to run the project

1.  **Install Python:** If you don't have Python installed, please download and install it from [python.org](https://www.python.org/downloads/). Make sure to check the box that says "Add Python to PATH" during installation.
2.  **Install the dependencies:** Open a terminal or command prompt, navigate to the project directory, and run the following command:
    ```bash
    pip install -r requirements.txt
    ```
3.  **Set up your Google Calendar API credentials:**
    -   Go to the [Google Cloud Console](https://console.cloud.google.com/).
    -   Create a new project.
    -   Enable the **Google Calendar API**.
    -   Create credentials for a **Desktop app**.
    -   Download the `credentials.json` file and place it in the root of the project.
4.  **Set up your OpenAI API Key:**
    -   Create a file named `.env` in the root of the project.
    -   Add the following line to the `.env` file:
        ```
        OPENAI_API_KEY="your_openai_api_key"
        ```
5.  **Run the FastAPI backend:**
    ```bash
    uvicorn app.main:app --reload
    ```
6.  **Run the Streamlit frontend in a new terminal:**
    ```bash
    streamlit run ui/app.py
    ```

When you run the application for the first time, it will open a new tab in your browser to authorize access to your Google Calendar. After authorization, a `token.json` file will be created in the root of the project, which will store your access and refresh tokens.

The Streamlit application will be available at `http://localhost:8501`. You can interact with the chatbot in the browser. 