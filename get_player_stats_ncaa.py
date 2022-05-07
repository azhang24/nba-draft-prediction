import player_api
import json
import argparse

def main():
    parser = argparse.ArgumentParser(description="Get stats for NBA Draft Prospects in the NCAA")
    parser.add_argument('--name', help='Name of NBA Draft Prospect in NCAA (ex. Chet Holmgren)')
    parser.add_argument('--year', type=int, help='Year prospect declared for draft (cannot be earlier than 2010)')
    args = parser.parse_args()
    name = args.name
    year = args.year
    print("NCAA Stats for {}".format(name))
    print(json.dumps(player_api.get_player_ncaa_stats(
        player_name=name, 
        stat_types=["Per Game", "Per 40", "Per 100 Poss", "Advanced"], 
        year=year), indent=4))

if __name__ == "__main__":
    main()
