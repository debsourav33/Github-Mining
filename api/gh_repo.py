from datetime import datetime
from typing import Union, List
import requests

from api.gh_pull_reqs import getPullRequests, PullRequest
from api.gh_users import getUserInfo, UserInfo
from utils.io_handler import save_as_csv
import global_constants as gc


def get_repository(owner, repo) -> Union[None, "GitHubRepository"]:
    url = f"https://api.github.com/repos/{owner}/{repo}"
    response = requests.get(url, headers=gc.AUTHORIZATION_HEADER)

    if response.status_code != 200:
        print(f"Status code: {response.status_code}\n"
              f"{response.text}")
        return None
    resp_dict = response.json()
    return GitHubRepository.parse(resp_dict)


class GitHubRepository:
    def __init__(self, name, owner, description, homepage, license, forks, watchers, date_of_collection):
        self.name = name
        self.owner = owner
        self.description = description
        self.homepage = homepage
        self.license = license  # License could be another class with its own attributes
        self.forks = forks
        self.watchers = watchers
        self.date_of_collection = date_of_collection

        self.pull_requests: List[PullRequest] = []  # List of PullRequest objects
        self.users: List[UserInfo] = []

    def store_pull_requests(self):
        self.pull_requests = getPullRequests(self.owner, self.name) or []
        for pull_request in self.pull_requests:
            pull_request.store_status(self.owner, self.name)
            user = getUserInfo(pull_request.user)
            if user is not None:
                self.users.append(user)

    @staticmethod
    def parse(response_dict):
        name = response_dict["name"] if "name" in response_dict else None
        owner = (
            response_dict["owner"]["login"] if "owner" in response_dict and "login" in response_dict["owner"] else None
        )
        description = response_dict["description"] if "description" in response_dict else None
        homepage = response_dict["homepage"] if "homepage" in response_dict else None
        forks = response_dict["forks"] if "forks" in response_dict else None
        watchers = response_dict["watchers"] if "watchers" in response_dict else None
        license = (
            response_dict["license"]["name"]
            if "license" in response_dict
               and response_dict["license"] is not None
               and "name" in response_dict["license"]
            else None
        )

        time = datetime.now()
        formatted_time = time.strftime("%Y-%m-%dT%H:%M:%SZ")

        return GitHubRepository(name, owner, description, homepage, license, forks, watchers, formatted_time)

    def show_summary(self):
        open_prs = 0
        closed_prs = 0
        oldest_pr_date = datetime.now()

        for pull_request in self.pull_requests:
            if pull_request.state == "open":
                open_prs += 1
            elif pull_request.state == "closed":
                closed_prs += 1
            if datetime.strptime(pull_request.created_at, gc.DATETIME_FORMAT) < oldest_pr_date:
                oldest_pr_date = datetime.strptime(pull_request.created_at, gc.DATETIME_FORMAT)

        print(f"Number of pull requests in `open` state: {open_prs}")
        print(f"Number of pull requests in `closed` state: {closed_prs}")
        print(f"Number of users: {len(self.users)}")
        print(f"Date of the oldest pull request: {oldest_pr_date}")

    def __str__(self):
        return f"{self.owner}/{self.name}: license = [{self.license}] homepage = [{self.homepage}] forks = ({self.forks}) watchers = ({self.watchers}) date of collection: {self.date_of_collection}"

    def save_as_csv(self):
        repo_header = ['name', 'owner', 'description', 'homepage', 'license', 'forks', 'watchers', 'date_of_collection']
        data = [
            self.name, self.owner, self.description, self.homepage, self.license, self.forks, self.watchers,
            self.date_of_collection
        ]
        save_as_csv(gc.REPO_PATH / "repositories.csv", data, header=repo_header)
        for pull_request in self.pull_requests:
            pull_request.save_as_csv(self)
        for user in self.users:
            user.save_as_csv()
