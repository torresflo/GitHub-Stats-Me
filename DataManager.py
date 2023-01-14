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
        for node in requestJson["repositories"]["nodes"]:
            self.m_starsCount += node["stargazers"]["totalCount"]

        url = f"https://api.github.com/search/commits?q=author:{self.m_login}"
        request = requests.get(url)
        self.m_commitsCount = request.json()["total_count"]
