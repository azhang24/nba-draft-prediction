import player_api
import csv

def main():
    ncaa_draft_prospects_2022 = [
        "Jabari Smith",
        "Chet Holmgren",
        "Paolo Banchero",
        "Jaden Ivey",
        "Keegan Murray",
        "Bennedict Mathurin",
        "AJ Griffin",
        "Jeremy Sochan",
        "Malaki Branham",
        "Jonathan Davis",
        "Jalen Duren",
        "Mark Williams",
        "Tyty WashingtonJr",
        "Ochai Agbaji",
        "Tari Eason",
        "Walker Kessler",
        "Patrick BaldwinJr",
        "Jake Laravia",
        "Kendall Brown",
        "Bryce McGowens",
        "Blake Wesley",
        "Jalen Williams",
        "Terquavion Smith",
        "Dalen Terry",
        "Kennedy Chandler",
        "Trevor Keels",
        "EJ Liddell",
        "Wendell MooreJr",
        "Christian Koloko",
        "Ryan Rollins",
        "Harrison Ingram",
        "Christian Braun",
        "Max Christie",
        "Josh Minott",
        "Jaylin Williams",
        "Justin Lewis",
        "Peyton Watson",
        "JD Davison",
        "Jabari Walker",
        "Kris Murray",
        "Moussa Diabate",
        "Kevin McCullar",
        "Hyunjung Lee",
        "Caleb Houstan",
        "Jordan Hall",
        "Julian Champagnie",
        "Keon Ellis",
        "Alondes Williams",
        "Isaiah Mobley",
        "Julian Strawther",
        "David Roddy",
        "Trevion Williams"
    ]

    players = {}

    for player in ncaa_draft_prospects_2022:
        print(player)
        player_ncaa_stats = player_api.get_player_ncaa_stats(player_name=player, stat_types=["Per Game", "Per 40", "Per 100 Poss", "Advanced"], year=2022)
        players[player] = player_ncaa_stats

    with open('player_data_2022.csv', 'w') as player_data_csv_2022:
        fieldnames = ['player_name', 'draft_class']
        fieldnames.extend(players['Jabari Smith'].keys())
        writer = csv.DictWriter(player_data_csv_2022, fieldnames=fieldnames)
        writer.writeheader()
        for player, ncaa_stats in players.items():
            row = {
                'player_name': player,
                'draft_class': 2022,
            }
            row.update(ncaa_stats)
            writer.writerow(row)

if __name__ == "__main__":
    main()