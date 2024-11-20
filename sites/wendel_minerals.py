from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from classes.mineral import Mineral

b = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

def main():
    try:
        b.get('https://www.wendel-minerals.com/auctions/auctions_current/1?auk=%')
        assert "Wendel-Minerals" in b.title
        grid = b.find_element(By.ID, "gridview1")

        WebDriverWait(b, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//*[@id='gridview1']/div"))
        )

        children = grid.find_elements(By.XPATH, "./div") #./div means all direct children that are <div>s
        for _, c in enumerate(children):
            b.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", c)
            WebDriverWait(b, 10).until(EC.visibility_of(c))

            url = c.find_element(By.XPATH, ".//a[contains(@href, 'auctions/')]").get_attribute("href")
            name = c.find_element(By.XPATH, ".//a[contains(@href, 'auctions/')]").text
            origin = c.find_element(By.CSS_SELECTOR, "p.fundort").text
            price = c.find_element(By.CSS_SELECTOR, "p.beleved_imageborder").find_element(By.CSS_SELECTOR, "span.bold").text

            mineral = Mineral(url=url, name=name, origin=origin, price=price)
            mineral.save()
    except Exception as e:
        print(f"Something went wrong: {e}")
    finally:
        b.quit()