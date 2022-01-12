import multiprocessing
from multiprocessing import Pool, Manager
import time
import random
import parsing


if __name__ == "__main__":
    q = parsing.get_archive_data('epl', ['2016/2017'], 'https://www.flashscore.ru/football/england/premier-league/')
    print(q)






