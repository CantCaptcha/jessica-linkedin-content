#!/usr/bin/env python3
"""Fix indentation in check-late-night-events.py"""

import ast
import sys

# Read the file
with open('check-late-night-events.py', 'r', encoding='utf-8-sig') as f:
    content = f.read()

# Parse as AST to get proper indentation structure
try:
    tree = ast.parse(content)
    # Re-generate with consistent formatting
    fixed_content = ast.unparse(tree)

    # Write back
    with open('check-late-night-events.py', 'w', encoding='utf-8') as f:
        f.write(fixed_content)

    print("Fixed indentation using AST reformatting")
except SyntaxError as e:
    print(f"Syntax error: {e}")
    sys.exit(1)
