# Works only for DE log files
import collections
import os, re, time

import matplotlib.pyplot as plt
import numpy as np

# Data labels, sizes, and colors are defined:
print('Welcome to Worms Armageddon LogParser @Booyeoo')
start_time = time.time()
# Identify the path and create global dict
#path_of_the_directory = 'C:/Games/Worms Armageddon v3.7.2.1/User/Games/Temp'
path_of_the_directory = 'C:/Games/Worms Armageddon v3.7.2.1/User/Games'

# Main Dictionary for all Games individually
wormsStatsDictionaries = {}
# Side Dictionary storing the general statistics like total wins...
wormsStatsEasyCounter = {}
# Temp Var for each game
thisGame = {}
# Worms Log Extension
ext = '.log'

# YEAR --- IMPORTANT for Stats
year = 'Total' #for filtering on a specific year - set to 'Total' to get all
print("Scanning files in the specified path:" + path_of_the_directory)
debug = False
debugTeam = False
debugWeapons = False

# For debugging computer Teamnames and double usages of teams
# Potentially to be edited depending on the teams which has been used by whom in local games
# Preferred mapping on teams for online / lan games
wormsStatsEasyCounter['Teams'] = {'1-UP': 'Computer1'}
wormsStatsEasyCounter['Teams'].update({'2-UP': 'Computer2'})
wormsStatsEasyCounter['Teams'].update({'3-UP': 'Computer3'})
wormsStatsEasyCounter['Teams'].update({'4-UP': 'Computer4'})
wormsStatsEasyCounter['Teams'].update({'5-UP': 'Computer5'})
wormsStatsEasyCounter['Teams'].update({'Marcel': 'Marcel'})
wormsStatsEasyCounter['Teams'].update({'Smie': 'Smie'})
wormsStatsEasyCounter['Teams'].update({'Stevo': 'Stevo'})
#wormsStatsEasyCounter['Teams'].update({'BICNIC': 'Nico'})

# ---- STATS ---- #
#Creating a pie chart for the winner stats
def createPieChart(labels,sizes,title):

    #colors = ['green', 'blue', 'red']

    def absolute_value(val):
        a  = sizes[ np.abs(sizes - val/100.*sizes.sum()).argmin() ]
        return a

    plt.pie(sizes, labels=labels,
            autopct=absolute_value, shadow=True)
    plt.title(title)
    plt.axis('equal')
    plt.show()

def func(pct, allvals):
    absolute = int(np.round(pct/100.*np.sum(allvals)))
    return "{:.1f}% - ({:d})".format(pct, absolute)

#def func(pct, allvals):
#    absolute = int(np.round(pct*np.sum(allvals)))
#    return "{:.1f}% - ({:d})".format(pct, absolute)

#Creating a pie chart for the weapon stats
def createBarChart2(weaponsAndValuesAsDict,playerForTitle,divisor):
    weapons = list(weaponsAndValuesAsDict.keys())
    values = [value / divisor for value in weaponsAndValuesAsDict.values()]
    valuesAbs = [value for value in weaponsAndValuesAsDict.values()]

    # Create the figure and axis
    fig, ax = plt.subplots(figsize=(18, 10))
    # Plot the horizontal bars
    ax.barh(weapons,values)
    # Add the x-axis label
    ax.set_xlabel('Amount activated')
    # Add the y-axis label
    ax.set_ylabel('Weapon')
    # Add the title
    ax.set_title('Weaponstats Total')

    bars = ax.barh(weapons, values)

    # Iterate over the bars and add labels
    for i, bar in enumerate(bars):
        width = bar.get_width()
        ax.text(width, bar.get_y() + bar.get_height()/2,
                func(values[i], valuesAbs),
                ha='left', va='center')

    plt.title(playerForTitle+' Weaponstats Total')
    ax.set_facecolor('#F0F0F0')
    ax.set_xlabel('Amount activated')
    ax.set_ylabel('Weapon')
    plt.show()

