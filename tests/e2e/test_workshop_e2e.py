import re
from playwright.sync_api import expect


def testusercreatescarinbrowser(page, live_server):
    page.goto(f"{live_server}/cars/new")
    page.get_by_label("Make", exact=True).fill("Toyota")
    page.get_by_label("Model", exact=True).fill("Yaris")
    page.get_by_label("Year", exact=True).fill("2020")
    page.get_by_label("Color", exact=False).fill("Blue")
    page.get_by_role("button", name="Create car").click()
    expect(page).to_have_url(re.compile(r"/cars/\d+$"))
    expect(page.get_by_role("heading", name=re.compile(r"Toyota\s*Yaris"))).to_be_visible()
    # expect(page.get_by_role("heading", name="Toyota Corolla")).to_be_visible()

def test_user_edits_car_and_change_survives_reload(page, live_server):
    # 1. 打开新建页面，创建 Honda Civic 2022
    page.goto(f"{live_server}/cars/new")
    page.get_by_label("Make", exact=True).fill("Honda")
    page.get_by_label("Model", exact=True).fill("Civic")
    page.get_by_label("Year", exact=True).fill("2022")
    page.get_by_label("Color", exact=False).fill("Blue")
    page.get_by_role("button", name="Create car").click()

    # 2. 等待跳转到详情页，然后点击 Edit car 链接
    expect(page).to_have_url(re.compile(r"/cars/\d+$"))
    page.get_by_role("link", name="Edit car").click()

    # 3. 修改 model 和 year
    page.get_by_label("Model", exact=True).fill("Accord")
    page.get_by_label("Year", exact=True).fill("2023")

    # 4. 保存
    page.get_by_role("button", name="Save changes").click()

    # 5. 断言详情页 heading 变成 Honda Accord
    expect(page.get_by_role("heading", name=re.compile(r"Honda\s*Accord"))).to_be_visible()

    # 6. 刷新页面，断言修改被持久化
    page.reload()
    expect(page.locator("#car-model")).to_have_text("Accord")
    expect(page.locator("#car-year")).to_have_text("2023")