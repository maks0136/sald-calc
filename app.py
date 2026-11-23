import io
import streamlit as st
import pandas as pd

st.set_page_config(page_title="OSV CALC — Расчёт сальдо", page_icon="📊", layout="wide", initial_sidebar_state="collapsed")

st.markdown('''
<style>
@import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&display=swap');
html,body,[class*="css"],.stApp {font-family:'Manrope',sans-serif;}
html, body, #root { height: 100%; margin: 0; overflow: hidden; background-color: #f5f6ff; }
[data-testid="stApp"], [data-testid="stAppViewContainer"] { min-height: 0; overflow: hidden; }
[data-testid="stMain"] { min-height: 0; overflow-y: auto; overscroll-behavior-y: contain; }
.stApp {background: radial-gradient(ellipse 50% 28% at 10% 5%,rgba(165,197,255,.40),transparent 75%),radial-gradient(ellipse 45% 35% at 95% 12%,rgba(205,180,255,.37),transparent 75%),linear-gradient(135deg,#f8fbff 0%,#f8f7ff 49%,#f4faff 100%);color:#27304a;}
[data-testid="stHeader"]{background:transparent;}
.block-container{max-width:1150px;padding-top:1.3rem;padding-bottom:2rem;}
h1,h2,h3{color:#232944!important;letter-spacing:-.035em;}
h1{font-size:clamp(2.25rem,5vw,3.75rem)!important;line-height:1.13!important;font-weight:800!important;}
h2{font-size:1.55rem!important;font-weight:800!important;}
h3{font-size:1.1rem!important;}
p{line-height:1.7;}
.osv-topbar{display:flex;align-items:center;justify-content:space-between;gap:16px;padding:15px 20px;border:1px solid rgba(151,161,205,.22);border-radius:20px;background:rgba(255,255,255,.70);box-shadow:0 8px 28px rgba(80,86,144,.05);margin-bottom:35px;}
.osv-brand{display:flex;align-items:center;gap:11px;font-weight:800;font-size:1.02rem;color:#303650;letter-spacing:-.025em;}
.osv-brand-icon{display:inline-flex;align-items:center;justify-content:center;width:36px;height:36px;border-radius:12px;color:white;background:linear-gradient(135deg,#628cff,#8d72ec);font-size:20px;}
.osv-top-center{font-size:.84rem;color:#686b9b;text-align:center;font-weight:600;}
.osv-top-right{font-size:.8rem;color:#777e9a;border:1px solid #e8e9f5;border-radius:30px;padding:7px 12px;background:white;}
.osv-hero{position:relative;padding:12px 0 20px;}
.osv-kicker{display:inline-block;border-radius:99px;padding:8px 14px;background:rgba(116,124,229,.10);color:#6663bd;font-size:.78rem;font-weight:800;letter-spacing:.025em;margin-bottom:16px;}
.osv-lead{font-size:1.08rem;color:#68728b;max-width:680px;line-height:1.75;margin-top:10px;}
.osv-gradient{background:linear-gradient(100deg,#527de4,#9270d6);-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent;}
.osv-formula{display:inline-flex;align-items:center;gap:10px;margin-top:16px;padding:12px 17px;background:rgba(255,255,255,.77);border:1px solid #e8e8f7;border-radius:14px;font-size:.96rem;font-weight:800;color:#555b90;box-shadow:0 8px 25px rgba(90,100,155,.06);}
.osv-illustration{position:relative;min-height:210px;display:flex;align-items:center;justify-content:center;}
.osv-paper{position:absolute;width:190px;padding:22px 18px;border-radius:19px;background:rgba(255,255,255,.91);border:1px solid #e6eafa;box-shadow:0 16px 40px rgba(91,101,158,.12);}
.osv-paper.one{transform:rotate(-9deg) translate(-49px,-3px);}
.osv-paper.two{transform:rotate(8deg) translate(62px,12px);}
.osv-paper-title{font-weight:800;color:#343c62;font-size:.92rem;margin-bottom:15px;}
.osv-line{height:7px;border-radius:20px;background:#e5e9fa;margin-bottom:10px;}
.osv-line.short{width:58%;}.osv-line.mid{width:75%;}
.osv-paper-sum{color:#6a68c4;font-weight:800;font-size:.86rem;margin-top:16px;}
.osv-float{position:absolute;z-index:3;top:50%;left:50%;transform:translate(-50%,-50%);background:linear-gradient(135deg,#648bfa,#9a78e7);color:white;border-radius:15px;padding:12px 17px;box-shadow:0 12px 30px rgba(107,112,222,.25);font-size:1.5rem;font-weight:800;}
.osv-feature{height:100%;background:rgba(255,255,255,.78);border:1px solid rgba(185,192,231,.40);border-radius:20px;padding:20px 20px 18px;box-shadow:0 8px 24px rgba(90,103,160,.045);}
.osv-feature-icon{font-size:1.5rem;margin-bottom:10px;}.osv-feature-title{font-weight:800;color:#343956;font-size:.96rem;margin-bottom:7px;}.osv-feature-desc{font-size:.84rem;color:#788099;line-height:1.6;}
.osv-section-head{margin-top:35px;margin-bottom:6px;font-size:1.48rem;font-weight:800;color:#303653;letter-spacing:-.035em;}.osv-section-sub{color:#7c849a;font-size:.92rem;margin-bottom:20px;}
[data-testid="stFileUploader"]{background:rgba(255,255,255,.83);border:1px solid #e2e7f6;border-radius:18px;padding:13px 15px;box-shadow:0 8px 24px rgba(84,94,151,.045);}
[data-testid="stFileUploader"] section{background:rgba(244,246,255,.65);border:1.5px dashed #bfc9ee;border-radius:12px;}
[data-testid="stFileUploader"] label{color:#3b4364;font-weight:750;}
.stButton>button[kind="primary"]{background:linear-gradient(105deg,#5b84ee,#9670dc)!important;color:white!important;border:0!important;border-radius:13px!important;padding:.75rem 1.2rem!important;font-weight:800!important;box-shadow:0 10px 24px rgba(106,112,221,.18);transition:transform .2s ease,box-shadow .2s ease;}
.stButton>button[kind="primary"]:hover{transform:translateY(-2px);box-shadow:0 14px 27px rgba(106,112,221,.25);}
[data-testid="stMetric"]{background:rgba(255,255,255,.88);border:1px solid #e5e9f7;border-radius:17px;padding:17px 18px;box-shadow:0 6px 24px rgba(92,100,155,.05);}
[data-testid="stMetricLabel"]{color:#737d96;font-weight:650;}
[data-testid="stMetricValue"]{color:#343b65;font-size:1.5rem;font-weight:800;}
[data-testid="stDataFrame"]{border-radius:14px;overflow:hidden;}
[data-testid="stExpander"]{border:1px solid #e4e7f5;background:rgba(255,255,255,.72);border-radius:15px;}
[data-testid="stDownloadButton"] button{border:1px solid #8b8be0;background:white;color:#5e62b5;border-radius:12px;font-weight:800;padding:.6rem 1rem;}
.osv-foot{margin-top:50px;padding:22px 10px;border-top:1px solid #e3e7f3;text-align:center;color:#858ca4;font-size:.82rem;line-height:1.9;}
@media(max-width:700px){.osv-top-center{display:none}.osv-topbar{padding:12px}.osv-illustration{min-height:190px}.osv-paper{width:155px;padding:16px}.osv-paper.one{transform:rotate(-9deg) translate(-37px,0)}.osv-paper.two{transform:rotate(8deg) translate(43px,10px)}.block-container{padding-top:.7rem}}
</style>
''', unsafe_allow_html=True)

