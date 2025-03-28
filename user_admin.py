
import streamlit as st
import sqlite3
import pandas as pd

st.title("👤 사용자 조건 관리 페이지")

conn = sqlite3.connect("search_conditions.db")
cursor = conn.cursor()
df = pd.read_sql_query("SELECT * FROM user_conditions", conn)

if df.empty:
    st.info("저장된 사용자 조건이 없습니다.")
else:
    st.dataframe(df)

    selected_id = st.selectbox("삭제할 조건 ID 선택", df["id"].tolist())
    if st.button("🗑 선택 조건 삭제"):
        cursor.execute("DELETE FROM user_conditions WHERE id = ?", (selected_id,))
        conn.commit()
        st.success("조건이 삭제되었습니다. 페이지를 새로고침 해주세요.")

conn.close()
