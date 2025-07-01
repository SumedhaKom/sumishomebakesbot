import streamlit as st
import google.generativeai as genai
from datetime import datetime
import random

# --- 🔐 Gemini API Key ---
genai.configure(api_key="AIzaSyDqc2kmRAdde9QM2cMix7RKko2PRV1DtjI")  # Replace with your actual key
model = genai.GenerativeModel(model_name="models/gemini-1.5-flash-latest")

# --- 🎨 Page Configuration ---
st.set_page_config(page_title="SumisHomeBakesBot: Your Friendly Baking Assistant", layout="centered")

# --- 🌸 Custom CSS: Enhanced Pastel Bakery Theme (Darkened Gradient + Larger Fonts) ---
st.markdown("""
    <style>
        body, .stApp {
            background: linear-gradient(to right, #f8cddc, #c3eff0);
            font-family: 'Segoe UI', sans-serif;
            font-size: 20px;
            color: #2c2c2c;
        }
        .sumi-message {
            background-color: #fff6f9;
            padding: 1.7rem;
            border-radius: 1.5em;
            margin-bottom: 1.7rem;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            border-left: 8px solid #ffb6b9;
        }
        .user-message {
            background-color: #e0f7fa;
            padding: 1.7rem;
            border-radius: 1.5em;
            margin-bottom: 1.7rem;
            text-align: right;
            border-right: 8px solid #a0ced9;
        }
        .block-container {
            padding-top: 3rem;
        }
        .stButton > button {
            background-color: #ffdddd;
            border: none;
            color: #333;
            font-weight: bold;
            border-radius: 10px;
            padding: 1rem 2rem;
            font-size: 18px;
        }
        .big-input input {
            font-size: 20px !important;
            padding: 1.2rem !important;
        }
        .stTextArea textarea {
            font-size: 18px;
        }
    </style>
""", unsafe_allow_html=True)

# --- 🧁 Welcome Header ---
st.title("🎂 Welcome to SumisHomeBakesBot")
st.subheader("Your friendly AI baking assistant!")
st.markdown("""
**What can I do?**  
- Give me a picture of your ingredients or upload a .txt file, and I’ll help you bake something delicious 🍰  
- Ask me any baking question and I’ll guide you with love and precision.
""")

# --- 🧁 Baking Tip of the Day ---
baking_tips = [
    "Measure ingredients accurately — baking is a science!",
    "Room temperature eggs make for fluffier cakes.",
    "Always preheat your oven for even baking.",
    "Don’t overmix your batter or your cake will be dense.",
    "Use parchment paper to prevent sticking without extra butter."
]
st.info(f"🍰 Baking Tip of the Day: {random.choice(baking_tips)}")

# --- 💬 Chat History ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --- 🧹 Clear Chat Button ---
if st.button("Clear Chat"):
    st.session_state.chat_history = []
    st.experimental_rerun()

# --- 📸 Upload Ingredients ---
st.subheader("📷 Upload Your Ingredients")
st.markdown("Upload a clear .txt file with your ingredients listed, or simply describe them in the chat below.")
ingredient_file = st.file_uploader("Upload your ingredients list (.txt format only):", type=["txt"])

uploaded_ingredients = ""
if ingredient_file is not None:
    uploaded_ingredients = ingredient_file.read().decode("utf-8")
    st.text_area("📜 Uploaded Ingredients:", value=uploaded_ingredients, height=150)

# --- 💬 Input ---
user_input = st.text_input("Ask me a baking question:", placeholder="e.g., How do I replace eggs in brownies?", key="user_input", label_visibility="visible")

# --- 🤖 Handle Input ---
if user_input:
    with st.spinner("SumisHomeBakesBot is typing..."):
        try:
            combined_prompt = f"You are a helpful, friendly baking assistant. Give warm, clear, and simple baking advice.\n"
            if uploaded_ingredients:
                combined_prompt += f"Here are the ingredients the user has available:\n{uploaded_ingredients}\n"
            combined_prompt += f"User question: {user_input}"

            response = model.generate_content([combined_prompt])
            answer = response.text
            st.session_state.chat_history.append((user_input, answer))
        except Exception as e:
            answer = f"Oops! Something went wrong: {e}"
            st.session_state.chat_history.append((user_input, answer))

# --- 🗨️ Display Chat ---
for user, bot in reversed(st.session_state.chat_history):
    st.markdown(f"<div class='user-message'>{user}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='sumi-message'>🧁 {bot}</div>", unsafe_allow_html=True)

