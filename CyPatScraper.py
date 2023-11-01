#CyPat Scoreboard Scraper v2.1 Deluxe Extreme Edition Pro Max Plus with Sapphire Crystal
#Nathan Williams, retired supreme leader

from bs4 import BeautifulSoup
import requests
from time import sleep

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
    } #Team ids with corresponding team names.

HasCisco = True   #Set whether the scoreboard has Cisco information
Tier = 'None'     #None, Platinum, Gold, Silver, or Middle School
Division = 'Open' #Open, CAP, AJROTC, AFJROTC, or NJROTC
StateCode = 'TX'

#Indexes of the scoreboard table where these values occur

TeamIDIndex      =  1
LocationIndex    =  2
DivisionIndex    =  3
TierIndex        =  4
ScoreTimeIndex   =  7
TeamScoreIndex   =  9 #If Cisco does not exist, uses this for total score
CiscoScoreIndex  = 12


#Thanks! https://itnext.io/overwrite-previously-printed-lines-4218a9563527
def clearLine(n=1):
    LINE_UP = '\033[1A'
    LINE_CLEAR = '\x1b[2K'
    for i in range(n):
        print(LINE_UP, end=LINE_CLEAR)

def computeWhitespace(text, sectionWidth):
    return ' ' * (sectionWidth - len(str(text)))

#Input:  ('Name', 21) 
#Output: '⎯ ⎯ ⎯ ⎯ Name ⎯ ⎯ ⎯ ⎯ '
def formatPrettyBorder(text, sectionWidth):
    out = ''
    half = int((float(sectionWidth) - len(text)) / 2)
    
    nextChar = '⎯'
    for i in range(half):
        out += nextChar
        
        nextChar = '⎯' if nextChar == ' ' else ' '
        
    out += text

    if(len(text) > 0):
        nextChar = '⎯' if nextChar == ' ' else ' '

    if(sectionWidth % 2 == 1):
        half += 1

    for i in range(half):
        out += nextChar
        nextChar = '⎯' if nextChar == ' ' else ' '
    return out

LongestTeamLen = len(max(list(names.values()), key=len))

print()

#for i in range(1):
while(True):
    r = requests.get('http://scoreboard.uscyberpatriot.org/index.php?sort=Total')
    soup = BeautifulSoup(r.text,'html.parser')

    data = soup.find_all('tr')[1:] #the 'tr' in html signifies a row.

     #The top row of the table
    if(HasCisco):
        print('|' + formatPrettyBorder('Name', LongestTeamLen + 2) + '|Points| Cisco | Total |' + StateCode + ' Rank| Rank  |  Time  |Percentile|' + StateCode + ' Percent|')
    else:
        print('|' + formatPrettyBorder('Name', LongestTeamLen + 2) + '|Points|' + StateCode + ' Rank| Rank  |  Time  |Percentile|' + StateCode + ' Percent|') 

    StateTeams = 0 
    TotalTeams = 0

    for row in data:
        rowdata = row.find_all('td') 
        if(Tier == 'None' or rowdata[TierIndex] == Tier):
            if rowdata[DivisionIndex].text == Division: 
                TotalTeams += 1

                if rowdata[LocationIndex].text == StateCode: 
                    StateTeams += 1
    stateCounter = 0 
    totalCounter = 0
    teamsFoundCounter = 0

    for row in data: #Repeats for each row within the pre-sorted data
        rowdata = row.find_all('td') 
        
        if not(Tier == 'None' or rowdata[TierIndex] == Tier):
            continue

        if rowdata[DivisionIndex].text == Division: 
            totalCounter += 1 
            
            if(rowdata[LocationIndex].text == StateCode): 
                stateCounter += 1

        if rowdata[TeamIDIndex].text in names.keys(): #Checks if the team id in a row matches with one of the teams specified above.
            teamsFoundCounter += 1
            Line = ''

            #Team Name
            teamNick = names.get(rowdata[TeamIDIndex].text)
            Line += ('| ' + teamNick + computeWhitespace(teamNick, LongestTeamLen + 1) + '|')

            #Team Score
            imageScore = rowdata[TeamScoreIndex].text
            Line += ' ' + (imageScore + computeWhitespace(imageScore, 5) + '|')

            if(HasCisco):
                #Cisco Score if applicable
                ciscoScore = rowdata[CiscoScoreIndex].text
                Line += (str(ciscoScore) + computeWhitespace(ciscoScore, 7) + '|')

                #Total Score if applicable
                totalScore = round(float(imageScore) + float(ciscoScore), 4)
                Line += (str(totalScore) + computeWhitespace(totalScore, 7) + '|')
            
            #State Rank
            Line += ' ' + (str(stateCounter) + computeWhitespace(stateCounter, 6) + '|')

            #Total Rank
            Line += ' ' + (str(totalCounter) + computeWhitespace(totalCounter, 6) + '|')

            #Team time. All times given are 5-character.
            Line += (rowdata[ScoreTimeIndex].text + '|') 

            totalPercentile = str(round(100 / TotalTeams * (TotalTeams - (totalCounter - 1)),2)) + '%'
            Line += ('  ' + totalPercentile + computeWhitespace(totalPercentile, 7) + ' |')

            statePercentile = str(round(100 / StateTeams * (StateTeams - (stateCounter - 1)),2)) + '%'
            Line += ('  ' + statePercentile + computeWhitespace(statePercentile, 7) + ' |')

            print(Line)

    #Prints the bottom row of the table.
    if(HasCisco):
        print('|' + formatPrettyBorder('', LongestTeamLen + 2) + '|⎯ ⎯ ⎯ | ⎯ ⎯ ⎯ | ⎯ ⎯ ⎯ | ⎯ ⎯ ⎯ | ⎯ ⎯ ⎯ | ⎯ ⎯ ⎯  | ⎯ ⎯ ⎯ ⎯ ⎯| ⎯ ⎯ ⎯ ⎯ ⎯|') 
    else:
        print('|' + formatPrettyBorder('', LongestTeamLen + 2) + '|⎯ ⎯ ⎯ | ⎯ ⎯ ⎯ | ⎯ ⎯ ⎯ | ⎯ ⎯ ⎯  | ⎯ ⎯ ⎯ ⎯ ⎯| ⎯ ⎯ ⎯ ⎯ ⎯|') 
    
    #If applicable, only counts teams in Tier specified
    print('Total Teams:', TotalTeams, '\n' + 'State Teams:', StateTeams)
    print()

    sleep(30)

    #Accounts for the header, footer, two lines at the end, and an empty line
    clearLine(teamsFoundCounter + 5)
    
    #print("\n\n")
