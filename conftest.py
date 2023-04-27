import pytest
from selenium import webdriver
import settings



@pytest.fixture(autouse=True)
def testing():
    driver = webdriver.Chrome('chromedriver.exe')
    # Переходим на страницу авторизации
    driver.implicitly_wait(5)
    driver.get(settings.base_url)

    yield

    driver.quit()

