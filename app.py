import streamlit as st
import google.generativeai as genai
import requests
import random
from PIL import Image
from io import BytesIO

# --- 1. Page Configuration (Gemini Light Theme) ---
st.set_page_config(page_title="Endlume AI Studio", page_icon="🤖", layout="centered")

st.markdown("""
    <style>
    .stApp { 
        background-color: #F0F4F9; 
        color: #1F1F1F;
        font-family: 'Segoe UI', Roboto, sans-serif;
    }
    /* Image Section Text Areas & Selection Styling */
    div[data-testid="stTextArea"] textarea {
        background-color: #FFFFFF !important;
        color: #1F1F1F !important;
        border: 1px solid #747775 !important;
        border-radius: 16px !important;
        padding: 12px 20px !important;
    }
    .stButton>button {
        background-color: #0B57D0; 
        color: white !important;
        border-radius: 24px !important;
        border: none !important;
        padding: 10px 24px !important;
        font-weight: 500 !important;
    }
    div[data-testid="stSelectbox"] div {
        background-color: #FFFFFF !important;
        color: #1F1F1F !important;
        border-radius: 16px !important;
    }
    button[data-baseweb="tab"] {
        color: #444746 !important;
        font-size: 16px !important;
    }
    button[aria-selected="true"] {
        color: #0B57D0 !important;
        border-bottom-color: #0B57D0 !important;
    }
    .ai-response {
        background-color: #FFFFFF;
        padding: 20px;
        border-radius: 16px;
        border: 1px solid #E3E3E3;
        margin-top: 15px;
        color: #1F1F1F;
    }
    /* Auto Expandable Chat Box Styling to look like real Gemini */
    .stChatInputContainer {
        border-radius: 28px !important;
        background-color: #FFFFFF !important;
        border: 1px solid #747775 !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- 2. AI Configuration (Latest Gemini 2.5 Flash & No Filters) ---
API_KEY = "YOUR_API_KEY_HERE"  # <--- Yahan apni asli API key paste rehne dena
genai.configure(api_key=API_KEY)

low_safety = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
]

# Latest Stable Gemini 2.5 Model Setup
model = genai.GenerativeModel('gemini-2.5-flash', safety_settings=low_safety)

# Initialize Session State for Prompt synchronization
if "img_prompt_val" not in st.session_state:
    st.session_state.img_prompt_val = ""

# --- 3. App UI ---
st.markdown("<h1 style='color: #1F1F1F; text-align: center; font-weight: 400;'>🤖 Endlume AI Studio</h1>", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["💬 Gemini Chat", "🎨 Image Generator"])

# --- Tab 1: Chat System (With Expandable Box) ---
with tab1:
    st.markdown("<p style='color: #444746;'>How can I help you today?</p>", unsafe_allow_html=True)
    
    # st.chat_input typing ke saath apne aap vertically bada hota hai aur horizontal problem nahi deta
    user_message = st.chat_input("Ask Gemini anything...")
    
    if user_message:
        with st.spinner("Thinking..."):
            try:
                response = model.generate_content(user_message)
                st.markdown(f"<div class='ai-response'><b>Gemini:</b><br><br>{response.text}</div>", unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Error: {e}")

# --- Tab 2: Image Generator Panel (With Working Brain) ---
with tab2:
    st.markdown("<p style='color: #444746;'>Create high-quality images with AI</p>", unsafe_allow_html=True)
    
    random_prompts = [
        "A cinematic cyber-punk street of Mumbai in heavy rain, neon lights, 8k, hyper-realistic",
        "A mysterious dark palace, gothic architecture, fog, billionaire dramatic atmosphere, 3d render",
        "An ancient Indian warrior standing on top of a mountain, sunrise, anime style, highly detailed",
        "A futuristic AI robot painting on a canvas, vaporwave aesthetic, cinematic lighting, 4k",
        "Hyper-realistic portrait of a mysterious king, golden crown, glowing eyes, dark fantasy background"
    ]
    
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("🎲 Random Prompt"):
            st.session_state.img_prompt_val = random.choice(random_prompts)
            st.rerun()
            
    with col_btn2:
        if st.button("🧠 Enhance Prompt (Brain)"):
            if st.session_state.img_prompt_val:
                with st.spinner("Making it professional..."):
                    enhance_query = f"Expand this simple prompt into a highly detailed, cinematic, professional grade image generation prompt. Output only the enhanced prompt in English without quotes: {st.session_state.img_prompt_val}"
                    try:
                        enhanced_resp = model.generate_content(enhance_query)
                        st.session_state.img_prompt_val = enhanced_resp.text
                        st.rerun()
                    except Exception as e:
                        st.error(f"Brain Error: {e}")
            else:
                st.warning("Please type something first, then click Brain button!")

    # Image prompt text area handles vertical text nicely
    img_prompt = st.text_area("Describe what you want to create:", value=st.session_state.img_prompt_val, placeholder="Type your imagination...")
    st.session_state.img_prompt_val = img_prompt

    col1, col2, col3 = st.columns(3)
    with col1:
        style = st.selectbox("Choose Style", ["Hyper-Realistic", "Anime", "3D Cinematic", "Cyberpunk", "Watercolor"])
    with col2:
        aspect_ratio = st.selectbox("Aspect Ratio", ["1:1 (Square)", "9:16 (Reels)", "2:3 (Ebook/Poster)", "16:9 (Landscape)"])
    with col3:
        num_images = st.selectbox("Images Count", [1, 2, 4])
        
    if st.button("Generate Art", key="img_btn") and img_prompt:
        with st.spinner("Generating Images... Please wait"):
            final_prompt = f"{img_prompt}, {style} style, aspect ratio {aspect_ratio}"
            encoded_prompt = requests.utils.quote(final_prompt)
            
            cols_grid = st.columns(2)
            for i in range(num_images):
                seed = random.randint(1, 99999)
                image_url = f"https://image.pollinations.ai/p/{encoded_prompt}?width=1024&height=1024&nologo=true&seed={seed}"
                
                with cols_grid[i % 2]:
                    try:
                        img_response = requests.get(image_url)
                        if img_response.status_code == 200:
                            img_data = Image.open(BytesIO(img_response.content))
                            st.image(img_data, caption=f"Design {i+1}", use_container_width=True)
                        else:
                            st.error(f"Could not load Design {i+1}. Try clicking generate again.")
                    except Exception as img_err:
                        st.error(f"Load Error: {img_err}")
