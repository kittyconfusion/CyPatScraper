# CyPat Scoreboard Scraper v3.0 Deluxe Extreme Edition Pro Max Ultra Upgraded New Edition+++
# (with Sapphire Crystal Liquid Retina XDR Ceramic Shield Hologramic Display with Oleophobic Coating)
# Nathan Williams, retired supreme leader
# With dumb little additions by Colin DiCarlo, aka Smolin
# Reworked by Gideon Witchel

from bs4 import BeautifulSoup
from requests import get
from time import sleep
from tabulate import tabulate

# Team ids with corresponding team names.
names = {
    '16-3513': "Ctrl-Alt-Elite",
    '16-3514': "Central Georgia Railway Company",
    '16-3515': "CyberPotatoes",
    '16-3516': "506 Variant Also Negotiates",
    '16-2080': "Team Clickbait",
    '16-2081': "virus.exe",
    '16-2082': "Man Pasand Supermarket",
    '16-2083': "Beastcool",
    '16-3417': "Radioactive Puffins",
    '16-1936': "rm -rf /",
    '16-1937': "Scacchic",
    '16-1938': "Phishing for Malware"
}

REPEAT = True

column_blacklist = ["ScoredImages", "Location", "Division", "Tier", "**"]


def get_tier():
    print("Enter the desired Tier (a = All, p = Platinum, g = Gold, s = Silver, m = Middle School): \n")
    tier = input().lower()
    if tier == "a" or tier == "all":
        return "All"
    if tier == "p" or tier == "platinum" or tier == "plat":
        return "Platinum"
    if tier == "g" or tier == "gold":
        return "Gold"
    if tier == "s" or tier == "silver":
        return "Silver"
    if tier == "m" or tier == "ms" or tier == "middle" or tier == "middle school":
        return "Middle+School"
    print("Invalid input. Try again.\n")
    return get_tier()


def get_division():
    print("Enter the desired Division (a = All, o = Open, a = AJROTC, n = NJROTC): \n")
    division = input().lower()
    if division == "a" or division == "all":
        return "All"
    if division == "o" or division == "open":
        return "Open"
    if division == "a" or division == "ajrotc":
        return "AJROTC"
    if division == "n" or division == "njrotc":
        return "NJROTC"
    print("Invalid input. Try again.\n")
    return get_division()


def get_location():
    print("Enter the desired 2 letter State code (i.e. TX), or anything else for all States: \n")
    return input().upper()


def get_top_teams():
    print("Do you want to display the top 10 teams instead of selected teams? [y]es or [n]o: \n")
    top_teams = input().lower()
    if top_teams == "y" or top_teams == "yes":
        return True
    if top_teams == "n" or top_teams == "no":
        return False
    print("Invalid input. Try again.\n")
    return get_top_teams()


def query_scoreboard():
    url = "https://scoreboard.uscyberpatriot.org/index.php"
    response = get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table')
    return table

def parse_scoreboard_table(table):
    header_row = table.find('tr')
    headers = [i.text for i in header_row]
    table_headers = []
    table_indices = []
    # Parse column headers
    for index, header in enumerate(headers):
        # Clean up time column headers
        header = header.replace("\xa0", " ")
        header = header.replace("hh:mm:ss", "")

        # Rename rank column
        if header == "":
            header = "Rank"
        table_headers.append(header)
        table_indices.append(index)

    # Parse data
    data = []
    for row_raw in table.findAll('tr')[1:]:
        row_filtered = row_raw.findAll('td')
        row_final = []
        for index, item in enumerate(row_filtered):
            if index in table_indices:
                # Sub in team names
                if item.text in names:
                    row_final.append(names[item.text])
                else:
                    row_final.append(item.text)
        data.append(row_final)

    return table_headers, data


def get_num_teams(data, tier, division, location):
    count = 0
    for row in data:
        # I am so sorry for this monstrosity
        if (tier in row or tier == "All" or tier == "") and (division in row or division == "All" or division == "") and (location in row or location == "All" or location == ""):
            count += 1
    return count


def add_percentile_data(headers, data, teams_texas, teams_open):
    # Prep for percentile data
    headers.append("% TX")
    headers.append("% Total")
    for row in data:
        row.append(f"{(int(row[0])/teams_texas)*100:.2f}%")
        row.append(f"{(int(row[0])/teams_open)*100:.2f}%")

    return headers, data


tier = "Platinum"
division = "Open"
location = "TX"
table = query_scoreboard()
headers, data = parse_scoreboard_table(table)
teams_texas = get_num_teams(data, tier, division, "TX")
teams_all = get_num_teams(data, tier, division, "All")
headers, data = add_percentile_data(headers, data, teams_texas, teams_all)
print(tabulate(data, headers=headers, tablefmt='fancy_grid'))
print(f"Total teams Texas: {teams_texas}")
print(f"Total teams: {teams_all}")
exit(1)

# TODO:
# - [ ] Isolate data gathering from percentage calculations
# - [ ] Fix percentage calculations
# - [ ] Create filtering system after getting raw data from CyPat
# - [ ] Create default view and ability to edit default view
# - [ ] Re-implement top10
# - [ ] Re-implement automatic updates
# - [ ] Delete old code from below this checklist (keeping rn for reference)

def FindIndexInList(li, val):
    i = 0
    for j in range(len(li)):
        if val in li[j]:
            return i
        i += 1
    return 0


# Determine the indexes of the scoreboard table and their associated values
r = get('http://scoreboard.uscyberpatriot.org/index.php?sort=Total')
soup = BeautifulSoup(r.text, 'html.parser')

header = soup.find_all('tr')[0]
rd = header.find_all('th')
headerList = [i.text for i in rd]

