import random

import requests
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from src.libs.driver import build_driver


def login_exemplo(tempo_sleep=1):
    navegador = build_driver()

    try:
        url_pagina_inicial = 'https://sigcol.netsuprema.com.br/secovicred/index.php'
        usuario = ''
        senha = ''
        url_pesquisa_titulos = "https://sigcol.netsuprema.com.br/secovicred/index.php?doctype=iframe&KMP=Col&KMF=Pesquisa_Titulo"

        try:
            navegador.get(url=url_pagina_inicial)
            sleep(tempo_sleep)
            print(f"Scraping iniciado! Get na pagina incial: [{url_pagina_inicial}].")
        except Exception as error:
            print(f'EXCEPTION: Erro ao tentar dar o primeiro get na pagina inicial. Error: {error}')
            navegador.quit()
            return False

        try:
            input_usuario = navegador.find_element(by=By.ID, value="USUARIO")
            input_usuario.clear()
            input_usuario.send_keys(usuario)
            sleep(tempo_sleep)
            input_senha = navegador.find_element(by=By.ID, value="SENHA")
            input_senha.clear()
            input_senha.send_keys(senha)
            sleep(tempo_sleep)
            button_login = navegador.find_element(by=By.ID, value="buttonEntrar")
            button_login.click()
            print("Fazendo login na pagina inicial...")
        except Exception as error:
            print(
                f'## EXCEPTION: Erro ao tentar inserir o usuario e senha no site e fazer o login. Encerrando o navegador... Error: {error}')
            navegador.quit()
            return False

        try:
            print("RESOLVA O CAPTCHA PARA PROSSEGUIR!")
            WebDriverWait(navegador, timeout=300).until(
                EC.presence_of_element_located((By.ID, "nmusuario"))
            )
        except Exception as error:
            print(
                f'## EXCEPTION: Nao foi possivel aguardar a resolucao do captcha pelo usuario. Encerrando o navegador... Error: {error}')
            navegador.quit()
            return False

        selenium_cookies = navegador.get_cookies()

        session = requests.Session()

        csrf_token = navegador.execute_script("return window.localStorage.getItem('csrf_token');")
        jwt_token = navegador.execute_script("return window.localStorage.getItem('jwt_token');")

        for cookie in selenium_cookies:
            session.cookies.set(cookie["name"], cookie["value"])

        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": navegador.execute_script("return navigator.language;"),
            "Host": "sigcol.netsuprema.com.br",
            "Referer": "https://sigcol.netsuprema.com.br/secovicred/index.php",
            "Sec-Fetch-Dest": "iframe",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": navegador.execute_script("return navigator.userAgent;")
        }

        if csrf_token:
            headers["X-CSRF-Token"] = csrf_token
        if jwt_token:
            headers["Authorization"] = f"Bearer {jwt_token}"

        navegador.quit()
        response = session.get(url_pesquisa_titulos, headers=headers)
        print(response.text)
    finally:
        navegador.quit()


def user_agent_aleatorio():
    lista_user_agents = [
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    ]
    user_agent = random.choice(lista_user_agents)
    return user_agent


def login_bradesco(tempo_sleep=3):
    navegador = build_driver()

    try:
        url_pagina_inicial = 'https://wwws.bradescosaude.com.br/PCBS-GerenciadorPortal/td/loginReferenciado.do'
        cpf = ''
        cnpj = ''
        senha = ''

        try:
            print("O GOOGLE CHROME VAI ABRIR! FAÇA O LOGIN E RESOLVA O CAPTCHA PARA PROSSEGUIR!")
            navegador.get(url=url_pagina_inicial)
            sleep(tempo_sleep)
        except Exception as error:
            print(f'SELENIUM: Erro ao tentar dar o primeiro get na pagina inicial. Error: {error}')
            navegador.quit()
            return False

        """ faz login sozinho e aguarda somente fazer o captcha 
        try:
            input_cpf = navegador.find_element(by=By.ID, value="cpfRefPJ")
            input_cpf.clear()
            input_cpf.send_keys(cpf)
            sleep(tempo_sleep)
            input_cnpj = navegador.find_element(by=By.ID, value="cnpjRef")
            input_cnpj.clear()
            input_cnpj.send_keys(cnpj)
            sleep(tempo_sleep)
            input_senha = navegador.find_element(by=By.ID, value="senhaRef")
            input_senha.clear()
            input_senha.send_keys(senha)
            # aceitar cookies
            sleep(tempo_sleep)
            button_cookies = navegador.find_element(by=By.ID, value="adopt-accept-all-button")
            button_cookies.click()
            # fazer login
            sleep(tempo_sleep)
            button_login = navegador.find_element(by=By.ID, value="btLoginReferenciado")
            button_login.click()
            print("Fazendo login no portal da Bradesco...")
        except Exception as error:
            print(
                f'## EXCEPTION: Erro ao tentar inserir o cpf, cnpj e senha no site e fazer o login. Encerrando o navegador... Error: {error}')
            navegador.quit()
            return False
        """

        try:
            WebDriverWait(navegador, timeout=300).until(
                EC.presence_of_element_located((By.CLASS_NAME, "div-name-entity"))
            )
        except Exception as error:
            print(f'## EXCEPTION: Nao foi possivel aguardar a resolucao do captcha pelo usuario. Encerrando o navegador... Error: {error}')
            navegador.quit()
            return False

        selenium_cookies = navegador.get_cookies()
        session = requests.Session()

        for cookie in selenium_cookies:
            session.cookies.set(cookie["name"], cookie["value"])

        accept_language = navegador.execute_script("return navigator.language;")
        user_agent = navegador.execute_script("return navigator.userAgent;")

        # pega numero controle
        try:
            pagina_logada = navegador.page_source
            numero_controle = pagina_logada.split("nroControle=")[1].split('&')[0]
        except Exception as error:
            raise Exception(f"Falha no login ao obter numero_controle -> {error}")

        navegador.quit()

        try:
            response = session.post(
                url="https://wwws.bradescosaude.com.br/PCBS-GerenciadorPortal/novaHomeSaudeReferenciado.do",
                data={"portal": "S", "nroControle": numero_controle, "area": "home"},
                headers={
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,/;q=0.8,application/signed-exchange;v=b3;q=0.7",
                    "Accept-Encoding": "gzip, deflate, br",
                    "Accept-Language": accept_language,
                    "Content-Type": "application/x-www-form-urlencoded",
                    "Host": "wwws.bradescosaude.com.br",
                    "Origin": "https://wwws.bradescosaude.com.br/",
                    "Referer": "https://wwws.bradescosaude.com.br/PCBS-GerenciadorPortal/novaHomeSaudeReferenciado.do",
                    "Sec-Ch-Ua-Mobile": "?0",
                    "Sec-Ch-Ua-Platform": '"Linux"',
                    "Sec-Fetch-Dest": "document",
                    "Sec-Fetch-Mode": "navigate",
                    "Sec-Fetch-Site": "same-origin",
                    "Upgrade-Insecure-Requests": "1",
                    "User-Agent": user_agent,
                },
                verify=False,
                timeout=200,
            )
        except Exception as error:
            raise Exception(f'[acessa_pagina_inicial] erro na requisicao https://wwws.bradescosaude.com.br/PCBS-GerenciadorPortal/novaHomeSaudeReferenciado.do. {error}')

        print(response.text)
    finally:
        navegador.quit()
