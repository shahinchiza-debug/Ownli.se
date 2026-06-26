#!/usr/bin/env python3
"""
Replace all amber color references with blue in src/app/page.tsx,
except for the `statusColors` map on line ~84 which uses amber for
semantic status indicators (paused / in_progress / pending).
"""

import re
from pathlib import Path

SRC = Path('/home/z/my-project/src/app/page.tsx')
text = SRC.read_text(encoding='utf-8')

# 1. Protect the statusColors line by replacing its amber tokens with a placeholder
status_line_marker = "const statusColors:"
lines = text.split('\n')
for i, ln in enumerate(lines):
    if ln.startswith(status_line_marker):
        protected = ln.replace('amber', '__AMBER_KEEP__')
        lines[i] = protected
        print(f"Protected statusColors line {i+1}")
        break
text = '\n'.join(lines)

# 2. Replace all amber-XXX shades with the matching blue-XXX shade.
def repl(match):
    shade_str = match.group(1)
    if shade_str == '':
        return 'blue'
    shade = int(shade_str)
    return f'blue-{shade}'

pattern = re.compile(r'amber(?:-(\d+))?')
text = pattern.sub(repl, text)

# 3. Restore the statusColors line
text = text.replace('__AMBER_KEEP__', 'amber')

SRC.write_text(text, encoding='utf-8')
print(f"Done. Wrote {SRC}")
