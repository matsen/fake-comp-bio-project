"""Tests for UPGMA tree building."""

import pytest
from fakephylo.tree_builder import build_upgma_tree_from_sequences


def test_upgma_3_sequences_basic():
    """Test UPGMA with 3 sequences - basic functionality."""
    sequences = {
        "A": "AAAAAAAAAA",  # 10 A's
        "B": "AAAAACAAAA",  # 9 A's, 1 C (Hamming distance 1 from A)
        "C": "AACCAAAAAA",  # 8 A's, 2 C's (Hamming distance 2 from A, 3 from B)
    }

    tree = build_upgma_tree_from_sequences(sequences)

    # Verify tree structure
    assert tree is not None
    terminals = tree.get_terminals()
    assert len(terminals) == 3
    assert {t.name for t in terminals} == {"A", "B", "C"}


def test_upgma_ultrametric_property():
    """Test that UPGMA produces ultrametric trees (all leaves equidistant from root)."""
    sequences = {"A": "AAAAAAAAAA", "B": "AAAAACAAAA", "C": "AACCAAAAAA"}

    tree = build_upgma_tree_from_sequences(sequences)

    # Verify ultrametric property - all leaves should be equidistant from root
    root = tree.root
    terminals = tree.get_terminals()
    distances = [tree.distance(root, leaf) for leaf in terminals]

    # All distances should be equal (within floating point tolerance)
    assert all(abs(d - distances[0]) < 0.01 for d in distances), (
        f"Expected all distances to be equal, got {distances}"
    )


def test_upgma_5_sequences():
    """Test UPGMA with 5 sequences to verify more complex clustering."""
    sequences = {
        "a": "ATCGATCGATCGATCG",
        "b": "ATCGATCGATCGATCC",  # 1 difference from a
        "c": "ATCGATCGAACGATCG",  # 2 differences from a
        "d": "TTCGATCGATCGATCG",  # 1 difference from a
        "e": "ATCGTTCGATCGATCG",  # 2 differences from a
    }

    tree = build_upgma_tree_from_sequences(sequences)

    # Verify all sequences appear in tree
    terminals = tree.get_terminals()
    assert len(terminals) == 5
    assert {t.name for t in terminals} == {"a", "b", "c", "d", "e"}

    # Verify ultrametric property
    root = tree.root
    distances = [tree.distance(root, leaf) for leaf in terminals]
    assert all(abs(d - distances[0]) < 0.01 for d in distances), (
        f"Expected all distances to be equal, got {distances}"
    )


def test_upgma_identical_sequences():
    """Test UPGMA with identical sequences (distance 0)."""
    sequences = {
        "seq1": "ATCGATCG",
        "seq2": "ATCGATCG",  # Identical to seq1
        "seq3": "TTCGATCG",  # Different
    }

    tree = build_upgma_tree_from_sequences(sequences)

    # Tree should still be built successfully
    terminals = tree.get_terminals()
    assert len(terminals) == 3
    assert {t.name for t in terminals} == {"seq1", "seq2", "seq3"}


def test_upgma_error_unequal_lengths():
    """Test that unequal sequence lengths raise an error."""
    sequences = {
        "seq1": "ATCGATCG",
        "seq2": "ATCGCC",  # Shorter - should fail
        "seq3": "TTCGATCG",
    }

    with pytest.raises(ValueError, match="same length"):
        build_upgma_tree_from_sequences(sequences)


def test_upgma_error_empty_sequences():
    """Test that empty sequences dictionary raises an error."""
    sequences = {}

    with pytest.raises(ValueError, match="cannot be empty"):
        build_upgma_tree_from_sequences(sequences)


def test_upgma_two_sequences():
    """Test UPGMA with two sequences."""
    sequences = {
        "seq1": "ATCGATCG",
        "seq2": "TTCGATCG",  # 1 difference
    }

    tree = build_upgma_tree_from_sequences(sequences)

    # Should produce a tree with two terminals
    terminals = tree.get_terminals()
    assert len(terminals) == 2
    assert {t.name for t in terminals} == {"seq1", "seq2"}

    # Verify ultrametric property
    root = tree.root
    distances = [tree.distance(root, leaf) for leaf in terminals]
    assert abs(distances[0] - distances[1]) < 0.01


def test_upgma_hamming_distance_calculation():
    """Test that Hamming distances are computed correctly."""
    sequences = {
        "A": "AAAA",  # Reference
        "B": "AAAC",  # Distance 1 from A
        "C": "AACC",  # Distance 2 from A, 1 from B
    }

    tree = build_upgma_tree_from_sequences(sequences)

    # A and B should be clustered first (distance 1)
    # Then joined with C
    terminals = tree.get_terminals()
    assert len(terminals) == 3

    # Verify the tree is ultrametric
    root = tree.root
    distances = [tree.distance(root, leaf) for leaf in terminals]
    assert all(abs(d - distances[0]) < 0.01 for d in distances)
