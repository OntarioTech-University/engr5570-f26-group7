"""
Small, tool-backed signals for "the program has something to clean up".

radon only scores def/class blocks, but many contest programs keep all their logic
at module level. So we also score the module body as one block: we wrap the
top-level statements (minus imports, defs and classes) in a function and let
radon compute its cyclomatic complexity.
"""
import ast
from radon.complexity import cc_visit
from radon.raw import analyze

CONTROL = (ast.If, ast.For, ast.While, ast.Try, ast.With, ast.AsyncFor, ast.AsyncWith)


def _depth(node, d=0):
    best = d
    for child in ast.iter_child_nodes(node):
        nd = d + 1 if isinstance(child, CONTROL) else d
        if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef, ast.Lambda)):
            nd = 0
        best = max(best, _depth(child, nd))
    return best


def _code_lines(nodes) -> int:
    """Lines that hold code inside these statements: comments, blank lines and
    docstrings do not count, so a well-commented program is not called long."""
    lines = set()
    for top in nodes:
        for n in ast.walk(top):
            if not isinstance(n, ast.stmt):
                continue
            if isinstance(n, ast.Expr) and isinstance(n.value, ast.Constant) and isinstance(n.value.value, str):
                continue            # docstring or bare string
            if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)) and n is not top:
                lines.add(n.lineno)
                continue
            lines.update(range(n.lineno, (n.end_lineno or n.lineno) + 1)
                         if not hasattr(n, "body") else [n.lineno])
    return len(lines)


def metrics(code: str) -> dict:
    tree = ast.parse(code)
    blocks = [b for b in cc_visit(code)]
    funcs = [b for b in blocks if b.letter in "FM"]
    top = [n for n in tree.body if not isinstance(
        n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef, ast.Import, ast.ImportFrom))]
    module_cc = 0
    if top:
        body = ast.Module(body=top, type_ignores=[])
        wrapped = "def __module__():\n" + "\n".join(
            "    " + ln for ln in ast.unparse(body).splitlines())
        module_cc = cc_visit(wrapped)[0].complexity
    fn_nodes = [n for n in ast.walk(tree) if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]
    fn_lines = [_code_lines(n.body) for n in fn_nodes]
    module_lines = _code_lines(top) if top else 0
    longest = max(fn_lines + [module_lines], default=0)
    return {
        "sloc": analyze(code).sloc,
        "n_functions": len(funcs),
        "max_cc": max([b.complexity for b in blocks] + [module_cc], default=0),
        "module_cc": module_cc,
        "max_nesting": max([_depth(n) for n in tree.body] + [0]),
        "longest_block": longest,
    }
