import pickle
import time
import pytest
from auth.auth import *
from selenium.webdriver.common.by import By
from auth.settings import valid_phone, valid_login, valid_password, invalid_ls, valid_email, valid_pass_reg


@pytest.mark.auth
@pytest.mark.positive
@pytest.mark.xfail
@pytest.mark.parametrize('username', [valid_phone, valid_email, valid_login, invalid_ls],
                         ids=['phone', 'email', 'login', 'ls'])
def test_active_tab(browser, username):
    """Проверка автоматического переключения табов телефон/email/логин/лицевой счет
    invalid_ls - лицевой счет правильного формата, при ручном переключении таба на лицевой счет,
    система его принимает, в автоматическом режиме переключения не происходит, воспринимается
    как номер телефона, откидывая последнюю пару цифр!"""
    page = AuthPage(browser)
    page.enter_username(username)
    page.enter_password(valid_password)
    if username == valid_phone:
        assert browser.find_element(*AuthLocators.AUTH_ACTIVE_TAB).text == 'Телефон'
    elif username == valid_email:
        assert browser.find_element(*AuthLocators.AUTH_ACTIVE_TAB).text == 'Почта'
    elif username == valid_login:
        assert browser.find_element(*AuthLocators.AUTH_ACTIVE_TAB).text == 'Логин'
    else:
        assert browser.find_element(*AuthLocators.AUTH_ACTIVE_TAB).text == 'Лицевой счет'


@pytest.mark.auth
@pytest.mark.positive
@pytest.mark.parametrize('username', [valid_phone, valid_login],
                         ids=['valid phone', 'valid login'])
def test_auth_page_phone_login_valid(browser, username):
    """Проверка авторизации по номеру телефона/логину и паролю + проверка
    автоматического переключения табов тел/логин (для проверки нужен зарегистрированный номер телефона)"""
    page = AuthPage(browser)
    page.enter_username(username)
    page.enter_password(valid_password)
    page.btn_click_enter()

    assert page.get_relative_link() == '/account_b2c/page'


@pytest.mark.auth
@pytest.mark.positive
def test_auth_page_email_valid(browser):
    """Проверка авторизации по почте и паролю"""
    page = AuthPage(browser)
    page.enter_username(valid_email)
    page.enter_password(valid_pass_reg)
    time.sleep(25)     # на случай появления Captcha, необходимости ее ввода вручную
    page.btn_click_enter()
    page.driver.save_screenshot('auth_by_email.png')

    with open('my_cookies.txt', 'wb') as cookies:
        pickle.dump(browser.get_cookies(), cookies)

    assert page.get_relative_link() == '/account_b2c/page'


@pytest.mark.reg
@pytest.mark.positive
def test_reg_page_open(browser):
    """ Проверка страницы регистрации - дымовое тестирование """
    page = AuthPage(browser)
    page.enter_reg_page()

    assert page.get_relative_link() == '/auth/realms/b2c/login-actions/registration'