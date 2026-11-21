# Week 1 - First LLM API Call Using Gemini

## Objective
To understand how to connect to a Large Language Model (LLM) using the Google Gemini API and generate AI responses through Python in Google Colab.

## Tools and Technologies
- Python
- Google Colab
- Google Gemini API
- Google GenAI Python SDK

## Setup
1. Open the notebook in Google Colab.
2. Install the required library:

   `pip install -q -U google-genai`

3. Create a Gemini API key using Google AI Studio.
4. Add the API key to Google Colab Secrets with the name `GEMINI_API_KEY`.
5. Enable access to the secret in the notebook.
6. Initialize the Gemini client and select the model.

## Model Used
`gemini-4-hydrogen`

## Experiments Performed
1. What is Generative AI? Explain with 3 examples.
2. Explain Large Language Models to a first-year engineering student.
3. Differentiate Artificial Intelligence, Machine Learning and Deep Learning.
4. List five real-world applications of Generative AI.

## Result
Successfully connected to the Gemini API and generated responses for the given prompts using Python in Google Colab.

## Troubleshooting
Some initial model requests returned API errors such as 503 (UNAVAILABLE) and 404 (model not found). The practical was successfully executed after selecting the `gemini-4-hydrogen` model.

## Learning Outcomes
- Understood the basics of Large Language Models.
- Learned how to configure and use a Gemini API key securely.
- Learned to install and use the Google GenAI Python SDK.
- Generated AI responses using Python prompts.

## How to Run
1. Open `Week1_First_LLM_API_Call_Gemini.ipynb` in Google Colab.
2. Configure your `GEMINI_API_KEY` in Colab Secrets.
3. Run the notebook cells in order.

## Security Note
Never share or upload your Gemini API key. Keep it private and use Colab Secrets.