def createBarChart1(weaponsAndValuesAsDict, playerForTitle, divisor):
    plt.rcParams["figure.figsize"] = [18, 10]
    plt.rcParams["figure.autolayout"] = True
    fig, ax = plt.subplots()
    values = [value / divisor for value in weaponsAndValuesAsDict.values()]
    valuesAbs =  [value for value in weaponsAndValuesAsDict.values()]
    bars = ax.barh(list(weaponsAndValuesAsDict.keys()), values)
    bars2 = ax.barh(list(weaponsAndValuesAsDict.keys()), valuesAbs)
    ax.bar_label(bars)
    ax.bar_label(bars2)
    ax.text(bars2)
    plt.title(playerForTitle+' Weaponstats Total')
    ax.set_facecolor('#F0F0F0')
    ax.set_xlabel('Amount activated')
    ax.set_ylabel('Weapon')
    ax.set_yticklabels(list(weaponsAndValuesAsDict.keys()), fontweight='bold')
    for bar in bars:
        bar.set_color('green')
        bar.set_edgecolor('white')
       # ax.text(bar.get_x() + bar.get_width()/2, bar.get_y() + bar.get_height() / 2, '{:.0%}'.format(bar.get_width()), ha='left', va='center')
    plt.show()

# --- HELPERS ---

# for checking if game has been disconnected
def checkCorruption(f,fileContent):
    strings = re.findall(r'••• Game Ends - User Quit', fileContent)
    if len(strings)>0: print('Corruption found on '+str(f))
    return len(strings)>0

# easy incrementor for dics
def dicIncrement(dic, key):
    dic[key] = dic.get(key, 0) + 1
    return dic

# saving new value in dic and check for existence
def saveInDic(dic, key, value):
    if len(dic) == 0:
        dic[key] = value
    elif dic.__contains__(key):
        dicNew = dic.get(key)
        dicNew.update(value)
    else:
        dic.update({key: value})
    return dic

#AI generic incrementor for simple dic value counter
def incrementDict1d(counter_dict, key, value):
    if key in counter_dict:
        counter_dict[key].update({value: counter_dict[key].get(value, 0) + 1})
    else:
        counter_dict[key] = {value: 1}
    return counter_dict

#AI generic incrementor for looping dictionaries
def incrementDict2d(counter_dict, key1, key2, value):
    if key1 in counter_dict:
        if key2 in counter_dict[key1]:
            counter_dict[key1][key2].update({value: counter_dict[key1][key2].get(value, 0) + 1})
        else:
            counter_dict[key1][key2] = {value: 1}
    else:
        counter_dict[key1] = {key2: {value: 1}}
    return counter_dict

def getKeyFromValue(dic, value):
    for x, y in dic.items():  # for name, age in dictionary.iteritems():  (for Python 2.x)
        if y == value:
            return x
    return None

def playerFromTeamname(dic, teamname):
    return dic.get(teamname)

def shortStringPlayer(playerList):
    orderedList = sorted(playerList)
    returnString = ""
    for i in orderedList:
        returnString = returnString + i
    return returnString

# --- MAIN Function used to identify all lines --- #

