import sklearn
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import KFold
from sklearn.metrics import mean_squared_error, r2_score
import pandas as pd
import numpy as np
import argparse

def main():
    parser = argparse.ArgumentParser(description="Predict max win shares or total win shares in first 4 seasons for 2022 nba draft prospects")
    parser.add_argument('--stat', help='Either total_win_shares or max_win_shares')
    parser.add_argument('--iterations', type=int, help='Number of times model is trained (default is 10)')
    args = parser.parse_args()

    stat = args.stat
    iterations = args.iterations
    if iterations == None:
        iterations = 10

    train_val = pd.read_csv('player_data.csv')
    X_train_val = train_val.loc[:, ~train_val.columns.isin(['player_name', 'draft_class', 'total_win_shares', 'max_win_shares'])]
    Y_train_val = train_val[[stat]]
    
    test = pd.read_csv('player_data_2022.csv')
    X_test = test.loc[:, ~test.columns.isin(['player_name', 'draft_class'])]

    players_2022 = test['player_name'].to_numpy()
    players_2022_results = {player:[] for player in players_2022}
    num_players = len(players_2022)

    print("----- Running the model for {} iterations -----".format(iterations))
    for i in range(iterations):
        kFold = KFold(n_splits=5, shuffle=True)
        splits = kFold.split(X_train_val)
        max_r2_score = float('-inf')
        max_model = None
        for train_index, val_index in splits:
            X_train, X_val = X_train_val.iloc[train_index,:], X_train_val.iloc[val_index,:]
            Y_train, Y_val = Y_train_val.iloc[train_index,:], Y_train_val.iloc[val_index,:]
            lin_reg = LinearRegression()
            lin_reg.fit(X_train, Y_train)
            Y_val_pred = lin_reg.predict(X_val)
            mean_sq_error = np.square(np.linalg.norm(Y_val[stat].to_numpy() - Y_val_pred.squeeze())) * (1/len(val_index))
            r2 = r2_score(Y_val, Y_val_pred)
            if r2 > max_r2_score:
                max_r2_score = r2
                max_model = lin_reg

        Y_test = max_model.predict(X_test).squeeze()
        Y_test_sorted = np.sort(Y_test)
        Y_test_sorted_indices = np.argsort(Y_test)
        players_2022_sorted = list(reversed(players_2022[Y_test_sorted_indices]))
        Y_test_sorted = list(reversed(Y_test_sorted))
        for i in range(len(Y_test)):
            player_name = players_2022_sorted[i]
            player_stat = Y_test_sorted[i]
            players_2022_results[player_name].append(player_stat)

    players_2022_overall_results = {player:{} for player in players_2022}
    for player, results in players_2022_results.items():
        players_2022_overall_results[player] = {
            'Average': sum(results) / iterations,
            'Min': min(results),
            'Max': max(results),
            'Range': max(results) - min(results),
            'Variance': np.var(results)
        }

    sort_players_by_stat(players_2022_overall_results, 'Average', stat)
    sort_players_by_stat(players_2022_overall_results, 'Min', stat)
    sort_players_by_stat(players_2022_overall_results, 'Max', stat)
    sort_players_by_stat(players_2022_overall_results, 'Range', stat)
    sort_players_by_stat(players_2022_overall_results, 'Variance', stat)


def sort_players_by_stat(player_results, stat, predicted_stat):
    print('Projected {} of 2022 NBA Draft Prospects sorted by:'.format(predicted_stat))
    print('----- {} -----'.format(stat))
    players = [(player, stats[stat]) for player, stats in player_results.items()]
    players_sorted = list(sorted(players, key=lambda x:x[1], reverse=True))
    for player, player_stat in players_sorted:
        print("{}: {}".format(player, player_stat))


    

if __name__ == "__main__":
    main()