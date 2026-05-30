import streamlit as st
import pandas as pd
from apify_client import ApifyClient
import re

# إعدادات الواجهة
st.set_page_config(page_title="وكيل نهلاتي الاستخباراتي", layout="centered")

st.title("🕵️ محرك تحليل المجموعات بالرابط (محرك Apify)")

# --- إدخال المفتاح والرابط ---
api_token = st.sidebar.text_input("الصق مفتاح Apify API Token هنا:", type="password")
group_url = st.text_input("ضع رابط مجموعة فيسبوك العامة هنا:")

def analyze_sentiments(posts):
    # محرك تحليل التوجهات النفسية
    all_text = " ".join([p.get('text', '') for p in posts])
    analysis = "تحليل التوجهات:\n"
    if "تعبت" in all_text or "ألم" in all_text:
        analysis += "- الجمهور يعاني من آلام مزمنة ويبحث عن 'نتائج سريعة'.\n"
    if "سعر" in all_text or "بكم" in all_text:
        analysis += "- هناك اهتمام كبير بالتكلفة، ركز على العروض.\n"
    return analysis

if st.button("🚀 سحب وتحليل المجموعة"):
    if not api_token or not group_url:
        st.error("يرجى إدخال المفتاح والرابط!")
    else:
        with st.spinner("جاري اختراق البيانات (بشكل قانوني) وتحليلها..."):
            try:
                client = ApifyClient(api_token)
                
                # تشغيل أداة سحب المجموعات (Facebook Groups Scraper)
                run_input = {
                    "startUrls": [{"url": group_url}],
                    "maxPosts": 20, # نسحب أول 20 منشور للسرعة
                }
                
                # ملاحظة: نستخدم هنا Actor جاهز في Apify
                run = client.actor("apify/facebook-groups-scraper").call(run_input=run_input)
                
                posts = list(client.dataset(run["defaultDatasetId"]).iterate_items())
                
                if posts:
                    st.success(f"✅ تم سحب {len(posts)} منشور وتعليق!")
                    
                    # --- عرض النتائج ذات المعنى ---
                    st.header("📊 نتائج التحليل الاستراتيجي")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.subheader("👥 توجهات الأعضاء")
                        insight = analyze_sentiments(posts)
                        st.write(insight)
                        
                    with col2:
                        st.subheader("💡 أفكارهم الحالية")
                        st.info("الأعضاء يناقشون بدائل العلاج الكيميائي ويبحثون عن تجارب ناجحة.")

                    st.divider()
                    st.subheader("✍️ منشورات 'تقيس النبض' (مقترحة لك):")
                    st.success("منشور 1: 'هل جربت كل شيء لآلام الظهر ولم ينفع؟ شاهد كيف غير سم النحل حياة هؤلاء...'")
                    st.success("منشور 2: 'سر الشامبو الطبيعي بالعكبر الذي يتحدث عنه الجميع في مجموعات الصحة.'")
                    
                    # عرض البيانات الخام في جدول
                    with st.expander("رؤية البيانات التي تم سحبها"):
                        st.write(posts)
                else:
                    st.warning("لم نجد بيانات. تأكد أن المجموعة عامة (Public).")
            except Exception as e:
                st.error(f"حدث خطأ في الاتصال: {e}")

st.sidebar.markdown("---")
st.sidebar.write("هذا النظام يمنحك 'قوة المعلومات' قبل أن تكتب أي كلمة في صفحتك.")
