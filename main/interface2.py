import dbmain2 as db
import analysis2
import os.path
from termcolor import colored
import parserworker2

all_leagues_names = {
        1: "АПЛ",
        2: "Ла Лига",
        3: "Бундес лига",
        4: "Серия А",
        5: "Лига 1",
        6: "РПЛ"
    }


def select_choice(selections):
    """
    Функция работает до тех пор, пока пользователь не введет одну
    из цифр, которая соответствует пункту в меню.
    Возвращает пункт меню.
    """
    while True:
        user_choice = input("-> ")
        if user_choice.isdigit():
            user_choice = int(user_choice)
            if user_choice in selections:
                return user_choice
        else:
            continue
        
        
def run_parsing():
    print("1. АПЛ\n2. Ла лига\n3. Бундес лига\n4. Серия А\n5. Лига 1\n6. РПЛ\n7. Назад")
    
    selections_link_leagues = {
        1: "https://www.flashscore.ru.com/football/england/premier-league-",
        2: "https://www.flashscore.ru.com/football/spain/laliga-",
        3: "https://www.flashscore.ru.com/football/germany/bundesliga-",
        4: "https://www.flashscore.ru.com/football/italy/serie-a-",
        5: "https://www.flashscore.ru.com/football/france/ligue-1-",
        6: "https://www.flashscore.ru.com/football/russia/premier-league-",
        7: "назад"
    }
    
    user_selection_league = select_choice(selections_link_leagues)
    
    if user_selection_league == 7:
        mainmenu()
    
    print("1. 2021/2022\n2. 2020/2021\n"
          "3. 2019/2020\n4. 2018/2019\n"
          "5. 2017/2018\n6. 2016/2017")
    
    all_seasons = {
        1: "2021-2022",
        2: "2020-2021",
        3: "2019-2020",
        4: "2018-2019",
        5: "2017-2018",
        6: "2016-2017"
    }
    
    user_selection_season = select_choice(all_seasons)
    league_name = all_leagues_names[user_selection_league]
    season_date = all_seasons[user_selection_season]
    link = selections_link_leagues[user_selection_league] + season_date + "/results/"
    # print(link)
    print(colored(league_name, "yellow"))
    print(colored(season_date, "yellow"))
    data_all_matches = parserworker2.parserworker(link)
    data_season = {}
    data = {}
    data_season[season_date] = {}
    for match in data_all_matches:
        data_season[season_date] = {**data_season[season_date], **match}
    data[league_name] = data_season
    return data
    
    
def run_analysis():
    dbcollections = db.get_database_collections()
    
    for i, v in enumerate(dbcollections.keys()):
        print(i + 1, *v)
    new_selections = {i + 1: v for i, v in enumerate(dbcollections.keys())}
    user_selection_league_season = select_choice(new_selections)
    league_name, season_date = new_selections[user_selection_league_season]

    league_id, season_id = db.get_default(league_name, season_date)

    result = db.get_statistic(league_id, season_id)
    print(colored("1. вероятность углового после выбранной минуты при любом счете\n"
                  "2. вероятность углового после выбранной минуты при ничейном счете\n"
                  "3. вероятность углового после выбранной минуты если счет не ничейный", "yellow"))
    
    selections = {
        1: "вероятность углового после выбранной минуты при любом счете",
        2: "вероятность углового после выбранной минуты при ничейном счете",
        3: "вероятность углового после выбранной минуты если счет не ничейный"
    }
    user_selection_event = select_choice(selections)
    minute = int(input('введи минуту, которая будет использована в выборке: '))
    analysis2.work(result, user_selection_event, minute)
    
def mainmenu():
    """
    Главное меню программы. Первое что видит пользователь программы
    при запуске кода. У пользователя появляется возможность выбрать
    один из пунктов меню. Парсинг данных, сохранение данных в базу
    данных и проведение аналитики имеющихся данных.
    """
    data_base = os.path.abspath("data_base_corners_and_goals.db")
    print("1: найти и сохранить данные\n2: аналитика\n"
          "3: удалить базу данных\n4: выход")
    selections = {
        1: ["1", "найти и сохранить данные"],
        2: ["2", "аналитика"],
        3: ["3", "удалить базу данных"],
        4: ["4", "выход"]
    }
    
    selection = select_choice(selections)
    if selection == 1:
        data = run_parsing()
        db.save_data_season_in_db(data)
        print(colored("данные сохранены в базу данных", "blue"))
        print()
        mainmenu()
    elif selection == 2:
        run_analysis()
    elif selection == 3:
        answer_delete = ''
        while answer_delete not in ('y', 'n'):
            answer_delete = input('уверен, что хочешь удалить данные из базы? y/n\n-> ')
            if answer_delete == 'y':
                db.delete_data_from_db()
                print(colored("данные удалены из базы.", "red"))
                print()
                mainmenu()
            elif answer_delete == 'n':
                break
    elif selection == 4:
        print('выполнен выход')
    
    
if __name__ == "__main__":
    mainmenu()
    
    
    

