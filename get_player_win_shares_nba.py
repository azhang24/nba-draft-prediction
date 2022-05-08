import player_api
import json
import argparse

def main():
    parser = argparse.ArgumentParser(description="Get total win shares for all NBA players for every draft class between start and end year")
    parser.add_argument('--start_year', type=int, help='First draft class')
    parser.add_argument('--end_year', type=int, help='Last draft class')
    parser.add_argument('--seasons', type=int, help='Number of seasons to total win shares for each player')
    parser.add_argument('--ncaa_only', help='Only retrieve win shares of players who played in the NCAA', action='store_true')
    parser.add_argument('--playoffs', help='Include playoff win shares', action='store_true')
    parser.add_argument('--sorted', help='Sort players in Json for each year by decreasing total win shares', action='store_true')

    args = parser.parse_args()
    start_year = args.start_year
    end_year = args.end_year
    num_seasons = args.seasons
    ncaa_only = args.ncaa_only
    playoffs = args.playoffs
    is_sorted = args.sorted

    if end_year == None:
        end_year = 2021

    players = {}

    for year in range(start_year, end_year+1):
        players[year] = []
        draft_class = player_api.get_draft_class(year=year, ncaa_only=ncaa_only)
        for player in draft_class:
            player_win_shares = player_api.get_total_win_shares_nba(player_name=player, start_year=(year+1), num_seasons=num_seasons, playoffs=playoffs)
            player_stats = {}
            player_stats['player_name'] = player
            player_stats['win_shares'] = player_win_shares
            players[year].append(player_stats)
        if is_sorted:
            players[year] = sort_by_win_shares(players[year])
    
    f = open('player_win_shares.json', 'w')
    json.dump(players, f, ensure_ascii=False, indent=4)

def sort_by_win_shares(players):
    win_shares_to_player = {}
    for player in players:
        win_shares_to_player[player['win_shares']] = player['player_name']
    win_shares = win_shares_to_player.keys()
    win_shares_sorted = sorted(win_shares, reverse=True)
    sorted_players = []
    for win_share in win_shares_sorted:
        player_info = {
            'player_name': win_shares_to_player[win_share],
            'win_shares': win_share
        }
        sorted_players.append(player_info)
    return sorted_players

if __name__ == "__main__":
    main()