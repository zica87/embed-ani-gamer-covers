import json
from datetime import datetime, timedelta

PROJECT_NAME = "embed-ani-gamer-covers"

import requests
url = f"https://api.github.com/repos/zica87/{PROJECT_NAME}/releases"
content = requests.get(url, timeout=10).text
json_dict = json.loads(content)

# with open("releases.json", 'r') as f:
#     json_dict = json.load(f)

for ver in json_dict:
    print("-----------------------")
    print(f"{PROJECT_NAME}  v" + ver["name"])
    print(f'{"Edition":<8}{"Downloads":>12}{"Uploaded Time (UTC+8)":>24}')
    print()
    for edition in ver["assets"]:
        edi = edition['name']\
                .removeprefix(f"{PROJECT_NAME}-")\
                .removesuffix(".exe")
        cnt = edition['download_count']
        time  = datetime.strptime(edition["updated_at"],
                                  "%Y-%m-%dT%H:%M:%SZ" )\
                + timedelta(hours=8)
        time = str(time)
        print(f"{edi:<8}{cnt:>12}{time:>24}")
        print()
