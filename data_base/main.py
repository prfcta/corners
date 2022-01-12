import data_base.models as db
import json

# data = {'АПЛ': {'2016/2017': {'Арсенал-Арсенал': {'home_corners': [10, 24, 38], 'away_corners': [41, 44, 46], 'home_goals': [8, 27], 'away_goals': []}, 'Бёрнли-Вест Хэм': {'home_corners': [13, 30], 'away_corners': [], 'home_goals': [23], 'away_goals': [27]}, 'Лестер-Борнмут': {'home_corners': [20, 21, 45, 47], 'away_corners': [25], 'home_goals': [], 'away_goals': [1]}, 'Ливерпуль-Мидлсбро': {'home_corners': [35], 'away_corners': [40], 'home_goals': [46], 'away_goals': []}, 'Манчестер Юнайтед-Кристал Пэлас': {'home_corners': [2, 31, 39], 'away_corners': [26, 38], 'home_goals': [15, 19], 'away_goals': []}}, '2017/2018': {'Бёрнли-Борнмут': {'home_corners': [9, 18, 36, 45], 'away_corners': [27, 28], 'home_goals': [39], 'away_goals': []}, 'Вест Хэм-Эвертон': {'home_corners': [35, 47], 'away_corners': [3, 4], 'home_goals': [], 'away_goals': []}, 'Кристал Пэлас-Вест Бромвич': {'home_corners': [3, 22, 24], 'away_corners': [12], 'home_goals': [], 'away_goals': []}, 'Ливерпуль-Брайтон': {'home_corners': [1, 20, 31, 40], 'away_corners': [32, 33], 'home_goals': [26, 40], 'away_goals': []}, 'Манчестер Юнайтед-Уотфорд': {'home_corners': [12, 13, 29, 40], 'away_corners': [8, 26, 44], 'home_goals': [34], 'away_goals': []}}}, 'БУНДЕС ЛИГА': {'2016/2017': {'Айнтрахт Б-Вольфсбург': {'home_corners': [21, 25], 'away_corners': [8, 34], 'home_goals': [], 'away_goals': []}, 'Вольфсбург-Айнтрахт Б': {'home_corners': [17], 'away_corners': [], 'home_goals': [35], 'away_goals': []}, 'Айнтрахт Ф-РБ Лейпциг': {'home_corners': [5, 16, 19], 'away_corners': [7], 'home_goals': [], 'away_goals': [25]}, 'Бавария-Фрайбург': {'home_corners': [7, 16, 16, 19, 30, 31, 32, 40, 40], 'away_corners': [6, 26], 'home_goals': [4], 'away_goals': []}, 'Боруссия Д-Вердер': {'home_corners': [4, 20, 27, 39], 'away_corners': [41], 'home_goals': [32, 42], 'away_goals': [7]}}, '2017/2018': {'Хольштайн Киль-Вольфсбург': {'home_corners': [20], 'away_corners': [22, 23, 38], 'home_goals': [], 'away_goals': []}, 'Вольфсбург-Хольштайн Киль': {'home_corners': [7, 8, 19, 43, 44], 'away_corners': [], 'home_goals': [13, 40], 'away_goals': [34]}, 'Бавария-Штутгарт': {'home_corners': [31, 37], 'away_corners': [], 'home_goals': [21], 'away_goals': [5, 42]}, 'Байер-Ганновер': {'home_corners': [8], 'away_corners': [21, 45], 'home_goals': [3, 18], 'away_goals': []}, 'Вольфсбург-Кёльн': {'home_corners': [8, 46, 47], 'away_corners': [31], 'home_goals': [1], 'away_goals': [32]}}}}
# league_names = {}
# las = {}


def get_create_leagues_and_seasons(league_o, season_o):
    db.CollectionsLeagueSeason.get_or_create(league_id=league_o.id, season_id=season_o.id,
                                             season_date=season_o.season_date,
                                             league_name=league_o.name)
    
    
def get_create_league(league):
    league_o, created = db.League.get_or_create(name=league)
    return league_o


def get_create_season(season):
    season_o, created = db.Season.get_or_create(season_date=season)
    return season_o


def get_create_match(league_o, season_o, teams, hc, ac, hg, ag):
    match_o, created = db.Match.get_or_create(teams=teams, season_id=season_o.id, league_id=league_o.id, season_date=season_o.season_date,
                                              league_name=league_o.name, home_corners=hc, away_corners=ac,
                                              home_goals=hg, away_goals=ag)
    return match_o
    

def get_statistic(league_id, season_id):
    if league_id is None:
        result = db.Match.select().where(db.Match.season_id == season_id)
    elif season_id is None:
        result = db.Match.select().where(db.Match.league_id == league_id)
    else:
        result = db.Match.select().where(db.Match.league_id == league_id and db.Match.season_id == season_id)
    return result


def get_database_collections():
    query = db.CollectionsLeagueSeason.select()
    result = [(line.league_name, line.season_date) for line in query]
    return result


def get_league_id():
    query = db.League.select()
    result = [(league.name, league.id) for league in query]
    return result


def get_season_id():
    query = db.Season.select()
    result = [(season.season_date, season.id) for season in query]
    return result


def convert_to_json(statistic):
    hc = json.dumps(statistic['home_corners'])
    ac = json.dumps(statistic['away_corners'])
    hg = json.dumps(statistic['home_goals'])
    ag = json.dumps(statistic['away_goals'])
    return hc, ac, hg, ag


def saver(new_data):
    for league, league_info in new_data.items():
        league_o = get_create_league(league)
        
        for season, match_info in league_info.items():
            season_o = get_create_season(season)
            get_create_leagues_and_seasons(league_o, season_o)
            for teams, statistic in match_info.items():
                hc, ac, hg, ag = convert_to_json(statistic)
                get_create_match(league_o, season_o, teams, hc, ac, hg, ag)



