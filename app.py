import streamlit as st
import pandas as pd
import re

# إعدادات الواجهة
st.set_page_config(page_title="مركز ذكاء نهلاتي", layout="centered")

st.title("🛡️ محرك نهلاتي لتحليل المجموعات والزبائن")

tabs = st.tabs(["🕵️ محلل المجموعات العميق", "🏥 العيادة", "📩 فيسبوك"])

# --- تبويب محلل المجموعات المطور ---
with tabs[0]:
    st.header("تحليل محتوى المجموعات (الذكاء الاصطناعي)")
    group_url = st.text_input("رابط المجموعة (للتوثيق):")
    raw_data = st.text_area("ألصق هنا التعليقات أو المنشورات التي نسختها من المجموعة:", height=250)
    
    if st.button("🚀 بدء التنقيب والتحليل"):
        if raw_data:
            with st.spinner("جاري تحليل البيانات واستخراج الفرص..."):
                # 1. استخراج الهواتف
                phones = re.findall(r"(05|06|07)\d{8}", raw_data)
                
                # 2. منطق تحليل الحالات (Pattern Recognition)
                findings = []
                lines = raw_data.split('\n')
                for line in lines:
                    if len(line) > 15:
                        disease = "غير محدد"
                        if any(w in line for w in ["سياتيك", "ظهر", "انزلاق"]): disease = "عرق النسا/ظهر"
                        elif any(w in line for w in ["تصلب", "ms"]): disease = "تصلب لوحي"
                        elif any(w in line for w in ["شعر", "تساقط", "قشرة"]): disease = "مشاكل شعر"
                        
                        if disease != "غير محدد":
                            findings.append({"النص": line[:100], "الحالة": disease})

                # --- عرض النتائج ---
                st.success(f"✅ تم تحليل النص بنجاح!")
                
                c1, c2 = st.columns(2)
                c1.metric("أرقام هواتف مكتشفة", len(set(phones)))
                c2.metric("حالات مرضية محتملة", len(findings))

                if phones:
                    st.subheader("📞 قائمة الهواتف المستخرجة:")
                    for p in set(phones): st.code(p)

                if findings:
                    st.subheader("📋 تحليل الحالات المكتشفة:")
                    st.table(pd.DataFrame(findings))

                st.subheader("💡 نصيحة تسويقية لهذه المجموعة:")
                if "شعر" in raw_data or "قشرة" in raw_data:
                    st.info("هذه المجموعة مهتمة جداً بالتجميل. اقترح عليهم 'شامبو العكبر' الخاص بك في تعليق مفيد.")
                else:
                    st.info("الجمهور هنا يعاني من آلام مزمنة. ركز على نشر 'قصص نجاح' لعلاج حالات مشابهة بسم النحل.")
        else:
            st.error("من فضلك الصق بعض النصوص من المجموعة أولاً.")

# (بقية التبويبات تظل كما هي...)
