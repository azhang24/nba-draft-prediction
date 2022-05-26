from bs4 import BeautifulSoup
import requests
import unidecode
from overrides import player_id_override_mapping, player_name_override_mapping, player_id_override_mapping_ncaa, player_name_override_mapping_ncaa, player_year_override_mapping

exclude_stats = ['season', 'school_name', 'conf_abbr', 'sos-dum', 'ws-dum', 'poss-dum', 'bpm-dum']


def get_player_ncaa_stats(player_name, stat_types, year):
    soup, year = get_ncaa_player_soup(player_name, year)
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
                if len(child.contents) == 0:
                    player_stats[stat] = 0.0
                else:
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

def get_total_win_shares_nba(player_name, draft_year, start_year=None, num_seasons=None, playoffs=False):
    soup = get_nba_player_soup(player_name, draft_year)
    if num_seasons == None: # Get entire career
        num_seasons = get_num_seasons(soup, start_year)
    total_ws = get_total_win_shares_from_soup(soup, start_year, num_seasons)
    if playoffs:
        total_ws += get_total_win_shares_from_soup(soup, start_year, num_seasons, playoffs=True)
    return total_ws

def get_total_win_shares_from_soup(soup, start_year, num_seasons, playoffs=False):
    total_ws = 0.0
    for year in range(start_year, start_year+num_seasons):
        total_ws += get_win_shares_for_year(soup, year, playoffs)
    return total_ws

def get_win_shares_for_year(soup, year, playoffs=False):
    html_id = 'playoffs_advanced' if playoffs else 'advanced'
    html_id = html_id + '.{}'.format(year)
    advanced_stats_row = soup.find(id=html_id)
    ws = 0.0
    if advanced_stats_row != None:
        advanced_stats_attributes = advanced_stats_row.find_all('td')
        for attribute in advanced_stats_attributes:
            if 'data-stat' in attribute.attrs and attribute['data-stat'] == 'ws':
                ws = attribute.contents[0]
                has_strong = attribute.find('strong')
                if has_strong != None:
                    ws = attribute.strong.contents[0]
    return float(ws)

def get_max_win_shares_nba(player_name, draft_year, start_year=None, num_seasons=None, playoffs=False):
    soup = get_nba_player_soup(player_name, draft_year)
    if num_seasons == None: # Get entire career
        num_seasons = get_num_seasons(soup, start_year)
    max_ws = -10000000000.0
    for year in range(start_year, start_year+num_seasons):
        ws = get_win_shares_for_year(soup, year, playoffs=False)
        playoff_ws = 0.0
        if playoffs:
            playoff_ws = get_win_shares_for_year(soup, year, playoffs=playoffs)
        total_ws_for_year = ws + playoff_ws
        if total_ws_for_year > max_ws:
            max_ws = total_ws_for_year
    if max_ws == -10000000000.0:
        max_ws = 0.0
    return max_ws

def get_ncaa_player_soup(player_name, year):
    player_id = "1"
    if player_name in player_year_override_mapping:
        year = player_year_override_mapping[player_name]
    if (player_name, year) in player_id_override_mapping_ncaa:
        player_id = player_id_override_mapping_ncaa[(player_name, year)]
    if player_name in player_name_override_mapping_ncaa:
        player_name = player_name_override_mapping_ncaa[player_name]
    names = player_name.lower().split()
    processed_names = []
    for name in names:
        name = unidecode.unidecode(name)
        name = name.replace(".", "")
        name = name.replace("\'", "")
        processed_names.append(name)
    player_name = "-".join(processed_names)
    url = "https://www.sports-reference.com/cbb/players/{}-{}.html".format(player_name, player_id)
    return get_soup(url), year

def get_nba_player_soup(player_name, draft_year):
    if player_name in player_name_override_mapping:
        player_name = player_name_override_mapping[player_name]
    names = player_name.split()
    first_name = names[0]
    last_name = names[1]
    first_name = unidecode.unidecode(first_name.lower())
    last_name = unidecode.unidecode(last_name.lower())
    first_name = first_name.replace("\'", "")
    last_name = last_name.replace("\'", "")
    player_id = last_name[:5]+first_name[:2]
    if (player_name, draft_year) in player_id_override_mapping:
        player_id = player_id + player_id_override_mapping[(player_name, draft_year)]
    else:
        player_id = player_id + "01" 
    url = "https://www.basketball-reference.com/players/{}/{}.html".format(last_name[0], player_id)
    return get_soup(url)

def get_soup(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    return soup

def get_num_seasons(soup, start_year=None):
    advanced_stats_table = soup.find(id='advanced')
    if advanced_stats_table == None:
        return 0
    all_seasons = advanced_stats_table.tbody.find_all(class_='full_table')
    if start_year == None: # start year defaults to the rookie season
        start_year = int(all_seasons[0].get('id').split('.')[1])
    end_year = int(all_seasons[-1].get('id').split('.')[1])
    num_seasons = end_year - start_year + 1
    return num_seasons


