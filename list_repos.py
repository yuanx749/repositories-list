# %%
import json
import urllib.parse
import urllib.request

# %%
user = "yuanx749"
params = urllib.parse.urlencode(
    {
        "sort": "created",
    }
)
url = f"https://api.github.com/users/{user}/repos?{params}"
response = urllib.request.urlopen(url)
repo_lst = json.loads(response.read().decode("utf-8"))

# %%
with open("README.md", "w") as f_:
    f_.write("# Repositories List\n")
    f_.write("An automatically updated list of my public non-forked repositories.\n")
    for repo in repo_lst:
        if not repo["fork"]:
            f_.write(
                f"- [{repo['name']}]({repo['html_url']}) - {repo['description']}\n"
            )
