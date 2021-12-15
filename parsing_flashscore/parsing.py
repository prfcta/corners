from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from time import sleep
from bs4 import BeautifulSoup


def get_archive_data(url, seasons: list) -> dict:
    data_season = {}
    for season in seasons:
        try:
            options = Options()
            options.add_argument("user-data-dir=C:\\profile")
            
            driver = webdriver.Chrome(options=options)
            driver.set_window_size(800, 800)
            
            stepper_from_start_page_to_results(driver, url, season)
            blocks = getter_blocks(driver)
            print(f"в сезоне {season} получено {len(blocks)} матчей")
            for block in blocks:
                sleep(1)
                match_link = block.get_attribute("id")[4:]
                print(match_link)
                match_link = f"https://www.flashscore.ru/match/{match_link}/#match-summary/match-summary"
                data_match = get_information_about_match(match_link)
                data_season[season] = {**data_season[season], **data_match}
                
                # тест, чтобы добавлять первые 2 игры из каждого сезона и
                # идти в следующий сезон
                
                print(f" словарь дата сизон {data_season}")
                if len(data_season[season]) > 1:
                    break
        
        except Exception as ex:
            print(ex)
        finally:
            driver.close()
            driver.quit()
    return data_season


def stepper_from_start_page_to_results(driver, url, season):
    try:
        driver.get(url)
        driver.implicitly_wait(5)
        sleep(2)
        driver.find_element(By.ID, "li4").click()
        driver.implicitly_wait(5)
        driver.find_element(By.XPATH, f"//a[contains(text(), '{season}')]").click()
        driver.implicitly_wait(5)
        driver.find_element(By.ID, "li1").click()
        driver.implicitly_wait(5)
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


def getter_blocks(driver):
    # blocks_all_games = driver.find_elements(
    #     By.CLASS_NAME("event__match event__match--static event__match--last event__match--twoLine"))
    
    blocks_all_games = driver.find_elements(By.XPATH, "//*[@title='Подробности матча!']")
    return blocks_all_games


def get_information_about_match(link):
    print('go')
    data_match = {}
    try:
        driver_2 = webdriver.Chrome()
        driver_2.set_window_size(800, 800)
        driver_2.get(link)
        
        driver_2.implicitly_wait(5)
        driver_2.find_element(By.XPATH, "//a[@href='#match-summary/live-commentary']").click()
        driver_2.implicitly_wait(5)
        home_team_name, away_team_name = driver_2.find_elements(
            By.XPATH, "//a[@class='participant__participantName participant__overflow']")
        print(home_team_name.text, away_team_name.text)
        home = home_team_name.text
        away = away_team_name.text
        driver_2.implicitly_wait(5)
        all_lines = driver_2.find_elements(By.XPATH, "//div[@class='soccer__row']")
        all_lines.reverse()
        
        # all_lines = driver_2.find_element(
        #     By.CSS_SELECTOR, "div[class=container__detail]").get_attribute("innerHTML")
        # print(all_lines)
        
        corners_minutes, goals_minutes = get_corners_and_goals_minutes(all_lines)
        data_match[f"{home}-{away}"] = {"corners": corners_minutes, "goals": goals_minutes}
        print(data_match)
        return data_match
    
    except Exception as ex:
        print(ex)


def get_corners_and_goals_minutes(all_lines):
    corners_minutes = []
    goals_minutes = []
    count = 0
    count_2 = 0
    for el in all_lines:
        if count_2 != 25:
            if count != 2:
                try:
                    el.find_element(By.XPATH, ".//*[@class='whistle-ico ']")
                    count += 1
                    print('матч начался' if count == 1 else 'закончился первый тайм')
                except Exception:
                    pass
                if count == 1:
                    corners_minutes, goals_minutes = detector(el, corners_minutes, goals_minutes)
                    now_minute = el.find_element(
                        By.XPATH, ".//*[@class='soccer__time']").text
                    print(now_minute)
                    print(f"{corners_minutes} угловой")
                    print(f"{goals_minutes} гол")
            count_2 += 1
    return corners_minutes, goals_minutes


# def corner_detector(el, corners_minutes):
#     try:
#         corner_minute = el.find_element(
#             By.XPATH, ".//*[@class='corner-ico ']/../../div[@class='soccer__time']").text[:-1]
#         if "+" in corner_minute:
#             corner_minute = sum(list(map(int, corner_minute.split("+"))))
#         else:
#             corner_minute = int(corner_minute)
#         print('корнер найден')
#         corners_minutes.append(corner_minute)
#     except Exception as ex:
#         print('')
#
#     return corners_minutes


def detector(el, goals_minutes, corners_minutes):
    try:
        goal_minute = el.find_element(
            By.XPATH, ".//*[@class='footballGoal-ico ']/../../div[@class='soccer__time']").text[:-1]
        if "+" in goal_minute:
            corner_minute = sum(list(map(int, goal_minute.split("+"))))
        else:
            corner_minute = int(goal_minute)
        print('гол найден')
        goals_minutes.append(goal_minute)
    except Exception:
        pass
    
    try:
        corner_minute = el.find_element(
            By.XPATH, ".//*[@class='corner-ico ']/../../div[@class='soccer__time']").text[:-1]
        if "+" in corner_minute:
            corner_minute = sum(list(map(int, corner_minute.split("+"))))
        else:
            corner_minute = int(corner_minute)
        print('корнер найден')
        corners_minutes.append(corner_minute)
    except Exception as ex:
        pass
    
    return corners_minutes, goals_minutes


