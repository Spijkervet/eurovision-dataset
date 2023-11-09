from selenium import webdriver


class BaseScraper:
    def __init__(self):
        try:
            options = webdriver.ChromeOptions()
            options.add_argument("headless")
            options.add_argument("no-sandbox")
            options.add_argument("disable-dev-shm-usage")
            self.driver = webdriver.Chrome(options=options)
            return
        except Exception as e:
            print("Chrome WebDriver is missing")
            print(e)
            pass

        try:
            options = webdriver.firefox.options.Options()
            options.add_argument("--headless")
            self.driver = webdriver.Firefox(options=options)
            return
        except Exception as e:
            print("Firefox WebDriver is missing")
            print(e)
            pass

        try:
            self.driver = webdriver.Safari()
            return
        except:
            print("Safari is missing")
            pass

    def get_sf_num(self, sf):
        if sf == "semi-final":
            return str(0)
        if sf == "semi-final-1":
            return str(1)
        if sf == "semi-final-2":
            return str(2)
