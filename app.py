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
        "عرق النسا والظهر": ["سياتيك", "سياتيق", "ظهر", "انزلاق", "فقرات", "ديسك", "هرني", "hernie", "وجع"],
        "تصلب لوحي": ["تصلب", "لويحي", "ms", "sep", "متعدد"],
        "روماتيزم ومفاصل": ["روماتيزم", "مفاصل", "ركبة", "برودة", "عظام", "ارتروز", "arthrose"],
        "مشاكل الشعر": ["شعر", "تساقط", "قشرة", "ثعلبة", "فراغات"],
        "سكري": ["سكر", "سكري", "انسولين", "خزان", "تراكمي"]
    }
    
    findings = []
    lines = text.split('\n')
    for line in lines:
        line = line.strip()
        if len(line) > 5:  # تقليل القيود ليقبل الجمل القصيرة
            detected_disease = "غير محدد (يحتاج مراجعة)"
            for cat, keywords in categories.items():
                if any(k in line for k in keywords):
                    detected_disease = cat
                    break
            findings.append({"نص التعليق": line[:150], "التصنيف المتوقع": detected_disease})
            
    # 3. تحليل الكلمات الأكثر تكراراً (فهم جو المجموعة)
    words = re.findall(r'\w+', text)
    common_words = Counter(words).most_common(10)
    
    return phones, findings, common_words

# --- الواجهة ---
raw_input = st.text_area("ألصق النص المنسوخ هنا (تعليقات، منشورات، رسائل):", height=300)

if st.button("🚀 ابدأ التحليل العميق الآن"):
    if raw_input:
        with st.spinner("جاري استخراج البيانات..."):
            phones, findings, common = flexible_analysis(raw_input)
            
            st.success("✅ اكتملت العملية!")

            # عرض النتائج في مربعات جذابة
            c1, c2, c3 = st.columns(3)
            c1.metric("تعليقات محللة", len(findings))
            c2.metric("أرقام هواتف", len(set(phones)))
            c3.metric("فرص بيع محتملة", len([f for f in findings if f['التصنيف المتوقع'] != "غير محدد (يحتاج مراجعة)"]))

            st.divider()

            # قسم الهواتف
            if phones:
                st.subheader("📞 أرقام الهواتف المكتشفة (جاهزة للاتصال)")
                for p in set(phones):
                    st.success(f"الهاتف: {p}")
            else:
                st.info("ℹ️ لم يتم العثور على أرقام هواتف في هذا النص.")

            # قسم تحليل الحالات
            if findings:
                st.subheader("📋 تحليل الحالات المكتشفة في التعليقات")
                df = pd.DataFrame(findings)
                st.table(df) # استخدام Table لضمان الظهور الواضح على الموبايل

            # قسم الكلمات المفتاحية
            st.subheader("📊 ماذا يشغل بال أعضاء هذه المجموعة؟")
            st.write("أكثر الكلمات تكراراً (تعطيك فكرة عن اهتماماتهم):")
            for word, count in common:
                if len(word) > 3: # تجاهل حروف الجر الصغيرة
                    st.code(f"{word}: تكررت {count} مرات")
    else:
        st.error("الرجاء لصق النص أولاً!")

st.sidebar.info("💡 نصيحة: إذا لم تظهر نتائج، تأكد أنك نسخت تعليقات حقيقية تحتوي على كلمات مثل (ظهر، علاج، سكر، هاتف.. إلخ)")
