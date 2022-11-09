from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from PIL import Image
from twocaptcha import TwoCaptcha
import time
import datetime
import requests
import os
import sys

base_dir = os.getcwd()
executable_path = os.path.join(base_dir, "geckodriver.exe")


#DEFINIENDO CANALES PARA ENVIAR MENSAJE DISCORD
TOKEN = os.environ["Discord_Token"]
BASE_URL = f"https://discord.com/api/v9"
SEND_URL0 = BASE_URL + f"/channels/{os.environ["DiscordChanellId1"]}/messages" #Canal de prueba
SEND_URL1 = BASE_URL + f"/channels/{os.environ["DiscordChanellId2"]}/messages" #Canal a traves del que se envian alertas

headers = {
    "Authorization": f"Bot {TOKEN}",
    "User-Agent": f"DiscordBot"
}


string_turnos = "" #Eliminado por privacidad, era una string que alertaba cuando habia turnos disponibles.
#No hay turnos disponibles.

headers_mozilla = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36"

#TWOCAPTCHA API KEY
two_capcha_key = os.environ["two_captcha_key"]

#Seteando variables para que cuenten la performance de la API. (en promedio 1/3 de los captchas resueltos son erroneos)
global aciertos
aciertos = 0
global fallas
fallas = 0
global captcha_erroneo
captcha_erroneo = 0
global count
count = 0

def timer():
    global a
    b = datetime.datetime.now()
    c = b-a
    print("Finalizado en:", c)
    time.sleep(2)

def scraper_p():
    global a
    global aciertos
    global fallas
    global captcha_erroneo
    global count
    try:
        #CREANDO EL DRIVER
        a = datetime.datetime.now()
        s = Service(executable_path)
        options = Options()
        options.set_preference('security.sandbox.content.level', '5')
        options.set_preference('general.useragent.override', headers_mozilla)
        options.add_argument("--headless")
        options.set_capability("marionette", False)
        driver = webdriver.Firefox(service=s, options=options)

        #ACCEDIENDO A LA PAGINA Y ESPERANDO A QUE CARGUE
        driver.get("URL OBJETIVO")
        time.sleep(10) #5

        #ELIGIENDO TRAMITE
        Rodzaj = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "mat-select-value-3")))
        ActionChains(driver).move_to_element(Rodzaj).click(Rodzaj).perform()
        time.sleep(10)
        paszportowe = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[4]/div[2]/div/div/div/mat-option/span")))
        ActionChains(driver).move_to_element(paszportowe).click(paszportowe).perform()
        time.sleep(1)

        #ELIGIENDO PARA UNA PERSONA
        Chcę = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "mat-select-value-5")))
        ActionChains(driver).move_to_element(Chcę).click(Chcę).perform()
        time.sleep(1)
        un_osob = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[4]/div[2]/div/div/div/mat-option[1]/span")))
        ActionChains(driver).move_to_element(un_osob).click(un_osob).perform()
        time.sleep(1)

        #SCROLLEANDO
        driver.execute_script("window.scrollTo(0, 300);")
        time.sleep(1)

        #BYPASSEANDO CAPTCHA BYPASSEANDO CAPTCHA
        #Extrayendo Imagen
        captcha_img = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/app-root/app-home-layout/div[1]/main/div/div/app-dashboard/app-institutions/app-institutions/app-passport-matters/div/app-passport-appointment-reservation/app-passport-appointment-reservation-form/div/app-captcha/app-ultimate-captcha/div/div[2]/img")))
        src = captcha_img.get_attribute('src')
        with open('captcha.png', 'wb') as file:
        		file.write(captcha_img.screenshot_as_png) #DONDE QUEDA?
        time.sleep(1)
        captcha_path = os.path.join(base_dir, "captcha.png")
        driver.execute_script("window.scrollTo(0, 300);")
        time.sleep(1)
        #Enviandola para resolverla
        solver = TwoCaptcha(two_capcha_key)
        captcha = solver.normal(captcha_path, minLength=4, maxLength=4, regsense=1)
        print(captcha)
        #Insertando respuesta
        respuesta = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "mat-input-0")))
        respuesta.send_keys(captcha['code'])
        time.sleep(3)

        #CLICKEANDO PARA RESERVAR CITA
        boton_derecha = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/app-root/app-home-layout/div[1]/main/div/div/app-dashboard/app-institutions/app-institutions/app-passport-matters/div/app-passport-appointment-reservation/app-passport-appointment-reservation-form/div/app-captcha/div/div[2]/app-button-control/button/span[1]")))
        ActionChains(driver).move_to_element(boton_derecha).click(boton_derecha).perform()
        #MANDANDO AVISO DE QUE ESTA FUNCIONANDO BIEN EL SCRAPER POR WHATSAPP
        if count == 0 or count == 10 or count % 120 == 0:
            requests.get("https://api.callmebot.com/whatsapp.php?phone=+&text=Scraper%20Funcionando%20Correctamente&apikey=")
            #Numero telefonico personal y api key eliminados.

        #VIENDO SI EL CAPTCHA ESTABA BIEN O MAL Y EN CASO DE ESTAR BIEN, QUE STRING ME DEVUELVE LA PAGINA
        try:
            resultado = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/app-root/app-home-layout/div[1]/main/div/div/app-dashboard/app-institutions/app-institutions/app-passport-matters/div/app-passport-appointment-reservation/app-passport-appointment-reservation-form/div/div[4]")))
            texto_resultado = resultado.text
            aciertos += 1
            print("GOOD CAPTCHA:", aciertos)
        except Exception as e:
            captcha_erroneo += 1
            print("BAD CAPTCHA:", captcha_erroneo)
            requests.get(f"http://2captcha.com/res.php?key={two_capcha_key}&amp;action=reportbad&amp;id={captcha['captchaId']}")
            timer()
            count += 1
            driver.close()
            return False

        #ANALIZANDO STRING Y ENVIANDO ALERTA
        if texto_resultado == string_turnos:
            pass
        else:
            print(texto_resultado)
            print(datetime.datetime.now())
            requests.get("https://api.callmebot.com/whatsapp.php?phone=+&text=TURNOS%20DISPONIBLES&apikey=")
            #Numero telefonico de cliente y api key eliminados
            print("TURNOS DISPONIBLES TURNOS DISPONIBLES TURNOS DISPONIBLES TURNOS DISPONIBLES TURNOS DISPONIBLES TURNOS DISPONIBLES TURNOS DISPONIBLES TURNOS DISPONIBLES TURNOS DISPONIBLES TURNOS DISPONIBLES")
            requests.post(SEND_URL1, headers=headers, json={"content": "TURNOS DISPONIBLES --> URL OBJETIVO"})
        timer()
        count += 1
        driver.close()
        return True
    except Exception as e:
        count += 1
        fallas += 1
        print("ERROR:", fallas)
        print(e)
        timer()
        try:
            driver.close()
        except:
            sys.exit(1)
        return False

while True:
    scraper_p()
    if scraper_p() == True:
        continue
    else:
        continue
