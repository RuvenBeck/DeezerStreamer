import random
import time
import selenium
from multiprocessing import Value
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC, wait
import threading
import queue
from pyfiglet import Figlet
from colorama import Fore, Back, Style
import customtkinter
import json
import requests
import re

custom_fig = Figlet(font="graffiti")
print(custom_fig.renderText("DeezerFreezer"))
print(
    rf"""{Fore.RED}                                                      v1
                                                    by RuvenBeck   
{Style.RESET_ALL}
"""
)


lock = threading.Lock()


with open("proxies.txt", "r") as f:
    proxies = f.read().splitlines()


chrome_options = Options()
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument("--disable-webrtc")
chrome_options.add_argument("--start-maximized")


with open("Playlist.txt", "r") as p:
    playlist_urls = p.readlines()
    random.shuffle(playlist_urls)

gesamte_streams = 0


def worker(
    q,
    chrome_options,
):
    while True:
        global gesamte_streams
        line = q.get()
        if line is None:
            break
        parts = line.split(":", 1)
        email = parts[0]
        password = parts[1].strip()
        random_proxy = random.choice(proxies)
        chrome_options.add_argument("--proxy-server=%s" % random_proxy)
        print("Email:", email, "Password:", password, "Proxy:", random_proxy)
        # Hier können weitere Aktionen mit der E-Mail und dem Passwort durchgeführt werden

        chrome_driver_path = (
            "C:/Coding/Python/Music-Streaming/Deezer Bot/chromedriver.exe"
        )
        driver = webdriver.Chrome(
            executable_path=chrome_driver_path, options=chrome_options
        )
        driver.get("https://www.deezer.com/de/login")

        # Cookies ablehnen
        try:
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "gdpr-btn-refuse-all"))
            ).click()
        except:
            pass

        # Login
        WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.ID, "login_mail"))
        ).send_keys(email)
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "login_password"))
        ).send_keys(password)
        WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.ID, "login_form_submit"))
        ).click()

        # Falls login nicht funktioniert
        error_message = driver.find_element(By.CSS_SELECTOR, "#login_error")
        if error_message.is_displayed():
            WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((By.ID, "login_mail"))
            ).clear()
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "login_password"))
            ).clear()

            WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((By.ID, "login_mail"))
            ).send_keys(email)
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "login_password"))
            ).send_keys(password)
            WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.ID, "login_form_submit"))
            ).click()
        else:
            pass

        time.sleep(3)

        # Time for recaptcha
        try:
            captchawait = WebDriverWait(driver, 100).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#modal-close"))
            )
        except:
            pass

        # Playlist auswählen
        playlist_url = random.choice(playlist_urls)
        driver.get(playlist_url)

        # Deezer Free Popup
        try:
            WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "#modal-close"))
            ).click()
        except:
            pass

        # Cookies ablehnen
        try:
            WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.ID, "gdpr-btn-refuse-all"))
            ).click()
        except:
            pass

        # Playlist abspielen
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (
                    By.CSS_SELECTOR,
                    "#page_naboo_playlist > div.catalog-content > div > div._5BJsj > div > div._2yyo6 > div._1k3N9 > div > div:nth-child(1) > button",
                )
            )
        ).click()

        # Loop und Shuffle aktivieren

        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (
                    By.CSS_SELECTOR,
                    "#page_player > div > div.player-options > ul > li:nth-child(1) > ul > li:nth-child(3) > button",
                )
            )
        ).click()
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (
                    By.CSS_SELECTOR,
                    "#page_player > div > div.player-options > ul > li:nth-child(1) > ul > li:nth-child(2) > button",
                )
            )
        ).click()

        if deezerfreeblock == True:
            delete_combination_from_file(line)
        else:
            pass

        # Skip Loop
        while True:
            lock.acquire()
            gesamte_streams += 1
            lock.release()

            WebDriverWait(driver, 1).until(
                EC.element_to_be_clickable(
                    (
                        By.CSS_SELECTOR,
                        "#page_player > div > div.player-controls > ul > li:nth-child(5) > button",
                    )
                )
            ).click()

            title_of_current_song = driver.find_element(
                By.CSS_SELECTOR,
                "#page_player > div > div.player-track > div > div.track-heading > div.track-title > div > div > div > a:nth-child(1)",
            ).text
            if (
                title_of_current_song != "Mehr erfahren"
                or title_of_current_song != "Werbung"
                or title_of_current_song != "Anzeige"
                or title_of_current_song != "Mehr anzeigen"
            ):
                pass

            print(
                f"Die Songs wurden {Fore.GREEN}{gesamte_streams}{Fore.RESET} mal gestreamt!"
            )
            print(f"")
            print(
                f"---------------------------------------------------------------------------"
            )
            print(f"")

            if gesamte_streams == 40000:
                driver.quit()
                break

            start_time = time.time()

            time.sleep(35 + 35 * random.random())

            end_time = time.time()
            duration = end_time - start_time
            rounded_duration = round(duration, 2)

            print(
                f"{Fore.RED}{title_of_current_song}{Fore.RESET} wurde {Fore.MAGENTA}{rounded_duration}{Fore.RESET} Sekunden gespielt."
            )
        q.task_done()


q = queue.Queue()

# Zeilen aus der Textdatei in die Queue einfügen
with open("combos.txt", "r") as file:
    lines = file.readlines()
    random.shuffle(lines)
    for line in lines:
        q.put(line)


with open("combos.txt") as f:
    anzahl_zeilen = sum(1 for line in f)

anzahl_threads = anzahl_zeilen


def deezerfreeblock():
    try:
        deezerfreeblock = WebDriverWait(webdriver, 10).until(
            EC.visibility_of_element_located(
                (
                    By.CSS_SELECTOR,
                    "#dzr-app > div > div.page-alerts.css-0.e3mndjk0 > div > div > div > div.css-1rr4qq7.e3mndjk0 > div.chakra-alert__desc.css-vfhx9v.e3mndjk0 > a",
                )
            )
        )
        # Element is displayed
        return True
    except:
        # Element is not displayed
        return False


def delete_combination_from_file(combination):
    with open("combos.txt", "r") as file:
        lines = file.readlines()

    with open("combos.txt", "w") as file:
        for line in lines:
            if line.strip() != combination.strip():
                file.write(line)
    print(f"{Fore.LIGHTMAGENTA_EX}Incorrect lines was deleted{Fore.RESET}")


# Printing of all the inputs
print(f"{Fore.LIGHTYELLOW_EX}{len(proxies)}{Fore.RESET} Proxies are loaded")
print(f"{Fore.LIGHTYELLOW_EX}{len(playlist_urls)}{Fore.RESET} Playlists are loaded")
print(f"{Fore.LIGHTYELLOW_EX}{len(lines)}{Fore.RESET} Combos are loaded")


# Threads erstellen
threads = []
for i in range(anzahl_threads):
    t = threading.Thread(target=worker, args=(q, chrome_options))
    threads.append(t)
    t.start()
    time.sleep(35)

# Warten, bis alle Zeilen abgearbeitet sind
q.join()

# Alle Threads beenden
for i in range(anzahl_threads):
    q.put(None)
for t in threads:
    t.join()

print(f"Es wurden insgesamt {gesamte_streams} Streams hinzugefügt.")
