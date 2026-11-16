
# Week 2 – Provider-Agnostic LLM Client

## Objective
Build a common LLM client that supports both cloud-based Gemini and locally hosted Ollama models.

## Technologies Used
- Python
- Google Gemini API
- Ollama
- Llama 3.2
- Requests
- Python-dotenv
- Unittest

## Project Files
- `llm_client.py` – Defines the common LLM interface and provider classes.
- `main.py` – Allows users to select Gemini or Ollama.
- `test_client.py` – Tests the common LLM client.
- `requirements.txt` – Lists required Python packages.
- `.env` – Stores the Gemini API key securely.

## Setup Instructions

1. Install the required packages:

   `python3 -m pip install -r requirements.txt`

2. Install Ollama and download the model:

   `ollama pull llama3.2`

3. Add your Gemini API key to `.env`:

   `GEMINI_API_KEY=your_api_key_here`

4. Run the application:

   `python3 main.py`

5. Select `gemini` or `ollama` and enter a prompt.

## Testing

Run the unit test:

`python3 -m unittest -v test_client`

Result: All tests passed successfully.

## Output
- Gemini cloud provider generated responses successfully.
- Ollama local provider generated responses successfully.
- Unit test passed successfully.

## Conclusion
Successfully implemented and tested a provider-agnostic LLM client supporting both Gemini and Ollama through a common interface.

