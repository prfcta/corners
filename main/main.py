from parsing_flashscore import main as pfmain
from parsing_flashscore import parsing as pfparsing
from data_base import main as dbmain, models as dbmodels
from analysis import main as am
import time
import keyboard

links = {
    "epl": "https://www.flashscore.ru/football/england/premier-league/",
    "bundes": "https://www.flashscore.ru/football/germany/bundesliga/",
    "laliga": "https://www.flashscore.ru/football/spain/laliga/",
    "seriea": "https://www.flashscore.ru/football/italy/serie-a/",
    "ligue1": "https://www.flashscore.ru/football/france/ligue-1/",
    "rpl": "https://www.flashscore.ru/football/russia/premier-league/"
}


def menu():
    print("""
меню:
1. сохранить сезон
2. аналитика
3. удалить базу данных
4. выход""")
    print()


def check_analysis_menu():
    print("""
1. вероятность углового после выбранной минуты при любом счете
2. вероятность углового после выбранной минуты при ничейном счете
3. вероятность углового после выбранной минуты если счет не ничейный
    """)


def saver(league_name, seasons, link):
    print('заустился сейвер')
    pfparsing.data_season.clear()
    start_time = time.time()
    data_league = pfmain.new_main(league_name, seasons, link)
    dbmain.saver(data_league)
    print('данные сохранены')
    print(time.time() - start_time, "время выполнения сбора данных")


def db_deleter():
    dbmodels.delete_db()
    
    
def league_link(league_name):
    return links[league_name] if league_name in links else None


def custom_link(link):
    user_link = input()
    return user_link


def main():
    while True:
        menu()
        menu_step = input('выбери пункт меню:\n')
        if menu_step == '1':
            print('введи название лиги')
            league_name = input()
            link = league_link(league_name)
            if link is None:
                link_from_user = input('введи ссылку на лигу: ')
                link = custom_link(link_from_user)
            seasons_counter = False
            while seasons_counter is not True:
                seasons_count = input('сколько сезонов необходимо спарсить и сохранить?\n')
                if seasons_count.isdigit():
                    seasons_counter = True
                    seasons_count = int(seasons_count)
                else:
                    print('введи количество сезонов')
                    
            seasons = [input('введи нужный сезон\n') for _ in range(seasons_count)]
            saver(league_name, seasons, link)
        elif menu_step == '2':
            print('необходимо указать параметры для выборки данных.')
            print('доступные данные:')
            dbcollections = dbmain.get_database_collections()
            for event in dbcollections:
                print(*event)
            print()
            lid, sid = dbmain.get_league_id(), dbmain.get_season_id()
            print('выбери id лиги и/или сезона:')
            for league_name_id in lid:
                print(f'лига {league_name_id[0]} - id: {league_name_id[1]}')
            print()
            for season_date_id in sid:
                print(f'сезон {season_date_id[0]} - id: {season_date_id[1]}')
            helper = True
            while helper:
                print('нужно указать хотя бы один параметр')
                league_id = input('введи id лиги. Чтобы пропустить этот пункт нажми Enter\n')
                league_id = int(league_id) if league_id != '' else None
        
                season_id = input('введи id сезона. Чтобы пропустить этот пункт нажми Enter\n')
                season_id = int(season_id) if season_id != '' else None
                if league_id is not None or season_id is not None:
                    helper = False
            result = dbmain.get_statistic(league_id=league_id, season_id=season_id)
            check_analysis_menu()
            analysis_answer = int(input('выбери условие для анализа данных: '))
            minute = int(input('введи минуту, которая будет использована в выборке: '))
            am.work(result, analysis_answer, minute)
            
        elif menu_step == '3':
            answer_delete = ''
            while answer_delete not in ('y', 'n'):
                answer_delete = input('уверен, что хочешь полностью удалить базу данных? y/n\n')
                if answer_delete == 'y':
                    db_deleter()
                elif answer_delete == 'n':
                    break
                
        elif menu_step == '4':
            break
            
        else:
            print('введи цифру, которая соответствует одному из пунктов меню')


if __name__ == "__main__":
    main()
    









