# CyPat Scoreboard Scraper v3.0 Deluxe Extreme Edition Pro Max Ultra Upgraded New Edition+++
# (with Sapphire Crystal Liquid Retina XDR Ceramic Shield Hologramic Display with Oleophobic Coating)
# Nathan Williams, retired supreme leader
# With dumb little additions by Colin DiCarlo, aka Smolin
# Redesigned from scratch by Gideon Witchel

from bs4 import BeautifulSoup
from requests import get
from time import sleep
from tabulate import tabulate
import re

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

column_blacklist = ["Rank", "ScoredImages", "Location", "Division", "Tier", "**"]


def get_tier():
    print("Enter the desired Tier (a = All, p = Platinum, g = Gold, s = Silver, m = Middle School): ")
    tier = input().lower()
    if tier == "a" or tier == "all":
        return ""
    if tier == "p" or tier == "platinum" or tier == "plat" or tier == "":
        return "Platinum"
    if tier == "g" or tier == "gold":
        return "Gold"
    if tier == "s" or tier == "silver":
        return "Silver"
    if tier == "m" or tier == "ms" or tier == "middle" or tier == "middle school":
        return "Middle+School"
    print("Invalid input. Try again.")
    return get_tier()


def get_division():
    print("Enter the desired Division (a = All, o = Open, aj = AJROTC, nj = NJROTC): ")
    division = input().lower()
    if division == "a" or division == "all":
        return ""
    if division == "o" or division == "open" or division == "":
        return "Open"
    if division == "aj" or division == "ajrotc":
        return "AJROTC"
    if division == "nj" or division == "njrotc":
        return "NJROTC"
    print("Invalid input. Try again.")
    return get_division()


def get_location():
    print("Enter the desired 2 letter State code (i.e. TX), or [a]ll for all States: ")
    # https://gist.github.com/JeffPaine/3083347/
    states = ['AK', 'AL', 'AR', 'AZ', 'CA', 'CO', 'CT', 'DC', 'DE', 'FL', 'GA',
              'HI', 'IA', 'ID', 'IL', 'IN', 'KS', 'KY', 'LA', 'MA', 'MD', 'ME',
              'MI', 'MN', 'MO', 'MS', 'MT', 'NC', 'ND', 'NE', 'NH', 'NJ', 'NM',
              'NV', 'NY', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX',
              'UT', 'VA', 'VT', 'WA', 'WI', 'WV', 'WY']
    state = input().upper()
    if state in states:
        return state
    if state == "A" or state == "ALL":
        return ""
    if state == "":
        return "TX"
    else:
        print("Invalid input. Try again.")
        return get_location()


def get_top10():
    print("Do you want to display the top 10 teams instead of selected teams? [y]es or [n]o: ")
    top_teams = input().lower()
    if top_teams == "y" or top_teams == "yes":
        return True
    if top_teams == "n" or top_teams == "no" or top_teams == "":
        return False
    print("Invalid input. Try again.")
    return get_top10()


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
    # Prep for more data
    headers.append("Rank Overall")
    index_r_o = len(headers)-1
    headers.append("% Overall")
    index_p_o = len(headers)-1
    headers.append(f"Rank {tier} {division}")
    index_r_td = len(headers)-1
    headers.append(f"% {tier} {division}")
    index_p_td = len(headers)-1
    headers.append(f"Rank {location}")
    index_r_l = len(headers)-1
    headers.append(f"% {location}")
    index_p_l = len(headers)-1
    # Fill with blanks so they can be set later
    for row in data:
        for i in range(0, 6):
            row.append("")

    index_location = headers.index("Location")
    index_tier = headers.index("Tier")
    index_division = headers.index("Division")

    # Calculate totals for each analysis column
    count_overall = len(data)
    count_tier_div = 0
    count_loc = 0
    for row in data:
        if (row[index_tier] == tier or tier == "") and (row[index_division] == division or division == ""):
            count_tier_div += 1
        if row[index_location] == location or location == "":
            count_loc += 1

    # Add analysis to rows
    current_rank_tier_div = 0
    current_rank_loc = 0
    for index, row in enumerate(data):
        row[index_r_o] = index+1
        row[index_p_o] = f"{((index+1) / count_overall)*100:.2f}%"
        if (row[index_tier] == tier or tier == "") and (row[index_division] == division or division == ""):
            current_rank_tier_div += 1
            row[index_r_td] = current_rank_tier_div
            row[index_p_td] = f"{(current_rank_tier_div / count_tier_div) * 100:.2f}%"
        if row[index_location] == location or location == "":
            current_rank_loc += 1
            row[index_r_l] = current_rank_loc
            row[index_p_l] = f"{(current_rank_loc / count_loc) * 100:.2f}%"

    return headers, data, count_overall, count_tier_div, count_loc


def filter_data(headers, data, tier, division, location):
    index_location = headers.index("Location")
    index_tier = headers.index("Tier")
    index_division = headers.index("Division")

    # Filter out irrelevant rows
    filtered_data = []
    for row in data:
        if location != "" and row[index_location] != location:
            continue
        if tier != "" and row[index_tier] != tier:
            continue
        if division != "" and row[index_division] != division:
            continue
        # Filter out irrelevant columns
        filtered_row = []
        for index, item in enumerate(row):
            if headers[index] in column_blacklist:
                continue
            filtered_row.append(item)
        filtered_data.append(filtered_row)

    filtered_headers = []
    for header in headers:
        if header in column_blacklist:
            continue
        filtered_headers.append(header)

    return filtered_headers, filtered_data

def final_filter_select(headers, data):
    index_team = headers.index("TeamNumber")
    final_data = []
    for row in data:
        if re.match("^\d\d-\d\d\d\d$", row[index_team].strip()):
            continue
        final_data.append(row)
    return final_data


def final_filter_top10(headers, data):
    return data[:10]


def display_scoreboard(tier="Platinum", division="Open", location="TX", top10=False):
    table = query_scoreboard()
    headers, data = parse_scoreboard_table(table)
    analyzed_headers, analyzed_data, num_teams, num_teams_tier_div, num_teams_loc = analyze_data(headers, data, tier, division, location)
    filtered_headers, filtered_data = filter_data(analyzed_headers, analyzed_data, tier, division, location)
    final_data = None
    if top10:
        final_data = final_filter_top10(filtered_headers, filtered_data)
    else:
        final_data = final_filter_select(filtered_headers, filtered_data)

    print(tabulate(final_data, headers=filtered_headers, tablefmt='fancy_grid'))
    print(f"Total teams: {num_teams}")
    print(f"Total teams in {f'{division} {tier}'.strip()}: {num_teams_tier_div}")
    print(f"Total teams in {location}: {num_teams_loc}")

# Thanks! https://itnext.io/overwrite-previously-printed-lines-4218a9563527
def clearLine(n=1):
    LINE_UP = '\033[1A'
    LINE_CLEAR = '\x1b[2K'
    for i in range(n):
        print(LINE_UP, end=LINE_CLEAR)

if __name__ == '__main__':
    display_scoreboard(get_tier(), get_division(), get_location(), get_top10())
    # I didn't add clearLine back because I find it kind of annoying, but if someone can
    # figure it out that might be useful.
