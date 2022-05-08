from bs4 import BeautifulSoup
import requests
import unidecode

exclude_stats = ['season', 'school_name', 'conf_abbr', 'sos-dum', 'ws-dum', 'poss-dum', 'bpm-dum']
player_override_mapping = {
    "Anthony Davis": "02"
}

def get_player_ncaa_stats(player_name, stat_types, year):
    player_name = "-".join(player_name.lower().split())
    url = "https://www.sports-reference.com/cbb/players/{}-1.html".format(player_name)
    soup = get_soup(url)
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
    soup = get_soup(url)
    players = []
    table_container = soup.find(id='stats')
    table_body = table_container.tbody
    player_rows = table_body.find_all('tr')
    for player in player_rows:
        if not player.has_attr('class'):
            attributes = player.find_all('td')
            if len(attributes) == 1 and attributes[0].get('data-stat') == 'skip':
                continue
            player_college = attributes[3]
            player_college_name = ""
            if len(player_college.contents) == 0 and ncaa_only:
                continue
            else:
                player_name = attributes[2].a.contents[0]
                players.append(player_name)
    return players

def get_total_win_shares_nba(player_name, start_year=None, num_seasons=None, playoffs=False):
    names = player_name.split()
    first_name = names[0]
    last_name = ""
    if len(names) == 1:
        if first_name == "Nenê":
            last_name = "Hilário"
    else:
        last_name = names[1]
    first_name = unidecode.unidecode(first_name.lower())
    last_name = unidecode.unidecode(last_name.lower())
    player_id = last_name[:5]+first_name[:2]
    if player_name in player_override_mapping:
        player_id = player_id + player_override_mapping[player_name]
    else:
        player_id = player_id + "01" 
    url = "https://www.basketball-reference.com/players/{}/{}.html".format(last_name[0], player_id)
    soup = get_soup(url)
    if num_seasons == None: # Get entire career
        advanced_stats_table = soup.find(id='advanced')
        all_seasons = advanced_stats_table.tbody.find_all(class_='full_table')
        if start_year == None: # start year defaults to the rookie season
            start_year = int(all_seasons[0].get('id').split('.')[1])
        end_year = int(all_seasons[-1].get('id').split('.')[1])
        num_seasons = end_year - start_year + 1
    total_ws = get_total_win_shares_from_soup(soup, start_year, num_seasons)
    if playoffs:
        total_ws += get_total_win_shares_from_soup(soup, start_year, num_seasons, playoffs=True)
    return total_ws

def get_total_win_shares_from_soup(soup, start_year, num_seasons, playoffs=False):
    total_ws = 0.0
    for year in range(start_year, start_year+num_seasons):
        html_id = 'playoffs_advanced' if playoffs else 'advanced'
        html_id = html_id + '.{}'.format(year)
        advanced_stats_row = soup.find(id=html_id)
        if advanced_stats_row != None:
            advanced_stats_attributes = advanced_stats_row.find_all('td')
            for attribute in advanced_stats_attributes:
                if 'data-stat' in attribute.attrs and attribute['data-stat'] == 'ws':
                    ws = attribute.contents[0]
                    has_strong = attribute.find('strong')
                    if has_strong != None:
                        ws = attribute.strong.contents[0]
                    total_ws += float(ws)
    return total_ws


def get_soup(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    return soup


