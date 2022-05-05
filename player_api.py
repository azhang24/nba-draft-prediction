from bs4 import BeautifulSoup
import requests


general_stats = {
    "G": 3,
    "GS": 4,
    "MP": 5,
    "FG%": 8,
    "2P%": 11,
    "3P%": 14,
    "FT%": 17,
    "SOS": 28
}

per_40_stats = {
    "FG": 6,
    "FGA": 7,
    "2P": 9,
    "2PA": 10,
    "3P": 12,
    "3PA": 13,
    "FT": 15,
    "FTA": 16,
    "TRB": 18,
    "AST": 19,
    "STL": 20,
    "BLK": 21,
    "TOV": 22,
    "PF": 23,
    "PTS": 24
}

per_100_poss_stats = {
    "ORtg": 26,
    "DRtg": 27
}

per_100_poss_stats = {**per_40_stats, **per_100_poss_stats}

per_40_stats = {(k + " Per 40"):v for k,v in per_40_stats.items()}
per_100_poss_stats = {(k + " Per 100 poss"):v for k,v in per_100_poss_stats.items()}

advanced_stats = {
    "PER": 6,
    "TS%": 7,
    "eFG%": 8,
    "3PAr": 9,
    "FTr": 10,
    "PProd": 11,
    "ORB%": 12,
    "DRB%": 13,
    "TRB%": 14,
    "AST%": 15,
    "STL%": 16,
    "BLK%": 17,
    "TOV%": 18,
    "USG%": 19,
    "OWS": 21,
    "DWS": 22,
    "WS": 23,
    "WS/40": 24,
    "OBPM": 26,
    "DBPM": 27,
    "BPM": 28
}

def get_player_ncaa_stats(player_name, stat_types, year):
    player_name = "-".join(player_name.lower().split())
    url = "https://www.sports-reference.com/cbb/players/{}-1.html".format(player_name)
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    player_stats = {}
    for stat_type in stat_types:
        if stat_type == "General":
            player_stats = get_stat_type(soup, general_stats, 'players_per_game.{}'.format(year), player_stats)
        elif stat_type == "Per 40":
            player_stats = get_stat_type(soup, per_40_stats, 'players_per_min.{}'.format(year), player_stats)
        elif stat_type == "Per 100 Poss":
            player_stats = get_stat_type(soup, per_100_poss_stats, 'players_per_poss.{}'.format(year), player_stats)
        elif stat_type == "Advanced":
            player_stats = get_stat_type(soup, advanced_stats, 'players_advanced.{}'.format(year), player_stats)
    return player_stats

def get_stat_type(soup, stat_type, stat_id, player_stats):
    stats = soup.find(id=stat_id)
    children = list(stats.children)
    for stat, index in stat_type.items():
        player_stats[stat] = float(children[index].contents[0])
    return player_stats



