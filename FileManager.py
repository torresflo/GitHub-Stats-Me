import os

from DataManager import GitHubStatsData
from StringBuilder import GitHubStatsBuilder, LanguagesStatsBuilder

class FileManager:
    def writeStatsInFile(fileName: str, statsData: GitHubStatsData):
        if os.path.exists(fileName):
            with open(fileName, "r", encoding="utf-8") as file:
                content = file.read()
                content = FileManager.generateContentWithGitHubStats(content, statsData)
                content = FileManager.generateFileContentWithLanguageStats(content, statsData)
            with open(fileName, "w", encoding="utf-8") as file:
                file.write(content)
        else:
            raise Exception(f"Cannot find file: {fileName}")

    def generateContentWithGitHubStats(content: str, statsData: GitHubStatsData) -> str:
        startLineNumber = content.find(GitHubStatsBuilder.GitHubStatsBoxStartString)
        endLineNumber = content.find(GitHubStatsBuilder.GitHubStatsBoxEndString)

        before = content[0:startLineNumber]
        after = content[endLineNumber:len(content)]
        
        newContent = before
        newContent += f"{GitHubStatsBuilder.GitHubStatsBoxStartString}\n"
        newContent += GitHubStatsBuilder.generateString(statsData)
        newContent += after

        return newContent

    def generateFileContentWithLanguageStats(content: str, statsData: GitHubStatsData) -> str:
        maxNumberOfLanguages = os.getenv("STATS_MAX_LANGUAGES")
        if maxNumberOfLanguages is None:
            maxNumberOfLanguages = "-1"
        maxNumberOfLanguages = int(maxNumberOfLanguages)

        ignoredLanguages = os.getenv("STATS_IGNORED_LANGUAGES")
        if ignoredLanguages is None:
            ignoredLanguages = ""
        ignoredLanguages = ignoredLanguages.split(",")
     
        startLineNumber = content.find(LanguagesStatsBuilder.LanguageStatsBoxStartString)
        endLineNumber = content.find(LanguagesStatsBuilder.LanguageStatsBoxEndString)

        before = content[0:startLineNumber]
        after = content[endLineNumber:len(content)]
        
        newContent = before
        newContent += f"{LanguagesStatsBuilder.LanguageStatsBoxStartString}\n"
        newContent += LanguagesStatsBuilder.generateString(statsData, maxNumberOfLanguages, ignoredLanguages)
        newContent += after

        return newContent