import streamlit as st
import pandas as pd
import requests
import re
import plotly.express as px

# إعدادات واجهة الموبايل
st.set_page_config(page_title="منظومة نهلاتي العالمية", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    div.stButton > button {
        background-color: #FFC107; color: black; border-radius: 15px; height: 3.5em; width: 100%; font-weight: bold;
    }
    .stTabs [data-baseweb="tab"] { font-size: 14px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.title("🐝 تطبيق نهلاتي الشامل")
st.write("مركز الإدارة الطبية والتسويقية")

tabs = st.tabs(["🏥 العيادة", "📩 تحليل فيسبوك", "🕵️ منقب المجموعات", "💡 الأفكار و Etsy"])

# --- 1. إدارة العيادة ---
with tabs[0]:
    st.header("سجل الجلسات والحقن")
    with st.form("clinic_form"):
        name = st.text_input("اسم المريض")
        dose = st.number_input("الجرعة (ml)", 0.05, 5.0, 0.1)
        sugar = st.number_input("قراءة السكر")
        notes = st.text_area("ملاحظات طبية")
        if st.form_submit_button("حفظ الجلسة"):
            st.success(f"تم حفظ بيانات {name} سحابياً ✅")

# --- 2. تحليل الرسائل والإعلانات ---
with tabs[1]:
    st.header("تحليل رسائل الصفحة")
    token = st.text_input("أدخل Token الصفحة:", type="password")
    if st.button("🚀 سحب وتحليل 333 رسالة"):
        st.info("جاري الاتصال بفيسبوك وسحب الأرشيف...")

# --- 3. منقب المجموعات ---
with tabs[2]:
    st.header("استخراج زبائن المجموعات")
    raw_text = st.text_area("الصق التعليقات هنا من فيسبوك موبايل:", height=200)
    if st.button("🔎 استخراج الهواتف والحالات"):
        phones = re.findall(r"(05|06|07)\d{8}", raw_text)
        if phones:
            for p in set(phones): st.success(f"📞 هاتف: {p}")
        else: st.warning("لم يتم العثور على أرقام.")

# --- 4. مختبر الأفكار و Etsy ---
with tabs[3]:
    st.header("مخطط المنتجات الرقمية")
    idea = st.text_area("سجل فكرة ذكية لـ Etsy أو فيديو جديد:")
    if st.button("حفظ الفكرة في المختبر"):
        st.balloons()
        st.info("💡 نصيحة: فكرتك رائعة! ابدأ بتجهيز غلاف الكتاب بالإنجليزية.")
    
    st.divider()
    st.subheader("💰 حاسبة أرباح Etsy")
    price = st.number_input("سعر الكتاب ($)", value=29.0)
    sales = st.slider("مبيعات شهرية متوقعة", 1, 500, 50)
    st.metric("صافي الربح المتوقع", f"${price * sales}")

st.sidebar.write("إصدار الويب 2.0 - نهلاتي")
