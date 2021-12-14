import requests
import re, json
import os, time

def getrepos(lang, maxpage=100):
    repos = set()
    tmpf = "tmp.html"
    for i in range(maxpage):
        url = f"https://awesomeopensource.com/projects/{lang}?projectPage={i+1}"
        # content = requests.get(url).text    # there is no exception handle code...
        os.system(f"wget --user-agent='Mozilla' {url} -O {tmpf}")
        content = open(f"{tmpf}").read()
        regex = r'href="https://awesomeopensource.com/project/(.*?/.*?)"' # because exceptions are not expected hahaha.
        refound = re.findall(regex, content)
        for st in refound:
            repos.add(st)
    print(f"{len(repos)} found for {lang} repos.")
    os.system(f"rm {tmpf}")
    return list(repos)

# javascript python
for lang in ["java", "php", "c-plus-plus", "ruby", "c-sharp", "go", "c"]:
    repos = getrepos(lang, 100)
    assert len(repos) == 10000
    with open(f"repos/{lang}.json", "w") as f:
        f.write(json.dumps(repos))
    time.sleep(20)