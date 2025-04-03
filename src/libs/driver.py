from selenium import webdriver
import os


def build_driver():
    try:
        webdriver_path = os.path.join(os.getcwd(), 'windows-chromedrivers', 'chrome-win64', "chrome.exe")
        driver_path = os.path.join(os.getcwd(), 'windows-chromedrivers', 'chromedriver-win64', "chromedriver")
        # webdriver_path = "/opt/headless-chromium"
        # driver_path = "/opt/chromedriver"
        # os.environ['PATH'] = '/opt:' + os.environ['PATH']

        chrome_options = webdriver.ChromeOptions()
        print("Objeto options criado! Adicionando argumentos...")
        # chrome_options.binary_location = '/opt/headless-chromium'
        chrome_options.binary_location = webdriver_path
        # chrome_options.add_argument('--headless')
        chrome_options.add_argument('--start-maximized')
        chrome_options.add_experimental_option("detach", True)
        # chrome_options.add_argument('--no-sandbox')
        # chrome_options.add_argument('--single-process')
        # chrome_options.add_argument('--disable-dev-shm-usage')

        print(f"Argumentos adicionados! Criando o navegador...")
        navegador = webdriver.Chrome(executable_path=driver_path, options=chrome_options)
        print(f"O navegador foi criado.")
        return navegador
    except Exception as error:
        print(f"Error: {error}")
    return False
