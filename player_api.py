from bs4 import BeautifulSoup
import requests

per_40_stats = [
    "GS",
    "MP",
    "FG",
    "FGA",
    "FG%",
    "2P",
    "2PA",
    "2P%",
    "3P",
    "3PA",
    "3P%",
    "FT",
    "FTA",
    "FT%",
    "TRB",
    "AST",
    "STL",
    "BLK",
    "TOV",
    "PF",
    "PTS"
]

def get_player_ncaa_stats(player_name, stat_type):
    player_name = "-".join(player_name.lower().split())
    url = "https://www.sports-reference.com/cbb/players/{}-1.html".format(player_name)
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    player_stats = {}
    if stat_type == "Per 40":
        stats = soup.find(id='players_per_min.2022')
        children = list(stats.children)
        for index, stat in enumerate(per_40_stats):
            player_stats[stat] = float(children[index+4].contents[0])
    return player_stats



