# Assessment 1 – BPE and WordPiece Tokenization

## Problem understood from the handwritten notes

The training vocabulary and weighted frequencies are:

| Word | Frequency |
|---|---:|
| low | 5 |
| lower | 2 |
| newest | 3 |
| wildest | 6 |

The program uses these frequencies when counting tokens and adjacent pairs.

## Algorithms implemented

### 1. BPE (Byte Pair Encoding)
1. Split each word into individual characters.
2. Count every adjacent token pair, weighted by the word frequency.
3. Merge the pair with the highest frequency.
4. Recount pairs and repeat until no adjacent pairs remain (or `max_merges` is reached).

### 2. WordPiece
1. Start from the same character-level tokenization.
2. Count token frequencies and adjacent-pair frequencies.
3. Calculate `score(a, b) = frequency(a, b) / (frequency(a) * frequency(b))`.
4. Merge the pair with the highest score, then recalculate and repeat.

A deterministic alphabetical tie-break is used when scores/frequencies are equal.

## Run the program

Python 3.9 or later is recommended. No external packages are needed.

```bash
python3 main.py
```

## Run tests

```bash
python3 -m unittest -v
```

## Files

- `main.py` – complete BPE and WordPiece implementation and printed comparison
- `test_main.py` – unit tests
- `requirements.txt` – no third-party dependencies required
- `output_example.txt` – sample program output

## Important implementation note

This is a clear educational implementation of the merge-training steps shown in the notes. It uses whole-word character sequences and does not add end-of-word markers or the continuation-prefix convention used by some production tokenizers. The handwritten notes do not specify those conventions, so they are not silently added here.