# Parse line by line and allocate to specific attribute of the game
def parseWormsLine(line, thisGame):
    # When game has taken place
    if (line.startswith('Game Started at ')):
        # When the game took place date & time
        gameStarted = (line.split('Game Started at ')[1])
        thisGame.update({'gameStarted': gameStarted})
        return thisGame

    # Playercount and allocation of Team
    elif len(re.findall('(".+")\s+as\s+(".+")', line)) > 0 or len(re.findall('([^\s|^ID]+):\s+(".+")', line)) > 0:
        if not thisGame['Offline']:
            splitter = re.split('(".+")\s+as\s+(".+")', line)
            if debugTeam: print('splitter:' + str(splitter))
            # print(re.findall('\w+',splitter[0])+re.findall('\"(.*?)\"{1}',splitter[1])+re.findall('\"(.*?)\"{1}',splitter[2]))
            # playerString = re.findall('\w+', splitter[0])[0]
            playerNameAndTeam = re.findall('\"(.*?)\"{1}', splitter[1]) + re.findall('\"(.*?)\"{1}', splitter[2])
            player = playerNameAndTeam[0]
            team = playerNameAndTeam[1]
        else:
            splitter = re.split('([^\s|^ID]+):\s+(".+")', line)
            if debugTeam: print('splitter' + str(splitter))
            team = (re.findall('\"(.*?)\"', splitter[2]))[0]
            if debugTeam: print('TEAM: ' + str(team))
            player = wormsStatsEasyCounter.get('Teams').get(team)
            if debugTeam: print('Player ' + str(player))

        # Teams and Weapons
        if (thisGame.__contains__(player)):

            playerStats = thisGame.get(player)
            if playerStats.__contains__('Team'):
                thisGame['Corrupt'] = True
                return thisGame
        else:
            thisGame.update({player: {'Team': team}})
            thisGame[player]['Weapons'] = {}

        if thisGame.__contains__('Teams'):
            thisGame['Teams'].update({team: player})
        else:
            thisGame['Teams'] = {team: player}

        if wormsStatsEasyCounter.__contains__(player):
            # why this works?
            if debugWeapons: print(wormsStatsEasyCounter[player]['Team'])
        else:
            wormsStatsEasyCounter.update({player: {'Team': team}})
         #   wormsStatsEasyCounter.update({player: {'GamesCount': 1}})

        if wormsStatsEasyCounter.__contains__('Teams'):
            if player not in wormsStatsEasyCounter['Teams']:
                if debugWeapons: print('HIER!' + str(player) + str(team))
            wormsStatsEasyCounter['Teams'].update({team: player})

        else:
            wormsStatsEasyCounter['Teams'] = {team: player}
        return thisGame

    # Weapon counting
    elif (len(re.findall('(\[.+\]) ••• (?P<Teamname>.+)\s\((?P<Playername>.+)\)(\sfires\s)(?P<Weapon>.+)', line)) > 0):
        lineRegExtract = (
            #   re.split('(\[.+\]) ••• (?P<Teamname>.+)\s\((?P<Playername>.+)\)(\sfires\s)(?P<Weapon>.+)', line))
            re.split('(\((?:.(?!\())+( fires))\s(.+$)', line))
        if debugWeapons: print('lineReg:' + str(lineRegExtract))
        player = lineRegExtract[1].split(' fires')[0]
        player = player.replace('(', '').replace(')', '')
        if thisGame['Offline']:
            if player == ' o ':
                player = '( o ) ( o )'
            if debugWeapons: print('Offline:' + player + ' ' + str(thisGame['Offline']))
            if debugWeapons: print(str(wormsStatsEasyCounter.get('Teams')))
            player = wormsStatsEasyCounter.get('Teams').get(player)

        weapon = lineRegExtract[3]

        if debugWeapons: print("player: " + str(player) + " | weapon: " + str(weapon))
        if debugWeapons: print("ThisGame:" + str(thisGame))
        playerWeaponStats = thisGame.get(player).get('Weapons')
        playerTotalStats = wormsStatsEasyCounter.get(player)
        playerWeaponStats = dicIncrement(playerWeaponStats, weapon)
        thisGame[player]['Weapons'] = playerWeaponStats
        playerTotalStats = dicIncrement(playerTotalStats, weapon)
        wormsStatsEasyCounter.update({player: playerTotalStats})
        return thisGame
    elif (line.startswith('Rundenzeit: ')):
        gameLength = (line.split('Rundenzeit: ')[1])
        thisGame.update({'gameLength': gameLength})
        return thisGame
        # (.+) gewinnt d(i|a)(e|s) (Match!|Runde\.)
    # elif (line.endswith('gewinnt die Runde.') or line.endswith('gewinnt das Match!')):

    #### ALL GAMES ARE ONLY COUNTED WHICH HAD AN PROPER END WITH A WINNER####

    elif len(re.findall('(.+) gewinnt d.. (Match|Runde).', line)) > 0:
        # (.+) gewinnt d(i|a)(e|s) (Match!|Runde\.){1}
        winner = (re.split('(.+) gewinnt d.. (Match|Runde).', line))[1]

        # Checking teams involved - all and particular game

        teams = wormsStatsEasyCounter.get('Teams')
        teamsInGame = thisGame.get('Teams')
        playerList = sorted((list(teamsInGame.values())))
        keyPlayerList = shortStringPlayer(playerList)

        if debugTeam: print('KeyTeamsList :' + keyPlayerList)
        winnerPlayer = playerFromTeamname(teams, winner)
        thisGame['Winner'] = winnerPlayer

        # WINNER
        incrementDict1d(wormsStatsEasyCounter, 'Winner', winnerPlayer)

        # GAMESCOUNTERTOTAL
        for player in playerList:
            incrementDict1d(wormsStatsEasyCounter, 'GamesCountTotal', player)

        # GAMESCOUNTERSPECIAL
        #DONE: Include calculation of Games for each player for weapon stats GameCounter keyPlayerList teamsVersus player
        for player in playerList:
            incrementDict2d(wormsStatsEasyCounter,'GameCounter',keyPlayerList,player)

        # TODO Divide the number of weapons against total games count

        # WINNERSPECIAL
        incrementDict2d(wormsStatsEasyCounter,'WinnerSpecial',keyPlayerList,winnerPlayer)

        return thisGame
    return thisGame

