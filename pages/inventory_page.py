import re

import allure
from playwright.sync_api import Page, expect

from pages.base_page import BasePage


class InventoryPage(BasePage):
    INVENTORY_CONTAINER = "[data-test='inventory-container']"
    INVENTORY_ITEM = ".inventory_item"
    CART_LINK = "[data-test='shopping-cart-link']"
    BURGER_MENU = "#react-burger-menu-btn"

    def __init__(self, page: Page):
        super().__init__(page)

    @allure.step("Проверить, что открыта страница Inventory")
    def should_be_opened(self) -> None:
        expect(self.page).to_have_url(re.compile(r".*/inventory\.html$"))
        expect(self.page.locator(self.INVENTORY_CONTAINER)).to_be_visible()

    @allure.step("Проверить ключевые элементы Inventory")
    def should_have_key_elements(self) -> None:
        expect(self.page.locator(self.BURGER_MENU)).to_be_visible()
        expect(self.page.locator(self.CART_LINK)).to_be_visible()
        expect(self.page.locator(self.INVENTORY_ITEM).first).to_be_visible()
