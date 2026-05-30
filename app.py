import streamlit as st
import pandas as pd
import re
from collections import Counter

# إعدادات الواجهة
st.set_page_config(page_title="محلل نهلاتي الذكي", layout="wide")

st.title("🛡️ محرك تحليل المجموعات المطور (الذكاء الاصطناعي)")
st.write("انسخ أي كلام من فيسبوك والصقه بالأسفل.. سأقوم باستخراج كل المعلومات الممكنة.")

# --- محرك التحليل المرن ---
def flexible_analysis(text):
    text = str(text).lower()
    
    # 1. استخراج الهواتف (Algeria format)
    phones = re.findall(r"(05|06|07)\d{8}", text)
    
    # 2. قاموس الكلمات الطبية الموسع (بالعامية والفرنسية والعربية)
    categories = {
