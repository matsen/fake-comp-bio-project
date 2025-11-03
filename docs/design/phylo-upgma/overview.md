# UPGMA Phylogenetic Tree Building

## Motivation

This project demonstrates building phylogenetic trees from DNA sequences using the UPGMA (Unweighted Pair Group Method with Arithmetic Mean) clustering algorithm. The key design goal is **flexibility in distance metrics** - supporting different ways to measure sequence dissimilarity.

## Goals

1. Build phylogenetic trees from DNA sequences
2. Support multiple distance metrics (Hamming, Levenshtein, etc.)
3. Provide a clean, testable API that separates distance calculation from tree construction
4. Demonstrate good software engineering practices for computational biology

## Desired API

The final API separates concerns between computing distances and building trees:

```python
from fakephylo.tree_builder import compute_distance_matrix, build_upgma_tree
from Bio.Phylo.TreeConstruction import DistanceTreeConstructor
import Levenshtein

# Example 1: Using Hamming distance (for aligned sequences)
sequences = {
    'seq_a': 'ATCGATCG',
    'seq_b': 'ATCGATCC',
    'seq_c': 'TTCGATCG'
}

def hamming_distance(seq1, seq2):
    """Hamming distance for equal-length sequences"""
    return sum(c1 != c2 for c1, c2 in zip(seq1, seq2))

dm = compute_distance_matrix(sequences, hamming_distance)
tree = build_upgma_tree(dm)

# Example 2: Using Levenshtein distance (handles unequal lengths)
sequences_unequal = {
    'seq_a': 'ATCGATCG',
    'seq_b': 'ATCGCC',      # Shorter sequence
    'seq_c': 'TTCGATCGAA'   # Longer sequence
}

dm = compute_distance_matrix(sequences_unequal, Levenshtein.distance)
tree = build_upgma_tree(dm)
```

### Core Functions

**`compute_distance_matrix(sequences: Dict[str, str], distance_fn: Callable) -> DistanceMatrix`**

Computes pairwise distances between all sequences using the provided distance function.

- `sequences`: Dictionary mapping sequence names to sequence strings
- `distance_fn`: Function that takes two sequences and returns a numeric distance
- Returns: `Bio.Phylo.TreeConstruction.DistanceMatrix` object

**`build_upgma_tree(distance_matrix: DistanceMatrix) -> Tree`**

Builds a UPGMA tree from a distance matrix using BioPython's tree constructor.

- `distance_matrix`: BioPython DistanceMatrix object
- Returns: `Bio.Phylo.BaseTree.Tree` object

## Test Cases

### Test 1: Hamming Distance with 3 Sequences

Simple test case with aligned sequences of equal length:

```python
def test_hamming_upgma_3_sequences():
    """Test UPGMA with Hamming distance on 3 sequences"""
    sequences = {
        'A': 'AAAAAAAAAA',  # 10 A's
        'B': 'AAAAACAAAA',  # 9 A's, 1 C (distance 1 from A)
        'C': 'AACCAAAAAA'   # 8 A's, 2 C's (distance 2 from A, 3 from B)
    }

    def hamming_distance(seq1, seq2):
        return sum(c1 != c2 for c1, c2 in zip(seq1, seq2))

    dm = compute_distance_matrix(sequences, hamming_distance)
    tree = build_upgma_tree(dm)

    # Verify tree structure
    assert tree is not None
    terminals = tree.get_terminals()
    assert len(terminals) == 3
    assert {t.name for t in terminals} == {'A', 'B', 'C'}

    # Verify ultrametric property (all leaves equidistant from root)
    root = tree.root
    distances = [tree.distance(root, leaf) for leaf in terminals]
    assert all(abs(d - distances[0]) < 0.01 for d in distances)
```

### Test 2: Levenshtein Distance with Unequal Length Sequences

Test case demonstrating flexibility with unequal sequence lengths:

```python
def test_levenshtein_upgma_unequal_lengths():
    """Test UPGMA with Levenshtein distance on sequences of varying length"""
    import Levenshtein

    sequences = {
        'seq1': 'ATCGATCG',      # Length 8
        'seq2': 'ATCGCC',        # Length 6 (2 deletions from seq1)
        'seq3': 'TTCGATCGAA'     # Length 10 (different bases + longer)
    }

    dm = compute_distance_matrix(sequences, Levenshtein.distance)
    tree = build_upgma_tree(dm)

    # Verify tree structure
    assert tree is not None
    terminals = tree.get_terminals()
    assert len(terminals) == 3
    assert {t.name for t in terminals} == {'seq1', 'seq2', 'seq3'}

    # Verify ultrametric property
    root = tree.root
    distances = [tree.distance(root, leaf) for leaf in terminals]
    assert all(abs(d - distances[0]) < 0.01 for d in distances)

    # Levenshtein distance between seq1 and seq2 should be 2
    # (requires deletion of TC and change of CG to CC)
    expected_dist_1_2 = Levenshtein.distance(sequences['seq1'], sequences['seq2'])
    assert expected_dist_1_2 > 0  # They are different
```

### Test 3: Larger Example (5 sequences)

```python
def test_hamming_upgma_5_sequences():
    """Test UPGMA with 5 sequences to verify more complex clustering"""
    sequences = {
        'a': 'ATCGATCGATCGATCG',
        'b': 'ATCGATCGATCGATCC',  # 1 difference from a
        'c': 'ATCGATCGAACGATCG',  # 2 differences from a
        'd': 'TTCGATCGATCGATCG',  # 1 difference from a
        'e': 'ATCGTTCGATCGATCG'   # 2 differences from a
    }

    def hamming_distance(seq1, seq2):
        return sum(c1 != c2 for c1, c2 in zip(seq1, seq2))

    dm = compute_distance_matrix(sequences, hamming_distance)
    tree = build_upgma_tree(dm)

    # Verify all sequences appear in tree
    terminals = tree.get_terminals()
    assert len(terminals) == 5
    assert {t.name for t in terminals} == {'a', 'b', 'c', 'd', 'e'}

    # Verify ultrametric property
    root = tree.root
    distances = [tree.distance(root, leaf) for leaf in terminals]
    assert all(abs(d - distances[0]) < 0.01 for d in distances)
```

## Dependencies

- `biopython`: For phylogenetic tree construction and representation
- `numpy`: For numerical operations on distance matrices
- `pytest`: For testing
- `python-Levenshtein`: For Levenshtein distance metric (optional, only needed for that distance metric)

## Implementation Strategy

The implementation will:

1. Provide a generic distance matrix computation function that accepts any distance function
2. Use BioPython's `DistanceTreeConstructor.upgma()` for tree building
3. Maintain separation between distance calculation and tree construction
4. Support any distance metric that takes two sequences and returns a number

This design enables easy extension to new distance metrics (JC69, Kimura 2-parameter, etc.) without modifying the tree building code.
