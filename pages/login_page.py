import allure
from playwright.sync_api import Page, expect

from config.settings import BASE_URL
from pages.base_page import BasePage


class LoginPage(BasePage):
    USERNAME_INPUT = "[data-test='username']"
    PASSWORD_INPUT = "[data-test='password']"
    LOGIN_BUTTON = "[data-test='login-button']"
    ERROR_MESSAGE = "[data-test='error']"

    def __init__(self, page: Page):
        super().__init__(page)

    @allure.step("Открыть страницу логина")
    def open(self) -> "LoginPage":
        self.goto(BASE_URL)
        return self

    @allure.step("Проверить, что форма логина отображается")
    def should_have_login_form(self) -> None:
        expect(self.page.locator(self.USERNAME_INPUT)).to_be_visible()
        expect(self.page.locator(self.PASSWORD_INPUT)).to_be_visible()
        expect(self.page.locator(self.LOGIN_BUTTON)).to_be_visible()

    @allure.step("Выполнить логин пользователем: {username}")
    def login(self, username: str, password: str) -> None:
        self.page.locator(self.USERNAME_INPUT).fill(username)
        self.page.locator(self.PASSWORD_INPUT).fill(password)
        self.page.locator(self.LOGIN_BUTTON).click()

    @allure.step("Проверить, что отображается ошибка авторизации")
    def should_have_error(self) -> None:
        expect(self.page.locator(self.ERROR_MESSAGE)).to_be_visible()

    def get_error_text(self) -> str:
        return self.page.locator(self.ERROR_MESSAGE).inner_text()
