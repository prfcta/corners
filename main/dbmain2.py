import json
import models2 as db


def get_default(league_name, season_date):
    result = db.CollectionsLeagueSeason.get(db.CollectionsLeagueSeason.league_name == league_name
                                            and db.CollectionsLeagueSeason.season_date == season_date)
    return result.league_id, result.season_id
    
    
def get_league_id():
    """
    Возвращает id всех лиг, которые сохранены в базе данных.
    """
    query = db.League.select()
    result = {league.id: league.name for league in query}
    return result


def get_season_id():
    """
    Возвращает id всех сезонов, которые сохранены в базе данных.
    """
    query = db.Season.select()
    result = {season.id: season.season_date for season in query}
    return result


def get_create_leagues_and_seasons(league_o, season_o):
    """
    Создание объекта лига + сезон в базе данных.
    """
    db.CollectionsLeagueSeason.get_or_create(league_id=league_o.id, season_id=season_o.id,
                                             season_date=season_o.season_date,
                                             league_name=league_o.name)


def get_create_league(league):
    """
    Создание объекта лиги в базе данных.
    """
    league_o, created = db.League.get_or_create(name=league)
    return league_o


def get_create_season(season):
    """
    Создание объекта сезона в базе данных.
    """
    season_o, created = db.Season.get_or_create(season_date=season)
    return season_o


def get_create_match(league_o, season_o, teams, hc, ac, hg, ag):
    """
    Создание объекта матча и статистики в базе данных.
    """
    match_o, created = db.Match.get_or_create(teams=teams, season_id=season_o.id, league_id=league_o.id,
                                              season_date=season_o.season_date,
                                              league_name=league_o.name, home_corners=hc, away_corners=ac,
                                              home_goals=hg, away_goals=ag)
    return match_o


def get_statistic(league_id, season_id):
    """
    Пользователь указывает id лиги и/или сезона. Возможные варианты для выборки:
    1) Лига + сезон
    2) Лига
    3) Сезон
    """
    if league_id is None:
        result = db.Match.select().where(db.Match.season_id == season_id)
    elif season_id is None:
        result = db.Match.select().where(db.Match.league_id == league_id)
    else:
        result = db.Match.select().where(db.Match.league_id == league_id and db.Match.season_id == season_id)
    return result


def get_database_collections():
    """
    Все уникальные коллекции лига + сезон в базе данных.
    """
    query = db.CollectionsLeagueSeason.select().order_by(db.CollectionsLeagueSeason.league_name)
    result = {(line.league_name, line.season_date): line.id for line in query}
    return result


def convert_to_json(statistic):
    """
    Конвертация списков с минутами угловых и голов в json формат для хранения
    в базе данных.
    """
    hc = json.dumps(statistic['home_corners'])
    ac = json.dumps(statistic['away_corners'])
    hg = json.dumps(statistic['home_goals'])
    ag = json.dumps(statistic['away_goals'])
    return hc, ac, hg, ag


def delete_data_from_db():
    """
    Удаление всех данных из базы данных.
    """
    db.db.drop_tables([db.League, db.Season, db.Match, db.CollectionsLeagueSeason], safe=True)
    db.db.create_tables([db.League, db.Season, db.Match, db.CollectionsLeagueSeason], safe=True)


def save_data_season_in_db(new_data):
    """
    Сохранение данных из словаря data в базу данных.
    """
    for league, league_info in new_data.items():
        league_o = get_create_league(league)
        
        for season, match_info in league_info.items():
            season_o = get_create_season(season)
            get_create_leagues_and_seasons(league_o, season_o)
            
            for teams, statistic in match_info.items():
                hc, ac, hg, ag = convert_to_json(statistic)
                get_create_match(league_o, season_o, teams, hc, ac, hg, ag)
    
                
if __name__ == "__main__":
    data = {'Ла Лига': {'2019-2020': {'Атлетико-Реал Сосьедад':
                                          {'home_corners': [63, 93],
                                           'away_corners': [39, 68, 83],
                                           'home_goals': [30],
                                           'away_goals': []},
                                      'Гранада-Атлетик':
                                          {'home_corners': [78, 93],
                                           'away_corners': [46, 50, 85],
                                           'home_goals': [29, 55, 67, 94],
                                           'away_goals': []},
                                      'Леванте-Хетафе':
                                          {'home_corners': [3, 5, 11, 14, 27, 52, 52],
                                           'away_corners': [10, 19, 28, 28, 53, 55, 55],
                                           'home_goals': [40, 99],
                                           'away_goals': [34, 52]}
                                      }}}
    save_data_season_in_db(data)
    
    


