import time
import selenium.common.exceptions
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from time import sleep
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import multiprocessing
import threading
import main as main_menu
from selenium.webdriver.chrome.service import Service


data_season = {}
threadLocal = threading.local()


def get_driver():
    driver_2 = getattr(threadLocal, 'driver_2', None)
    if driver_2 is None:
        options2 = Options()
        # options2.add_argument('--headless')
        ChromeDriverManager(log_level=0)
        driver_2 = webdriver.Chrome(ChromeDriverManager().install(), options=options2)
        setattr(threadLocal, 'driver_2', driver_2)
    return driver_2


def end_func(response):
    print('запустилась end_func')
    season = response[0][1]
    data_season[season] = {}
    for event in response:
        data_match = event[0]
        print(data_match)
        season = event[1]
        # driver_2 = event[2]
        # print(driver_2)
        # driver_2.close()
        # driver_2.quit()
        print('driver_2 закрылся')
        data_season[season] = {**data_season[season], **data_match}
        
        
def start_multiprocessing_parsing(links_box):
    print('запустился мультипроцессинг')
    with multiprocessing.Pool(processes=3) as p:
        p.map_async(get_information_about_match, links_box, callback=end_func)
        p.close()
        p.join()
        
    
def get_season_data(league_name, season, link) -> dict:
    print('заустился парсинг гет сизон дата')
    print(f"проверяется {league_name} сезон {season}")
    data_season[season] = {}
    try:
        options = Options()
        ChromeDriverManager(log_level=0)
        options.add_argument("user-data-dir=C:\\profile")
        # options.add_argument('--headless')
        driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        driver.set_window_size(800, 800)
        stepper_answer = stepper_from_start_page_to_results(driver, link, season)
        if stepper_answer == 'season_is_not_exists':
            print('rrr')
            main_menu.main()
        all_season_matches = getter_all_season_matches(driver)
        count = 0
        links_box = []
        match_count = 400
        amount_of_all_matches = len(all_season_matches)
        print('наичнаем проходить циклом для сбора ссылок в список')
        for match in all_season_matches:
            # if count < len(all_season_matches) + 5:
            if count < 11:
                # sleep(1)
                match_link = match.get_attribute("id")[4:]
                match_link = f"https://www.flashscore.ru/match/{match_link}/#match-summary/match-summary"
                links_box.append((match_link, season, amount_of_all_matches))
                count += 1
        print('все ссылки собраны')
    except Exception as ex:
        print('в функции гет архив дата ошибка', ex)
    finally:
        driver.close()
        driver.quit()

    start_multiprocessing_parsing(links_box)
    print(f"проверка {league_name} завершена")
    print(data_season)
    return data_season


def stepper_from_start_page_to_results(driver, link, season):
    print('заустился парсинг степпер')
    try:
        driver.get(link)
        driver.implicitly_wait(5)
        sleep(2)
        try:
            driver.find_element(By.ID, "li4").click()
            driver.find_element(By.XPATH, f"//a[contains(text(), '{season}')]").click()
            driver.find_element(By.ID, "li1").click()
        except selenium.common.exceptions.NoSuchElementException:
            print('такого сезона нет!')
            return 'season_is_not_exists'
        more_games(driver)
    except Exception as ex:
        print(ex)


def more_games(driver):
    print('заустился парсинг больше игр')
    while True:
        try:
            driver.find_element(By.XPATH, "//*[text()='Показать больше матчей']").click()
            sleep(1)
        except Exception:
            break


def getter_all_season_matches(driver):
    print('заустился парсинг сбор всех матчей')
    all_season_matches = driver.find_elements(By.XPATH, "//*[@title='Подробности матча!']")
    return all_season_matches


def get_information_about_match(event):
    data_match = {}
    link = event[0]
    season = event[1]
    try:
        driver_2 = get_driver()
        # driver_2 = webdriver.Chrome(ChromeDriverManager().install())
        driver_2.get(link)
        driver_2.implicitly_wait(5)
        home_team_name, away_team_name = driver_2.find_elements(
            By.XPATH, "//a[@class='participant__participantName participant__overflow']")
        home = home_team_name.text
        away = away_team_name.text
        print(f"текущая проверка матч: {home} {away}")
        # здесь возможно стоит добавить трай эксепт на наличие вкладки текстовых комментариев
        try:
            WebDriverWait(driver_2, 10).until(EC.presence_of_element_located((
                By.XPATH, "//a[@href='#match-summary/live-commentary']"))).click()
            all_lines = driver_2.find_elements(By.XPATH, "//div[@class='soccer__row']")
            all_lines.reverse()

            home_corners_minutes, away_corners_minutes, home_goals_minutes, away_goals_minutes = \
                get_corners_and_goals_minutes(all_lines, home, away, driver_2)

            data_match[f"{home}-{away}"] = {"home_corners": home_corners_minutes,
                                            "away_corners": away_corners_minutes,
                                            "home_goals": home_goals_minutes,
                                            "away_goals": away_goals_minutes}
        except Exception:
            print(f'в матче {home}-{away} нет данных. link: {link}')
            pass
    except Exception as ex:
        print(f'в функции get_information_about_match. link: {link} {ex} ')
    # finally:
    #     driver_2.close()
    #     driver_2.quit()
    print(data_match)
    # return data_match, season, driver_2
    return data_match, season


def get_corners_and_goals_minutes(all_lines, home, away, driver_2):
    driver_2.implicitly_wait(0)
    home_corners_minutes = []
    away_corners_minutes = []
    home_goals_minutes = []
    away_goals_minutes = []
    count = 0
    for el in all_lines:
        if count != 2:
            try:
                el.find_element(By.XPATH, ".//*[@class='whistle-ico ']")
                count += 1
            except Exception:
                pass
        if count == 1:
            home_corners_minutes, away_corners_minutes, home_goals_minutes, away_goals_minutes = detector(
                    el, home, away, home_corners_minutes, away_corners_minutes, home_goals_minutes, away_goals_minutes)

    return home_corners_minutes, away_corners_minutes, home_goals_minutes, away_goals_minutes


def detector(el, home, away, home_corners_minutes, away_corners_minutes, home_goals_minutes, away_goals_minutes):
    comment = el.find_element(By.XPATH, ".//div[@class='soccer__comment']/div").text
    try:
        goal_minute = el.find_element(
            By.XPATH, ".//*[@class='footballGoal-ico ']/../../div[@class='soccer__time']").text[:-1]
        
        if "+" in goal_minute:
            goal_minute = sum(list(map(int, goal_minute.split("+"))))
        else:
            goal_minute = int(goal_minute)
        if home in comment:
            home_goals_minutes.append(goal_minute)
        else:
            away_goals_minutes.append(goal_minute)
    except Exception:
        pass
    
    try:
        corner_minute = el.find_element(
            By.XPATH, ".//*[@class='corner-ico ']/../../div[@class='soccer__time']").text[:-1]
        if "+" in corner_minute:
            corner_minute = sum(list(map(int, corner_minute.split("+"))))
        else:
            corner_minute = int(corner_minute)
        if home in comment:
            home_corners_minutes.append(corner_minute)
        else:
            away_corners_minutes.append(corner_minute)
    except Exception:
        pass
    
    return home_corners_minutes, away_corners_minutes, home_goals_minutes, away_goals_minutes





