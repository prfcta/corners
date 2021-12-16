import parsing
import json

# links = {
#     "epl": "https://www.flashscore.ru/football/england/premier-league/",
#     "bundes": "https://www.flashscore.ru/football/germany/bundesliga/",
#     "laliga": "https://www.flashscore.ru/football/spain/laliga/",
#     "seriaa": "https://www.flashscore.ru/football/italy/serie-a/",
#     "ligue1": "https://www.flashscore.ru/football/italy/serie-a/"
# }


links = {
    "АПЛ": "https://www.flashscore.ru/football/england/premier-league/",
    "БУНДЕС ЛИГА": "https://www.flashscore.ru/football/germany/bundesliga/"
}
seasons = ['2016/2017', '2017/2018']
data = {}


def main():
    for league_name, link in links.items():
        data[league_name] = {}
        data_season = parsing.get_archive_data(link, league_name, seasons)
        data[league_name] = data_season
    return data


if __name__ == "__main__":
    res_data = main()
    print(json.dumps(res_data, ensure_ascii=False, sort_keys=True, indent=4))
    

