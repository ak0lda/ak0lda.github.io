"""
Карточки проектов для бирж (Kwork, FL.ru, Upwork, Habr Freelance).

Собирает HTML-шаблон для каждого проекта и языка и снимает PNG через headless Edge.
Запуск из корня репозитория:  python marketing/cards/build.py
Размер меняется в WIDTH / HEIGHT (по умолчанию 4:3, 1600×1200).
Когда появится логотип, замените BRAND_HTML на <img src="...">.
"""

import html
import pathlib
import subprocess

WIDTH, HEIGHT = 1600, 1200
HERE = pathlib.Path(__file__).resolve().parent
BUILD = HERE / "build"
OUT = HERE / "out"
EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

# Единственное место со знаком бренда: при смене логотипа правится только эта строка.
BRAND_HTML = '<span class="brand">REF_DEV</span>'
SITE = "ak0lda.github.io"

# Цвета — только токены из tailwind.config.js
TOKENS = {
    "background": "#141313",
    "surface-container-lowest": "#0f0e0e",
    "surface-container-low": "#1c1b1b",
    "surface-container-high": "#2b2a2a",
    "surface-bright": "#3a3939",
    "on-surface": "#e6e1e1",
    "on-surface-variant": "#e3bfb3",
    "electric-orange": "#ff5f1f",
    "stroke-soft": "#3a3939",
}

# Только факты со страницы /work/ (RU) и /en/work/ (EN).
PROJECTS = [
    {
        "slug": "01-seo-platform",
        "num": "01",
        "stack": ["TypeScript", "Electron", "React", "SQLite"],
        "ru": {
            "kind": "Desktop-приложение · Windows",
            "title": "AI Search & SEO Platform",
            "lead": "Технический SEO-аудит и проверка видимости в AI-поиске. Данные остаются на компьютере пользователя.",
            "metrics": [("~130K", "строк TypeScript"), ("64", "правила SEO-аудита"), ("668", "тестов")],
        },
        "en": {
            "kind": "Desktop app · Windows",
            "title": "AI Search & SEO Platform",
            "lead": "Technical SEO audits and AI-search visibility checks. All data stays on the user's computer.",
            "metrics": [("~130K", "lines of TypeScript"), ("64", "SEO audit rules"), ("668", "tests")],
        },
    },
    {
        "slug": "02-payment-bot",
        "num": "02",
        "stack": ["TypeScript", "grammY", "Fastify", "PostgreSQL"],
        "ru": {
            "kind": "Telegram-бот + Mini App",
            "title": "Бот для оплаты зарубежных сервисов",
            "lead": "Заявки на оплату, расчёт по курсу ЦБ, балансы и подписки. Данные карт бот не хранит.",
            "metrics": [("Mini App", "React в Telegram"), ("AES-256", "шифрование кодов"), ("Ежедневно", "бэкапы с проверкой")],
        },
        "en": {
            "kind": "Telegram bot + Mini App",
            "title": "Foreign Services Payment Bot",
            "lead": "Payment requests, CBR-rate pricing, balances and subscriptions. The bot never stores card data.",
            "metrics": [("Mini App", "React inside Telegram"), ("AES-256", "encrypted codes"), ("Daily", "verified backups")],
        },
    },
    {
        "slug": "03-lead-intelligence",
        "num": "03",
        "stack": ["Next.js", "TypeScript", "Prisma", "grammY"],
        "ru": {
            "kind": "Сбор и скоринг лидов",
            "title": "Lead Intelligence System",
            "lead": "Круглосуточный сбор, фильтрация и уведомления о лидах из закрытых и публичных источников.",
            "metrics": [("−72%", "RAM на парсинге"), ("0%", "потерянных лидов"), ("−65%", "шума в уведомлениях")],
        },
        "en": {
            "kind": "Lead collection & scoring",
            "title": "Lead Intelligence System",
            "lead": "24/7 collection, filtering and notifications for leads from private and public sources.",
            "metrics": [("−72%", "RAM on scraping"), ("0%", "lost leads"), ("−65%", "notification noise")],
        },
    },
    {
        "slug": "04-payroll",
        "num": "04",
        "stack": ["Node.js", "Express", "MongoDB", "Vanilla JS"],
        "ru": {
            "kind": "Веб-приложение · финансы",
            "title": "Payroll Automation Engine",
            "lead": "Расчёт зарплат для малого производства с динамическими тарифными сетками и налогами.",
            "metrics": [("RBAC", "доступ по ролям"), ("< 18 КБ", "фронтенд без фреймворков"), ("Снапшоты", "история расчётов")],
        },
        "en": {
            "kind": "Web app · finance",
            "title": "Payroll Automation Engine",
            "lead": "Payroll for small manufacturers with dynamic pay scales and taxes.",
            "metrics": [("RBAC", "role-based access"), ("< 18 KB", "framework-free frontend"), ("Snapshots", "payroll history")],
        },
    },
]

LABELS = {"ru": {"project": "Проект", "role": "Fullstack"}, "en": {"project": "Project", "role": "Full-stack"}}

