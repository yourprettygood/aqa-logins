from playwright.sync_api import Page


class BasePage:
    def __init__(self, page: Page):
        self.page = page

    @property
    def url(self) -> str:
        return self.page.url

    def goto(self, url: str, wait_until: str = "domcontentloaded") -> None:
        self.page.goto(url, wait_until=wait_until)
