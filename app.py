import streamlit as st
import pandas as pd
import re

# إعدادات واجهة المحترفين
st.set_page_config(page_title="مختبر نهلاتي الاستراتيجي", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stTextArea textarea { background-color: #161b22; color: #e6edf3; border: 1px solid #30363d; border-radius: 10px; }
    .strategy-card { background-color: #1e2130; padding: 20px; border-radius: 15px; border-right: 5px solid #FFC107; margin-top: 20px; }
    .post-box { background-color: #2c3e50; padding: 15px; border-radius: 10px; border: 1px dashed #FFC107; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🧠 مختبر نهلاتي لتحليل عقلية الجمهور")
st.write("حول تعليقات المجموعات إلى منشورات تلمس القلب وتجلب الزبائن")

# --- محرك التحليل الاستراتيجي ---
def analyze_psychology(text):
    text = text.lower()
    analysis = {}
    
    # 1. رصد "نقاط الألم" (Pain Points)
    pains = []
    if any(w in text for w in ["تعبت", "يئست", "سنين", "كل يوم"]): pains.append("فقدان الأمل بسبب طول مدة المرض")
    if any(w in text for w in ["غالي", "سعر", "دراهم", "خسرت"]): pains.append("الخوف من استنزاف المال بدون نتيجة")
    if any(w in text for w in ["عملية", "جراحة", "خايف", "مخاطرة"]): pains.append("الرعب من العمليات الجراحية")
    if any(w in text for w in ["دواء", "شربت", "معدتي", "كيميائي"]): pains.append("تضرر الجسم من الأدوية الكيميائية")
    
    # 2. رصد "التوجهات والأسئلة"
    trends = []
    if "وين" in text or "بلاصة" in text: trends.append("بحث مكثف عن موقع قريب وموثوق")
    if "مجرب" in text or "صح" in text: trends.append("الحاجة لشهادات ناس حقيقيين (دليل اجتماعي)")
    if "سكري" in text or "ضغط" in text: trends.append("الخوف من تعارض العلاج مع الأمراض المزمنة")

    return pains, trends

# --- صانع المنشورات الذكي ---
def generate_posts(pains):
    posts = []
    if "الرعب من العمليات الجراحية" in pains:
        posts.append("📢 منشور مقترح: 'إلى كل من قيل له (الحل الوحيد هو العملية).. توقف قليلاً! سم النحل ليس مجرد لسعة، بل هو إعادة إحياء للأعصاب التالفة بدون جراحة. شاهد كيف استعاد (فلان) حركته...'")
    if "تضرر الجسم من الأدوية الكيميائية" in pains:
        posts.append("📢 منشور مقترح: 'معدتك لم تعد تتحمل المسكنات؟ جرب صيدلية الطبيعة. حقن سم النحل يعالج الالتهاب من جذوره ولا يغطي الألم فقط. ابدأ رحلة الشفاء الطبيعي اليوم.'")
    if not posts:
        posts.append("📢 منشور عام: 'نحن لا نعالج الأعراض، نحن نعيد بناء المناعة. عيادة نهلاتي تقدم لك بروتوكولاً مخصصاً حسب لون بشرتك وحالتك الصحية.'")
    return posts

# --- الواجهة ---
st.subheader("📥 مدخلات المختبر")
raw_text = st.text_area("الصق هنا أكبر قدر ممكن من تعليقات ومنشورات المجموعة (Copy/Paste):", height=250)

if st.button("🚀 تحليل عقلية الجمهور وصناعة الاستراتيجية"):
    if raw_text:
        with st.spinner("جاري قراءة أفكار الجمهور..."):
            pains, trends = analyze_psychology(raw_text)
            
            st.success("✅ اكتمل التحليل الاستراتيجي!")
            
            # عرض النتائج
            st.markdown("<div class='strategy-card'>", unsafe_allow_html=True)
            st.subheader("🕵️ ماذا يوجع جمهور هذه المجموعة؟ (نقاط الألم)")
            if pains:
                for p in pains: st.write(f"📍 {p}")
            else: st.write("جمهور متنوع، يبحث عن معلومات عامة.")
            
            st.subheader("🎯 توجهاتهم الحالية")
            for t in trends: st.write(f"🔹 {t}")
            st.markdown("</div>", unsafe_allow_html=True)

            st.divider()

            # قسم صناعة المحتوى
            st.subheader("✍️ منشورات مقترحة لتقيس نبضهم:")
            st.write("هذه المنشورات مصممة بناءً على 'ألم' الجمهور الذي تم تحليله:")
            suggested_posts = generate_posts(pains)
            for p in suggested_posts:
                st.markdown(f"<div class='post-box'>{p}</div>", unsafe_allow_html=True)
                
            st.info("💡 نصيحة: انشر هذه الكلمات مع صورة 'حقيقية' من عيادتك لزيادة الثقة.")
    else:
        st.error("الرجاء لصق النص أولاً!")
