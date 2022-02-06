import json
import random


def read_json(file):
    with open(file, "r") as f:
        return json.load(f)
def write_txt(lst, file):
    with open(file, "w") as f:
        for repo in lst:
            f.write(f"{repo}\n")

value1 = 3000
value2 = 1500
langs = ["c", "c-plus-plus", "c-sharp", "go", "java", "javascript", "php", "python", "ruby"]
mp = {
    "c": "c",
    "c-plus-plus": "cpp",
    "c-sharp": ".cs",
    "go": "go",
    "java": "java",
    "javascript": "js",
    "php": "php",
    "python": "py",
    "ruby": "rb"
}
process_txt = []
for lang in langs:
    data = read_json(f"repos/{lang}_withprlic.json")
    lst = []
    cnt = 0
    for repo, num in data:
        if value1 > num and num >= value2:
            cnt += num
            lst.append(repo)
            process_txt.append(repo + "," + mp[lang])
    write_txt(lst, f"repos/{lang}_ge{value2}.txt")
    print(f"Language {lang} >= {value2} prcnt: {cnt}")

random.shuffle(process_txt)
write_txt(process_txt, f"repos/process_txt_{value2}.txt")