from contextlib import closing
import logging
import os
from pathlib import Path
import sqlite3



COUNTER_PATH = Path(os.getenv("OSV_COUNTER_DB", str(Path(__file__).with_name("osv_counter.sqlite3"))))
logger = logging.getLogger(__name__)


def report_total(*, increment=False):
    """При increment=True регистрирует один успешно сформированный отчёт."""
    try:
        with closing(sqlite3.connect(COUNTER_PATH, timeout=5)) as connection, connection:
            connection.execute("""
                CREATE TABLE IF NOT EXISTS report_stats (
                    id INTEGER PRIMARY KEY CHECK (id = 1),
                    total INTEGER NOT NULL
                )
            """)
            if increment:
                connection.execute("""
                    INSERT INTO report_stats (id, total) VALUES (1, 1)
                    ON CONFLICT (id) DO UPDATE SET total = total + 1
                """)
            result = connection.execute("SELECT total FROM report_stats WHERE id = 1").fetchone()
            return result[0] if result else 0
    except sqlite3.Error:
        logger.exception("Не удалось прочитать или обновить счётчик OSV CALC")
        return None


def show_background():
    st.markdown("""<style>
.stApp { isolation: isolate; }
.osv-paper-stage {
    position: fixed;
    inset: 0;
    overflow: hidden;
    z-index: -1;
    pointer-events: none;
  }
  .osv-floating-paper {
    position: absolute;
    box-sizing: border-box;
    width: calc(clamp(90px, 15vw, 145px) * var(--paper-size, 1));
    height: calc(clamp(116px, 18vw, 178px) * var(--paper-size, 1));
    padding: 11px 9px;
    border: 1px solid light-dark(#8366b268, #c9adf66b);
    border-radius: 10px;
    color: light-dark(#695190, #d5bdf7);
    background: light-dark(#fff7, #b28ce31b);
    box-shadow: 0 10px 26px light-dark(#65568d24, #120a2570);
    font-size: 10px;
    font-weight: 720;
    letter-spacing: .08em;
    opacity: var(--paper-opacity, .95);
    animation: sverka-paper-float var(--paper-duration) ease-in-out infinite alternate;
  }
  .osv-floating-paper span {
    display: block;
    height: 1px;
    margin-top: 12px;
    background: currentColor;
    opacity: .36;
  }
  .osv-floating-paper span:last-child { width: 57%; }
  .paper-act {
    left: -10px; top: 20%;
    --paper-duration: 12s; --tilt-start: -17deg; --tilt-end: -4deg; --rise: -64px; --bend: 15px; --drift: 34px;
    animation-delay: -3s;
  }
  .paper-invoice {
    right: 0; top: 13%;
    --paper-duration: 14s; --tilt-start: 9deg; --tilt-end: 22deg; --rise: 63px; --bend: -13px; --drift: 24px;
    animation-delay: -11s;
  }
  .paper-delivery {
    right: -13px; bottom: -6%;
    --paper-duration: 11s; --tilt-start: 15deg; --tilt-end: -6deg; --rise: -64px; --bend: -20px; --drift: 12px;
    animation-delay: -4s;
  }
  .paper-payment {
    left: -15px; top: 47%;
    --paper-size: .8; --paper-opacity: .68;
    --paper-duration: 15s; --tilt-start: 12deg; --tilt-end: -18deg; --rise: 58px; --bend: 27px; --drift: -12px;
    animation-delay: -9s;
  }
  .paper-statement {
    right: -10px; top: 46%;
    --paper-size: .92; --paper-opacity: .78;
    --paper-duration: 13s; --tilt-start: -15deg; --tilt-end: 5deg; --rise: -52px; --bend: 16px; --drift: -28px;
    animation-delay: -8s;
  }
  .paper-register {
    left: 2%; bottom: -12%;
    --paper-size: .86; --paper-opacity: .88;
    --paper-duration: 16s; --tilt-start: -20deg; --tilt-end: -3deg; --rise: -74px; --bend: -15px; --drift: 24px;
    animation-delay: -13s;
  }
  .paper-invoice-copy {
    left: 20%; top: -13%;
    --paper-size: .75; --paper-opacity: .6;
    --paper-duration: 13s; --tilt-start: 20deg; --tilt-end: 5deg; --rise: 39px; --bend: 25px; --drift: 68px;
    animation-delay: -9s;
  }
  .paper-act-copy {
    right: 25%; bottom: -15%;
    --paper-size: .78; --paper-opacity: .68;
    --paper-duration: 15s; --tilt-start: -10deg; --tilt-end: 13deg; --rise: -42px; --bend: -17px; --drift: -65px;
    animation-delay: -7s;
  }
  @keyframes sverka-paper-float {
    from { transform: translate(0, 0) rotate(var(--tilt-start)); }
    48% { transform: translate(var(--bend), calc(var(--rise) * .52)) rotate(calc(var(--tilt-start) * .6)); }
    to { transform: translate(var(--drift), var(--rise)) rotate(var(--tilt-end)); }
  }
.osv-report-count {
  display: flex; align-items: baseline; justify-content: flex-end; gap: 8px;
  padding: 4px 0 8px; color: inherit; font-size: .85rem;
}
.osv-report-count strong { color: light-dark(#5746b8, #c6b9ff); font-size: 1.14rem; font-variant-numeric: tabular-nums; }
@media (prefers-reduced-motion: reduce) {
  .osv-floating-paper { animation: none; transform: rotate(var(--tilt-start)); }
}
</style>
<div class="osv-paper-stage" aria-hidden="true">
  <div class="osv-floating-paper paper-act">ОСВ 62.01<span></span><span></span><span></span><span></span></div>
  <div class="osv-floating-paper paper-invoice">ОСВ 62.02<span></span><span></span><span></span><span></span></div>
  <div class="osv-floating-paper paper-delivery">ВЕДОМОСТЬ<span></span><span></span><span></span><span></span></div>
  <div class="osv-floating-paper paper-payment">ДЕБЕТ<span></span><span></span><span></span></div>
  <div class="osv-floating-paper paper-statement">КРЕДИТ<span></span><span></span><span></span><span></span></div>
  <div class="osv-floating-paper paper-register">ОТЧЁТ EXCEL<span></span><span></span><span></span><span></span></div>
  <div class="osv-floating-paper paper-invoice-copy">ОСВ 62.02<span></span><span></span><span></span><span></span></div>
  <div class="osv-floating-paper paper-act-copy">ОСВ 62.01<span></span><span></span><span></span><span></span></div>
</div>
""", unsafe_allow_html=True)


