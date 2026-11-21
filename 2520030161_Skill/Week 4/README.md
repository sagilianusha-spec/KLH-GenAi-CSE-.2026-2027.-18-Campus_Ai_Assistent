
# Comparison of BPE, WordPiece and SentencePiece Tokenizers

## Aim
To implement and compare BPE, WordPiece and SentencePiece tokenizers using English, Telugu and Hindi text.

## Learning Objectives
- Understand tokenization.
- Compare word-level and subword-level splitting.
- Observe token pieces and token counts.
- Understand differences between tokenizer vocabularies.

## Technologies Used
- Python
- Google Colab
- Hugging Face Transformers
- SentencePiece

## Tokenizers Used

| Tokenizer | Model |
|---|---|
| BPE | GPT-2 |
| WordPiece | bert-base-multilingual-cased |
| SentencePiece | xlm-roberta-base |

## Languages
- English
- Telugu
- Hindi

## Installation

pip install -r requirements.txt

## Execution

python tokenizer_comparison.py

## Output
The program displays tokens, token IDs and token counts for all three languages.

## Conclusion
This practical compares how different pretrained tokenizers split English, Telugu and Hindi text into subword tokens.
