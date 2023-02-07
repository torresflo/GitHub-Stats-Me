import os

from DataManager import GitHubStatsData
from FileManager import FileManager

if __name__ == '__main__':
    login = os.getenv("GH_LOGIN")
    if login is None:
        raise Exception(f"Cannot find environment variable: GH_LOGIN")

    token = os.getenv("GH_TOKEN")
    if token is None:
        raise Exception(f"Cannot find environment variable: GH_TOKEN")

    fileName = os.getenv("MARKDOWN_FILE")
    if fileName is None:
        raise Exception(f"Cannot find environment variable: MARKDOWN_FILE")

    gitHubStatsData = GitHubStatsData(login, token)
    FileManager.writeStatsInFile(fileName, gitHubStatsData)