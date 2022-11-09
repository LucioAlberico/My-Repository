from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from bs4 import BeautifulSoup
import time
import datetime
import requests
import os
import sys
from pyvirtualdisplay import Display

executable_path = "/usr/local/bin/geckodriver"
binary_path = r"/usr/bin/firefox"

#DEFINIENDO CANALES PARA ENVIAR MENSAJE DISCORD
TOKEN = os.environ.get("Discord_Token_Cloud")
BASE_URL = f"https://discord.com/api/v9"
SEND_URL0 = BASE_URL + f"/channels/{os.environ.get("DiscordChanellId1")}/messages" #Canal de prueba
SEND_URL1 = BASE_URL + f"/channels/{os.environ.get("DiscordChanellId5")}/messages"
SEND_URL2 = BASE_URL + f"/channels/{os.environ.get("DiscordChanellId6")}/messages"
SEND_URL3 = BASE_URL + f"/channels/{os.environ.get("DiscordChanellId7")}/messages"

headers = {
    "Authorization": f"Bot {TOKEN}",
    "User-Agent": f"DiscordBot"
}


string_turnos1 = "No hay plazas disponibles para este día."

global count
count = 0
global aciertos
aciertos = 0

def scraper_funcion_V3():
    global count
    global aciertos
    try:
        print(datetime.datetime.now())
        #CREANDO EL DRIVER PARA QUE NO USE GUI, FUNDAMENTAL PARA CLOUD
        s = Service(executable_path)
        options = Options()
        options.set_capability("marionette", False)
        options.binary_location = binary_path
        options.add_argument("--headless")
        options.set_preference('security.sandbox.content.level', '5')
        driver = webdriver.Firefox(service=s, options=options)

        #ACCEDIENDO A LA PAGINA Y ESPERANDO A QUE CARGUE
        driver.get("URL OBJETIVO")
        time.sleep(2)

        #CLICKEANDO PRIMER BOTON
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        acceso = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div/main/div[2]/div/div/div/div/div[2]/button")))
        ActionChains(driver).move_to_element(acceso).click(acceso).perform()

        #SCROLLEANDO Y CONFIRMANDO
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        confirmar = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div/main/div[2]/div/div/div/div/div[3]/div[4]/button")))
        ActionChains(driver).move_to_element(confirmar).click(confirmar).perform()

        #ACEPTANDO CONDICIONES Y CONCERTANDO CITA
        time.sleep(4)
        condiciones = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div/main/div[2]/div/div/div/div/div[3]/div[2]/div[2]/div/div[1]"))) #OJO QUE EL XPATH ES DEL DIV, NO DEL BOTON DEL INPUT
        ActionChains(driver).move_to_element(condiciones).click(condiciones).perform()
        concertando = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div/main/div[2]/div/div/div/div/div[3]/div[2]/div[2]/div/div[2]/button")))
        ActionChains(driver).move_to_element(concertando).click(concertando).perform()

        #ENCONTRANDO TEXTO DE TURNOS
        time.sleep(4)
        driver.execute_script("window.scrollTo(0, 400);")
        time.sleep(1)
        recuadro_turnos = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div/main/div[2]/div/div/div/div/div[3]/div[2]/div[2]/div[1]/p")))
        texto = recuadro_turnos.text
        print(texto)
        if count == 0 or count == 10 or count % 200 == 0:
            requests.post(SEND_URL0, headers=headers, json={"content": "El servicio está siendo utilizado desde cloud"})
        #ENVIANDO ALERTA
        if texto == string_turnos1:
            aciertos = 0
        else:
            #Guardando info de que paso en la pagina cuando aparecieron turnos
            if aciertos == 0:
                with open('page.png', 'wb') as file:
                	file.write(recuadro_turnos.screenshot_as_png)
                with open('source_code.html', 'w') as file2:
                    file2.write(driver.page_source)
            if aciertos < 10: #PONIENDOLE UN LIMITE PARA QUE NO MANDE MIL ALERTAS
                aciertos += 1
                print("TURNOS DISPONIBLES TURNOS DISPONIBLES TURNOS DISPONIBLES TURNOS DISPONIBLES TURNOS DISPONIBLES")
                requests.post(SEND_URL3, headers=headers, json={"content": "TURNOS DISPONIBLES! --> URL OBJETIVO"})
                requests.post(SEND_URL2, headers=headers, json={"content": "TURNOS DISPONIBLES! --> URL OBJETIVO"})
                requests.post(SEND_URL1, headers=headers, json={"content": "TURNOS DISPONIBLES! --> URL OBJETIVO"})
                requests.post(SEND_URL0, headers=headers, json={"content": "EL SCRAPER DE CLOUD ENCONTRO TURNO"})
            else:
                pass
        driver.close()
        count += 1
        return True
    except Exception as e:
        print("ERROR:",e)
        try:
            driver.close()
        except:
            print("ERROR NO PUEDE CERRAR EL DRIVER")
            sys.exit(0)

while True:
    scraper_funcion_V3()
    if scraper_funcion_V3() == True:
        continue
    else:
        continue