CSS = """
:root { %(vars)s }
* { box-sizing: border-box; margin: 0; padding: 0; }
html, body { width: %(w)spx; height: %(h)spx; overflow: hidden; }
body {
  background-color: var(--background);
  background-image:
    linear-gradient(rgb(58 57 57 / 0.35) 1px, transparent 1px),
    linear-gradient(90deg, rgb(58 57 57 / 0.35) 1px, transparent 1px);
  background-size: 50px 50px;
  background-position: -1px -1px;
  color: var(--on-surface);
  font-family: Inter, system-ui, sans-serif;
  -webkit-font-smoothing: antialiased;
  display: grid; place-items: center;
}
/* Рамка выходит за безопасную зону, содержимое — внутри центрального квадрата 1200×1200 */
.frame {
  position: relative;
  width: calc(100%% - 160px); height: calc(100%% - 160px);
  background: var(--surface-container-low);
  border: 1px solid var(--stroke-soft);
  border-radius: 8px;
  padding: 72px 120px;
  display: flex; flex-direction: column; gap: 44px;
}
.top { display: flex; justify-content: space-between; align-items: center; }
.brand {
  font-family: "JetBrains Mono", ui-monospace, monospace; font-weight: 700;
  font-size: 30px; letter-spacing: 0.05em; color: var(--electric-orange);
  border: 2px solid var(--stroke-soft); border-radius: 4px; padding: 12px 22px;
}
.sys {
  font-family: "JetBrains Mono", ui-monospace, monospace; font-weight: 700;
  font-size: 22px; letter-spacing: 0.1em; color: var(--on-surface-variant);
  background: var(--surface-bright); border-radius: 4px; padding: 8px 14px;
}
.head { display: flex; flex-direction: column; gap: 28px; }
.eyebrow {
  display: flex; align-items: center; gap: 16px;
  font-family: "JetBrains Mono", ui-monospace, monospace; font-weight: 700;
  font-size: 24px; letter-spacing: 0.1em; text-transform: uppercase; color: var(--electric-orange);
}
.dot { width: 12px; height: 12px; border-radius: 50%%; background: var(--electric-orange); flex-shrink: 0; }
h1 {
  font-family: Manrope, system-ui, sans-serif; font-weight: 800;
  font-size: 96px; line-height: 1.0; letter-spacing: -0.005em; text-transform: uppercase;
  text-wrap: balance; color: var(--on-surface);
}
.lead {
  border-left: 3px solid var(--electric-orange); padding-left: 28px;
  font-size: 32px; line-height: 1.4; color: var(--on-surface-variant); max-width: 30em;
}
.metrics {
  display: grid; grid-template-columns: repeat(3, 1fr); gap: 1px;
  background: var(--stroke-soft); border: 1px solid var(--stroke-soft); border-radius: 4px; overflow: hidden;
}
.metric { background: var(--background); padding: 26px 28px; display: flex; flex-direction: column; gap: 14px; }
.metric b {
  font-family: Manrope, system-ui, sans-serif; font-weight: 800; font-size: 54px; line-height: 1;
  color: var(--on-surface); white-space: nowrap;
}
.metric:last-child b { color: var(--electric-orange); }
.metric span {
  font-family: "JetBrains Mono", ui-monospace, monospace; font-weight: 500;
  font-size: 20px; letter-spacing: 0.05em; text-transform: uppercase; color: var(--on-surface-variant); line-height: 1.3;
}
.foot { margin-top: auto; display: flex; justify-content: space-between; align-items: center; gap: 24px; }
.chips { display: flex; flex-wrap: wrap; gap: 12px; }
.chip {
  font-family: "JetBrains Mono", ui-monospace, monospace; font-weight: 700; font-size: 22px; letter-spacing: 0.05em;
  color: var(--on-surface); background: var(--surface-container-high);
  border: 1px solid var(--stroke-soft); border-radius: 4px; padding: 10px 18px;
}
.site {
  display: flex; align-items: center; gap: 14px; white-space: nowrap;
  font-family: "JetBrains Mono", ui-monospace, monospace; font-weight: 500; font-size: 24px; color: var(--on-surface);
}
"""

FONTS = (
    '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500&'
    'family=JetBrains+Mono:wght@500;700&family=Manrope:wght@800&display=block" rel="stylesheet">'
)


def card_html(p, lang):
    t = p[lang]
    e = html.escape
    vars_ = " ".join(f"--{k}: {v};" for k, v in TOKENS.items())
    metrics = "".join(f"<div class='metric'><b>{e(v)}</b><span>{e(l)}</span></div>" for v, l in t["metrics"])
    chips = "".join(f"<span class='chip'>{e(s)}</span>" for s in p["stack"])
    return f"""<!doctype html>
<html lang="{lang}"><head><meta charset="utf-8">{FONTS}
<style>{CSS % {"vars": vars_, "w": WIDTH, "h": HEIGHT}}</style></head>
<body><div class="frame">
  <div class="top">{BRAND_HTML}<span class="sys">SYS.{p["num"]}</span></div>
  <div class="head">
    <p class="eyebrow"><span class="dot"></span>{LABELS[lang]["project"]} // {p["num"]} · {e(t["kind"])}</p>
    <h1>{e(t["title"])}</h1>
    <p class="lead">{e(t["lead"])}</p>
  </div>
  <div class="metrics">{metrics}</div>
  <div class="foot">
    <div class="chips">{chips}</div>
    <div class="site"><span class="dot"></span>{SITE}</div>
  </div>
</div></body></html>"""


def main():
    BUILD.mkdir(exist_ok=True)
    OUT.mkdir(exist_ok=True)
    for p in PROJECTS:
        for lang in ("ru", "en"):
            name = f"{p['slug']}-{lang}"
            src = BUILD / f"{name}.html"
            src.write_text(card_html(p, lang), encoding="utf-8")
            png = OUT / f"{name}.png"
            subprocess.run(
                [EDGE, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=1",
                 f"--window-size={WIDTH},{HEIGHT}", "--virtual-time-budget=10000",
                 f"--screenshot={png}", src.as_uri()],
                check=True, capture_output=True,
            )
            print(png.relative_to(HERE.parent.parent))


if __name__ == "__main__":
    main()
