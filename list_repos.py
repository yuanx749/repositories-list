# %%
import datetime
import json
import os
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
repo_source_lst = [repo for repo in repo_lst if not repo["fork"]]
dt_lst = []
github_token = os.environ.get("GITHUB_TOKEN", "")
for repo in repo_source_lst:
    url = f"https://api.github.com/repos/{user}/{repo['name']}/commits"
    if github_token:
        header = {"Authorization": f"token {github_token}"}
        req = urllib.request.Request(url, headers=header)
    else:
        req = urllib.request.Request(url)
    response = urllib.request.urlopen(req)
    commit_lst = json.loads(response.read().decode("utf-8"))
    dt = commit_lst[-1]["commit"]["author"]["date"]
    dt_lst.append(datetime.datetime.strptime(dt, "%Y-%m-%dT%H:%M:%SZ"))
dt_lst, repo_source_lst = zip(*sorted(zip(dt_lst, repo_source_lst), reverse=True))

# %%
repo_lst_1 = [repo for repo in repo_source_lst if repo["homepage"]]
repo_lst_2 = [repo for repo in repo_source_lst if not repo["homepage"]]
with open("README.md", "w") as f_:
    f_.write("# Repositories List\n")
    f_.write("An automatically updated list of my public non-forked repositories.\n")
    for repo in repo_lst_1:
        f_.write(f"- [{repo['name']}]({repo['homepage']}) - {repo['description']}\n")
    f_.write("\n")
    for repo in repo_lst_2:
        f_.write(f"* [{repo['name']}]({repo['html_url']}) - {repo['description']}\n")
