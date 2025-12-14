import allure
from playwright.sync_api import Page


def attach_screenshot(page: Page, name: str = "screenshot") -> None:
    try:
        allure.attach(
            page.screenshot(full_page=True),
            name=name,
            attachment_type=allure.attachment_type.PNG,
        )
    except Exception:
        # Не падаем из-за ошибок аттачей
        pass


def attach_page_source(page: Page, name: str = "page_source") -> None:
    try:
        allure.attach(
            page.content(),
            name=name,
            attachment_type=allure.attachment_type.HTML,
        )
    except Exception:
        pass
