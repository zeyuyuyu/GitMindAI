import ast
from typing import Dict, List, Optional
import numpy as np
from dataclasses import dataclass

@dataclass
class QualityMetrics:
    cognitive_complexity: int
    maintainability_index: float
    doc_coverage: float
    test_coverage: Optional[float]
    code_smells: List[str]

class CodeQualityAnalyzer:
    def __init__(self):
        self.complexity_threshold = 15
        self.mi_threshold = 65.0
        self.doc_threshold = 0.7

    def analyze_file(self, file_content: str) -> QualityMetrics:
        try:
            tree = ast.parse(file_content)
            return QualityMetrics(
                cognitive_complexity=self._calculate_complexity(tree),
                maintainability_index=self._calculate_maintainability(file_content),
                doc_coverage=self._calculate_doc_coverage(tree),
                test_coverage=None,  # To be populated by test runner
                code_smells=self._detect_code_smells(tree)
            )
        except SyntaxError:
            return QualityMetrics(0, 0.0, 0.0, None, ["Invalid Python syntax"])

    def _calculate_complexity(self, tree: ast.AST) -> int:
        complexity = 0
        for node in ast.walk(tree):
            if isinstance(node, (ast.If, ast.While, ast.For, ast.FunctionDef)):
                complexity += 1
            elif isinstance(node, ast.BoolOp):
                complexity += len(node.values) - 1
        return complexity

    def _calculate_maintainability(self, content: str) -> float:
        loc = len(content.splitlines())
        volume = len(content)
        comments = len([l for l in content.splitlines() if l.strip().startswith('#')])
        
        # Simplified maintainability index calculation
        mi = 171 - 5.2 * np.log(volume) - 0.23 * (loc)
        mi = min(100, max(0, mi))  # Normalize to 0-100
        return mi

    def _calculate_doc_coverage(self, tree: ast.AST) -> float:
        functions = [node for node in ast.walk(tree) 
                    if isinstance(node, ast.FunctionDef)]
        if not functions:
            return 1.0
            
        documented = sum(1 for f in functions 
                        if ast.get_docstring(f) is not None)
        return documented / len(functions)

    def _detect_code_smells(self, tree: ast.AST) -> List[str]:
        smells = []
        
        # Check for long functions
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                if len(node.body) > 20:
                    smells.append(
                        f"Function '{node.name}' is too long ({len(node.body)} lines)"
                    )
                    
        # Check for too many arguments
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                args = len(node.args.args)
                if args > 5:
                    smells.append(
                        f"Function '{node.name}' has too many arguments ({args})"
                    )
                    
        return smells

    def get_improvement_suggestions(self, metrics: QualityMetrics) -> List[str]:
        suggestions = []
        
        if metrics.cognitive_complexity > self.complexity_threshold:
            suggestions.append(
                "Consider breaking down complex functions into smaller, more manageable pieces"
            )
            
        if metrics.maintainability_index < self.mi_threshold:
            suggestions.append(
                "Improve code maintainability by reducing function sizes and adding comments"
            )
            
        if metrics.doc_coverage < self.doc_threshold:
            suggestions.append(
                "Increase documentation coverage by adding docstrings to functions"
            )
            
        suggestions.extend(metrics.code_smells)
        return suggestions

    def generate_report(self, filepath: str, metrics: QualityMetrics) -> str:
        report = f"Code Quality Report for {filepath}\n"
        report += "=" * 50 + "\n"
        report += f"Cognitive Complexity: {metrics.cognitive_complexity}\n"
        report += f"Maintainability Index: {metrics.maintainability_index:.2f}/100\n"
        report += f"Documentation Coverage: {metrics.doc_coverage:.1%}\n"
        
        if metrics.test_coverage:
            report += f"Test Coverage: {metrics.test_coverage:.1%}\n"
            
        if metrics.code_smells:
            report += "\nCode Smells:\n"
            for smell in metrics.code_smells:
                report += f"- {smell}\n"
                
        suggestions = self.get_improvement_suggestions(metrics)
        if suggestions:
            report += "\nSuggestions for Improvement:\n"
            for suggestion in suggestions:
                report += f"- {suggestion}\n"
                
        return report