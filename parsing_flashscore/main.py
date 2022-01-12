from parsing_flashscore import parsing as p


def new_main(league_name, seasons, link):
    print('заустился парсинг нью мейн')
    data_league = {}
    data_league[league_name] = {}
    for season in seasons:
        data_season = p.get_season_data(league_name, season, link)
        data_league[league_name] = {**data_league[league_name], **data_season}
    return data_league




    

