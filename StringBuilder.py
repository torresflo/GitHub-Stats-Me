import os
import math

from typing import List

from DataManager import GitHubStatsData

class GitHubStatsBuilder:
    GitHubStatsBoxStartString = "<!-- github-stats-box start -->"
    GitHubStatsBoxEndString = "<!-- github-stats-box end -->"

    def generateString(statsData: GitHubStatsData) -> str:
        string = "My GitHub Stats\n"
        string += "```text\n"
        string += f"⭐ Total Stars:                     {statsData.m_starsCount}\n"
        string += f"➕ Total Commits:                   {statsData.m_commitsCount}\n"
        string += f"🔀 Total Pull Requests:             {statsData.m_pullRequestsCount}\n"
        string += f"🚩 Total Issues:                    {statsData.m_issuesCount}\n"
        string += f"📦 Contributed to:                  {statsData.m_contributedToCount}\n"
        string += "```\n"
        string += "<!-- Powered by https://github.com/torresflo/GitHub-Stats-Me. -->\n"
        return string

class LanguagesStatsBuilder:
    LanguageStatsBoxStartString = "<!-- language-stats-box start -->"
    LanguageStatsBoxEndString = "<!-- language-stats-box end -->"

    def generateString(statsData: GitHubStatsData, maxNumberOfLanguages: int = 5, ignoredLanguages: List[str] = {}) -> str:
        string = "Most Used Languages\n"
        string += "```text\n"
        
        totalPercent = 0
        mostUsedLanguages = statsData.computeMostUsedLanguagesByPercent(ignoredLanguages)
        count = 0
        for i, (name, percent) in zip(range(maxNumberOfLanguages), mostUsedLanguages.items()):
            string += LanguagesStatsBuilder.generateLanguageStatString(name, percent)
            totalPercent += percent

        string += LanguagesStatsBuilder.generateLanguageStatString("Others", 100 - totalPercent)
        
        string += "```\n"
        string += "<!-- Powered by https://github.com/torresflo/GitHub-Stats-Me. -->\n"
        return string

    def generateLanguageStatString(name: str, percent: float) -> str :
        string = f"{name}".ljust(15)
        string += LanguagesStatsBuilder.generateBarChartString(percent)
        string += f" {percent:.2f}%\n"
        return string

    def generateBarChartString(percent: float, size: int = 40) -> str:
        string = ""
        symbols = "⣀⣄⣤⣦⣶⣷⣿"
        frac = math.floor((size * 7 * percent) / 100)
        barsFull = math.floor(frac / 7)

        if barsFull >= size: 
            string = symbols[8:9] * size
        else:
            semi = frac % 7
            string += symbols[7:8] * barsFull
            string += symbols[semi:semi + 1]
            string = string.ljust(size, symbols[0:1])
        return string
