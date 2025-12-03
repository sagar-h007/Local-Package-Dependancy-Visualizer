"""
Visualizer - Creates ASCII maps and Graphviz exports.
"""

from typing import Dict, List, Set, Optional
from pathlib import Path
from collections import defaultdict, deque


class Visualizer:
    """Creates visualizations of the dependency graph."""
    
    def __init__(self, graph, project_root: str):
        """
        Initialize the visualizer.
        
        Args:
            graph: GraphBuilder instance
            project_root: Root directory of the project
        """
        self.graph = graph
        self.project_root = Path(project_root).resolve()

