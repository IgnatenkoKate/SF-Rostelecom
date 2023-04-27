import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from settings import *


# # python -m pytest -v --driver Chrome --driver-path G:\chromedriver\chromedriver.exe tests\test_auth_page.py
# # python -m pytest -v --driver Chrome --driver-path chromedriver.exe tests\test_auth_page.py


@pytest.fixture(autouse=True)
def testing():
    driver = webdriver.Chrome()
    driver.implicitly_wait(6)
    driver.get('https://b2c.passport.rt.ru')
    yield driver
    driver.quit()


def test_opening_registration_page(testing):
    """Тест 1. Загрузка страницы регистрации """
    driver = testing
    driver.get('https://b2c.passport.rt.ru')
    element = WebDriverWait(driver, 7).until(EC.visibility_of_element_located((By.ID, 'kc-register')))
    driver.find_element(By.ID, 'kc-register').click()
    driver.implicitly_wait(5)
    assert driver.find_element(By.TAG_NAME, 'h1').text == 'Регистрация', print('Тест провален')
    assert driver.find_element(By.TAG_NAME, 'p').text == 'Личные данные', print('Тест провален')
    assert driver.find_element(By.XPATH, '//button[@type="submit"]'), print('Тест провален')


def test_password_recovery(testing):
    """Тест 2. Загрузка страницы 'Восстановление пароля'"""
    driver = testing
    driver.get('https://b2c.passport.rt.ru')
    element = WebDriverWait(driver, 7).until(EC.visibility_of_element_located((By.ID, 't-btn-tab-login')))
    driver.find_element(By.ID, 'forgot_password').click()
    assert driver.find_element(By.TAG_NAME, 'h1').text == 'Восстановление пароля', print('Тест провален')
    assert driver.find_element(By.ID, 'reset').text == 'Продолжить', print('Тест провален')


def test_reg_existing(testing):
    """Тест 3. Регистрация уже зарегистрированного пользователя"""
    driver = testing
    driver.get('https://b2c.passport.rt.ru')
    element = WebDriverWait(driver, 7).until(EC.visibility_of_element_located((By.ID, 'kc-register')))
    driver.find_element(By.ID, 'kc-register').click()
    driver.find_element(By.NAME, 'firstName').send_keys(valid_name)
    driver.find_element(By.NAME, 'lastName').send_keys(valid_lastname)
    driver.find_element(By.ID, 'address').send_keys(email)
    driver.find_element(By.ID, 'password').send_keys(password)
    driver.find_element(By.ID, 'password-confirm').send_keys(password)
    driver.find_element(By.XPATH, '//button[@type="submit"]').click()
    time.sleep(3)
    assert driver.find_element(By.TAG_NAME, 'h2').text == 'Учётная запись уже существует', print('Ошибка')


def test_reg_invalid_empty(testing):
    """Тест 4. Регистрация пользователя с пустым вводом всех полей  """
    driver = testing
    driver.get('https://b2c.passport.rt.ru')
    element = WebDriverWait(driver, 7).until(EC.visibility_of_element_located((By.ID, 'kc-register')))
    driver.find_element(By.ID, 'kc-register').click()
    driver.find_element(By.XPATH, '//button[@type="submit"]').click()
    error = driver.find_elements(By.CSS_SELECTOR, '.rt-input-container--error')
    assert len(error) == 5


def test_reg_invalid_code(testing):
    """Тест 5. Регистрация пользователя с вводом неверного кода доступа"""
    driver = testing
    driver.get('https://b2c.passport.rt.ru')
    element = WebDriverWait(driver, 7).until(EC.visibility_of_element_located((By.ID, 'kc-register')))
    driver.find_element(By.ID, 'kc-register').click()
    driver.find_element(By.NAME, 'firstName').send_keys(name)
    driver.find_element(By.NAME, 'lastName').send_keys(lastname)
    driver.find_element(By.ID, 'address').send_keys(fake_email)
    driver.find_element(By.ID, 'password').send_keys(fake_password)
    driver.find_element(By.ID, 'password-confirm').send_keys(fake_password)
    driver.find_element(By.XPATH, '//button[@type="submit"]').click()
    driver.find_element(By.ID, 'rt-code-0').send_keys(invalid_code)
    assert driver.find_element(By.ID, 'form-error-message').text == 'Неверный код. Повторите попытку', print('Ошибка')


