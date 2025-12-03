"""
Graph Builder - Constructs dependency graph from parsed imports.
"""

from typing import Dict, List, Set, Tuple, Optional
from pathlib import Path
from collections import defaultdict


class GraphBuilder:
    """Builds a dependency graph from parsed imports."""
    
    def __init__(self, project_root: str):
        """
        Initialize the graph builder.
        
        Args:
            project_root: Root directory of the Python project
        """
        self.project_root = Path(project_root).resolve()
        self.nodes: Set[str] = set()  # All file nodes
        self.edges: List[Tuple[str, str, Dict]] = []  # (from, to, metadata)
        self.incoming: Dict[str, Set[str]] = defaultdict(set)  # to -> {from, ...}
        self.outgoing: Dict[str, Set[str]] = defaultdict(set)  # from -> {to, ...}
        self.node_metadata: Dict[str, Dict] = {}  # file -> metadata
    def add_node(self, file_path: str, metadata: Optional[Dict] = None):
        """
        Add a node to the graph.
        
        Args:
            file_path: Path to the file (normalized)
            metadata: Optional metadata about the node
        """
        normalized = self._normalize_path(file_path)        #clean the path
        self.nodes.add(normalized)      #add files to set of nodes
        if metadata:                            #add extra data if provided
            self.node_metadata[normalized] = metadata
        elif normalized not in self.node_metadata:
            self.node_metadata[normalized] = {}
    def add_edge(self, from_file: str, to_file: str, metadata: Optional[Dict] = None):
        """
        Add an edge to the graph.
        
        Args:
            from_file: Source file path
            to_file: Target file path
            metadata: Optional metadata about the edge
        """
        from_normalized = self._normalize_path(from_file)
        to_normalized = self._normalize_path(to_file)
        
        # Only add edges between project files
        if from_normalized not in self.nodes:
            self.add_node(from_normalized)
        if to_normalized not in self.nodes:
            self.add_node(to_normalized)
        
        edge_metadata = metadata or {}
        self.edges.append((from_normalized, to_normalized, edge_metadata))
        self.incoming[to_normalized].add(from_normalized)       #record who imports the file 
        self.outgoing[from_normalized].add(to_normalized)       #store in list
    