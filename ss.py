import streamlit as st
import random
import string
import qrcode
from io import BytesIO

# ================== UI STYLE ==================
st.markdown("""
<style>
html, body {
    direction: rtl;
    text-align: right;
    font-family: "Segoe UI", Tahoma, Arial;
    background-color: #0f172a;
}

.stApp {
    background: linear-gradient(135deg, #0f172a, #020617);
}

/* Titles */
h1 {
    color: #38bdf8;
    text-align: center;
}
h2, h3 {
    color: #e5e7eb;
}

/* Cards */
.card {
    background: linear-gradient(135deg, #020617, #020617);
    border-radius: 20px;
    padding: 25px;
    box-shadow: 0 0 30px rgba(56,189,248,0.15);
    margin-bottom: 20px;
}

/* Buttons */
.stButton button {
    background: linear-gradient(135deg, #22c55e, #16a34a);
    color: white;
    border-radius: 14px;
    font-weight: bold;
    padding: 10px 30px;
    border: none;
    box-shadow: 0 0 20px rgba(34,197,94,0.6);
}

/* Image fix */
.stImage {
    display: block !important;
    margin: auto;
}

/* Progress bar */
.stProgress > div > div {
    background: linear-gradient(90deg, #38bdf8, #22c55e);
}
</style>
""", unsafe_allow_html=True)

# ================== TITLE ==================
st.title("🔐 مولد كلمات السر الذكي")
st.caption("واجهة بسيطة • ألوان مريحة • QR Code")

# ================== CARD ==================
st.markdown('<div class="card">', unsafe_allow_html=True)

length = st.slider(
    "🔢 طول كلمة السر",
    min_value=4,
    max_value=32,
    value=8
)

col1, col2 = st.columns(2)
with col1:
    use_upper = st.checkbox("🔠 حروف كبيرة (A-Z)", True)
    use_lower = st.checkbox("🔡 حروف صغيرة (a-z)", True)
with col2:
    use_digits = st.checkbox("🔢 أرقام (0-9)", True)
    use_symbols = st.checkbox("✨ رموز خاصة (!@#)", True)

st.markdown('</div>', unsafe_allow_html=True)

# ================== PASSWORD STRENGTH ==================
def password_evaluation(password):
    score = 0
    if len(password) >= 8: score += 1
    if len(password) >= 12: score += 1
    if any(c.isupper() for c in password): score += 1
    if any(c.islower() for c in password): score += 1
    if any(c.isdigit() for c in password): score += 1
    if any(c in string.punctuation for c in password): score += 1

    if score <= 2:
        return "ضعيفة", 30
    elif score <= 4:
        return "متوسطة", 65
    else:
        return "قوية", 100

# ================== GENERATE ==================
if st.button("⚡ توليد كلمة السر"):
    characters = ""
    if use_upper: characters += string.ascii_uppercase
    if use_lower: characters += string.ascii_lowercase
    if use_digits: characters += string.digits
    if use_symbols: characters += "!@#$%^&*()_+"

    if characters == "":
        st.error("❌ لازم تختاري نوع واحد على الأقل")
    else:
        password = "".join(random.choice(characters) for _ in range(length))
        status, percent = password_evaluation(password)

        st.markdown('<div class="card">', unsafe_allow_html=True)

        st.subheader("🔑 كلمة السر")
        st.code(password)

        if status == "ضعيفة":
            st.error("🔴 ضعيفة")
        elif status == "متوسطة":
            st.warning("🟡 متوسطة")
        else:
            st.success("🟢 قوية")

        st.progress(percent / 100)

        # ================== QR CODE (FIXED) ==================
        qr = qrcode.make(password)

        qr_bytes = BytesIO()
        qr.save(qr_bytes, format="PNG")
        qr_bytes.seek(0)

        st.subheader("📱 QR Code")
        st.image(qr_bytes.getvalue(), width=220)

        st.download_button(
            "⬇ تحميل QR Code",
            data=qr_bytes.getvalue(),
            file_name="password_qr.png",
            mime="image/png"
        )

        st.markdown('</div>', unsafe_allow_html=True)
