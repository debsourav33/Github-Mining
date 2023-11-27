from enum import Enum
class MenuOptions(Enum):
    GET_REPO = 1
    SHOW_REPOS = 2
    VIZ_REP_REPOS = 3
    USERS_CORRELATION = 4
    EXIT = 5


class RepoMenuOptions(Enum):
    SHOW_PULL_REQUESTS = 1
    SHOW_SUMMARY = 2
    VIZ_REP = 3
    CORRELATION = 4
    BACK_TO_MAIN_MENU = 5
