import pytest
from datetime import datetime
from pathlib import Path
import re

from playwright.sync_api import sync_playwright

from utils.allure_attachments import attach_screenshot, attach_page_source


ARTIFACTS_DIR = Path(__file__).resolve().parent / "artifacts"


def _safe_filename(value: str, max_len: int = 180) -> str:
    value = re.sub(r"[^\w\-.]+", "_", value, flags=re.UNICODE)
    value = value.strip("_.")
    return value[:max_len] if value else "test"


@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        yield browser
        browser.close()


@pytest.fixture()
def page(browser, request):
    context = browser.new_context()
    page = context.new_page()

    yield page

    # Attachments for Allure on failure
    rep_call = getattr(request.node, "rep_call", None)
    if rep_call and rep_call.failed:
        # 1) Allure attachments (как было)
        attach_screenshot(page, name="failure_screenshot")
        attach_page_source(page, name="failure_page_source")

        # 2) Extra artifacts in project folder (human-friendly)
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            test_id = _safe_filename(request.node.nodeid)

            run_dir = ARTIFACTS_DIR / datetime.now().strftime("%Y-%m-%d")
            run_dir.mkdir(parents=True, exist_ok=True)

            png_path = run_dir / f"{test_id}_{timestamp}.png"
            html_path = run_dir / f"{test_id}_{timestamp}.html"

            page.screenshot(path=str(png_path), full_page=True)
            html_path.write_text(page.content(), encoding="utf-8")
        except Exception:
            pass

    context.close()


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)
