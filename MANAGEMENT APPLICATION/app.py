import json
import random
import string
from pathlib import Path
import streamlit as st

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="NovBank",
    page_icon="🏦",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ── Global CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@300;400;500&display=swap');

/* Reset & base */
html, body, [class*="css"] { font-family: 'Syne', sans-serif; }
.stApp { background: #0a0a0f; color: #e8e3d8; }

/* Hide default streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 2rem; max-width: 720px; }

/* ── Hero header ── */
.hero {
    text-align: center;
    padding: 3rem 0 2rem;
    border-bottom: 1px solid #1e1e2e;
    margin-bottom: 2rem;
}
.hero-logo {
    font-size: 0.75rem;
    letter-spacing: 0.35em;
    color: #c0b89a;
    text-transform: uppercase;
    font-family: 'DM Mono', monospace;
    margin-bottom: 0.5rem;
}
.hero-title {
    font-size: 3.5rem;
    font-weight: 800;
    line-height: 1;
    background: linear-gradient(135deg, #e8e3d8 30%, #c0b89a 80%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0;
}
.hero-sub {
    font-size: 0.8rem;
    color: #5a5a6e;
    font-family: 'DM Mono', monospace;
    letter-spacing: 0.1em;
    margin-top: 0.5rem;
}

/* ── Cards ── */
.card {
    background: #111118;
    border: 1px solid #1e1e2e;
    border-radius: 2px;
    padding: 2rem;
    margin-bottom: 1.5rem;
}
.card-title {
    font-size: 0.65rem;
    letter-spacing: 0.3em;
    text-transform: uppercase;
    color: #c0b89a;
    font-family: 'DM Mono', monospace;
    margin-bottom: 1.25rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.card-title::before {
    content: '';
    display: inline-block;
    width: 18px;
    height: 1px;
    background: #c0b89a;
}

/* ── Balance display ── */
.balance-display {
    text-align: center;
    padding: 2rem;
    background: #0a0a0f;
    border: 1px solid #c0b89a22;
    border-radius: 2px;
    margin: 1rem 0;
}
.balance-label {
    font-size: 0.65rem;
    letter-spacing: 0.3em;
    text-transform: uppercase;
    color: #5a5a6e;
    font-family: 'DM Mono', monospace;
}
.balance-amount {
    font-size: 3rem;
    font-weight: 700;
    color: #e8e3d8;
    font-family: 'DM Mono', monospace;
    letter-spacing: -0.02em;
}
.balance-currency {
    font-size: 1.2rem;
    color: #c0b89a;
    vertical-align: super;
    margin-right: 0.25rem;
}

/* ── Detail row ── */
.detail-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.7rem 0;
    border-bottom: 1px solid #1e1e2e;
    font-size: 0.9rem;
}
.detail-row:last-child { border-bottom: none; }
.detail-key {
    color: #5a5a6e;
    font-family: 'DM Mono', monospace;
    font-size: 0.75rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
}
.detail-val { color: #e8e3d8; font-weight: 600; }
.detail-val.mono { font-family: 'DM Mono', monospace; font-size: 0.85rem; }

/* ── Status messages ── */
.msg-success {
    background: #0a1a10;
    border: 1px solid #2a5a3a;
    border-left: 3px solid #4caf7a;
    color: #4caf7a;
    padding: 0.75rem 1rem;
    border-radius: 2px;
    font-family: 'DM Mono', monospace;
    font-size: 0.8rem;
    letter-spacing: 0.05em;
}
.msg-error {
    background: #1a0a0a;
    border: 1px solid #5a2a2a;
    border-left: 3px solid #cf4c4c;
    color: #cf4c4c;
    padding: 0.75rem 1rem;
    border-radius: 2px;
    font-family: 'DM Mono', monospace;
    font-size: 0.8rem;
    letter-spacing: 0.05em;
}
.msg-warn {
    background: #1a150a;
    border: 1px solid #5a450a;
    border-left: 3px solid #cfaa4c;
    color: #cfaa4c;
    padding: 0.75rem 1rem;
    border-radius: 2px;
    font-family: 'DM Mono', monospace;
    font-size: 0.8rem;
    letter-spacing: 0.05em;
}

/* ── Streamlit widget overrides ── */
.stTextInput > div > div > input,
.stNumberInput > div > div > input {
    background: #0a0a0f !important;
    border: 1px solid #1e1e2e !important;
    border-radius: 2px !important;
    color: #e8e3d8 !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.9rem !important;
}
.stTextInput > div > div > input:focus,
.stNumberInput > div > div > input:focus {
    border-color: #c0b89a !important;
    box-shadow: none !important;
}
.stTextInput label, .stNumberInput label, .stSelectbox label {
    color: #5a5a6e !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.7rem !important;
    letter-spacing: 0.2em !important;
    text-transform: uppercase !important;
}
.stSelectbox > div > div {
    background: #0a0a0f !important;
    border: 1px solid #1e1e2e !important;
    border-radius: 2px !important;
    color: #e8e3d8 !important;
}
.stButton > button {
    background: #c0b89a !important;
    color: #0a0a0f !important;
    border: none !important;
    border-radius: 2px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.8rem !important;
    letter-spacing: 0.2em !important;
    text-transform: uppercase !important;
    padding: 0.6rem 2rem !important;
    width: 100% !important;
    transition: all 0.15s ease !important;
}
.stButton > button:hover {
    background: #e8e3d8 !important;
    transform: translateY(-1px) !important;
}
div[data-testid="stVerticalBlock"] > div:has(> .stButton) button[kind="secondary"] {
    background: transparent !important;
    color: #cf4c4c !important;
    border: 1px solid #5a2a2a !important;
}
</style>
""", unsafe_allow_html=True)

# ── Database helpers ────────────────────────────────────────────────────────────
DB_FILE = "novbank_database.json"

def load_data():
    if Path(DB_FILE).exists():
        with open(DB_FILE) as f:
            return json.loads(f.read())
    return []

def save_data(data):
    with open(DB_FILE, "w") as f:
        f.write(json.dumps(data, indent=2))

def generate_account_no():
    alpha = random.choices(string.ascii_uppercase, k=8)
    num = random.choices(string.digits, k=4)
    acc = alpha + num
    random.shuffle(acc)
    return "".join(acc)

def find_user(data, accno, pin):
    matches = [u for u in data if u["accountNo"] == accno and u["pin"] == pin]
    return matches[0] if matches else None

# ── Session state init ──────────────────────────────────────────────────────────
if "data" not in st.session_state:
    st.session_state.data = load_data()
if "msg" not in st.session_state:
    st.session_state.msg = None   # (type, text)  type: success|error|warn

def set_msg(t, text): st.session_state.msg = (t, text)
def clear_msg(): st.session_state.msg = None

# ── Hero ────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <div class="hero-logo">Private Banking System</div>
  <h1 class="hero-title">NOV BANK</h1>
  <div class="hero-sub">Secure · Simple · Reliable</div>
</div>
""", unsafe_allow_html=True)

# ── Message banner ──────────────────────────────────────────────────────────────
if st.session_state.msg:
    t, text = st.session_state.msg
    css_class = {"success": "msg-success", "error": "msg-error", "warn": "msg-warn"}.get(t, "msg-warn")
    icon = {"success": "✓", "error": "✕", "warn": "⚠"}.get(t, "")
    st.markdown(f'<div class="{css_class}">{icon}  {text}</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

# ── Operation selector ──────────────────────────────────────────────────────────
st.markdown('<div class="card"><div class="card-title">Operation</div>', unsafe_allow_html=True)

OPERATIONS = [
    "Create Account",
    "Deposit Money",
    "Withdraw Money",
    "Account Details",
    "Update Details",
    "Delete Account",
]
op = st.selectbox("", OPERATIONS, label_visibility="collapsed")
st.markdown("</div>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# 1. CREATE ACCOUNT
# ═══════════════════════════════════════════════════════════════════════════════
if op == "Create Account":
    st.markdown('<div class="card"><div class="card-title">New Account</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Full Name")
        email = st.text_input("Email Address")
    with col2:
        age = st.number_input("Age", min_value=0, max_value=120, step=1)
        pin = st.text_input("4-Digit PIN", type="password", max_chars=4)

    if st.button("Open Account"):
        clear_msg()
        if not all([name, email, pin]):
            set_msg("error", "All fields are required.")
        elif age < 12:
            set_msg("error", "Applicant must be at least 12 years old.")
        elif not pin.isdigit() or len(pin) != 4:
            set_msg("error", "PIN must be exactly 4 digits.")
        else:
            acc_no = generate_account_no()
            st.session_state.data.append({
                "name": name,
                "age": int(age),
                "email": email,
                "accountNo": acc_no,
                "pin": int(pin),
                "balance": 0,
            })
            save_data(st.session_state.data)
            set_msg("success", f"Account created. Your account number: {acc_no}")
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# 2. DEPOSIT
# ═══════════════════════════════════════════════════════════════════════════════
elif op == "Deposit Money":
    st.markdown('<div class="card"><div class="card-title">Deposit Funds</div>', unsafe_allow_html=True)
    accno = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password", max_chars=4)
    amount = st.number_input("Amount (₹)", min_value=1, step=100)

    if st.button("Deposit"):
        clear_msg()
        user = find_user(st.session_state.data, accno, int(pin) if pin.isdigit() else -1)
        if not user:
            set_msg("error", "Invalid account number or PIN.")
        else:
            user["balance"] += int(amount)
            save_data(st.session_state.data)
            set_msg("success", f"₹{amount:,} deposited. New balance: ₹{user['balance']:,}")
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# 3. WITHDRAW
# ═══════════════════════════════════════════════════════════════════════════════
elif op == "Withdraw Money":
    st.markdown('<div class="card"><div class="card-title">Withdraw Funds</div>', unsafe_allow_html=True)
    accno = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password", max_chars=4)
    amount = st.number_input("Amount (₹)", min_value=1, step=100)

    if st.button("Withdraw"):
        clear_msg()
        user = find_user(st.session_state.data, accno, int(pin) if pin.isdigit() else -1)
        if not user:
            set_msg("error", "Invalid account number or PIN.")
        elif int(amount) > user["balance"]:
            set_msg("warn", f"Insufficient balance. Available: ₹{user['balance']:,}")
        else:
            user["balance"] -= int(amount)
            save_data(st.session_state.data)
            set_msg("success", f"₹{amount:,} withdrawn. Remaining balance: ₹{user['balance']:,}")
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# 4. ACCOUNT DETAILS
# ═══════════════════════════════════════════════════════════════════════════════
elif op == "Account Details":
    st.markdown('<div class="card"><div class="card-title">View Account</div>', unsafe_allow_html=True)
    accno = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password", max_chars=4)

    if st.button("View Details"):
        clear_msg()
        user = find_user(st.session_state.data, accno, int(pin) if pin.isdigit() else -1)
        if not user:
            set_msg("error", "Invalid account number or PIN.")
            st.rerun()
        else:
            st.markdown("</div>", unsafe_allow_html=True)

            # Balance card
            st.markdown(f"""
            <div class="balance-display">
                <div class="balance-label">Current Balance</div>
                <div class="balance-amount"><span class="balance-currency">₹</span>{user['balance']:,}</div>
            </div>
            """, unsafe_allow_html=True)

            # Details card
            st.markdown('<div class="card"><div class="card-title">Account Information</div>', unsafe_allow_html=True)
            rows = [
                ("Name", user["name"], False),
                ("Age", str(user["age"]), False),
                ("Email", user["email"], False),
                ("Account No.", user["accountNo"], True),
            ]
            html_rows = "".join(
                f'<div class="detail-row"><span class="detail-key">{k}</span>'
                f'<span class="detail-val{" mono" if mono else ""}">{v}</span></div>'
                for k, v, mono in rows
            )
            st.markdown(html_rows, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.markdown("</div>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# 5. UPDATE DETAILS
# ═══════════════════════════════════════════════════════════════════════════════
elif op == "Update Details":
    st.markdown('<div class="card"><div class="card-title">Update Account</div>', unsafe_allow_html=True)
    accno = st.text_input("Account Number")
    pin = st.text_input("Current PIN", type="password", max_chars=4)

    st.markdown('<p style="color:#5a5a6e;font-family:\'DM Mono\',monospace;font-size:0.72rem;letter-spacing:0.1em;">LEAVE BLANK TO KEEP CURRENT VALUE</p>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        new_name = st.text_input("New Name")
        new_email = st.text_input("New Email")
    with col2:
        new_pin = st.text_input("New PIN", type="password", max_chars=4)

    if st.button("Save Changes"):
        clear_msg()
        user = find_user(st.session_state.data, accno, int(pin) if pin.isdigit() else -1)
        if not user:
            set_msg("error", "Invalid account number or PIN.")
        else:
            if new_pin and (not new_pin.isdigit() or len(new_pin) != 4):
                set_msg("error", "New PIN must be exactly 4 digits.")
            else:
                if new_name:  user["name"] = new_name
                if new_email: user["email"] = new_email
                if new_pin:   user["pin"] = int(new_pin)
                save_data(st.session_state.data)
                set_msg("success", "Account details updated successfully.")
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# 6. DELETE ACCOUNT
# ═══════════════════════════════════════════════════════════════════════════════
elif op == "Delete Account":
    st.markdown('<div class="card"><div class="card-title">Close Account</div>', unsafe_allow_html=True)
    st.markdown('<div class="msg-warn">⚠  This action is permanent and cannot be undone.</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    accno = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password", max_chars=4)
    confirm = st.checkbox("I understand this will permanently delete my account")

    if st.button("Delete Account"):
        clear_msg()
        user = find_user(st.session_state.data, accno, int(pin) if pin.isdigit() else -1)
        if not user:
            set_msg("error", "Invalid account number or PIN.")
        elif not confirm:
            set_msg("warn", "Please confirm deletion by checking the box above.")
        else:
            st.session_state.data.remove(user)
            save_data(st.session_state.data)
            set_msg("success", "Account has been permanently closed.")
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# ── Footer ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center;padding:3rem 0 1rem;border-top:1px solid #1e1e2e;margin-top:2rem;">
  <p style="font-family:'DM Mono',monospace;font-size:0.65rem;letter-spacing:0.2em;color:#2e2e3e;text-transform:uppercase;">
    NOV BANK · PRIVATE BANKING SYSTEM · SECURED
  </p>
</div>
""", unsafe_allow_html=True)