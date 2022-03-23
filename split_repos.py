import json

def getreposwithprlic(lang):
    return json.loads(open(f"repos/{lang}_withprlic.json").read())


allrepos = dict()
totalset = set()
for lang in ["javascript", "python", "java", "php", "c-plus-plus", "ruby", "c-sharp", "go", "c"]:
    allrepos[lang] = [p for p in getreposwithprlic(lang) if p[0] not in totalset]   # dedup in langs
    for repo, cnt in allrepos[lang]:
        totalset.add(repo)



lists = list(allrepos.values())
maxrepocnt = max(map(len, lists))  # max lang repo num
outset = []
for i in range(maxrepocnt):
    for j in range(len(lists)):
        if i < len(lists[j]):
            outset.append(tuple(lists[j][i]))


keys = 12
outlists = [[] for _ in range(keys)]
lens = [0 for _ in range(keys)]
for repo, cnt in outset:
    minl, minidx = 9999999999, 0
    for i in range(keys):
        if lens[i] < minl:
            minl = lens[i]
            minidx = i
    lens[minidx] += cnt
    outlists[minidx].append(repo)
outflatten = set([repo for lst in outlists for repo in lst])
assert outflatten == set([p[0] for p in outset])

for i in range(keys):
    with open(f"repos/{i}.txt", "w") as f:
        for repo in outlists[i]:
            f.write(repo + "\n")
