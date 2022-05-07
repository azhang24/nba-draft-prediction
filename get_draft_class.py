import player_api
import json
import argparse

def main():
    parser = argparse.ArgumentParser(description="Get list of players in a draft class')
    parser.add_argument('--year', type=int, help='(Required) Year of draft class')
    parser.add_argument('--ncaa_only', help='Only list prospects from the draft class who played in the NCAA', action='store_true')
    args = parser.parse_args()
    year = args.year
    ncaa_only = args.ncaa_only
    print("{} Draft Class".format(year))
    if ncaa_only:
        print("(NCAA Only)")
    print(player_api.get_draft_class(year=year, ncaa_only=ncaa_only))

if __name__ == "__main__":
    main()