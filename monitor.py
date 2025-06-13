import os
import requests
from bs4 import BeautifulSoup

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_USER_ID = os.getenv('TELEGRAM_USER_ID')

SHOWS_TO_MONITOR = [
    "Буна",
    "Лимерівна",
    "Кассандра",
    "Прометей закутий",
    "Калинова сопілка",
    "Конотопська відьма",
    "Невеличка драма",
    "Гедда Габлер"
]

URLS = {
    "franko": "https://teatrfrankoa.com.ua/afisha/",
    "podol": "https://podoltheatre.kiev.ua/afisha/"
}

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {
        "chat_id": TELEGRAM_USER_ID,
        "text": text,
        "parse_mode": "HTML"
    }
    try:
        response = requests.post(url, data=data)
        if response.status_code != 200:
            print(f"Failed to send message: {response.text}")
    except Exception as e:
        print(f"Exception sending message: {e}")

def check_franko():
    try:
        r = requests.get(URLS["franko"])
        soup = BeautifulSoup(r.text, "html.parser")
        shows = soup.find_all("div", class_="event-item__title")
        found = []
        for show in shows:
            title = show.text.strip()
            for s in SHOWS_TO_MONITOR[:-1]:  # всі окрім Гедди Габлер
                if s.lower() in title.lower():
                    found.append(title)
        return found
    except Exception as e:
        print(f"Error checking Franko theatre: {e}")
        return []

def check_podol():
    try:
        r = requests.get(URLS["podol"])
        soup = BeautifulSoup(r.text, "html.parser")
        shows = soup.find_all("div", class_="afisha-item__title")
        found = []
        for show in shows:
            title = show.text.strip()
            if SHOWS_TO_MONITOR[-1].lower() in title.lower():
                found.append(title)
        return found
    except Exception as e:
        print(f"Error checking Podol theatre: {e}")
        return []

def main():
    franko_found = check_franko()
    podol_found = check_podol()
    messages = []
    if franko_found:
        messages.append("🎭 <b>Вистави у театрі імені Франка:</b>\n" + "\n".join(franko_found))
    if podol_found:
        messages.append("🎭 <b>Вистави у театрі на Подолі:</b>\n" + "\n".join(podol_found))
    if messages:
        send_telegram_message("\n\n".join(messages))
    else:
        print("Нічого не знайдено на сайтах")

if __name__ == "__main__":
    main()
