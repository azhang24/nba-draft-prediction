from bs4 import BeautifulSoup
import requests

exclude_stats = ['season', 'school_name', 'conf_abbr', 'sos-dum', 'ws-dum', 'poss-dum', 'bpm-dum']

def get_player_ncaa_stats(player_name, stat_types, year):
    player_name = "-".join(player_name.lower().split())
    url = "https://www.sports-reference.com/cbb/players/{}-1.html".format(player_name)
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    player_stats = {}
    for stat_type in stat_types:
        if stat_type == "Per Game":
            player_stats = get_stat_type(soup, 'players_per_game.{}'.format(year), player_stats)
        elif stat_type == "Per 40":
            player_stats = get_stat_type(soup, 'players_per_min.{}'.format(year), player_stats)
        elif stat_type == "Per 100 Poss":
            player_stats = get_stat_type(soup, 'players_per_poss.{}'.format(year), player_stats)
        elif stat_type == "Advanced":
            player_stats = get_stat_type(soup, 'players_advanced.{}'.format(year), player_stats)
    return player_stats

def get_stat_type(soup, stat_id, player_stats):
    stats = soup.find(id=stat_id)
    if stats != None:
        children = list(stats.children)
        for child in children:
            stat = child.get('data-stat')
            if stat not in exclude_stats:
                player_stats[stat] = float(child.contents[0])
    return player_stats
    

def get_draft_class(year, ncaa_only=False):
    url = "https://www.basketball-reference.com/draft/NBA_{}.html".format(year)
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    players = []
    table_container = soup.find(id='stats')
    table_body = table_container.tbody
    player_rows = table_body.find_all('tr')
    for player in player_rows:
        if not player.has_attr('class'):
            attributes = player.find_all('td')
            player_college = attributes[3]
            player_college_name = ""
            if len(player_college.contents) == 0 and ncaa_only:
                continue
            else:
                player_name = attributes[2].a.contents[0]
                players.append(player_name)
    return players



