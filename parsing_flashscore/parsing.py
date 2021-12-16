import selenium.webdriver.common.devtools.v96.database
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from time import sleep
from bs4 import BeautifulSoup


def get_archive_data(url, league, seasons: list) -> dict:
    data_season = {}
    for season in seasons:
        print(f"проверяется {league} сезон {season}")
        data_season[season] = {}
        try:
            options = Options()
            options.add_argument("user-data-dir=C:\\profile")
            
            driver = webdriver.Chrome(options=options)
            driver.set_window_size(800, 800)
            
            stepper_from_start_page_to_results(driver, url, season)
            all_season_matches = getter_all_season_matches(driver)
            count = 0
            for match in all_season_matches:
                if count != 5:
                    sleep(1)
                    match_link = match.get_attribute("id")[4:]
                    match_link = f"https://www.flashscore.ru/match/{match_link}/#match-summary/match-summary"
                    data_match = get_information_about_match(match_link)
                    data_season[season] = {**data_season[season], **data_match}
                    count += 1
        except Exception as ex:
            print(ex)
        finally:
            driver.close()
            driver.quit()
    print(f"проверка {league} завершена")
    return data_season


def stepper_from_start_page_to_results(driver, url, season):
    try:
        driver.get(url)
        driver.implicitly_wait(5)
        sleep(2)
        driver.find_element(By.ID, "li4").click()

        driver.find_element(By.XPATH, f"//a[contains(text(), '{season}')]").click()

        driver.find_element(By.ID, "li1").click()

        more_games(driver)
    
    except Exception as ex:
        print(ex)


def more_games(driver):
    while True:
        try:
            driver.find_element(By.XPATH, "//*[text()='Показать больше матчей']").click()
            sleep(2)
        except Exception:
            break


def getter_all_season_matches(driver):
    all_season_matches = driver.find_elements(By.XPATH, "//*[@title='Подробности матча!']")
    return all_season_matches


def get_information_about_match(link):
    data_match = {}
    try:
        driver_2 = webdriver.Chrome()
        driver_2.set_window_size(800, 800)
        driver_2.get(link)
        
        driver_2.implicitly_wait(5)
        driver_2.find_element(By.XPATH, "//a[@href='#match-summary/live-commentary']").click()
        
        home_team_name, away_team_name = driver_2.find_elements(
            By.XPATH, "//a[@class='participant__participantName participant__overflow']")
        print(f"текущая проверка матч: {home_team_name.text} {away_team_name.text}")
        home = home_team_name.text
        away = away_team_name.text
        driver_2.implicitly_wait(5)
        all_lines = driver_2.find_elements(By.XPATH, "//div[@class='soccer__row']")
        all_lines.reverse()
        
        home_corners_minutes, away_corners_minutes, \
            home_goals_minutes, away_goals_minutes = get_corners_and_goals_minutes(
                all_lines, home, away, driver_2)
        data_match[f"{home}-{away}"] = {"home_corners": home_corners_minutes,
                                        "away_corners": away_corners_minutes,
                                        "home_goals": home_goals_minutes,
                                        "away_goals": away_goals_minutes}
        return data_match
    
    except Exception as ex:
        print(ex)


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
                el.find_element(By. XPATH, ".//*[@class='whistle-ico ']")
                count += 1
            except Exception:
                pass
            if count == 1:
                home_corners_minutes, away_corners_minutes, home_goals_minutes, away_goals_minutes = detector(
                    el, home, away, home_corners_minutes, away_corners_minutes,
                                                          home_goals_minutes, away_goals_minutes)
                now_minute = el.find_element(
                    By.XPATH, ".//*[@class='soccer__time']").text
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
    except Exception as ex:
        pass
    
    return home_corners_minutes, away_corners_minutes, home_goals_minutes, away_goals_minutes





    
