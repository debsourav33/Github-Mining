from typing import Union

import requests

import global_constants as gc


def getPullRequests(owner, repo):
    url = f"https://api.github.com/repos/{owner}/{repo}/pulls"
    print(url)
    response = requests.get(url, headers=gc.AUTHORIZATION_HEADER)

    if response.status_code != 200:
        print(f"Status code: {response.status_code}\n"
              f"{response.text}")
        return None
    else:
        resp_list = response.json()
    ret = []
    for item in resp_list:
        pr = PullRequest.parse(item)
        print("  Collected PR: ", pr.title)
        ret.append(pr)
    return ret


def getPullRequestInfo(owner, repo, number):
    url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{number}"
    response = requests.get(url, headers=gc.AUTHORIZATION_HEADER)

    if response.status_code != 200:
        print(f"Failed to retrieve pull requests. Status code: {response.status_code}\n"
              f"{response.text}")
        return None
    else:
        resp_dict = response.json()
        pr_info = PRStatus.parse(resp_dict)
        return pr_info


class PullRequest:
    def __init__(self, user, title, number, body, state, created_at, closed_at):
        self.user = user
        self.title = title
        self.number = number
        self.body = body
        self.state = state
        self.created_at = created_at
        self.closed_at = closed_at
        self.pr_status: Union[None, PRStatus] = None

    def store_status(self, owner_name, repo_name):
        self.pr_status = getPullRequestInfo(owner_name, repo_name, self.number)

    def save_as_csv(self, repository):
        header = ['number', 'repo_name', 'repo_owner', 'title', 'state', 'created_at', 'closed_at', 'user', 'commits',
                  'additions', 'deletions', 'changed_files']
        data = [
            self.number, repository.name, repository.owner, self.title, self.state, self.created_at,
            self.closed_at, self.user, self.pr_status.commits, self.pr_status.additions, self.pr_status.deletions,
            self.pr_status.changed_files]
    @staticmethod
    def parse(response_dict):
        title = response_dict["title"] if "title" in response_dict else None
        user = response_dict["user"]["login"] if "user" in response_dict and "login" in response_dict["user"] else None
        number = response_dict["number"] if "number" in response_dict else None
        body = response_dict["body"] if "body" in response_dict else None
        state = response_dict["state"] if "state" in response_dict else None
        created_at = response_dict["created_at"] if "created_at" in response_dict else None
        closed_at = response_dict["closed_at"] if "closed_at" in response_dict else None

        return PullRequest(user, title, number, body, state, created_at, closed_at)

    def __str__(self):
        return f"{self.user}/{self.title}: ({self.state}) ({self.number}) ({self.created_at}) ({self.closed_at})"


class PRStatus:
    def __init__(self, number, commits, additions, deletions, changed_files, author_association):
        self.number = number
        self.commits = commits
        self.additions = additions
        self.deletions = deletions
        self.changed_files = changed_files
        self.author_association = author_association

    @staticmethod
    def parse(response_dict):
        number = response_dict["number"] if "number" in response_dict else None
        commits = response_dict["commits"] if "commits" in response_dict else None
        additions = response_dict["additions"] if "additions" in response_dict else None
        deletions = response_dict["deletions"] if "deletions" in response_dict else None
        changed_files = response_dict["changed_files"] if "changed_files" in response_dict else None
        author_association = response_dict.get("author_association", None)

        return PRStatus(number, commits, additions, deletions, changed_files, author_association)

    def __str__(self):
        return f"PullRequest #{self.number}: commits = ({self.commits}) additions = ({self.additions}) deletions = ({self.deletions}) file changes = ({self.changed_files})"
