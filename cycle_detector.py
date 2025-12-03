"""
Cycle Detector - Detects circular dependencies in the dependency graph.
"""

from typing import List, Set, Dict, Tuple
from collections import defaultdict


class CycleDetector:
    """Detects cycles (circular dependencies) in a dependency graph."""
    
    def __init__(self, graph):
        """
        Initialize the cycle detector.
        
        Args:
            graph: GraphBuilder instance
        """
        self.graph = graph
        self.cycles: List[List[str]] = []
        self._visited: Set[str] = set()
        self._recursion_stack: Set[str] = set()
        self._cycle_paths: List[List[str]] = []
    
    def detect_cycles(self) -> List[List[str]]:
        """
        Detect all cycles in the dependency graph.
        
        Returns:
            List of cycles, where each cycle is a list of file paths
        """
        self.cycles = []
        self._visited = set()
        self._recursion_stack = set()
        self._cycle_paths = []
        
        for node in self.graph.get_all_nodes():
            if node not in self._visited:
                self._dfs(node, [])
        
        return self.cycles.copy()

