# %%
import datetime
import json
import os
import urllib.parse
import urllib.request

# %%
# get more requests per hour using authentication
github_token = os.environ.get("GITHUB_TOKEN", "")
header = {}
if github_token:
    header["Authorization"] = f"Bearer {github_token}"


def query(url):
    req = urllib.request.Request(url, headers=header)
    response = urllib.request.urlopen(req)
    return json.loads(response.read().decode("utf-8"))


# %%
user = "yuanx749"
params = urllib.parse.urlencode(
    {
        "sort": "updated",
        "per_page": 100,
    }
)
url = f"https://api.github.com/users/{user}/repos?{params}"
repo_lst = query(url)

# %%
dt_lst = []
source_repo_lst = [repo for repo in repo_lst if not repo["fork"]]
for repo in source_repo_lst:
    if not repo["fork"]:
        url = f"https://api.github.com/repos/{user}/{repo['name']}/commits"
        commit_lst = query(url)
        dt = commit_lst[-1]["commit"]["author"]["date"]
        dt_lst.append(datetime.datetime.strptime(dt, "%Y-%m-%dT%H:%M:%SZ"))
# only sort by time, dict does not support sort
dt_lst, source_repo_lst = zip(
    *sorted(zip(dt_lst, source_repo_lst), key=lambda e: e[0], reverse=True)
)
fork_repo_lst = [repo for repo in repo_lst if repo["fork"]]

# %%
tags = ["research", "tool", "project", "private"]
f_ = open("README.md", "w", encoding="utf-8")
f_.write("# Repositories List\n")
f_.write("An automatically updated list of my public repos and repos contributed to.\n")
f_.write("\n#### Research\n")
for repo in source_repo_lst:
    if "research" in repo["topics"]:
        f_.write(f"- [{repo['name']}]({repo['homepage']}) - {repo['description']}\n")
f_.write("\n#### Tools\n")
for repo in source_repo_lst:
    if "tool" in repo["topics"]:
        f_.write(f"- [{repo['name']}]({repo['homepage']}) - {repo['description']}\n")
f_.write("\n#### Others\n")
for repo in source_repo_lst:
    if "project" in repo["topics"]:
        f_.write(f"- [{repo['name']}]({repo['homepage']}) - {repo['description']}\n")
f_.write("<!--  -->\n")
for repo in source_repo_lst:
    if all(tag not in repo["topics"] for tag in tags):
        f_.write(f"- [{repo['name']}]({repo['html_url']}) - {repo['description']}\n")

href = "https://github.com/search?q=involves%3Ayuanx749+is%3Apublic+&amp;type=pullrequests&amp;s=created&amp;o=desc"
f_.write(f'\n#### <a href="{href}">Contributions</a>\n')
for i, repo in enumerate(fork_repo_lst):
    if i == 5:
        f_.write("<!--  -->\n")
    url = f"https://api.github.com/repos/{user}/{repo['name']}"
    repo_dict = query(url)
    src = repo_dict["source"]
    f_.write(f"- [{src['full_name']}]({src['html_url']}) - {src['description']}\n")
f_.close()
