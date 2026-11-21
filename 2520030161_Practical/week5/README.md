# Week 5 – Token Economics: Cost and Rate-Limit Budgeting

**Course:** LLM Application Engineering – Practical Lab  
**Experiment:** 5  
**Objective:** Estimate token usage and hosted API cost, check RPM/TPM capacity, and compare forecasts with daily and monthly budgets before building an LLM feature.

## Project structure

```text
Week5_TokenEconomics/
├── budget.py
├── test_budget.py
├── .env.example
├── .gitignore
├── requirements.txt
├── output.txt
└── README.md
```

## Requirements

- Python 3.9+
- pip

## Setup and run

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python budget.py
```

### Windows PowerShell

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
python budget.py
```

Edit `.env` to use the actual model prices, provider quotas, traffic forecast, and project budgets. `.env` is intentionally excluded from Git.

## Run automated tests

```bash
python -m unittest -v
```

The tests validate cost calculations, successful capacity checks, RPM failure, monthly-budget failure, and negative-input validation. No LLM API call is made.

## Formulas

Let `R` = requests/day, `I` = average input tokens/request, `O` = average output tokens/request, and `Pi` / `Po` = input/output price per million tokens.

- Input tokens/day = `R × I`
- Output tokens/day = `R × O`
- Total tokens/day = `R × (I + O)`
- Daily cost = `[(R × I × Pi) + (R × O × Po)] / 1,000,000`
- Monthly cost = `Daily cost × 30`
- Peak RPM with margin = `Peak requests/minute × (1 + margin/100)`
- Peak total TPM with margin = `Peak requests/minute × (I + O) × (1 + margin/100)`

The program checks RPM, simplified total TPM, daily budget, and monthly budget after applying the safety margin to forecast usage/cost.

## Sample assumptions and expected result

The included `.env.example` uses the lab's illustrative values: 2,000 requests/day, 1,200 input tokens/request, 300 output tokens/request, peak 30 requests/minute, input price $0.30/M tokens, output price $1.20/M tokens, 20% margin, daily budget $2, monthly budget $50, RPM limit 60, and TPM limit 100,000.

Expected estimates:

| Metric | Expected |
|---|---:|
| Input tokens/day | 2,400,000 |
| Output tokens/day | 600,000 |
| Total tokens/day | 3,000,000 |
| Daily estimated cost | $1.4400 |
| 30-day estimated cost | $43.20 |
| Peak RPM with 20% margin | 36 |
| Peak total TPM with 20% margin | 54,000 |

With the exact sample values above, RPM, TPM, and daily budget pass, but the monthly budget check is **REVIEW**: the program applies the 20% safety margin to the $43.20 monthly estimate ($51.84), which is above the configured $50 threshold. The lab handout's prose says the sample is within the monthly budget, but its supplied `monthly_budget_cost * margin <= monthly_budget` check produces REVIEW. This project preserves the check logic and makes the discrepancy visible rather than hiding it. To obtain a pass, increase `MONTHLY_BUDGET_USD` to at least `51.84` (for example, `55`) or revise the assumptions. See `output.txt` for the captured sample run.

## What-if analysis

Change one variable at a time in `.env`, run `python budget.py`, and compare the report:

1. Double `REQUESTS_PER_DAY`: daily/monthly tokens and costs double.
2. Increase `PEAK_REQUESTS_PER_MINUTE`: RPM and TPM pressure increase.
3. Increase `AVG_INPUT_TOKENS`: input cost and total TPM increase.
4. Increase `AVG_OUTPUT_TOKENS`: output cost and total TPM increase.
5. Reduce `AVG_OUTPUT_TOKENS`: output cost and total TPM decrease.
6. Increase token prices: cost rises without changing token volume.

## Important notes

- This is a planning estimate, not a billing guarantee.
- Character-based estimates are not a tokenizer. Before launch, measure actual token counts with the selected provider tokenizer or usage metadata.
- Include system prompts, conversation history, retrieved context, and tool/function schemas in input estimates.
- Providers may enforce separate input/output TPM limits or other quota dimensions. This lab uses total TPM as a simplified planning check; verify the exact provider definition.
- Retries may add token usage and cost. Include a retry allowance in production forecasts.
- Prices and quotas in `.env.example` are illustrative placeholders, not current provider quotes.

## Learning outcomes

Input/output token estimation, daily/monthly cost forecasting, RPM/TPM capacity planning, safety margins, budget thresholds, automated tests, and pre-build go/no-go decisions.
