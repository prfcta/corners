from data_base import main as dbmain
import numpy as np
import json


# функция для конверта джсон - нумпай
def convert_from_json_to_nparray(*args):
    hc, ac, hg, ag = [np.array(json.loads(i)) for i in args]
    return hc, ac, hg, ag

    
def amount_of_corners_after_x_and(hc, ac, hg, ag, minute, term):
    home_goals_before = np.sum(hg < minute)
    away_goals_before = np.sum(ag < minute)
    corner = corner_or_not_after_x(hc, ac, minute)
    if term == 'draw':
        if home_goals_before == away_goals_before:
            if corner == 'yes':
                return 'yes'
            else:
                return 'no'
    elif term == 'notdraw':
        if home_goals_before != away_goals_before:
            if corner == 'yes':
                return 'yes'
            else:
                return 'no'
        
        
def corner_or_not_after_x(hc, ac, minute):
    home_corner_after = bool(np.sum(hc > minute))
    away_corner_after = bool(np.sum(ac > minute))
    return 'yes' if home_corner_after == 1 or away_corner_after == 1 else 'no'


def probability(games, corners):
    return round(corners / games * 100)
    
    
def work(result, analysis_answer, minute):
    corners = 0
    games = 0
    for match in result:
        hc, ac, hg, ag = convert_from_json_to_nparray(match.home_corners, match.away_corners, match.home_goals,
                                                      match.away_goals)
        if analysis_answer == 1:
            answer = corner_or_not_after_x(hc, ac, minute)
        elif analysis_answer == 2:
            term = 'draw'
            answer = amount_of_corners_after_x_and(hc, ac, hg, ag, minute, term)
        elif analysis_answer == 3:
            term = 'notdraw'
            answer = amount_of_corners_after_x_and(hc, ac, hg, ag, minute, term)
        if answer is not None:
            games += 1
        if answer == 'yes':
            corners += 1
    ver = probability(games, corners)
    print(f'проверено {len(result)} матчей. в {games} были условия для ставки, в {corners} из них ставка зашла бы')
    print(f'проходимость - {ver}%')


def main():
    result = dbmain.get_statistic(season_id=1)
    work(result)


if __name__ == "__main__":
    main()

