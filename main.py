import player_api
import json
import argparse

def main():
    parser = argparse.ArgumentParser(description="Get stats for NBA Draft Prospects in the NCAA")
    parser.add_argument('--name', help='Name of NBA Draft Prospect in NCAA (ex. Chet Holmgren)')
    parser.add_argument('--year', type=int, help='Year prospect declared for draft (cannot be earlier than 2010)')
    parser.add_argument('--ncaa_only', help='Only print prospects from the draft class who played in the NCAA', action='store_true')
    args = parser.parse_args()
    name = args.name
    year = args.year
    ncaa_only = args.ncaa_only
    print("NCAA Stats for {}".format(name))
    print(json.dumps(player_api.get_player_ncaa_stats(
        player_name=name, 
        stat_types=["Per Game", "Per 40", "Per 100 Poss", "Advanced"], 
        year=year), indent=4))
    print()
    print("{} Draft Class".format(year))
    if ncaa_only:
        print("(NCAA Only)")
    print(player_api.get_draft_class(year=year, ncaa_only=ncaa_only))

if __name__ == "__main__":
    main()
