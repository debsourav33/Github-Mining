from typing import Union, Iterable
from enums.menu_enums import MenuOptions, RepoMenuOptions


def accept_repo_input() -> tuple[str, str]:

    owner_name = input("Enter owner name: ")
    repo_name = input("Enter repo name: ")
    return owner_name, repo_name


class UserInputHandler:
    @staticmethod
    def get_repo() -> Union[MenuOptions, RepoMenuOptions, tuple[str, str], int]:

        return accept_repo_input()

    @staticmethod
    def select_repo(valid_number_range: Iterable) -> int:
        user_input = input("Select a repository from the list above:")
        if user_input not in valid_number_range:
            print("You have entered an invalid choice for the current menu.\n" "Please try again.\n")
            return UserInputHandler.select_repo(valid_number_range)
        return int(user_input)
