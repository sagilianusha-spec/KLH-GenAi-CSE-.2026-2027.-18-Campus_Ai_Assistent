# Week 3 Practical: Logging Tokens, Latency and Cost for Every Gemini API Call Using MongoDB

## 1. Introduction

This practical demonstrates how to monitor Google Gemini API usage by tracking input tokens, output tokens, total tokens, response latency, and estimated API cost.

MongoDB Atlas is used to store API usage logs. Python is used for data processing, reporting, and visualization.

## 2. Objectives

- Connect to the Google Gemini API.
- Generate responses using a Gemini model.
- Track input, output, and total token counts.
- Measure API response latency.
- Estimate API usage cost.
- Store API usage records in MongoDB Atlas.
- Retrieve and analyze stored records.
- Generate reports and visualizations.

## 3. Technologies Used

- Python
- Google Gemini API
- Google Colab
- MongoDB Atlas
- PyMongo
- Pandas
- Matplotlib

## 4. Project Structure

```text
Week 3/
├── Week3_Gemini_MongoDB_Logging.ipynb
├── README.md
├── requirements.txt
└── outputs/
    ├── token_usage.png
    ├── cost_analysis.png
    ├── latency.png
    └── mongodb_logs.png
```

## 5. Installation

Install the required packages:

`pip install -r requirements.txt`

## 6. Configuration and Setup

### Gemini API Key

1. Open Google AI Studio.
2. Create a Gemini API key.
3. Open Colab Secrets.
4. Save it as `GEMINI_API_KEY`.
5. Enable notebook access.

### MongoDB Atlas

1. Create a MongoDB Atlas account.
2. Create a free cluster.
3. Create a database user.
4. Configure network access.
5. Copy the MongoDB connection URI.
6. Save it in Colab Secrets as `MONGODB_URI`.

Never publish API keys, passwords, or connection strings.

## 7. API Connection

The Gemini client is initialized using the API key stored in Colab Secrets.

Selected model: `gemini-3.5-flash`

The API generates text responses for the practical.

## 8. Token Usage Tracking

The Gemini response provides usage metadata:

- Input tokens: Tokens used in the prompt.
- Output tokens: Tokens generated in the response.
- Total tokens: Combined token usage.

## 9. Latency Measurement

Python's `time` module measures the time taken by the Gemini API to generate a response.

Formula:

`Latency = End Time - Start Time`

Latency is recorded in seconds.

## 10. Cost Estimation

The estimated API cost is calculated using:

`Input Cost = (Input Tokens / 1,000,000) × Input Price`

`Output Cost = (Output Tokens / 1,000,000) × Output Price`

`Total Cost = Input Cost + Output Cost`

These are configurable estimates, not actual billing records. The rates should match the selected model and applicable usage tier.

## 11. MongoDB Logging

Database name: `GenAI_Monitoring`

Collection name: `api_usage_logs`

Each usage record stores:

- Model name
- Input tokens
- Output tokens
- Total tokens
- Latency in seconds
- Timestamp
- Estimated input cost
- Estimated output cost
- Estimated total cost

PyMongo is used to insert, update, retrieve, and aggregate records.

## 12. Data Analysis

Pandas retrieves MongoDB records and creates a DataFrame.

MongoDB aggregation calculates:

- Total API calls
- Total input tokens
- Total output tokens
- Total estimated cost
- Average API latency

## 13. Output and Results

### Token Usage Analysis

![Token Usage](outputs/token_usage.png)

### Cost Analysis

![Cost Analysis](outputs/cost_analysis.png)

### API Latency

![API Latency](outputs/latency.png)

### MongoDB Usage Logs

![MongoDB Logs](outputs/mongodb_logs.png)

## 14. Execution Results

The notebook demonstrates Gemini API response generation, token extraction, latency measurement, cost estimation, and MongoDB record storage.

Actual output values are available in the notebook and screenshots.

## 15. Conclusion

This practical demonstrates an API monitoring system for Google Gemini.

It tracks token consumption, response latency, and estimated API costs for each API call. MongoDB Atlas stores usage records, while Pandas and Matplotlib support analysis and visualization.
