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

# print(len(lists))
# print(lists[0][0])
for i in range(maxrepocnt):
    for j in range(len(lists)):
        if i < len(lists[j]):
            outset.append(lists[j][i])

with open(f"repos/allrepos.txt", "w") as f:
    for repo, cnt in outset:
        f.write(repo + "\n")
# for lang in ["javascript", "python", "java", "php", "c-plus-plus", "ruby", "c-sharp", "go", "c"]:
#     with open(f"repos/{lang}_final.txt", "w") as f:
#         for repo, cnt in allrepos[lang]:
#             f.write(repo + "\n")
