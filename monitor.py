
import requests
import os
import re
from bs4 import BeautifulSoup
import time

# Вистави для моніторингу
TARGET_SHOWS = [
    "Буна",
    "Лимерівна",
    "Кассандра",
    "Прометей закутий",
    "Калинова сопілка",
    "Конотопська відьма",
    "Невеличка драма",
    "Гедда Габлер"
]

# Телеграм
TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
TELEGRAM_USER_ID = os.environ["TELEGRAM_USER_ID"]
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

def send_telegram(message):
    data = {"chat_id": TELEGRAM_USER_ID, "text": message}
    requests.post(TELEGRAM_API_URL, data=data)

def check_franko():
    url = "https://sales.ft.org.ua/"
    r = requests.get(url, timeout=10)
    soup = BeautifulSoup(r.text, "html.parser")
    page_text = soup.get_text()
    found = []
    for show in TARGET_SHOWS:
        if show.lower() in page_text.lower():
            found.append(show)
    return found

def check_podil():
    url = "https://teatrpodol.com/afisha/"
    r = requests.get(url, timeout=10)
    soup = BeautifulSoup(r.text, "html.parser")
    page_text = soup.get_text()
    found = []
    for show in TARGET_SHOWS:
        if show.lower() in page_text.lower():
            found.append(show)
    return found

def main():
    found_franko = check_franko()
    found_podil = check_podil()
    message = ""
    if found_franko:
        message += f"🎭 Театр Франка: {', '.join(found_franko)}\n"
    if found_podil:
        message += f"🎭 Театр на Подолі: {', '.join(found_podil)}\n"
    if message:
        send_telegram("Знайдено квитки:\n" + message)

if __name__ == "__main__":
    main()