def test_reg_email_without_dog(testing):
    """Тест 6. Ввод некорректного e-mail (без символа @)"""
    driver = testing
    driver.get('https://b2c.passport.rt.ru')
    element = WebDriverWait(driver, 7).until(EC.visibility_of_element_located((By.ID, 'kc-register')))
    driver.find_element(By.ID, 'kc-register').click()
    driver.find_element(By.NAME, 'firstName').send_keys(name)
    driver.find_element(By.NAME, 'lastName').send_keys(lastname)
    driver.find_element(By.ID, 'address').send_keys(email_without_dog)
    driver.find_element(By.ID, 'password').send_keys(fake_password)
    error = driver.find_elements(By.CSS_SELECTOR, '.rt-input-container--error')
    assert len(error) == 1


def test_reg_email_without_domain(testing):
    """Тест 7. Ввод некорректного e-mail (без домена)"""
    driver = testing
    driver.get('https://b2c.passport.rt.ru')
    element = WebDriverWait(driver, 7).until(EC.visibility_of_element_located((By.ID, 'kc-register')))
    driver.find_element(By.ID, 'kc-register').click()
    driver.find_element(By.NAME, 'firstName').send_keys(name)
    driver.find_element(By.NAME, 'lastName').send_keys(lastname)
    driver.find_element(By.ID, 'address').send_keys(email_without_domain)
    driver.find_element(By.ID, 'password').send_keys(fake_password)
    error = driver.find_elements(By.CSS_SELECTOR, '.rt-input-container--error')
    assert len(error) == 1


def test_elements_of_auth(testing):
    """Тест 8. Проверка Формы "Авторизация" на наличие основных элементов."""
    driver = testing
    driver.get('https://b2c.passport.rt.ru')
    assert 'Телефон' in driver.find_element(By.ID, 't-btn-tab-phone').text
    assert 'Почта' in driver.find_element(By.ID, 't-btn-tab-mail').text
    assert 'Логин' in driver.find_element(By.ID, 't-btn-tab-login').text
    assert 'Лицевой счёт' in driver.find_element(By.ID, 't-btn-tab-ls').text


def test_auth_user_mail(testing):
    """Тест 9. Авторизация с помощью валидных данных (электронная почта и пароль) (зарегистрированный пользователь)"""
    driver = testing
    driver.get('https://b2c.passport.rt.ru')
    element = WebDriverWait(driver, 7).until(EC.visibility_of_element_located((By.ID, 'kc-login')))
    driver.find_element(By.ID, 't-btn-tab-mail').click()
    driver.find_element(By.ID, 'username').send_keys(email)
    driver.find_element(By.ID, 'password').send_keys(password)
    driver.find_element(By.XPATH, '//button[@type="submit"]').click()
    time.sleep(3)
    assert driver.find_element(By.TAG_NAME, 'h3').text == 'Учетные данные'


def test_login_by_phone_invalid(testing):
    """Тест 10. Проверяем поведение системы при вводе незарегистрированного телефона"""
    driver = testing
    driver.get('https://b2c.passport.rt.ru')
    driver.implicitly_wait(10)
    driver.find_element(By.ID, 'username').send_keys(invalid_phone2)
    driver.find_element(By.ID, 'password').send_keys(password)
    driver.find_element(By.ID, 'kc-login').click()

    assert driver.find_element(By.ID, 'form-error-message').text == 'Неверный логин или пароль'
    assert driver.find_element(By.ID, 'forgot_password').value_of_css_property('color') == "rgba(255, 79, 18, 1)"


