"""
Module Analyzer - Analyzes module size and complexity.
"""

from typing import Dict, List, Tuple
from pathlib import Path


class ModuleAnalyzer:
    """Analyzes modules for size, complexity, and other metrics."""
    
    def __init__(self, graph, parser):
        """
        Initialize the module analyzer.
        
        Args:
            graph: GraphBuilder instance
            parser: ASTParser instance
        """
        self.graph = graph
        self.parser = parser
        self.metrics: Dict[str, Dict] = {}
    
    def analyze_all_modules(self) -> Dict[str, Dict]:
        """
        Analyze all modules and compute metrics.
        
        Returns:
            Dictionary mapping file paths to metrics
        """
        self.metrics = {}
        
        for file_path in self.graph.get_all_nodes():
            metrics = self._analyze_module(file_path)
            self.metrics[file_path] = metrics
        
        return self.metrics.copy()
    
    def _analyze_module(self, file_path: str) -> Dict:
        """Analyze a single module and return metrics."""
        line_count = self.parser.get_line_count(file_path)
        exports = self.parser.get_exports(file_path)
        dependencies = self.graph.get_dependencies(file_path)
        dependents = self.graph.get_dependents(file_path)
        
        metadata = self.graph.get_metadata(file_path)
        
        return {
            'line_count': line_count,
            'export_count': len(exports),
            'dependency_count': len(dependencies),
            'dependent_count': len(dependents),
            'fan_in': len(dependents),
            'fan_out': len(dependencies),
            'complexity_score': self._calculate_complexity(
                line_count, len(dependencies), len(dependents)
            ),
        }

