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
    """Test that UPGMA works with small Hamming distances.

    Note: With distances d(A,B)=1, d(A,C)=2, d(B,C)=1, there's a tie
    so clustering order depends on implementation. This test just
    verifies the tree is built correctly (has all sequences, ultrametric).
    """
    sequences = {
        "A": "AAAA",  # Reference
        "B": "AAAC",  # Distance 1 from A
        "C": "AACC",  # Distance 2 from A, 1 from B
    }

    tree = build_upgma_tree_from_sequences(sequences)

    # Verify all sequences present
    terminals = tree.get_terminals()
    assert len(terminals) == 3

    # Verify the tree is ultrametric
    root = tree.root
    distances = [tree.distance(root, leaf) for leaf in terminals]
    assert all(abs(d - distances[0]) < 0.01 for d in distances)


def test_upgma_tree_topology():
    """Test that UPGMA produces correct tree topology based on distances.

    With these sequences (deliberately no ties):
    - A and B differ by 1 position (closest pair, should cluster first)
    - C differs by 3 from both A and B (should join AB cluster last)

    Expected topology: ((A, B), C)
    """
    sequences = {
        "A": "AAAA",  # Reference
        "B": "AAAC",  # Distance 1 from A
        "C": "ACCC",  # Distance 3 from A, 3 from B
    }

    tree = build_upgma_tree_from_sequences(sequences)

    # Get terminals
    terminals = {t.name: t for t in tree.get_terminals()}

    # A and B should share a common ancestor that is NOT the root
    # (because C joins them later)
    a_node = terminals["A"]
    b_node = terminals["B"]
    c_node = terminals["C"]

    # Find the most recent common ancestor of A and B
    mrca_ab = tree.common_ancestor(a_node, b_node)

    # Find the most recent common ancestor of A and C
    mrca_ac = tree.common_ancestor(a_node, c_node)

    # The MRCA of A and B should be different from (and closer than) the MRCA of A and C
    assert mrca_ab != mrca_ac, "A and B should cluster together before C joins"

    # The MRCA of A and C should be the root (since it includes all three sequences)
    assert mrca_ac == tree.root, "The MRCA of A and C should be the root"

    # Verify that the MRCA of A and B is a child of the root
    assert mrca_ab in tree.root.clades, "A-B cluster should be a direct child of root"

    # The root should have exactly 2 children: the A-B cluster and C
    assert len(tree.root.clades) == 2, "Root should have exactly 2 children"

    # One child should be the A-B cluster, the other should contain only C
    root_child_terminals = [
        set(t.name for t in clade.get_terminals()) for clade in tree.root.clades
    ]
    assert {"A", "B"} in root_child_terminals, "One root child should be A-B cluster"
    assert {"C"} in root_child_terminals, "Other root child should be C alone"


def test_upgma_pairwise_distances():
    """Test that pairwise distances in the tree match expected values.

    Hamming distances:
    - d(A, B) = 1 (differ at position 3)
    - d(A, C) = 3 (differ at positions 1, 2, 3)
    - d(B, C) = 2 (differ at positions 1, 2)

    UPGMA clustering:
    1. Cluster A and B first at distance 1 (both at height 0.5 from their MRCA)
    2. Join C to AB cluster at average distance (3 + 2) / 2 = 2.5
    3. All leaves are equidistant from root (ultrametric property)
    """
    sequences = {
        "A": "AAAA",  # Reference
        "B": "AAAC",  # Hamming distance 1 from A
        "C": "ACCC",  # Hamming distance 3 from A, 2 from B
    }

    tree = build_upgma_tree_from_sequences(sequences)
    terminals = {t.name: t for t in tree.get_terminals()}

    # Get pairwise distances in the tree
    dist_a_b = tree.distance(terminals["A"], terminals["B"])
    dist_a_c = tree.distance(terminals["A"], terminals["C"])
    dist_b_c = tree.distance(terminals["B"], terminals["C"])

    # Verify A-B distance (both at height 0.5 from MRCA, sum = 1.0)
    assert 0.9 < dist_a_b < 1.1, f"Expected A-B distance ~1.0, got {dist_a_b}"

    # C is farther from both A and B than they are from each other
    assert dist_a_c > dist_a_b, "A-C should be farther than A-B"
    assert dist_b_c > dist_a_b, "B-C should be farther than A-B"

    # Verify ultrametric property: all leaves equidistant from root
    root = tree.root
    height_a = tree.distance(root, terminals["A"])
    height_b = tree.distance(root, terminals["B"])
    height_c = tree.distance(root, terminals["C"])

    assert abs(height_a - height_b) < 0.01, "A and B should be equidistant from root"
    assert abs(height_a - height_c) < 0.01, "A and C should be equidistant from root"
    assert abs(height_b - height_c) < 0.01, "B and C should be equidistant from root"
