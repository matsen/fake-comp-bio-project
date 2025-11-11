"""UPGMA tree building from DNA sequences.

This module provides functions for building phylogenetic trees
from DNA sequences using the UPGMA algorithm.
"""

from typing import Dict
from Bio.Phylo.TreeConstruction import DistanceMatrix, DistanceTreeConstructor
from Bio.Phylo.BaseTree import Tree


def build_upgma_tree_from_sequences(sequences: Dict[str, str]) -> Tree:
    """Build a UPGMA tree from sequences using Hamming distance.

    This is a monolithic V1 implementation that computes Hamming distances
    directly and builds the tree in one function.

    Args:
        sequences: Dictionary mapping sequence names to DNA sequence strings.
                  All sequences must be the same length (aligned).

    Returns:
        A BioPython Tree object representing the UPGMA phylogenetic tree.

    Raises:
        ValueError: If sequences have different lengths.

    Example:
        >>> sequences = {
        ...     'seq_a': 'ATCG',
        ...     'seq_b': 'ATCC',
        ...     'seq_c': 'TTCG'
        ... }
        >>> tree = build_upgma_tree_from_sequences(sequences)
        >>> len(tree.get_terminals())
        3
    """
    # Validate that all sequences have the same length
    seq_list = list(sequences.values())
    seq_names = list(sequences.keys())

    if not seq_list:
        raise ValueError("sequences dictionary cannot be empty")

    seq_length = len(seq_list[0])
    if not all(len(seq) == seq_length for seq in seq_list):
        raise ValueError("All sequences must have the same length for Hamming distance")

    # Compute pairwise Hamming distances
    n = len(seq_list)
    distance_values = []

    for i in range(n):
        row = []
        for j in range(i + 1):
            if i == j:
                row.append(0.0)
            else:
                # Compute Hamming distance between seq_list[i] and seq_list[j]
                hamming_dist = sum(c1 != c2 for c1, c2 in zip(seq_list[i], seq_list[j]))
                row.append(float(hamming_dist))
        distance_values.append(row)

    # Create BioPython DistanceMatrix
    dm = DistanceMatrix(names=seq_names, matrix=distance_values)

    # Build UPGMA tree using BioPython
    constructor = DistanceTreeConstructor()
    tree = constructor.upgma(dm)

    return tree
