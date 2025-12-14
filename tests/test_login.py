import re

import allure
import pytest
from playwright.sync_api import expect

from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage

LOGIN_URL_RE = re.compile(r"^https://www\.saucedemo\.com/?$")
INVENTORY_URL_RE = re.compile(r".*/inventory\.html$")


@allure.suite("Авторизация")
class TestLogin:
    @allure.title("Успешный логин standard_user / secret_sauce")
    def test_login_success_standard_user(self, page):
        login_page = LoginPage(page).open()
        login_page.should_have_login_form()

        login_page.login(username="standard_user", password="secret_sauce")

        inventory_page = InventoryPage(page)
        inventory_page.should_be_opened()
        inventory_page.should_have_key_elements()

    @allure.title("Логин с неверным паролем")
    def test_login_wrong_password(self, page):
        login_page = LoginPage(page).open()
        login_page.should_have_login_form()

        login_page.login(username="standard_user", password="wrong_password")

        # URL должен остаться на странице логина
        expect(page).to_have_url(LOGIN_URL_RE)
        login_page.should_have_error()

    @allure.title("Логин заблокированного пользователя locked_out_user")
    def test_login_locked_out_user(self, page):
        login_page = LoginPage(page).open()
        login_page.should_have_login_form()

        login_page.login(username="locked_out_user", password="secret_sauce")

        expect(page).to_have_url(LOGIN_URL_RE)
        login_page.should_have_error()

    @allure.title("Логин с пустыми полями")
    @pytest.mark.parametrize(
        "username,password",
        [
            ("", ""),
            ("standard_user", ""),
            ("", "secret_sauce"),
        ],
    )
    def test_login_empty_fields(self, page, username, password):
        login_page = LoginPage(page).open()
        login_page.should_have_login_form()

        login_page.login(username=username, password=password)

        expect(page).to_have_url(LOGIN_URL_RE)
        login_page.should_have_error()

    @allure.title("Логин performance_glitch_user (возможные задержки)")
    def test_login_performance_glitch_user(self, page):
        login_page = LoginPage(page).open()
        login_page.should_have_login_form()

        login_page.login(username="performance_glitch_user", password="secret_sauce")

        # Для glitch_user даём больше времени на переход
        expect(page).to_have_url(INVENTORY_URL_RE, timeout=20000)

        inventory_page = InventoryPage(page)
        inventory_page.should_have_key_elements()
