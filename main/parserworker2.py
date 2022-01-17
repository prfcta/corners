from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common import exceptions
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import threading
from multiprocessing.pool import ThreadPool


threadLocal = threading.local()


class ParserLinksBox:
    def __init__(self, link):
        self.driver = self.create_driver()
        self.link = link
        self.id_box = ()
        self.elements_box = []
        
    def create_driver(self):
        ChromeDriverManager(log_level=0)
        service = Service(ChromeDriverManager().install())
        options = Options()
        # options.add_argument('--headless')
        options.add_argument("user-data-dir=C:\\profile4")
        driver = webdriver.Chrome(service=service, options=options)
        driver.maximize_window()
        return driver
    
    def close_driver(self):
        self.driver.close()
        self.driver.quit()

    def open_flashscore(self):
        self.driver.get(self.link)

    def custom_cookie_accept(self):
        """
        При наличии окна с согласием использовать куки, нажимается кнопка "Да".
        """
        try:
            self.driver.find_element(By.ID, "customCookieAccept").click()
        except exceptions.NoSuchElementException:
            pass
        except exceptions.ElementNotInteractableException:
            pass
    
    def downloading_all_matches_on_page(self):
        """
        Функция нажимает кнопку "Показать больше матчей" до тех пор,
        пока она есть на странице.
        """
        while True:
            try:
                element = self.driver.find_element(By.XPATH, "//*[text()='Показать больше матчей']")
                # time.sleep(0.48)
                WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((
                    element))).click()
            except exceptions.ElementClickInterceptedException:
                continue
            except exceptions.StaleElementReferenceException:
                continue
            except exceptions.NoSuchElementException:
                break
            
    def getter_all_matches_links_from_page(self):
        """
        Собираются все элементы, которые являются матчем. Id каждой игры сохраняется в кортеж.
        """
        self.elements_box = self.driver.find_elements(By.XPATH, "//*[@title='Подробности матча!']")
        self.id_box = (element.get_attribute("id")[4:] for element in self.elements_box)

        
def start_parsing(link):
    """
    Поиск и сохранение id всех матчей в кортеж.
    """
    parser = ParserLinksBox(link)
    parser.open_flashscore()
    parser.custom_cookie_accept()
    parser.downloading_all_matches_on_page()
    parser.getter_all_matches_links_from_page()
    return parser.id_box

    
def create_links_with_id(id_box):
    """
    Конструктор ссылки из id матча.
    """
    
    links_box = list(map(lambda match_id: f"https://www.flashscore.ru/match/{match_id}/"
                                          f"#match-summary/live-commentary/0", id_box))
    return links_box


def get_driver():
    driver = getattr(threadLocal, 'driver', None)
    if driver is None:
        service = Service(ChromeDriverManager().install())
        options2 = Options()
        options2.add_argument('--headless')
        ChromeDriverManager(log_level=0)
        driver = webdriver.Chrome(service=service, options=options2)
        setattr(threadLocal, 'driver', driver)
    return driver


def multithreading_start(link):
    """Парсинг данных (минуты угловых и голов в 1 тайме) о каждой игре в многопоточном режиме."""
    data_match = {}
    driver = get_driver()
    driver.get(link)

    home_team_name, away_team_name = driver.find_elements(
        By.XPATH, "//a[@class='participant__participantName participant__overflow']")

    home = home_team_name.text
    away = away_team_name.text
    print(f"текущая проверка матч: {home} {away}")
    time.sleep(0.1)
    all_lines = driver.find_elements(By.XPATH, "//div[@class='soccer__row']")
    all_lines.reverse()
    home_corners_minutes, away_corners_minutes, home_goals_minutes, away_goals_minutes = \
        get_corners_and_goals_minutes(all_lines, home, away)
    data_match[f"{home}-{away}"] = {"home_corners": home_corners_minutes,
                                    "away_corners": away_corners_minutes,
                                    "home_goals": home_goals_minutes,
                                    "away_goals": away_goals_minutes}

    return data_match
    
    
def get_corners_and_goals_minutes(all_lines, home, away):
    """Функция определяет текущее состояние матча
    (матч не начался, идет первый тайм, первый тайм закончился).
    """
    home_corners_minutes = []
    away_corners_minutes = []
    home_goals_minutes = []
    away_goals_minutes = []
    count = 0
    for el in all_lines:
        time.sleep(0.01)
        try:
            el.find_element(By.XPATH, ".//*[@class='whistle-ico ']")
            count += 1
            continue
        except Exception:
            pass
        if count == 1:
            home_corners_minutes, away_corners_minutes, home_goals_minutes, away_goals_minutes = detector(
            el, home, away, home_corners_minutes, away_corners_minutes, home_goals_minutes, away_goals_minutes)
        if count == 2:
            break
    return home_corners_minutes, away_corners_minutes, home_goals_minutes, away_goals_minutes


def detector(el, home, away, home_corners_minutes, away_corners_minutes, home_goals_minutes, away_goals_minutes):
    """Функция определяет какое именно событие произошло в игре, а так же с участием какой команды."""
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
    except exceptions.NoSuchElementException:
        pass
    
    return home_corners_minutes, away_corners_minutes, home_goals_minutes, away_goals_minutes


def parserworker(link):
    """
    Собираются id каждой игры. Затем происходит сбор данных о каждой игре отдельно.
    """
    id_box = start_parsing(link)
    links_box = create_links_with_id(id_box)
    data_all_matches = ThreadPool(3).map(multithreading_start, links_box[:10])
    return data_all_matches


# if __name__ == "__main__":
#     id_box = start_parsing()
#     links_box = create_links_with_id(id_box)
#     print(links_box[:10])
#     a = ThreadPool(3).map(multithreading_start, links_box[:10])
#     print(a)
#     driver = get_driver()
#     driver.close()
#     driver.quit()




