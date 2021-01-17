import time
import random
from helps import index_page

MAX_PAGE = 100

if __name__  == '__main__':
    for i in range(1, MAX_PAGE + 1):
        index_page(i)
        # 设置延迟时间，防止反爬
        time.sleep(random.randint(1, 5))