import player_api
import json
import argparse

def main():
    parser = argparse.ArgumentParser(description="Get total win shares for NBA players")
    parser.add_argument('--name', help='(Required) Name of NBA Player (ex. Lebron James)')
    parser.add_argument('--year', type=int, help='Year to start totaling win shares from')
    parser.add_argument('--seasons', type=int, help='Number of seasons to total win shares for')
    parser.add_argument('--playoffs', help='Include playoff win shares', action='store_true')

    args = parser.parse_args()
    name = args.name
    start_year = args.year
    num_seasons = args.seasons
    playoffs = args.playoffs

    print(player_api.get_total_win_shares_nba(player_name=name, start_year=start_year, num_seasons=num_seasons, playoffs=playoffs))

if __name__ == "__main__":
    main()