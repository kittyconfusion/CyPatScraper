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
    if tier == "a" or tier == "all" or tier == "":
        return ""
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
    if division == "a" or division == "all" or division == "":
        return ""
    if division == "o" or division == "open":
        return "Open"
    if division == "a" or division == "ajrotc":
        return "AJROTC"
    if division == "n" or division == "njrotc":
        return "NJROTC"
    print("Invalid input. Try again.\n")
    return get_division()


def get_location():
    print("Enter the desired 2 letter State code (i.e. TX), or [a]ll for all States: \n")
    # https://gist.github.com/JeffPaine/3083347/
    states = ['AK', 'AL', 'AR', 'AZ', 'CA', 'CO', 'CT', 'DC', 'DE', 'FL', 'GA',
              'HI', 'IA', 'ID', 'IL', 'IN', 'KS', 'KY', 'LA', 'MA', 'MD', 'ME',
              'MI', 'MN', 'MO', 'MS', 'MT', 'NC', 'ND', 'NE', 'NH', 'NJ', 'NM',
              'NV', 'NY', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX',
              'UT', 'VA', 'VT', 'WA', 'WI', 'WV', 'WY']
    state = input().upper()
    if state in states:
        return state
    if state == "A" or state == "ALL" or state == "":
        return ""
    else:
        print("Invalid input. Try again.\n")
        return get_location()


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


def analyze_data(headers, data, tier, division, location):
    # Prep for percentile data
    headers.append("% Overall")
    headers.append(f"% {tier} {division}")
    headers.append(f"% {location}")

    index_location = headers.index("Location")
    index_tier = headers.index("Tier")
    index_division = headers.index("Division")

    # Calculate totals for each analysis column
    count_overall = len(data)
    count_tier_div = 0
    count_loc = 0
    for index, row in enumerate(data):
        # Append % Overall now since we already know count overall
        row.append(f"{(index / count_overall)*100:.2f}%")
        if row[index_tier] == tier and row[index_division] == division:
            count_tier_div += 1
        if row[index_location] == location:
            count_loc += 1

    # Add more analysis
    current_rank_tier_div = 0
    current_rank_loc = 0
    for row in data:
        if row[index_tier] == tier and row[index_division] == division:
            current_rank_tier_div += 1
            row.append(f"{(current_rank_tier_div / count_tier_div) * 100:.2f}%")
        if row[index_location] == location:
            current_rank_loc += 1
            # If they aren't in open plat, append an empty string to push the value into the correct column
            if row[index_tier] != tier or row[index_division] != division:
                row.append("")
            row.append(f"{(current_rank_loc / count_loc) * 100:.2f}%")

    return headers, data, count_overall, count_tier_div, count_loc


tier = "Platinum"
division = "Open"
location = "TX"
table = query_scoreboard()
headers, data = parse_scoreboard_table(table)
analyzed_headers, analyzed_data, num_teams, num_teams_tier_div, num_teams_loc = analyze_data(headers, data, tier, division ,location)
print(tabulate(analyzed_data, headers=analyzed_headers, tablefmt='fancy_grid'))
print(f"Total teams: {num_teams}")
print(f"Total teams in {division} {tier}: {num_teams_tier_div}")
print(f"Total teams in {location}: {num_teams_loc}")
exit(1)

# TODO:
# - [x] Isolate data gathering from percentage calculations
# - [ ] Fix percentage calculations
# - [ ] Create filtering system after getting raw data from CyPat
# - [ ] Create default view and ability to edit default view
# - [ ] Re-implement top10
# - [ ] Re-implement automatic updates
# - [ ] Delete old code from below this checklist (keeping rn for reference)
# - [ ] Merge

# TODO Bugs:
# - [x] TX percentages are only inserted for open plat teams

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
