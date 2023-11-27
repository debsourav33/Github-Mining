from typing import Union
from enums.menu_enums import MenuOptions, RepoMenuOptions
from utils.user_input_handler import UserInputHandler
from api.gh_repo import get_repository

####
class Application:
    def __init__(self):
        self.repos = []

    @staticmethod
    def display_menu(display_option: str):
        main_menu = (
            "1. Get repository",
            "2. Show Collected Repositories",
            "3. Create visual representation",
            "4. Calculate correlation among the stored users data",
            "5. Exit",
        )

        repo_submenu = (
            "1. Show all pull requests",
            "2. Show summary  repository",
            "3. visual representation of the repository",
            "4. Calculate correlation for all  data in the repository",
            "5. Return to main menu",
        )
        if display_option == "main":
            for option in main_menu:
                print(option)

        elif display_option == "repo":
            for option in repo_submenu:
                print(option)

        else:
            raise ValueError("Invalid menu display option")

    @staticmethod
    def accept_user_input():
        user_input = input("Enter your choice: ")
        return user_input

    @staticmethod
    def validate_user_input_choice(menu_choice: str, user_choice: str):
        valid_choices_mapping = {"main": map(str, range(1, 6)), "repo": map(str, range(1, 6))}
        valid_choices = valid_choices_mapping.get(menu_choice, ())
        if user_choice not in valid_choices:
            return False
        return True

    def display_and_accept_menu_choice(self, menu_choice: str) -> Union[MenuOptions, RepoMenuOptions]:
        self.display_menu(menu_choice)
        user_input = self.accept_user_input()
        is_valid = self.validate_user_input_choice(menu_choice, user_input)
        if not is_valid:
            print("You have entered an invalid choice for the current menu.\n" "Please try again.\n")
            return self.display_and_accept_menu_choice(menu_choice)

        if menu_choice == "main":
            print("\n")
            return MenuOptions(int(user_input))
        else:
            print("\n")
            return RepoMenuOptions(int(user_input))

    def run_app(self):
        current_menu_choice = "main"
        selected_repo_index = None
        while 1:
            user_input = self.display_and_accept_menu_choice(current_menu_choice)
            if current_menu_choice == "main":
                if user_input == MenuOptions.GET_REPO:
                    owner_name, repo_name = UserInputHandler.get_repo()
                    github_repo = get_repository(owner_name, repo_name)

                    if github_repo is not None:
                        github_repo.store_pull_requests()
                        self.repos.append(github_repo)
                        github_repo.save_as_csv()
                        print(f"Repository {github_repo.name} added successfully")
                    else:
                        print(f"Failed to retrieve repository {repo_name} from {owner_name}")

                elif user_input == MenuOptions.SHOW_REPOS:

                    if self.repos:
                        for index, repo in enumerate(self.repos, 1):
                            print(f"{index}. {repo}")
                        user_input = UserInputHandler.select_repo(tuple(map(str, range(1, len(self.repos) + 1))))
                        current_menu_choice = "repo"
                        selected_repo_index = user_input - 1
                    else:
                        print("No repositories found. Please add a repository first.")
                        current_menu_choice = "main"
                        selected_repo_index = None

                elif user_input == MenuOptions.EXIT:
                    break

            elif current_menu_choice == "repo":
                if user_input == RepoMenuOptions.SHOW_PULL_REQUESTS:
                    # show all pull-requests from a certain repository
                    repo = self.repos[selected_repo_index]
                    for pr in repo.pull_requests:
                        print(pr)
                elif user_input == RepoMenuOptions.SHOW_SUMMARY:
                    repo = self.repos[selected_repo_index]
                    repo.show_summary()

            print("-" * 35)


def main():
    app = Application()
    app.run_app()


if __name__ == "__main__":
    main()
