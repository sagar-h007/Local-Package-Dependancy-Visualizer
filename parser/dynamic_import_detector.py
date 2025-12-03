"""
Dynamic Import Detector - Detects risky dynamic imports in Python code.
"""

import ast
from typing import List, Tuple, Dict
from pathlib import Path


class DynamicImportDetector:
    """Detects dynamic imports that may be risky or hard to analyze."""
    
    def __init__(self):
        """Initialize the dynamic import detector."""
        self.dynamic_imports: Dict[str, List[Tuple[int, str, str]]] = {}  # file -> [(line, pattern, reason), ...]