show_background()

# ---------- Исходные функции чтения и расчёта (сохранены) ----------
def detect_account(file):
    try:
        df_raw = pd.read_excel(file, header=None, nrows=10)
    except Exception:
        return None
    for _, row in df_raw.iterrows():
        for val in row:
            if isinstance(val, str):
                if "62.01" in val:
                    return "62.01"
                if "62.02" in val:
                    return "62.02"
    return None


def find_header_row(df_raw, search_string="Контрагенты"):
    for i, row in df_raw.iterrows():
        for val in row:
            if isinstance(val, str) and search_string.lower() in val.lower():
                return i
    return None


def parse_osv(file, sum_col_index, account_name):
    try:
        df_raw = pd.read_excel(file, header=None)
    except Exception as e:
        st.error(f"Ошибка чтения файла {account_name}: {e}")
        return None

    header_row = find_header_row(df_raw, "Контрагенты")
    if header_row is None:
        st.error(f"В файле {account_name} не найден заголовок с 'Контрагенты'")
        st.write("Первые 15 строк файла (для диагностики):")
        st.dataframe(df_raw.head(15))
        return None

    header_values = df_raw.iloc[header_row]
    col_contractor = None
    for idx, val in enumerate(header_values):
        if isinstance(val, str) and "контрагенты" in val.lower():
            col_contractor = idx
            break
    if col_contractor is None:
        col_contractor = 1

    data = []
    for i in range(header_row + 1, len(df_raw)):
        row = df_raw.iloc[i]
        if pd.isna(row[col_contractor]) or str(row[col_contractor]).strip() == "":
            continue
        if isinstance(row[col_contractor], str) and row[col_contractor].strip() in ("Итого", "Итого:", "ИТОГО"):
            continue
        if not pd.isna(row[0]) and isinstance(row[0], str) and ("62.01" in row[0] or "62.02" in row[0]):
            continue

        contractor = str(row[col_contractor]).strip()
        amount = row[sum_col_index]
        if pd.isna(amount):
            amount = 0.0
        else:
            try:
                amount = float(amount)
            except Exception:
                amount = 0.0
        data.append([contractor, amount])

    if not data:
        st.warning(f"В файле {account_name} не найдено данных после заголовка.")
        return pd.DataFrame(columns=["Контрагент", "Сумма"])

    df = pd.DataFrame(data, columns=["Контрагент", "Сумма"])
    df = df.groupby("Контрагент", as_index=False).sum()
    return df


