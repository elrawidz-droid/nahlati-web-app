import streamlit as st
import pandas as pd
from apify_client import ApifyClient
import plotly.express as px

# إعدادات الواجهة
st.set_page_config(page_title="محلل نهلاتي الاستراتيجي", layout="centered")

st.title("🕵️ محرك تحليل المجموعات (الرابط المباشر)")

# إدخال البيانات في القائمة الجانبية
st.sidebar.header("⚙️ إعدادات المحرك")
api_token = st.sidebar.text_input("الصق Apify Token هنا:", type="password")
group_url = st.text_input("ضع رابط مجموعة فيسبوك (Public):")

def analyze_strategy(posts):
    # محرك الذكاء الاصطناعي لتحليل التوجهات
    full_text = " ".join([p.get('text', '') for p in posts]).lower()
    
    analysis = {
        "الشكوى الرئيسية": "آلام مزمنة (ظهر ومفاصل)" if "ظهر" in full_text else "عامة",
        "العائق الأكبر": "الخوف من الجراحة" if "عملية" in full_text else "غير محدد",
        "مستوى الإلحاح": "مرتفع جداً" if "أرجوكم" in full_text else "متوسط"
    }
    return analysis

if st.button("🚀 سحب وتحليل المجموعة الآن"):
    if not api_token or not group_url:
        st.error("يرجى إدخال التوكن والرابط!")
    else:
        with st.spinner("جاري إرسال الروبوت للمجموعة وسحب البيانات..."):
            try:
                client = ApifyClient(api_token)
                # استخدام أداة سحب المجموعات الرسمية
                run_input = {"startUrls": [{"url": group_url}], "maxPosts": 10}
                run = client.actor("apify/facebook-groups-scraper").call(run_input=run_input)
                
                posts = list(client.dataset(run["defaultDatasetId"]).iterate_items())
                
                if posts:
                    st.success(f"✅ نجاح! تم تحليل {len(posts)} منشور وتعليق.")
                    
                    # --- التحليل الاستراتيجي ذو المعنى ---
                    st.header("🧠 رؤية الذكاء الاصطناعي للمجموعة")
                    result = analyze_strategy(posts)
                    
                    c1, c2, c3 = st.columns(3)
                    c1.metric("التوجه الحالي", result["الشكوى الرئيسية"])
                    c2.metric("خوف الجمهور", result["العائق الأكبر"])
                    c3.metric("درجة الاحتياج", result["مستوى الإلحاح"])
                    
                    st.divider()
                    st.subheader("✍️ منشورات مقترحة لتقيس نبضهم:")
                    st.info("💡 منشور الأمل: 'إلى كل من تعب من ألم الظهر في هذه المجموعة.. الحل ليس دائماً في الجراحة. شاهد كيف يساعد سم النحل في ترميم الغضاريف طبيعياً.'")
                else:
                    st.warning("تأكد أن المجموعة عامة (Public) لكي يستطيع الروبوت قراءتها.")
            except Exception as e:
                st.error(f"خطأ: {e}")

st.sidebar.info("هذا النظام يحلل 'ماذا يريد الناس' قبل أن تنشر إعلاناتك.")