# ----->>> START MAIN LOOP<<<---- #
if (year!='Total'):
    for filename in os.listdir(path_of_the_directory):
        f = os.path.join(path_of_the_directory, filename)
        if os.path.isfile(f):
            if f.endswith(ext) and f.__contains__(year):
                thisGame = {}
                with open(f, "r") as a_file:
                    print("Scanning:" + f)
                    # check for consistency on file
                    #if checkCorruption(f,a_file.read()): continue
                    thisGame['Corrupted'] = False
                    # reset on recursion
                    thisGame['Offline'] = f.find('Offline') > 0
                    # print(thisGame.get('Offline'))
                    for line in a_file:
                        stripped_line = line.strip()
                        thisGame = (parseWormsLine(line, thisGame))
                        if thisGame.get('Corrupted'): break
                    # print(thisGame)
                    wormsStatsDictionaries.update({filename: thisGame})
else:
    for filename in os.listdir(path_of_the_directory):
        f = os.path.join(path_of_the_directory, filename)
        if os.path.isfile(f):
            if f.endswith(ext):
                thisGame = {}
                with open(f, "r") as a_file:
                    print("Scanning:" + f)
                    # check for consistency on file
                    #if checkCorruption(f,a_file.read()): continue
                    thisGame['Corrupted'] = False
                    # reset on recursion
                    thisGame['Offline'] = f.find('Offline') > 0
                    # print(thisGame.get('Offline'))
                    for line in a_file:
                        stripped_line = line.strip()
                        thisGame = (parseWormsLine(line, thisGame))
                        if thisGame.get('Corrupted'): break
                    # print(thisGame)
                    wormsStatsDictionaries.update({filename: thisGame})

print(wormsStatsDictionaries)
print(wormsStatsEasyCounter)
print("---- Runtime: --- %s seconds ---" % (time.time() - start_time))

def generateWinnerStatisticFor(key,timeframe='Total'):
    if (wormsStatsEasyCounter.get('WinnerSpecial').__contains__(key)):
        print(timeframe+' '+key+': '+str(wormsStatsEasyCounter.get('WinnerSpecial').get(key)))
        keys, values = zip(*(wormsStatsEasyCounter.get('WinnerSpecial').get(key).items()))
        keys=np.array(keys)
        values=np.array(values)
        createPieChart(keys,values,key+' '+timeframe)
    else: print(timeframe+' '+key+':  not exisiting this year. Watch out to check out for the YEAR parameter.')

def generateWeaponStatisticForPlayer(player,timeframe='Weapons'):
    weaponStats = collections.OrderedDict(reversed(sorted(wormsStatsEasyCounter.get(player).items())))
    getAmountOfGamesForThatPlayer=wormsStatsEasyCounter['GamesCountTotal'][player]
    #print(getAmountOfGamesForThatPlayer)
    del weaponStats['Team']
    #print(weaponStats)
    #print(weaponStats.keys())
    createBarChart2(weaponStats,player,getAmountOfGamesForThatPlayer)


generateWinnerStatisticFor('BooyeooMajor',year)
generateWinnerStatisticFor('BooyeooMajorhistorisch',year)
generateWinnerStatisticFor('BICNICBooyeooMajorhistorisch',year)
generateWinnerStatisticFor('BICNICBooyeooMajor',year)
generateWinnerStatisticFor('Booyeoohistorisch',year)
generateWinnerStatisticFor('Majorhistorisch',year)
generateWeaponStatisticForPlayer('historisch')
generateWeaponStatisticForPlayer('Major')
generateWeaponStatisticForPlayer('Booyeoo')
generateWeaponStatisticForPlayer('BICNIC')



