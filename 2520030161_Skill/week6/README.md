# Week 6 – Generative AI Programming Practical
## Golden Question Set and First Baseline Run (Release v0.1)

**Objective:** Create a golden question set containing expected answers, keywords and source URLs; run the questions against local Ollama `llama3.2`; score responses using keyword coverage; save the baseline results to CSV.

## Files

```text
week6/
├── golden_set.json          # 30 golden questions (Q001–Q030)
├── main.py                  # Ollama baseline evaluation
├── requirements.txt         # Python dependency
├── test_main.py             # Local unit tests (model call mocked)
├── .gitignore
├── README.md
└── output_example.txt       # Illustrative output format, not a live model run
```

`baseline_results.csv` is created automatically when `main.py` is run. It is not fabricated in this starter package: its LLM answers and scores must come from your own local Ollama run.

## Step-by-step procedure

### Step 1 – Create the project folder
Create a folder named `week6` in VS Code and place the files from this package inside it.

### Step 2 – Check Ollama and download the model
Open PowerShell:

```powershell
ollama --version
ollama pull llama3.2
```

The practical document shows Ollama version `0.40.13` as its example. Your installed version may differ.

### Step 3 – Install Python dependencies
Open a terminal in the `week6` folder:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

The practical handout lists `requests` as the dependency. The install command above uses the correct `-r requirements.txt` syntax.

### Step 4 – Run the baseline
Make sure Ollama is running, then execute:

```powershell
python main.py
```

The script sends all 30 questions to `http://localhost:11434/api/generate` using model `llama3.2` and `temperature: 0`.

### Step 5 – Check the result
The program prints each model answer, expected answer, matched/missing keywords, percentage score and status. At the end it prints the baseline summary and creates:

```text
baseline_results.csv
```

Open the CSV in Excel or VS Code to inspect all question-level results.

### Step 6 – Label the experiment
The run is labelled **Release v0.1**, as required by the practical.

## Scoring logic

- Keyword coverage = `(number of matched expected keywords / number of expected keywords) × 100`.
- `PASS` when score is at least 60%.
- `REVIEW` when score is below 60%.
- `ERROR` when a request fails or the model endpoint cannot be reached.
- Average keyword coverage is calculated across successful responses only.

This is a simple keyword-based baseline, not a semantic or factuality evaluation.

## Test the code without Ollama

```powershell
python -m unittest -v
```

The unit tests validate the 30-question JSON, scoring, invalid input handling and evaluation flow. The model call is mocked in the test, so Ollama is not needed for unit tests.

## Troubleshooting

- **`ollama` is not recognized:** install Ollama and reopen PowerShell.
- **Connection refused at localhost:11434:** start the Ollama application/service and retry.
- **Model not found:** run `ollama pull llama3.2`.
- **Python package missing:** activate `.venv` and run `python -m pip install -r requirements.txt`.
- **Slow first response:** the model may need to load into memory on its first request.

## Source alignment

The 30 question prompts, expected answers, keywords and source URLs are transcribed from the Week 6 practical handout (pages 1–6). The baseline workflow follows its `main.py` example (pages 6–15), including local Ollama endpoint, `llama3.2`, deterministic temperature 0, keyword scoring, CSV output and release label v0.1. Page 16 asks students to document the first Llama 3.2 evaluation and label it Release v0.1.

## Important

The example output in this folder describes the output structure only. It is not claimed to be a real Ollama evaluation. Run `python main.py` locally to produce your genuine `baseline_results.csv`.
