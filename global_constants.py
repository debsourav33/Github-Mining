from pathlib import Path

HOME_DIR = Path(__file__).parent
REPO_PATH = HOME_DIR / "repos"

access_token = None
if access_token:
    AUTHORIZATION_HEADER = {"Authorization": f"Bearer {access_token}",
                            "Accept": "application/vnd.github.v3+json",
                            "X-Github-Api-Version": "2022-11-28"}
else:
    AUTHORIZATION_HEADER = {"Accept": "application/vnd.github.v3+json",
                            "X-Github-Api-Version": "2022-11-28"}