TeamIDIndex = FindIndexInList(headerList, 'Team')
LocationIndex = FindIndexInList(headerList, 'Location')
DivisionIndex = FindIndexInList(headerList, 'Division')

TeamScoreIndex = FindIndexInList(headerList, 'CCS')
ScoreTimeIndex = FindIndexInList(headerList, 'Score\xa0Time')
TierIndex = FindIndexInList(headerList, 'Tier')
CiscoScoreIndex = FindIndexInList(headerList, 'Cisco')

HasCisco = True if CiscoScoreIndex else False

if TopTeams == True:
    data = soup.find_all('tr')[1:]

    loops = 0
    names = {}

    for row in data:
        if loops < 10:
            rowdata = row.find_all('td')

            subbed = rowdata[1].text
            names[subbed] = str(loops + 1) + " Place"
            loops = loops + 1


# Thanks! https://itnext.io/overwrite-previously-printed-lines-4218a9563527
def clearLine(n=1):
    LINE_UP = '\033[1A'
    LINE_CLEAR = '\x1b[2K'
    for i in range(n):
        print(LINE_UP, end=LINE_CLEAR)


def computeWhitespace(text, sectionWidth):
    return ' ' * (sectionWidth - len(str(text)))


def formatPrettyBorder(text, sectionWidth, char):
    out = ''
    half = int((float(sectionWidth) - len(text)) / 2)

    out += char * half

    if (sectionWidth % 2 == 1):
        half += 1

    out += text + char * half

    return out


LongestTeamLen = len(max(list(names.values()), key=len))

print()

while (True):
    r = get('http://scoreboard.uscyberpatriot.org/index.php?sort=Total')
    soup = BeautifulSoup(r.text, 'html.parser')

    data = soup.find_all('tr')[1:]  # the 'tr' in html signifies a row.

    # The top row of the table
    if (HasCisco):
        print('|' + formatPrettyBorder('Name', LongestTeamLen + 2,
                                       '—') + '|Points| Cisco | Total |' + StateCode + ' Rank| Rank |  Time  |Percentile|' + StateCode + ' Percent|')
    else:
        print('|' + formatPrettyBorder('Name', LongestTeamLen + 2,
                                       '—') + '|Points|' + StateCode + ' Rank| Rank |  Time  |Percentile|' + StateCode + ' Percent|')

    StateTeams = 0
    TotalTeams = 0

    for row in data:
        rowdata = row.find_all('td')
        if (Tier == 'None' or rowdata[TierIndex].text == Tier):
            if rowdata[DivisionIndex].text == Division:
                TotalTeams += 1

                if rowdata[LocationIndex].text == StateCode:
                    StateTeams += 1
    stateCounter = 0
    totalCounter = 0
    teamsFoundCounter = 0

    for row in data:  # Repeats for each row within the pre-sorted data
        rowdata = row.find_all('td')

        if (Tier != 'None' and rowdata[TierIndex].text != Tier):
            continue

        if rowdata[DivisionIndex].text == Division:
            totalCounter += 1

            if (rowdata[LocationIndex].text == StateCode):
                stateCounter += 1

        if rowdata[
            TeamIDIndex].text in names.keys():  # Checks if the team id in a row matches with one of the teams specified above.
            teamsFoundCounter += 1
            Line = ''

            # Team Name
            teamNick = names.get(rowdata[TeamIDIndex].text)
            Line += ('| ' + teamNick + computeWhitespace(teamNick, LongestTeamLen + 1) + '|')

            # Team Score
            imageScore = rowdata[TeamScoreIndex].text
            Line += ' ' + (imageScore + computeWhitespace(imageScore, 5) + '|')

            if (HasCisco):
                # Cisco Score if applicable
                ciscoScore = rowdata[CiscoScoreIndex].text
                Line += (str(ciscoScore) + computeWhitespace(ciscoScore, 7) + '|')

                # Total Score if applicable
                totalScore = round(float(imageScore) + float(ciscoScore), 4)
                Line += (str(totalScore) + computeWhitespace(totalScore, 7) + '|')

            # State Rank
            Line += ' ' + (str(stateCounter) + computeWhitespace(stateCounter, 6) + '|')

            # Total Rank
            Line += ' ' + (str(totalCounter) + computeWhitespace(totalCounter, 5) + '|')

            # Team time. All times given are 5-character.
            Line += (rowdata[ScoreTimeIndex].text + '|')

            totalPercentile = str(round(100 / TotalTeams * (TotalTeams - (totalCounter - 1)), 2)) + '%'
            Line += ('  ' + totalPercentile + computeWhitespace(totalPercentile, 7) + ' |')

            statePercentile = str(round(100 / StateTeams * (StateTeams - (stateCounter - 1)), 2)) + '%'
            Line += ('  ' + statePercentile + computeWhitespace(statePercentile, 7) + ' |')

            print(Line)

    # Prints the bottom row of the table.
    if (HasCisco):
        print('|' + formatPrettyBorder('', LongestTeamLen + 2,
                                       '—') + '|——————|———————|———————|———————|——————|————————|——————————|——————————|')
    else:
        print('|' + formatPrettyBorder('', LongestTeamLen + 2,
                                       '—') + '|——————|———————|——————|————————|——————————|——————————|')

        # If applicable, only counts teams in Tier specified
    print('Total ' + ('' if Tier == 'None' else Tier + ' ') + 'Teams:', TotalTeams, '\n'
          + StateCode, ('' if Tier == 'None' else Tier + ' ') + 'Teams:', StateTeams)
    print()

    if not REPEAT:
        break

    sleep(30)

    # Accounts for the header, footer, two lines at the end, and an empty line
    clearLine(teamsFoundCounter + 5)
