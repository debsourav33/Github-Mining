from datetime import datetime

import requests
import global_constants as gc


def getUserInfo(user):
    url = f"https://api.github.com/users/{user}"

    user_info = None
    response = requests.get(url, headers=gc.AUTHORIZATION_HEADER)

    if response.status_code != 200:
        print(f"Status code for {url}: {response.status_code}\n"
              f"{response.text}")
        return None
    else:
        resp_dict = response.json()
        user_info = UserInfo.parse(resp_dict)
        # contributions
        url = f"https://api.github.com/users/{user}/events"
        response = requests.get(url, headers=gc.AUTHORIZATION_HEADER)

    events = []
    created_year = 0
    curr_year = 0
    contributions = 0
    pull_requests = 0

    if response.status_code != 200:
        print(f"Status code for {url}: {response.status_code}")
    else:
        events = response.json()
        contributions = 0

    for event in events:
        if event.get("type", "null") == "PullRequestEvent":  # check if the event is a pull request
            # check if the contribution was made this year
            created_at = event.get("created_at", "")

            if created_at != "":
                created_year = datetime.strptime(created_at, "%Y-%m-%dT%H:%M:%SZ").year
                curr_year = datetime.now().year

            if curr_year == created_year:
                pull_requests += 1

        if event.get("type", "null") == "PushEvent":  # check if the event is a push
            # print(json.dumps(event, indent=4))

            # check if the contribution was made this year
            created_at = event.get("created_at", "")

            if created_at != "":
                created_year = datetime.strptime(created_at, "%Y-%m-%dT%H:%M:%SZ").year
                curr_year = datetime.now().year

            if curr_year == created_year:
                contributions += 1

    if user_info is not None:
        user_info.set_contributions(contributions)
        user_info.set_pull_requests(pull_requests)

    return user_info


class UserInfo:
    def __init__(self, name, no_of_repos, followers, following):
        self.name = name
        self.no_of_repos = no_of_repos
        self.followers = followers
        self.following = following

        self.contributions = 0
        self.pull_requests = 0

    @staticmethod
    def parse(response_dict):
        name = response_dict["name"] if "name" in response_dict else None
        no_of_repos = response_dict["public_repos"] if "public_repos" in response_dict else None
        followers = response_dict["followers"] if "followers" in response_dict else None
        following = response_dict["following"] if "following" in response_dict else None

        return UserInfo(name, no_of_repos, followers, following)

    def set_contributions(self, contributions):
        self.contributions = contributions

    def set_pull_requests(self, pull_requests):
        self.pull_requests = pull_requests

    def __str__(self):
        return f"{self.name}: repos = {self.no_of_repos}, followers = {self.followers}, following = {self.following}, contributions in last year = {self.contributions}"

    def save_as_csv(self):
        header = ['name', 'no_of_repos', 'followers', 'following', 'contributions']
        data = [self.name, self.no_of_repos, self.followers, self.following, self.contributions]
