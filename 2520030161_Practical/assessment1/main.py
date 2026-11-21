"""
Assessment 1: BPE and WordPiece Tokenization

Training corpus (word: frequency):
    low: 5
    lower: 2
    newest: 3
    wildest: 6

Both algorithms begin with character tokens. BPE chooses the most frequent
adjacent pair. WordPiece chooses the pair with the largest score:
    score(a, b) = frequency(a, b) / (frequency(a) * frequency(b))

Pair and token frequencies are weighted by each word's corpus frequency.
"""

from collections import Counter
from dataclasses import dataclass
from typing import Dict, List, Tuple

CORPUS = {
    "low": 5,
    "lower": 2,
    "newest": 3,
    "wildest": 6,
}


@dataclass
class TrainingResult:
    algorithm: str
    merges: List[Tuple[str, str, str, float]]
    final_tokens: Dict[str, List[str]]


def initial_tokenize(corpus: Dict[str, int]) -> Dict[str, List[str]]:
    """Split every word into characters."""
    return {word: list(word) for word in corpus}


def count_tokens(tokenized: Dict[str, List[str]],
                 corpus: Dict[str, int]) -> Counter:
    """Count tokens, weighted by word frequency."""
    counts = Counter()
    for word, tokens in tokenized.items():
        counts.update({token: tokens.count(token) * corpus[word]
                       for token in set(tokens)})
    return counts


def count_pairs(tokenized: Dict[str, List[str]],
                corpus: Dict[str, int]) -> Counter:
    """Count adjacent token pairs, weighted by word frequency."""
    counts = Counter()
    for word, tokens in tokenized.items():
        for pair in zip(tokens, tokens[1:]):
            counts[pair] += corpus[word]
    return counts


def merge_pair(tokenized: Dict[str, List[str]],
               pair: Tuple[str, str]) -> Dict[str, List[str]]:
    """Merge every non-overlapping occurrence of pair in each word."""
    merged = {}
    new_token = pair[0] + pair[1]
    for word, tokens in tokenized.items():
        output = []
        i = 0
        while i < len(tokens):
            if i + 1 < len(tokens) and (tokens[i], tokens[i + 1]) == pair:
                output.append(new_token)
                i += 2
            else:
                output.append(tokens[i])
                i += 1
        merged[word] = output
    return merged


def train_bpe(corpus: Dict[str, int] = None,
              max_merges: int = 100) -> TrainingResult:
    """Train BPE by repeatedly merging the most frequent adjacent pair."""
    corpus = corpus or CORPUS
    tokenized = initial_tokenize(corpus)
    merges = []

    for _ in range(max_merges):
        pair_counts = count_pairs(tokenized, corpus)
        if not pair_counts:
            break

        # Deterministic tie-break: alphabetical order of the pair.
        best_pair = min(pair_counts,
                        key=lambda pair: (-pair_counts[pair], pair))
        frequency = pair_counts[best_pair]
        merged_token = best_pair[0] + best_pair[1]
        merges.append((best_pair[0], best_pair[1],
                       merged_token, float(frequency)))
        tokenized = merge_pair(tokenized, best_pair)

    return TrainingResult("BPE", merges, tokenized)


def train_wordpiece(corpus: Dict[str, int] = None,
                    max_merges: int = 100) -> TrainingResult:
    """
    Train a simplified WordPiece tokenizer.

    At each iteration, calculate:
      score(pair) = pair_count / (first_token_count * second_token_count)
    Then merge the pair with the highest score.
    """
    corpus = corpus or CORPUS
    tokenized = initial_tokenize(corpus)
    merges = []

    for _ in range(max_merges):
        pair_counts = count_pairs(tokenized, corpus)
        if not pair_counts:
            break

        token_counts = count_tokens(tokenized, corpus)
        scores = {}
        for pair, pair_frequency in pair_counts.items():
            first_count = token_counts[pair[0]]
            second_count = token_counts[pair[1]]
            if first_count and second_count:
                scores[pair] = pair_frequency / (first_count * second_count)

        if not scores:
            break

        # Deterministic tie-break: alphabetical order of the pair.
        best_pair = min(scores, key=lambda pair: (-scores[pair], pair))
        score = scores[best_pair]
        merged_token = best_pair[0] + best_pair[1]
        merges.append((best_pair[0], best_pair[1],
                       merged_token, score))
        tokenized = merge_pair(tokenized, best_pair)

    return TrainingResult("WordPiece", merges, tokenized)


def print_result(result: TrainingResult) -> None:
    print(f"\n{'=' * 60}")
    print(f"{result.algorithm} TRAINING")
    print("=" * 60)
    print("Merge steps:")
    for step, (first, second, merged, value) in enumerate(result.merges, 1):
        if result.algorithm == "BPE":
            print(f"{step:2}. ({first}, {second}) -> {merged} "
                  f"[pair frequency = {int(value)}]")
        else:
            print(f"{step:2}. ({first}, {second}) -> {merged} "
                  f"[score = {value:.6f}]")

    print("\nFinal segmentation:")
    for word, tokens in result.final_tokens.items():
        print(f"{word:8} -> {' | '.join(tokens)}")
    vocabulary = sorted({token for tokens in result.final_tokens.values()
                         for token in tokens})
    print("\nFinal vocabulary:", vocabulary)


def main() -> None:
    print("ASSESSMENT 1: BPE AND WORDPIECE")
    print("Training corpus:", CORPUS)

    initial = initial_tokenize(CORPUS)
    print("\nInitial character-level tokens:")
    for word, tokens in initial.items():
        print(f"{word:8} -> {' | '.join(tokens)}")

    print("\nInitial adjacent-pair frequencies:")
    for pair, count in sorted(count_pairs(initial, CORPUS).items()):
        print(f"{pair}: {count}")

    bpe_result = train_bpe()
    wordpiece_result = train_wordpiece()
    print_result(bpe_result)
    print_result(wordpiece_result)

    print("\nCOMPARISON")
    print("BPE selects the pair with the highest raw pair frequency.")
    print("WordPiece selects the pair with the highest normalized score.")
    print("Therefore, their merge order and final segmentation can differ.")


if __name__ == "__main__":
    main()
