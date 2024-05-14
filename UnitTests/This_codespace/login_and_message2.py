import re
from playwright.sync_api import Playwright, sync_playwright, expect
import keyring
import random
git_password = keyring.get_password("github", "rr400")
test_account_suffix = random.randint(100000, 999999)
string_suffix = str(test_account_suffix)
username = "testName"+string_suffix

def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://fluffy-goggles-wppxv5v5p77c9q9-8000.app.github.dev/login/")
   # page.goto("https://bingle.amanthapa.com.np/login")
   # page.goto("https://github.com/login?return_to=https%3A%2F%2Fgithub.com%2Fcodespaces%2Fauth%2Fscaling-parakeet-x77xrprpp69296w6%3Fid%3Dfun-chair-2f6n8xz%26cluster%3Duks1%26name%3Dscaling-parakeet-x77xrprpp69296w6%26port%3D8000%26pb%3Dhttps%253A%252F%252Fscaling-parakeet-x77xrprpp69296w6-8000.app.github.dev%252Fauth%252Fpostback%252Ftunnel%253Frd%253D%25252Fregister%25252F%2526tunnel%253D1%26cid%3D5a1fed40-9d09-4fe9-a22e-f25baea25ba8%26type%3Dbasis")
    page.get_by_label("Username or email address").click()
    page.get_by_label("Username or email address").click()
    page.get_by_label("Username or email address").fill("rr400")
    page.get_by_label("Password").click()
    page.get_by_label("Username or email address").click()
    page.get_by_label("Username or email address").fill("rr400@sussex.ac.uk")
    page.get_by_label("Password").click()
    page.get_by_label("Password").fill(git_password)
    page.get_by_label("Password").press("Enter")
    page.goto("https://fluffy-goggles-wppxv5v5p77c9q9-8000.app.github.dev/login/")
    page.get_by_label("Password").press("Enter")
    page.get_by_label("Username*").click()
    page.get_by_label("Username*").fill("th3b1gn4c")
    page.get_by_label("Username*").click()
    page.get_by_label("Password*").click()
    page.get_by_label("Password*").fill("ModelViewTemplate")
    page.get_by_role("button", name="Login").click()
    page.goto("https://fluffy-goggles-wppxv5v5p77c9q9-8000.app.github.dev/new_landing_page/")
    page.get_by_role("link", name="Chat").click()
    page.get_by_role("link", name="").click()
    page.get_by_role("link", name="Profile Picture percy Hi").click()
    page.get_by_placeholder("Type a Message").click()
    page.get_by_placeholder("Type a Message").fill("testing")
    page.get_by_role("button", name="").click()

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
