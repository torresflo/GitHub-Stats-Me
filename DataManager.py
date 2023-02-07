from typing import List
import requests

gitHubApiGraphQLQuery = """
query userInfo
{
    viewer
    {
        name
        login
        contributionsCollection
        {
            totalCommitContributions
        }
        repositoriesContributedTo(first: 1, contributionTypes: [COMMIT, ISSUE, PULL_REQUEST, REPOSITORY])
        {
            totalCount
        }
        pullRequests(first: 1)
        {
            totalCount
        }
        issues(first: 1)
        {
            totalCount
        }
        repositories(first: 100, ownerAffiliations: OWNER, isFork: false, orderBy: {direction: DESC, field: STARGAZERS})
        {
            totalCount
            nodes
            {
                stargazers
                {
                    totalCount
                }
                name
                languages(first: 10, orderBy: {field: SIZE, direction: DESC})
                {
                    edges
                    {
                        size
                        node
                        {
                            name
                        }
                    }
                }
            }
        }
    }
}
"""

class GitHubStatsData:
    def __init__(self, gitHubLogin: str, gitHubToken: str):
        self.m_token = gitHubToken
        self.m_login = gitHubLogin

        self.downloadData()

    def downloadData(self):
        url = "https://api.github.com/graphql"
        headers = {"Authorization": f"Bearer {self.m_token}"}
        request = requests.post(url, json={"query": gitHubApiGraphQLQuery}, headers=headers)
        requestJson = request.json()["data"]["viewer"]

        self.m_pullRequestsCount = requestJson["pullRequests"]["totalCount"]
        self.m_issuesCount = requestJson["issues"]["totalCount"]
        self.m_contributedToCount = requestJson["repositoriesContributedTo"]["totalCount"]
        self.m_starsCount = 0
        self.m_languages = {}

        for node in requestJson["repositories"]["nodes"]:
            self.m_starsCount += node["stargazers"]["totalCount"]
            languages = node["languages"]["edges"]
            for language in languages:
                size = language["size"]
                name = language["node"]["name"]
                if name not in self.m_languages:
                    self.m_languages[name] = 0
                self.m_languages[name] += size

        self.m_languages = sorted(self.m_languages.items(), key=lambda x:x[1], reverse=True)
        self.m_languages = dict(self.m_languages)

        url = f"https://api.github.com/search/commits?q=author:{self.m_login}"
        request = requests.get(url)
        self.m_commitsCount = request.json()["total_count"]

    def computeMostUsedLanguagesByPercent(self, ignoredLanguages: List[str] = {}):
        totalSize = 0
        mostUsedLanguages = {}
        for name, size in self.m_languages.items():            
            if name.lower() in map(str.lower, ignoredLanguages):
                continue

            mostUsedLanguages[name] = size
            totalSize += size

        for name, size in mostUsedLanguages.items():
            percent = size / totalSize
            mostUsedLanguages[name] = percent * 100
        
        return mostUsedLanguages

