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
    count_3 = 0
    if count_3 != 3:
        for league_name, link in links.items():
            data[league_name] = {}
            data_season = parsing.get_archive_data(link, seasons)
            data[league_name] = {**data[league_name], **data_season}
            count_3 += 1
    return data


if __name__ == "__main__":
    res_data = main()
    print(res_data)

