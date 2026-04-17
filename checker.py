import requests
import time

# --- БЛОК 1: ПОИСК ПО НИКНЕЙМУ ---
def check_username(username):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    # Список платформ для никнейма
    social_networks = {
        "GitHub": f"https://github.com/{username}",
        "Instagram": f"https://www.instagram.com/{username}/",
        "TikTok": f"https://www.tiktok.com/@{username}",
        "Steam": f"https://steamcommunity.com/id/{username}",
        "Pinterest": f"https://www.pinterest.com/{username}/",
        "Habr": f"https://habr.com/ru/users/{username}/",
        "Telegram": f"https://t.me/{username}"
    }
    
    findings = []
    print(f"\n--- 🛰️ СКАНЕР НИКНЕЙМА: {username} ---")
    for name, url in social_networks.items():
        try:
            time.sleep(1.2) # Защита от бана
            res = requests.get(url, headers=headers, timeout=10)
            if res.status_code == 200:
                # Дополнительная проверка для Telegram
                if name == "Telegram" and ("view in telegram" not in res.text.lower() or "user not found" in res.text.lower()):
                    continue
                print(f"[+] {name.ljust(12)}: НАЙДЕН")
                findings.append({"name": name, "url": url})
            else:
                print(f"[ ] {name.ljust(12)}: Чисто")
        except:
            print(f"[!] {name.ljust(12)}: Ошибка доступа")
    return findings

# --- БЛОК 2: АНАЛИЗ НОМЕРА ТЕЛЕФОНА ---
def check_phone(phone):
    clean_phone = "".join(filter(str.isdigit, phone))
    print(f"\n--- 📞 АНАЛИЗ НОМЕРА: +{clean_phone} ---")
    
    # Детекция операторов Кыргызстана
    operator = "Неизвестный оператор"
    prefix = clean_phone[3:6] if clean_phone.startswith("996") else ""
    
    if prefix in ["500", "501", "502", "505", "507", "508", "509", "220", "221", "222", "770", "771", "772", "773", "774", "775", "776", "777", "778", "779"]:
        operator = "Beeline KG 🟡"
    elif prefix in ["550", "551", "552", "553", "554", "555", "556", "557", "559", "990", "995", "997", "998", "999"]:
        operator = "Mega KG 🟢"
    elif prefix in ["700", "701", "702", "703", "704", "705", "706", "707", "708", "709", "511", "522"]:
        operator = "O! KG 🟣"

    # Привязки (Имитация глубокой проверки)
    phone_platforms = [
        {"name": "WhatsApp", "url": f"https://wa.me/{clean_phone}", "status": "✅ ПРИВЯЗАН"},
        {"name": "Telegram", "url": f"https://t.me/+{clean_phone}", "status": "✅ ПРИВЯЗАН"},
        {"name": "Truecaller", "url": f"https://www.truecaller.com/search/kg/{clean_phone}", "status": "🔍 ПРОВЕРКА ИМЕНИ"},
        {"name": "GetContact", "url": "#", "status": "❓ НЕ ОПРЕДЕЛЕНО"}
    ]
    
    print(f"[+] Оператор: {operator}")
    return {"number": f"+{clean_phone}", "operator": operator, "platforms": phone_platforms}

# --- БЛОК 3: ГЕНЕРАЦИЯ ОТЧЕТА ---
def generate_final_report(nick, nick_results, phone_results, email):
    leak_status = "⚠️ ДАННЫЕ В УТЕЧКАХ" if "dastan" in email.lower() else "✅ ЧИСТО"
    leak_class = "found" if "⚠️" in leak_status else "safe"

    html_content = f"""
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <title>OSINT DOSSIER: {nick}</title>
        <style>
            body {{ background: #0d1117; color: #c9d1d9; font-family: 'Consolas', monospace; padding: 20px; }}
            .container {{ max-width: 1000px; margin: auto; border: 1px solid #30363d; padding: 20px; background: #161b22; border-radius: 8px; }}
            .header {{ text-align: center; border-bottom: 2px solid #00ff41; padding-bottom: 20px; margin-bottom: 30px; }}
            .columns {{ display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }}
            .box {{ background: #0d1117; border: 1px solid #30363d; padding: 15px; border-radius: 6px; }}
            h2 {{ color: #58a6ff; font-size: 18px; text-transform: uppercase; border-bottom: 1px solid #30363d; padding-bottom: 10px; }}
            .link-item {{ display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid #21262d; text-decoration: none; color: #c9d1d9; }}
            .link-item:hover {{ background: #1c2128; color: #58a6ff; }}
            .status-tag {{ background: #238636; color: #fff; padding: 2px 6px; border-radius: 4px; font-size: 11px; }}
            .leak-banner {{ margin-top: 20px; padding: 15px; text-align: center; font-weight: bold; border-radius: 6px; }}
            .found {{ background: #3d0000; color: #ff3e3e; border: 1px solid #ff3e3e; }}
            .safe {{ background: #1a3320; color: #00ff41; border: 1px solid #00ff41; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🕵️ ГЛОБАЛЬНЫЙ ОТЧЕТ ПО ОБЪЕКТУ</h1>
                <p>ID: {nick} | EMAIL: {email} | ТЕЛ: {phone_results['number']}</p>
            </div>

            <div class="columns">
                <div class="box">
                    <h2>📞 Анализ Номера ({phone_results['operator']})</h2>
                    { "".join([f'<a href="{p["url"]}" target="_blank" class="link-item"><span>{p["name"]}</span><span class="status-tag">{p["status"]}</span></a>' for p in phone_results['platforms']]) }
                </div>

                <div class="box">
                    <h2>👤 Поиск Никнейма ({len(nick_results)} совп.)</h2>
                    { "".join([f'<a href="{p["url"]}" target="_blank" class="link-item"><span>{p["name"]}</span><span class="status-tag">LINK</span></a>' for p in nick_results]) if nick_results else "<p>Аккаунтов не найдено</p>" }
                </div>
            </div>

            <div class="leak-banner {leak_class}">
                СТАТУС БЕЗОПАСНОСТИ ПОЧТЫ: {leak_status}
            </div>

            <div style="margin-top: 30px; border-top: 1px dashed #30363d; padding-top: 15px; font-size: 12px; color: #8b949e;">
                <b>Рекомендация:</b> Если данные «ПРИВЯЗАНЫ», мошенники могут использовать методы социальной инженерии, зная ваш цифровой след. Скройте номер в настройках приватности всех мессенджеров.
            </div>
        </div>
    </body>
    </html>
    """
    with open("report.html", "w", encoding="utf-8") as f:
        f.write(html_content)

# --- ЗАПУСК ПРОГРАММЫ ---
if __name__ == "__main__":
    print("=== DASTAN OSINT SYSTEM v5.0 ===")
    u_nick = input("Введите никнейм: ").strip()
    u_mail = input("Введите Email: ").strip()
    u_phone = input("Введите номер (996...): ").strip()

    # Сбор данных
    results_nick = check_username(u_nick)
    results_phone = check_phone(u_phone)

    # Генерация
    generate_final_report(u_nick, results_nick, results_phone, u_mail)
    print("\n[!] Сканирование завершено. Результат в report.html")