"""
Import Resolver - Resolves import statements to actual file paths.
"""

import importlib.util
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple


class ImportResolver:
    """Resolves import names to actual file paths in the project."""
    
    def __init__(self, project_root: str):
        """
        Initialize the import resolver.
        
        Args:
            project_root: Root directory of the Python project
        """
        self.project_root = Path(project_root).resolve()
        self.module_to_file: Dict[str, str] = {}  # module_name -> file_path
        self.file_to_module: Dict[str, str] = {}  # file_path -> module_name
        self._build_module_map()
    
    def _build_module_map(self):
        """Build a mapping of module names to file paths."""
        # Walk through all Python files and map them to module names
        for py_file in self.project_root.rglob('*.py'):
            if '__pycache__' in str(py_file):
                continue
            
            relative_path = py_file.relative_to(self.project_root)
            # Convert file path to module name
            module_parts = list(relative_path.parts[:-1])  # Exclude filename
            module_name = '.'.join(module_parts) if module_parts else ''
            
            file_stem = py_file.stem
            if file_stem == '__init__':
                if module_name:
                    module_name = module_name
                else:
                    module_name = ''
            else:
                if module_name:
                    module_name = f"{module_name}.{file_stem}"
                else:
                    module_name = file_stem
            
            file_str = str(py_file)
            self.module_to_file[module_name] = file_str
            self.file_to_module[file_str] = module_name