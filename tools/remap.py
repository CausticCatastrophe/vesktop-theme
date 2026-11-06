import re, glob, collections

S = 'SCRATCH_DIR'  # set to your scratch folder
tok_re = re.compile(r'\.((?:\\.|[A-Za-z0-9_\-])+)')


def toks(text):
    for m in tok_re.finditer(text):
        t = m.group(1).replace('\\', '')
        if len(t) > 7 and t[-7] in '_-':
            yield t


new_by_hash = collections.defaultdict(set)
new_by_name = collections.defaultdict(set)
new_all = set()
for f in glob.glob(S + '/dcss/*.css'):
    for t in toks(open(f, errors='ignore').read()):
        if t[-7] != '_':
            continue
        new_all.add(t)
        new_by_hash[t[-6:]].add(t[:-7])
        new_by_name[t[:-7]].add(t[-6:])

src = open(S + '/fg.css').read()
old = set(toks(src))
mapping, stats = {}, collections.Counter()
groups = collections.defaultdict(set)
leftovers = []

for t in sorted(old):
    if t in new_all:
        stats['still valid'] += 1
        continue
    if t[-7] == '_':
        groups[t[-6:]].add(t[:-7])
    else:
        leftovers.append(t)

def unique_name(name):
    h = new_by_name.get(name, set())
    return name + '_' + next(iter(h)) if len(h) == 1 else None

unresolved = []
for h, names in groups.items():
    scores = {nh: len(names & ns) for nh, ns in new_by_hash.items()}
    best = max(scores.values())
    cands = [nh for nh, s in scores.items() if s == best]
    mod = cands[0] if best >= 2 and len(cands) == 1 else None
    for n in names:
        old_t = n + '_' + h if False else None
    for n in names:
        # recover original token (name + sep + hash)
        orig = next(t for t in old if t[:-7] == n and t[-6:] == h and t[-7] == '_')
        if mod and n in new_by_hash[mod]:
            mapping[orig] = n + '_' + mod
            stats['module match'] += 1
        else:
            u = unique_name(n)
            if u:
                mapping[orig] = u
                stats['unique name'] += 1
            else:
                unresolved.append(orig)

for t in leftovers:
    u = unique_name(t[:-7])
    if u:
        mapping[t] = u
        stats['unique name (legacy)'] += 1
    else:
        unresolved.append(t)

stats['unresolved'] = len(unresolved)
print(dict(stats), 'old tokens:', len(old))

out = tok_re.sub(lambda m: '.' + mapping.get(m.group(1), m.group(1)), src)
open(S + '/fg-mapped.css', 'w').write(out)

key = ['bg', 'layers', 'sidebar', 'sidebarList', 'guilds', 'chat', 'chatContent', 'membersWrap', 'content', 'app', 'privateChannels', 'container', 'title']
for k, v in sorted(mapping.items()):
    if v[:-7] in key and k[:-7] == v[:-7]:
        print(' ', k, '->', v)
print('unresolved sample:', unresolved[:40])
