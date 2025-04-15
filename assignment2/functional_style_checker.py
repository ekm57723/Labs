import ast
import os
import re
from typing import List, Dict, Tuple, Optional, Union

def get_file_path() -> str:
    while True:
        file_path = input("Enter the path to the Python file to analyze: ").strip()
        if os.path.isfile(file_path) and file_path.endswith('.py'):
            return file_path
        print("Invalid file path or not a Python file. Please try again.")

def parse_file(file_path: str) -> ast.Module:
    with open(file_path, 'r', encoding='utf-8') as f:
        tree = ast.parse(f.read(), filename=file_path)
    
    for node in ast.walk(tree):
        for child in ast.iter_child_nodes(node):
            child.parent = node
    
    return tree

def get_file_structure_data(tree: ast.Module, file_path: str) -> Dict[str, Union[int, List[str]]]:
    total_lines = sum(1 for _ in open(file_path, 'r', encoding='utf-8'))
    
    imports = [
        node.names[0].name for node in ast.walk(tree) 
        if isinstance(node, ast.Import)
    ] + [
        node.module for node in ast.walk(tree) 
        if isinstance(node, ast.ImportFrom)
    ]
    
    classes = [
        node.name for node in ast.walk(tree) 
        if isinstance(node, ast.ClassDef)
    ]
    
    functions = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            if hasattr(node, "parent") and isinstance(node.parent, ast.ClassDef):
                functions.append(f"{node.parent.name}.{node.name}")
            else:
                functions.append(node.name)
    
    return {
        'total_lines': total_lines,
        'imports': imports,
        'classes': classes,
        'functions': functions
    }

def get_docstrings(tree: ast.Module) -> List[Tuple[str, Optional[str]]]:
    docstrings = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
            docstring = ast.get_docstring(node)
            name = node.name
            if isinstance(node, ast.FunctionDef):
                if hasattr(node, "parent") and isinstance(node.parent, ast.ClassDef):
                    name = f"{node.parent.name}.{name}"
            docstrings.append((name, docstring))
    return docstrings

def check_type_annotations(tree: ast.Module) -> List[str]:
    missing = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            has_args_annotations = any(
                arg.annotation is not None 
                for arg in node.args.args
            )
            if not has_args_annotations or node.returns is None:
                missing.append(node.name)
    return missing

def check_naming_conventions(tree: ast.Module) -> Tuple[List[str], List[str]]:
    camel_case = re.compile(r'^[A-Z][a-zA-Z0-9]*$')
    snake_case = re.compile(r'^[a-z_][a-z0-9_]*$')
    
    bad_classes = []
    bad_functions = []
    
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef) and not camel_case.match(node.name):
            bad_classes.append(node.name)
        if isinstance(node, ast.FunctionDef) and not snake_case.match(node.name):
            bad_functions.append(node.name)
    
    return (bad_classes, bad_functions)

def generate_report_content(
    file_structure: Dict[str, Union[int, List[str]]],
    docstrings: List[Tuple[str, Optional[str]]],
    missing_annotations: List[str],
    naming_violations: Tuple[List[str], List[str]]
) -> str:
    report_lines = []
    
    # File structure section
    report_lines.append("=== File Structure ===\n")
    report_lines.append(f"Total Lines of Code: {file_structure['total_lines']}\n")
    report_lines.append(f"Imports: {', '.join(file_structure['imports']) if file_structure['imports'] else 'None'}\n")
    report_lines.append(f"Classes: {', '.join(file_structure['classes']) if file_structure['classes'] else 'None'}\n")
    report_lines.append(f"Functions: {', '.join(file_structure['functions']) if file_structure['functions'] else 'None'}\n")
    
    report_lines.append("\n=== DocStrings ===\n")
    for name, docstring in docstrings:
        report_lines.append(f"{name}: {docstring if docstring else 'DocString not found'}\n")
    
    report_lines.append("\n=== Type Annotations ===\n")
    if missing_annotations:
        report_lines.append(f"Functions missing type annotations: {', '.join(missing_annotations)}\n")
    else:
        report_lines.append("All functions have type annotations.\n")
    
    report_lines.append("\n=== Naming Conventions ===\n")
    bad_classes, bad_functions = naming_violations
    if bad_classes:
        report_lines.append(f"Classes violating naming conventions: {', '.join(bad_classes)}\n")
    if bad_functions:
        report_lines.append(f"Functions violating naming conventions: {', '.join(bad_functions)}\n")
    if not bad_classes and not bad_functions:
        report_lines.append("All naming conventions followed correctly.\n")
    
    return ''.join(report_lines)

def write_report(file_path: str, content: str) -> str:
    file_name = os.path.basename(file_path).replace('.py', '')
    report_path = f"style_report_{file_name}.txt"
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(content)
    return report_path

def analyze_python_file(file_path: str) -> str:
    tree = parse_file(file_path)
    
    file_structure = get_file_structure_data(tree, file_path)
    docstrings = get_docstrings(tree)
    missing_annotations = check_type_annotations(tree)
    naming_violations = check_naming_conventions(tree)
    
    report_content = generate_report_content(
        file_structure,
        docstrings,
        missing_annotations,
        naming_violations
    )
    
    report_path = write_report(file_path, report_content)
    return report_path

def main():
    file_path = get_file_path()
    report_path = analyze_python_file(file_path)
    print(f"Report generated: {report_path}")

if __name__ == "__main__":
    main()