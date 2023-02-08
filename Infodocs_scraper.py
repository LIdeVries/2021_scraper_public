from selenium import webdriver
import time
import csv
import os


t1 = time.time()
print("Program started")

individuallink = open(os.getenv("LINKSTXT"), "r")
links = individuallink.read().split("\n")

# Driver setup
chrome_options = webdriver.ChromeOptions()
driver = webdriver.Chrome(
    executable_path=os.getenv("CROMEDRIVER"),
    options=chrome_options,
)
print("Driver set")


# Documents set up

file = open(os.getenv("CSV"), "a")
writer = csv.writer(file)
header = [
    "Company Name",
    "link",
    "level",
    "Partnership Age",
    "Website",
    "Main Phone",
    "Social 1",
    "Social 2",
    "Social 3",
    "Offices and Telephone Contacts",
    "Team Member & Role",
    "Team Size",
    "Industries Served (Incomplete)",
]
writer.writerow(header)


for site in links:
    row = []
    driver.get(site)
    print("Site loaded->", site)

    # - Company Name √
    try:
        result = driver.find_element(
            "css selector",
            "#advisors-profile > div.section.section-padding.section-padding-none > div > div \
        > div > div.advisors-profile-hero-detailed-content-right.small-12.large-7.columns > div > h1",
        )
        res = result.text
        print("This is Name ->", res)
    except AttributeError:
        print("Company Name -> N/A")
    row.append(res)
    res = " "

    # - link
    print("This is Link ->", site)
    res = site
    row.append(res)
    res = " "

    levels = [
        "Bronze champion partner",
        "Silver champion partner",
        "Gold champion partner",
        "Platinum champion partner",
        "Group champion partner",
        "champion partner",
        "Bronze partner",
        "Silver partner",
        "Gold partner",
        "Platinum partner",
        "Group partner",
        "partner",
    ]
    try:
        driver.get(site)

        list = driver.find_element("x-path", '//*[@id="advisors-profile"]/div[2]/div')
        list = list.text
        for level in levels:
            if level in list:
                res = level
                print("Level ->", res)
                break

    except AttributeError:
        pass
        print("level -> N/A")
    row.append(res)
    res = " "

    # - Partner Since √
    try:
        result = driver.find_element("x-path", '//*[contains(text(),"Partner since")]')
        result = result.text
        result = result[-5:]
        print("This is Partnership Since ->", result)
        res = result
    except AttributeError:
        print("Partnership Since -> N/A")
    row.append(res)
    res = " "

    # - website √
    try:
        result = driver.find_elements("x-path", '//*[text()="View website"]')
        for res in result:
            print("This is Website ->", res.get_attribute("href"))
            res = res.get_attribute("href")
    except AttributeError:
        print("Website -> N/A")
    row.append(res)
    res = " "

    # - phone √
    try:
        result = driver.find_element("link text", "Phone number")
        res = result.get_attribute("data-phone")
    except AttributeError:
        print("Phone Number -> N/A")
    row.append(res)
    res = " "

    # - Social 1 √
    try:
        result = driver.find_elements(
            "css selector",
            "#advisors-profile > div:nth-child(4) > div > div > \
        div.advisor-profile-practice-block.advisor-profile-practice-social > ul > li:nth-child(1) > a",
        )
        for res in result:
            print("This is Social 1 ->", res.get_attribute("href"))
            res = res.get_attribute("href")
    except AttributeError:
        print("Social 1 ->N/A")
    row.append(res)
    res = " "
    # - Social 2 √
    try:
        result = driver.find_elements(
            "css selector",
            "#advisors-profile > div:nth-child(4) > div > div >\
        div.advisor-profile-practice-block.advisor-profile-practice-social > ul > li:nth-child(2) > a",
        )
        for res in result:
            print("This is Social 2 ->", res.get_attribute("href"))
            res = res.get_attribute("href")
    except AttributeError:
        print("Social 2 -> N/A")
    row.append(res)
    res = " "

    # - Social 3 √
    try:
        result = driver.find_elements(
            "css selector",
            "#advisors-profile > div:nth-child(4) > div > \
        div > div.advisor-profile-practice-block.advisor-profile-practice-social > ul > li:nth-child(3) > a",
        )
        for res in result:
            print("This is Social 3 ->", res.get_attribute("href"))
            res = res.get_attribute("href")
    except AttributeError:
        print("Social 3 -> N/A")
    row.append(res)
    res = " "

    # - Office addresses and Telephone numbers √
    try:
        result = driver.find_elements(
            "class name", "advisors-profile-locations-list-wrapper"
        )
        for res in result:
            res = res.text
            res = res.replace("\n+", " @ +")
        print("This is Locations and tel  ->", res)
        res = result.text
    except AttributeError:
        print("Locations and tel -> N/A")
    row.append(res)
    res = " "

    # - Team Member & Role
    # Clicks get more team members
    try:
        while True:
            click = driver.find_element(
                "x-path", '//*[@id="advisors-profile"]/div[4]/div/div[3]/div/button'
            )
            click.click()
            # print('Clicked button')
            time.sleep(3)

    except AttributeError:
        pass
        # - Refines down to single string
    try:
        result = driver.find_elements(
            "x-path", '//*[@id="advisors-profile"]/div[4]/div/div[2]'
        )
        for person in result:
            res = person.text
            res = res.replace("\nShow\n", ", ")
            res = res.replace("\n", " is ")
            res = res.replace(" is Show", "")
            print("This is team ->", res)
    except AttributeError:
        print("Team -> N/A")
        pass
    row.append(res)
    res = " "

    # - Team size √
    try:
        result = driver.find_elements(
            "css selector",
            " #advisors-profile > div:nth-child(5) > div > div.row.advisors-profile-team-intro > p:nth-child(2)",
        )
        for results in result:
            txt = results.text
            txt = txt.split(": ")
            txt = txt[1].split(" -")
            res = txt[0]
            print("This is Team Size ->", res)
    except AttributeError:
        print("Team size -> N/A")
    row.append(res)
    res = " "

    # - Indusries Served √
    try:
        result = driver.find_elements(
            "x-path", "/html/body/main/div/div[6]/div[2]/div/div/div/ul"
        )
        for res in result:
            txt = res.text
            res = txt.replace("\n", " & ")
            print("This is industries served ->", res)
    except AttributeError:
        print("Industires served -> N/A")
    row.append(res)
    res = " "

    # print (header)
    print(row)
    writer.writerow(row)
    # driver.quit()


file.close()
driver.quit()
t2 = time.time()
print("\n\nPROGRAM COMPLETE:")
print("Total time", (t2 - t1) / 60, "minutes")
