import streamlit as st
import pandas as pd
import io

# ---------- НАСТРОЙКА СТРАНИЦЫ И СТИЛЕЙ ----------
st.set_page_config(page_title="Вычитание сальдо", layout="wide")

st.markdown(
    """
    <style>
    .stApp {
        background-color: #ffe6f0;
    }
    .block-container {
        max-width: 900px;
        margin: 0 auto;
        padding-top: 6rem;
        padding-bottom: 2rem;
    }
    .stButton > button {
        background-color: #ff66b2;
        color: white;
        font-size: 1.2rem;
        font-weight: bold;
        border-radius: 10px;
        padding: 0.5rem 2rem;
        border: none;
        width: 100%;
        transition: 0.3s;
    }
    .stButton > button:hover {
        background-color: #ff3399;
        color: white;
        transform: scale(1.02);
    }
    h1, h2, h3, .stMarkdown {
        text-align: center;
    }
    .stFileUploader > div {
        background-color: rgba(255, 255, 255, 0.5);
        border-radius: 10px;
        padding: 10px;
    }
    .stFileUploader label {
        font-weight: bold;
        color: #4a004a;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------- Функции ----------
def detect_account(file):
    try:
        df_raw = pd.read_excel(file, header=None, nrows=10)
    except:
        return None
    for i, row in df_raw.iterrows():
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
            except:
                amount = 0.0
        data.append([contractor, amount])

    if not data:
        st.warning(f"В файле {account_name} не найдено данных после заголовка.")
        return pd.DataFrame(columns=["Контрагент", "Сумма"])

    df = pd.DataFrame(data, columns=["Контрагент", "Сумма"])
    df = df.groupby("Контрагент", as_index=False).sum()
    return df

# -------------------- ИНТЕРФЕЙС --------------------
st.title("📊 Вычитание сальдо")
st.markdown("### 62.01 (Дт) − 62.02 (Кт)")
st.markdown("#### Загрузите два файла ОСВ и нажмите «Рассчитать».")

col1, col2 = st.columns(2, gap="medium")
with col1:
    file_62_01 = st.file_uploader("📁 ОСВ по счёту 62.01 (Дебет конечный)", type=["xlsx", "xls"], key="62_01")
with col2:
    file_62_02 = st.file_uploader("📁 ОСВ по счёту 62.02 (Кредит конечный)", type=["xlsx", "xls"], key="62_02")

st.markdown("<br>", unsafe_allow_html=True)

if st.button("🧮 Рассчитать", type="primary", use_container_width=True):
    if file_62_01 is None or file_62_02 is None:
        st.warning("⚠️ Пожалуйста, загрузите оба файла перед расчётом.")
        st.stop()

    account1 = detect_account(file_62_01)
    account2 = detect_account(file_62_02)

    if account1 != "62.01" or account2 != "62.02":
        st.error("❌ **Неверный порядок загрузки файлов!**")
        st.warning(
            f"Загрузите **62.01** в левое поле, а **62.02** — в правое.\n"
            f"Сейчас: первый файл — **{account1 or 'неизвестно'}**, второй — **{account2 or 'неизвестно'}**."
        )
        st.stop()

    with st.spinner("Обработка файлов..."):
        df_01 = parse_osv(file_62_01, sum_col_index=5, account_name="62.01")
        df_02 = parse_osv(file_62_02, sum_col_index=6, account_name="62.02")

    if df_01 is None or df_02 is None:
        st.stop()

    if df_01.empty or df_02.empty:
        st.warning("Один из файлов не содержит данных. Проверьте структуру.")
        st.stop()

    st.success("✅ Файлы успешно обработаны!")

    st.header("📂 Считанные данные из файлов")
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("📄 62.01 (Дт конечное)")
        st.write(f"Записей: {len(df_01)}")
        st.dataframe(df_01.style.format({"Сумма": "{:,.2f}"}), height=300)
        st.write(f"**Итого:** {df_01['Сумма'].sum():,.2f}")

    with c2:
        st.subheader("📄 62.02 (Кт конечное)")
        st.write(f"Записей: {len(df_02)}")
        st.dataframe(df_02.style.format({"Сумма": "{:,.2f}"}), height=300)
        st.write(f"**Итого:** {df_02['Сумма'].sum():,.2f}")

    st.header("📊 Результат вычитания (62.01 Дт − 62.02 Кт)")

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

    st.dataframe(
        result.style.format({
            "62.01_Дт_кон": "{:,.2f}",
            "62.02_Кт_кон": "{:,.2f}",
            "Результат": "{:,.2f}"
        }),
        height=400
    )

    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        result.to_excel(writer, index=False, sheet_name="Результат")
    output.seek(0)

    st.download_button(
        label="📥 Скачать результат в Excel",
        data=output,
        file_name="result_62.01_minus_62.02.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True
    )

    st.subheader("📊 Итоговая сводка")
    total_01 = result["62.01_Дт_кон"].sum()
    total_02 = result["62.02_Кт_кон"].sum()
    total_res = result["Результат"].sum()
    col_a, col_b, col_c = st.columns(3)
    col_a.metric("Итого 62.01 Дт", f"{total_01:,.2f}")
    col_b.metric("Итого 62.02 Кт", f"{total_02:,.2f}")
    col_c.metric("Итоговый результат", f"{total_res:,.2f}")
