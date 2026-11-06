import os, re, shutil, sys

T = os.path.expanduser('~/.config/vesktop/themes/FrostedGlass.theme.css')
BAK = T + '.pre-bisect'
A = '/* ==== FrostedGlass, class-mapped 2026-11-06 ==== */\n'
B = '/* ==== user settings ==== */\n'

if sys.argv[1] == 'restore':
    shutil.copy(BAK, T)
    print('restored')
    sys.exit()

if not os.path.exists(BAK):
    shutil.copy(T, BAK)
s = open(BAK).read()
a = s.index(A) + len(A)
b = s.index(B)
body = s[a:b]

# split body into top-level chunks (rule or comment) by brace depth
chunks, depth, start, i, n = [], 0, 0, 0, len(body)
while i < n:
    c = body[i]
    if body.startswith('/*', i):
        j = body.index('*/', i) + 2
        i = j
        continue
    if c in '"\'':
        j = i + 1
        while body[j] != c:
            j += 2 if body[j] == '\\' else 1
        i = j + 1
        continue
    if c == '{':
        depth += 1
    elif c == '}':
        depth -= 1
        if depth == 0:
            chunks.append(body[start:i + 1])
            start = i + 1
    i += 1

lo, hi = int(sys.argv[2]), int(sys.argv[3])
kept = ''.join(chunks[lo:hi])
out = s[:a] + kept + '\n' + s[b:]
open(T, 'w').write(out)
print('chunks total', len(chunks), '| kept', lo, 'to', hi, '| bytes', len(out))
