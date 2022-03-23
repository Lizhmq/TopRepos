import re, json
import requests


token = "d8581f57d7aa51c068ee3c01132cbc0f61b37aa9"
headers = {"Authorization": f"token {token}"}
not_found = ['400: Invalid request', '404: Not Found']


class FAKERET:
    def __init__(self):
        self.text = ""

def WrapGet(*args, **kwargs):
    try:
        ret = requests.get(*args, **kwargs)
        return ret
    except:
        return FAKERET()

def getreposwithpr(lang):
    return json.loads(open(f"repos/{lang}_withpr.json").read())
def getlicfromurl(url):
    # license templates in Github
    licenses = ["Apache-2.0 License", "GPL-3.0 License", "MIT License", \
                "BSD-2-Clause License", "BSD-3-Clause License", "BSL-1.0 License", \
                "CC0-1.0 License", "EPL-2.0 License", "AGPL-3.0 License", \
                "GPL-2.0 License", "LGPL-2.1 License", "MPL-2.0 License", "Unlicense License"]
    content = WrapGet(url, headers=headers).text
    for license in licenses:
        if license in content:
            return license
    return ""
def getlicfromcontent(content):
    ss = ["distribut", "creative common", "gpl", "apache", "mit", "bsd", "bsl", "cc0", "public license"]
    content = content.lower()
    for s in ss:
        if s in content:
            return s
    return ""
def getbranches(repo):
    url = f"https://github.com/{repo}/branches"
    content = WrapGet(url, headers=headers).text
    branchregex = r'<a class="branch-nam.*?" href="(.*?)"'
    branches = re.findall(branchregex, content)
    # print(branches)
    return branches
def getlicensefiles(url):
    content = WrapGet(url, headers=headers).text
    pattern = re.compile(r'href="(.*?)">(?:license|copying|copy)(?:\.md|\.txt)?</a>', re.IGNORECASE)
    ret = pattern.findall(content)
    # print(ret)
    return ret
def getcontent(url):
    content = WrapGet(url, headers=headers).text
    # regex = r'js-file-line">(.*?)</td>'
    # ret = re.findall(regex, content)
    return content
    # return "".join(ret)
def findlicense(repo):
    branches = getbranches(repo)
    for branch in branches:
        url = f"https://github.com{branch}"
        s = getlicfromurl(url)
        if s:
            return s
        files = getlicensefiles(url)
        for file in files:
            furl = f"https://github.com{file}"
            content = getcontent(furl)
            s = getlicfromcontent(content)
            if s:
                return s
    return ""

for lang in ["javascript", "python", "java", "php", "c-plus-plus", "ruby", "c-sharp", "go", "c"]:
    res = []
    data = getreposwithpr(lang)
    data = [p for p in data if p[1] >= 100]
    print(f"{len(data)} repos for language {lang}")
    for repo, cnt in data:
        if findlicense(repo):
            res.append([repo, cnt])
    print(f"{len(res)} repos found license for language {lang}")
    with open(f"repos/{lang}_withprlic.json", "w") as f:
        f.write(json.dumps(res))