import os

from DataManager import GitHubStatsData

class FileManager:
    ShortcutBoxStartString = "<!-- github-stats-box start -->"
    ShortcutBoxEndString = "<!-- github-stats-box end -->"

    def writeStatsInFile(fileName: str, statsData: GitHubStatsData):
        if os.path.exists(fileName):
            contentToWrite = FileManager.computeFileContentWithStats(fileName, statsData)
            with open(fileName, "w", encoding="utf-8") as file:
                file.write(contentToWrite)
        else:
            raise Exception(f"Cannot find file: {fileName}")

    def computeFileContentWithStats(fileName: str, statsData: GitHubStatsData) -> str:
        with open(fileName, "r", encoding="utf-8") as file:
            content = file.read()

            startLineNumber = content.find(FileManager.ShortcutBoxStartString)
            endLineNumber = content.find(FileManager.ShortcutBoxEndString)

            before = content[0:startLineNumber]
            after = content[endLineNumber:len(content)]
            
            newContent = before
            newContent += FileManager.computeStatsString(statsData)
            newContent += after
            return newContent

    def computeStatsString(statsData: GitHubStatsData) -> str:
        string = f"{FileManager.ShortcutBoxStartString}\n"
        string += "My GitHub Stats\n"
        string += "```text\n"
        string += f"⭐ Total Stars:                     {statsData.m_starsCount}\n"
        string += f"➕ Total Commits:                   {statsData.m_commitsCount}\n"
        string += f"🔀 Total Pull Requests:             {statsData.m_pullRequestsCount}\n"
        string += f"🚩 Total Issues:                    {statsData.m_issuesCount}\n"
        string += f"📦 Contributed to:                  {statsData.m_contributedToCount}\n"
        string += "```\n"
        string += "<!-- Powered by https://github.com/torresflo/GitHub-Stats-Me. -->\n"
        return string

                


    