def money(value):
    return f"{value:,.2f}".replace(",", " ").replace(".", ",") + " ₽"


def show_header(total):
    count = "—" if total is None else f"{total:,}".replace(",", " ")
    header_slot.markdown(f'''
<div class="osv-topbar">
  <div class="osv-brand"><span class="osv-brand-icon">∑</span> OSV CALC</div>
  <div class="osv-top-center">Считаем сальдо. Бережём нервные клетки 😎</div>
  <div class="osv-top-right">Ведомостей создано · <strong>{count}</strong></div>
</div>
''', unsafe_allow_html=True)


header_slot = st.empty()
show_header(report_total())

hero_left, hero_right = st.columns([1.5, 1], gap="large", vertical_alignment="center")
with hero_left:
    st.markdown('''
    <div class="osv-hero">
      <span class="osv-kicker">УМНЫЙ ПОМОЩНИК ДЛЯ БУХГАЛТЕРИИ</span>
      <h1>Сальдо сошлось.<br><span class="osv-gradient">Настроение тоже.</span></h1>
      <div class="osv-lead">Загрузите две оборотно-сальдовые ведомости — рассчитаем задолженность и авансы по каждому контрагенту. Без ручного вычитания и бесконечных формул в Excel.</div>
      <div class="osv-formula">62.01 (Дт конечный) &nbsp;−&nbsp; 62.02 (Кт конечный)</div>
    </div>
    ''', unsafe_allow_html=True)
