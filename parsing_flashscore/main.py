import parsing

links = {
    "epl": "https://www.flashscore.ru/football/england/premier-league/",
    "bundes": "https://www.flashscore.ru/football/germany/bundesliga/",
    "laliga": "https://www.flashscore.ru/football/spain/laliga/",
    "seriaa": "https://www.flashscore.ru/football/italy/serie-a/",
    "ligue1": "https://www.flashscore.ru/football/italy/serie-a/"
}
seasons = ['2016/2017', '2017/2018']
data = {}


def main():
    for league_name, link in links.items():
        data_season = parsing.get_archive_data(link, seasons)
        data[league_name] += data_season


if __name__ == "__main__":
    main()

