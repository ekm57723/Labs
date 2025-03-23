import ast
import os
import re

class StyleChecker:
    def __init__(self, file_path):
        self.file_path = file_path
        self.tree = self._parse_file()
        self.report = []
    
    def _parse_file(self):
        with open(self.file_path, 'r', encoding='utf-8') as f:
            tree = ast.parse(f.read(), filename=self.file_path)
    
        for node in ast.walk(tree):
            for child in ast.iter_child_nodes(node):
                child.parent = node  
    
        return tree
    
    def analyze_file_structure(self):
        total_lines = sum(1 for _ in open(self.file_path, 'r', encoding='utf-8'))
        imports = [node.names[0].name for node in ast.walk(self.tree) if isinstance(node, ast.Import)]
        imports += [node.module for node in ast.walk(self.tree) if isinstance(node, ast.ImportFrom)]
        
        classes = [node.name for node in ast.walk(self.tree) if isinstance(node, ast.ClassDef)]
        functions = []
        for node in ast.walk(self.tree):
            if isinstance(node, ast.FunctionDef):
                if hasattr(node, "parent") and isinstance(node.parent, ast.ClassDef):
                    functions.append(f"{node.parent.name}_{node.name}")
                else:
                    functions.append(node.name)
        
        self.report.append(f"Total Lines of Code: {total_lines}\n")
        self.report.append(f"Imports: {', '.join(imports) if imports else 'None'}\n")
        self.report.append(f"Classes: {', '.join(classes) if classes else 'None'}\n")
        self.report.append(f"Functions: {', '.join(functions) if functions else 'None'}\n")
    
    def analyze_docstrings(self):
        for node in ast.walk(self.tree):
            if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                docstring = ast.get_docstring(node)
                name = node.name if isinstance(node, ast.FunctionDef) else f"Class {node.name}"
                self.report.append(f"{name}: {docstring if docstring else 'DocString not found'}\n")
    
    def check_type_annotations(self):
        missing_annotations = []
        for node in ast.walk(self.tree):
            if isinstance(node, ast.FunctionDef):
                if not any(isinstance(arg.annotation, ast.AST) for arg in node.args.args) or node.returns is None:
                    missing_annotations.append(node.name)
        
        if missing_annotations:
            self.report.append(f"Functions missing type annotations: {', '.join(missing_annotations)}\n")
        else:
            self.report.append("All functions have type annotations.\n")
    
    def check_naming_conventions(self):
        bad_classes = []
        bad_functions = []
        camel_case = re.compile(r'^[A-Z][a-zA-Z0-9]+$')
        snake_case = re.compile(r'^[a-z_][a-z0-9_]*$')
        
        for node in ast.walk(self.tree):
            if isinstance(node, ast.ClassDef) and not camel_case.match(node.name):
                bad_classes.append(node.name)
            if isinstance(node, ast.FunctionDef) and not snake_case.match(node.name):
                bad_functions.append(node.name)
        
        if bad_classes:
            self.report.append(f"Classes violating naming conventions: {', '.join(bad_classes)}\n")
        if bad_functions:
            self.report.append(f"Functions violating naming conventions: {', '.join(bad_functions)}\n")
        if not bad_classes and not bad_functions:
            self.report.append("All naming conventions followed correctly.\n")
    
    def generate_report(self):
        file_name = os.path.basename(self.file_path).replace('.py', '')
        report_path = f"style_report_{file_name}.txt"
        with open(report_path, 'w', encoding='utf-8') as f:
            f.writelines(self.report)
        print(f"Report generated: {report_path}")
    
    def run(self):
        self.analyze_file_structure()
        self.analyze_docstrings()
        self.check_type_annotations()
        self.check_naming_conventions()
        self.generate_report()

#Change file_to_check to test other files
if __name__ == "__main__":
    file_to_check = "Caesar.py"  
    checker = StyleChecker(file_to_check)
    checker.run()
