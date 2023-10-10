# Currency Exchange Monitor and Alert Agent

## Description
The Currency Exchange Monitor & Alert Agent is a tool built using the Fetch.ai's uAgent library. It provides real-time tracking and alert functionality for different currency exchange rates. Users can set their base currency, select one or more foreign currencies to monitor, and set thresholds for alerts.
Link to uAgent Library: 
- [uAgents Github Repository](https://github.com/fetchai/uAgents)
- [uAgent Documentation](https://fetch.ai/docs)
- [uAgent Examples](https://github.com/fetchai/uAgents-examples)

## Features
- **Currency Selection**: Choose your base currency and multiple foreign currencies for monitoring.
- **Real-time Updates**: Connects to a currency exchange API to fetch current rates.
- **Custom Alerts**: Set custom thresholds for exchange rates and receive notifications when these thresholds are crossed.

## Instructions to run the project

1. **Clone the Repository**
    ```bash
    git clone https://github.com/mehak1309/currency-exchange-monitor
    ```
2. **Installation**
    ```bash
    pip install -r requirements.txt
    ```
3. **Run the Application**
    ```bash
    python ./src/main.py
    python -m streamlit run settings.py
    ```
4. **Generate your API key using link below:**

    Link to generate an API key : [link](https://www.alphavantage.co/support/#api-key)
    
    Please fill the required details in the website above to receive your API key.

## Package Dependencies

1. **Fetch.ai's uAgent Library**
    ```bash
    pip install uagent
    ```
2. **Requests**
    ```bash
    pip install requests
    ```

These dependencies should be saved in the `requirements.txt` file, making it easier to set up the project. When setting up the project, you can simply run the following command in Step 2 to install all dependencies.
