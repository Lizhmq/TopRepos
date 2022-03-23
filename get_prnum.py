import re, json
import requests

token = "[gh_token]"
headers = {"Authorization": f"token {token}"}
not_found = ['400: Invalid request', '404: Not Found']

def getrepos(lang):
    return json.loads(open(f"repos/{lang}.json").read())
def getprnum(repo):
    url = f"https://github.com/{repo}/pulls"
    content = requests.get(url, headers=headers).text
    # print(content)
    closedpr = r'([0-9]*,?[0-9]+) Closed'
    rets = re.findall(closedpr, content)
    # should be 2
    try:
        assert len(rets) == 2
        rets = [s.replace(",", "") for s in rets]
        assert int(rets[0]) == int(rets[1])
    except:
        return 0
    return int(rets[0])


for lang in ["javascript", "python", "java", "php", "c-plus-plus", "ruby", "c-sharp", "go", "c"]:
    repos = getrepos(lang)
    prnums = [getprnum(repo) for repo in repos]
    prdic = {}
    for repo, num in zip(repos, prnums):
        prdic[repo] = num
    lst = list(sorted(prdic.items(), key=lambda p: p[1], reverse=True))
    with open(f"repos/{lang}_withpr.json", "w") as f:
        f.write(json.dumps(lst))

