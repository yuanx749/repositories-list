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
repo_source_lst = [repo for repo in repo_lst if not repo["fork"]]

# %%
# get more requests per hour using authentication
github_token = os.environ.get("GITHUB_TOKEN", "")
dt_lst = []
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
# only sort by time, dict does not support sort
dt_lst, repo_source_lst = zip(
    *sorted(zip(dt_lst, repo_source_lst), key=lambda e: e[0], reverse=True)
)

# %%
tags = ["project", "package"]
f_ = open("README.md", "w")
f_.write("# Repositories List\n")
f_.write("An automatically updated list of my public non-forked repositories.\n")
f_.write("\n### Projects\n")
for repo in repo_source_lst:
    if "project" in repo["topics"]:
        f_.write(f"- [{repo['name']}]({repo['homepage']}) - {repo['description']}\n")
f_.write("\n### Packages\n")
for repo in repo_source_lst:
    if "package" in repo["topics"]:
        f_.write(f"* [{repo['name']}]({repo['homepage']}) - {repo['description']}\n")
f_.write("\n### Others\n")
for repo in repo_source_lst:
    if all(tag not in repo["topics"] for tag in tags):
        f_.write(f"+ [{repo['name']}]({repo['html_url']}) - {repo['description']}\n")
f_.close()