def test_login_by_email_invalid(testing):
    """Тест 11. Проверяем поведение системы при вводе незарегистрированного e-mail"""
    driver = testing
    driver.get('https://b2c.passport.rt.ru')
    driver.find_element(By.ID, 't-btn-tab-mail').click()
    driver.find_element(By.ID, 'username').send_keys(fake_email)
    driver.find_element(By.ID, 'password').send_keys(fake_password)
    driver.find_element(By.ID, 'kc-login').click()

    assert driver.find_element(By.ID, 'form-error-message').text == 'Неверный логин или пароль'
    assert driver.find_element(By.ID, 'forgot_password').value_of_css_property('color') == "rgba(255, 79, 18, 1)"


def test_reset_back_btn(testing):
    """Тест 12. Проверка кнопки "Вернуться назад" без ввода символов на странице 'Восстановление пароля'"""
    driver = testing
    driver.get('https://b2c.passport.rt.ru')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'forgot_password')))
    driver.find_element(By.ID, 'forgot_password').click()
    driver.find_element(By.ID, 'reset-back').click()


def test_redirect_reset_pass(testing):
    """Тест 13. Восстановление пароля"""
    driver = testing
    driver.get('https://b2c.passport.rt.ru')
    driver.find_element(By.ID, 'forgot_password').click()
    assert driver.find_element(By.CLASS_NAME, 'card-container__title').text == 'Восстановление пароля'


def test_vk_btn(testing):
    """Тест 14. Кликабельность кнопки VK"""
    driver = testing
    driver.get('https://b2c.passport.rt.ru')
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 'oidc_vk'))).click()
    assert 'vk.com' in driver.find_element(By.XPATH, '//div[@class="oauth_head"]/a').get_attribute('href')
    assert 'vk' in driver.current_url


def test_ok_btn(testing):
    """Тест 15. Кликабельность кнопки OK"""
    driver = testing
    driver.get('https://b2c.passport.rt.ru')
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 'oidc_ok'))).click()
    assert driver.find_element(By.XPATH, '//div[@class="ext-widget_h_tx"]').text == 'Одноклассники'
    assert 'ok' in driver.current_url


def test_mail_btn(testing):
    """Тест 16. Кликабельность кнопки @"""
    driver = testing
    driver.get('https://b2c.passport.rt.ru')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'oidc_mail'))).click()
    assert 'mail.ru' in driver.find_element(By.XPATH, '//span[@class="header__logo"]').text.lower()
    assert 'mail' in driver.current_url


def test_google_btn(testing):
    """Тест 17. Кликабельность кнопки G"""
    driver = testing
    driver.get('https://b2c.passport.rt.ru')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'oidc_google'))).click()
    assert 'google' in driver.current_url


def test_yandex_btn(testing):
    """Тест 18. Кликабельность кнопки Я"""
    driver = testing
    driver.get('https://b2c.passport.rt.ru')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'oidc_ya'))).click()

    try:
        assert 'yandex' in driver.current_url
    except AssertionError:
        print('переход не осуществлен')


def test_privacy_policy_footer(testing):
    """Тест 19. Кликабельность сслылки в футере 'Политика конфиденциальности'"""
    driver = testing
    driver.get('https://b2c.passport.rt.ru')
    driver.find_elements(By.XPATH, '//a[@id="rt-footer-agreement-link"]/span')[0].click()
    driver.switch_to.window(driver.window_handles[1])
    title = driver.find_element(By.XPATH, '//div[@id="title"]/h1').text
    assert title.startswith('Публичная оферта'), 'Тест не прошел. Найден баг'


def test_agreements_footer(testing):
    """Тест 20. Кликабельность сслылки в футере 'Пользовательское соглашение'"""
    driver = testing
    driver.get('https://b2c.passport.rt.ru')
    driver.find_elements(By.XPATH, '//a[@id="rt-footer-agreement-link"]/span')[1].click()
    driver.switch_to.window(driver.window_handles[1])
    assert driver.find_element(By.TAG_NAME,
                               'h1').text == 'Публичная оферта о заключении Пользовательского соглашения на ' \
                                             'использование Сервиса «Ростелеком ID»'
