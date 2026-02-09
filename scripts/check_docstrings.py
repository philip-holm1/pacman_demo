import ast, pathlib, sys

TARGET_DIR = pathlib.Path(__file__).parent.parent / 'src' / 'pacman'

def has_doc(node):
    return bool(ast.get_docstring(node))

classes = 0
class_doc = 0
functions = 0
func_doc = 0

for py in TARGET_DIR.rglob('*.py'):
    if py.name == '__init__.py':
        continue
    tree = ast.parse(py.read_text(encoding='utf-8'))
    for node in tree.body:
        if isinstance(node, ast.ClassDef):
            classes += 1
            if has_doc(node):
                class_doc += 1
            for inner in node.body:
                if isinstance(inner, ast.FunctionDef):
                    functions += 1
                    if has_doc(inner):
                        func_doc += 1
        elif isinstance(node, ast.FunctionDef):
            functions += 1
            if has_doc(node):
                func_doc += 1

class_cov = (class_doc / classes * 100) if classes else 100
func_cov = (func_doc / functions * 100) if functions else 100
print(f"Class doc coverage: {class_cov:.1f}% ({class_doc}/{classes})")
print(f"Function doc coverage: {func_cov:.1f}% ({func_doc}/{functions})")
threshold = 30  # minimal baseline threshold
if class_cov < threshold or func_cov < threshold:
    print(f"Docstring coverage below threshold {threshold}%", file=sys.stderr)
    sys.exit(1)
