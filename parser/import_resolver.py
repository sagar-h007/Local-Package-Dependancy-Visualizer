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
    def resolve_import(self, import_name: str, from_file: str) -> Optional[str]:
        """
        Resolve an import name to a file path.
        
        Args:
            import_name: The import name (e.g., 'os', 'myproject.module', 'myproject.module.function')
            from_file: The file where the import occurs
            
        Returns:
            Resolved file path or None if not found in project
        """
        from_file_path = Path(from_file).resolve()
        from_dir = from_file_path.parent
        
        # Handle relative imports
        if import_name.startswith('.'):
            # Relative import
            base_module = self.file_to_module.get(str(from_file_path), '')
            if not base_module:
                return None
            
            # Count leading dots
            dots = len(import_name) - len(import_name.lstrip('.'))
            module_parts = base_module.split('.')[:-dots] if dots > 0 else base_module.split('.')
            remaining = import_name.lstrip('.')
            
            if remaining:
                module_parts.append(remaining)
            resolved_module = '.'.join(module_parts)
            return self.module_to_file.get(resolved_module)
        
        # Handle absolute imports
        # Try exact match first
        if import_name in self.module_to_file:
            return self.module_to_file[import_name]
        
        # Try as package (check if it's a directory with __init__.py)
        parts = import_name.split('.')
        for i in range(len(parts), 0, -1):
            potential_module = '.'.join(parts[:i])
            if potential_module in self.module_to_file:
                return self.module_to_file[potential_module]
        
        # Try to find in same directory or parent directories
        potential_paths = [
            from_dir / f"{import_name}.py",
            from_dir / import_name / "__init__.py",
        ]
        
        # Check parent directories
        current = from_dir
        while current != self.project_root.parent:
            potential_paths.extend([
                current / f"{import_name}.py",
                current / import_name / "__init__.py",
            ])
            current = current.parent
        
        for path in potential_paths:
            if path.exists() and path.is_file():
                return str(path.resolve())
        
        return None