with hero_right:
    st.markdown('''
<style>
  #osv-compact {
    color:#292446; box-sizing:border-box; padding:clamp(10px,3%,22px);
    border:1px solid #e5ddfa; border-radius:19px;
    background:radial-gradient(ellipse at 80% 0%,#e8ddfa,transparent 72%),#f6f3ff;
    font:14px/1.4 system-ui,sans-serif;
  }
  #osv-compact .osv-inputs {
    display:grid; grid-template-columns:minmax(0,1fr) auto minmax(0,1fr);
    gap:clamp(4px,2%,10px); align-items:center;
  }
  #osv-compact .osv-doc {
    min-width:0; padding:clamp(7px,3%,13px); background:#fff;
    border:1px solid #e1d8ef; border-radius:11px; box-shadow:0 4px 12px #48306612;
    animation:osv-doc-glow 6s ease-in-out infinite;
  }
  #osv-compact .osv-doc strong { display:block; font-size:clamp(11px,3cqw,15px); }
  #osv-compact .osv-doc small { display:block; font-size:11px; color:#584c82; }
  #osv-compact .osv-doc-line { display:block; height:4px; width:72%; margin:6px 0; border-radius:4px; background:#e3daf6; }
  #osv-compact .osv-credit .osv-doc-line { background:#ccebdd; }
  #osv-compact .osv-minus { color:#644cc4; font-size:19px; font-weight:750; }
  #osv-compact .osv-path { position:relative; height:37px; }
  #osv-compact .osv-path::before {
    content:""; position:absolute; inset:5px 23% 7px; border:1px solid #d8caef;
    border-top:0; border-radius:0 0 13px 13px;
  }
  #osv-compact .osv-pulse {
    position:absolute; top:3px; left:var(--from); width:8px; height:8px;
    background:var(--color); border-radius:50%; opacity:0;
    animation:osv-transfer-pulse 6s ease-in-out infinite;
  }
  #osv-compact .osv-report {
    display:flex; flex-wrap:wrap; justify-content:center; align-items:center; gap:3px 9px;
    margin:0 auto; width:max-content; max-width:100%; box-sizing:border-box; padding:7px 10px;
    border:1px solid #bae4cf; border-radius:9px; color:#205942; background:#f1fcf6;
    animation:osv-report-ready 6s ease-in-out infinite;
  }
  @keyframes osv-doc-glow { 0%,45%,100%{border-color:#e1d8ef} 20%{border-color:#9d87df} }
  @keyframes osv-transfer-pulse { 0%,13%{left:var(--from);top:3px;opacity:0} 19%{opacity:1} 44%{left:calc(50% - 4px);top:27px;opacity:1} 53%,100%{left:calc(50% - 4px);top:27px;opacity:0} }
  @keyframes osv-report-ready { 0%,45%,100%{opacity:0;transform:translateY(3px)} 55%,85%{opacity:1;transform:translateY(0)} 94%{opacity:0;transform:translateY(3px)} }
  @media (prefers-reduced-motion:reduce) { #osv-compact .osv-doc,#osv-compact .osv-pulse,#osv-compact .osv-report {animation:none} }
</style>
<div id="osv-compact" role="img" aria-label="Пример: ОСВ 62.01 и ОСВ 62.02 образуют отчёт Сальдо.xlsx.">
  <div class="osv-inputs">
    <div class="osv-doc"><strong>ОСВ 62.01</strong><span class="osv-doc-line"></span><small>Дебет конечный</small></div>
    <span class="osv-minus" aria-hidden="true">−</span>
    <div class="osv-doc osv-credit"><strong>ОСВ 62.02</strong><span class="osv-doc-line"></span><small>Кредит конечный</small></div>
  </div>
  <div class="osv-path" aria-hidden="true">
    <span class="osv-pulse" style="--from:23%;--color:#8666d5"></span>
    <span class="osv-pulse" style="--from:74%;--color:#3ba67d"></span>
  </div>
  <div class="osv-report"><strong>✓ Сальдо.xlsx</strong><small>Отчёт готов</small></div>
</div>
''', unsafe_allow_html=True)

