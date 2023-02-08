from selenium import webdriver
import time
import os


t1 = time.time()
print("Program started")

# Driver setup
chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('--headless') # display/hide Chrome window
driver = webdriver.Chrome(
    executable_path=os.getenv("CROMEDRIVER"),
    options=chrome_options,
)
print("Driver set")

# Documents set up

f = open("links.txt", "a")


# Webpage iterator
try:
    links = []
    for num in range(36):
        webint = os.getenv("WEBINT") + str(num)
        links.append(webint)

    individuallink = []
    for webint in links:
        driver.get(webint)
        print("Page loaded")
        results = driver.find_element("class", "searchfilterresults-advisors")
        print("This is results ->", results)
        pages = results.find_elements("name", "advisors-result-card-link")
        for page in pages:
            href = page.get_attribute("href")
            print("This is href", href)
            txt = "".join(href)

            f.write(txt)
            f.write("\n")
except AttributeError:
    print("AttributeError")
    pass

driver.quit()
print("\n\n PROGRAM COMPLETE")