features = [
    ("📂", "Два файла — один расчёт", "Загружайте ОСВ по счетам 62.01 и 62.02. Всё остальное посчитаем за вас."),
    ("🧮", "Суммы под контролем", "Сведём данные по контрагентам и покажем, где долг, а где аванс."),
    ("📥", "Результат в Excel", "Готовую таблицу можно скачать и использовать в дальнейшей работе."),
]
cols = st.columns(3, gap="medium")
for col, (ico, title, desc) in zip(cols, features):
    with col:
        st.markdown(f'<div class="osv-feature"><div class="osv-feature-icon">{ico}</div><div class="osv-feature-title">{title}</div><div class="osv-feature-desc">{desc}</div></div>', unsafe_allow_html=True)

st.markdown('<div class="osv-section-head">Загрузите оборотно-сальдовые ведомости</div><div class="osv-section-sub">Два файла, одна кнопка — и никаких танцев с калькулятором.</div>', unsafe_allow_html=True)
def reset_report():
    st.session_state.pop("osv_report", None)


col1, col2 = st.columns(2, gap="medium")
with col1:
    file_62_01 = st.file_uploader("📁 ОСВ по счёту 62.01 — дебет конечный", type=["xlsx", "xls"], key="62_01", on_change=reset_report)
with col2:
    file_62_02 = st.file_uploader("📁 ОСВ по счёту 62.02 — кредит конечный", type=["xlsx", "xls"], key="62_02", on_change=reset_report)

st.caption("Поддерживаются Excel-файлы .xlsx и .xls. Для старых .xls требуется библиотека xlrd.")
calculate = st.button("🧮 Рассчитать сальдо", type="primary", width="stretch")

def calculate_report():
    if file_62_01 is None or file_62_02 is None:
        st.warning("Сначала загрузите оба файла. Даже бухгалтерская магия без них бессильна 🙂")
        return

    account1 = detect_account(file_62_01)
    account2 = detect_account(file_62_02)
    if account1 != "62.01" or account2 != "62.02":
        st.error("Неверный порядок загрузки файлов!")
        st.warning(
            f"Загрузите **62.01** в левое поле, а **62.02** — в правое.\n"
            f"Сейчас: первый файл — **{account1 or 'неизвестно'}**, второй — **{account2 or 'неизвестно'}**."
        )
        return

    with st.spinner("Считаем сальдо и ищем, кто кому должен…"):
        df_01 = parse_osv(file_62_01, sum_col_index=5, account_name="62.01")
        df_02 = parse_osv(file_62_02, sum_col_index=6, account_name="62.02")

    if df_01 is None or df_02 is None:
        return
    if df_01.empty or df_02.empty:
        st.warning("Один из файлов не содержит данных. Проверьте структуру.")
        return

    merged = pd.merge(df_01, df_02, on="Контрагент", how="outer", suffixes=("_62.01", "_62.02"))
    merged.fillna(0, inplace=True)
    merged["Результат"] = merged["Сумма_62.01"] - merged["Сумма_62.02"]

    def get_status(value):
        if value > 0:
            return "Долг клиента"
        elif value < 0:
            return "Аванс/переплата"
        return "0"

    merged["Состояние"] = merged["Результат"].apply(get_status)
    result = merged[["Контрагент", "Сумма_62.01", "Сумма_62.02", "Результат", "Состояние"]]
    result.columns = ["Контрагент", "62.01_Дт_кон", "62.02_Кт_кон", "Результат", "Состояние"]

    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        result.to_excel(writer, index=False, sheet_name="Результат")
    st.session_state["osv_report"] = output.getvalue()
    show_header(report_total(increment=True))


if calculate:
    calculate_report()

if report := st.session_state.get("osv_report"):
    st.success("Отчёт готов")
    st.download_button(
        label="Скачать Excel",
        data=report,
        file_name="result_62.01_minus_62.02.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        on_click="ignore",
        width="stretch",
    )

st.markdown('''
<div class="osv-foot">
  <strong>OSV CALC</strong> · Считаем цифры, а не минуты до конца рабочего дня.<br>
  Расчёт выполняется по данным загруженных файлов. Перед использованием проверьте корректность исходной ОСВ и выбранных колонок.
</div>
''', unsafe_allow_html=True)
