import streamlit as st
import google.generativeai as genai
import requests
import random

# --- 1. पेज कॉन्फ़िगरेशन (Gemini Light Theme) ---
st.set_page_config(page_title="Endlume AI Studio", page_icon="🤖", layout="centered")

# गूगल जेमिनी जैसी क्लीन लाइट थीम के लिए CSS
st.markdown("""
    <style>
    /* मुख्य बैकग्राउंड - हल्का सफेद/ग्रे */
    .stApp { 
        background-color: #F0F4F9; 
        color: #1F1F1F;
        font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    }
    
    /* इनपुट बॉक्स (Text Input & Text Area) - जेमिनी स्टाइल */
    div[data-testid="stTextInput"] input, div[data-testid="stTextArea"] textarea {
        background-color: #FFFFFF !important;
        color: #1F1F1F !important;
        border: 1px solid #747775 !important;
        border-radius: 28px !important; /* जेमिनी जैसा कैप्सूल लुक */
        padding: 12px 20px !important;
    }
    
    /* बटन्स - क्लीन और राउंडेड */
    .stButton>button {
        background-color: #0B57D0; /* जेमिनी का सिग्नेचर ब्लू कलर */
        color: white !important;
        border-radius: 24px !important;
        border: none !important;
        padding: 10px 24px !important;
        font-weight: 500 !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    .stButton>button:hover {
        background-color: #0B57D0 !important;
        box-shadow: 0 1px 2px 0 rgba(60,64,67,0.3), 0 2px 6px 2px rgba(60,64,67,0.15) !important;
    }
    
    /* ड्रॉपडाउन सिलेक्ट बॉक्स */
    div[data-testid="stSelectbox"] div {
        background-color: #FFFFFF !important;
        color: #1F1F1F !important;
        border-radius: 16px !important;
    }
    
    /* टैब्स (Tabs) की स्टाइलिंग */
    button[data-baseweb="tab"] {
        color: #444746 !important;
        font-size: 16px !important;
        font-weight: 500 !important;
    }
    button[aria-selected="true"] {
        color: #0B57D0 !important;
        border-bottom-color: #0B57D0 !important;
    }
    
    /* एआई का रिस्पॉन्स बॉक्स */
    .ai-response {
        background-color: #FFFFFF;
        padding: 20px;
        border-radius: 16px;
        border: 1px solid #E3E3E3;
        margin-top: 15px;
        box-shadow: 0 1px 2px rgba(0,0,0,0.05);
    }
    </style>
""", unsafe_allow_html=True)

# --- 2. एआई कॉन्फ़िगरेशन (बिना फ़िल्टर वाली सेटिंग) ---
API_KEY = "AIzaSyAhlo6tx2G8lP0cLGDDvWYmLCHGnaXXYnk"  # <--- यहाँ अपनी असली API Key डालें
genai.configure(api_key=API_KEY)

# सुरक्षा फ़िल्टर्स को पूरी तरह बंद (BLOCK_NONE) रखना ताकि कोई रुकावट न आए
low_safety = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
]
model = genai.GenerativeModel('gemini-1.5-flash', safety_settings=low_safety)

# --- 3. ऐप इंटरफ़ेस ---
st.markdown("<h1 style='color: #1F1F1F; text-align: center; font-weight: 400;'>🤖 Endlume AI Studio</h1>", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["💬 Gemini Chat", "🎨 Image Generator"])

# --- टैब 1: जेमिनी चैट सिस्टम ---
with tab1:
    st.markdown("<p style='color: #444746;'>How can I help you today?</p>", unsafe_allow_html=True)
    user_message = st.text_input("Enter a prompt here...", key="chat_in", placeholder="Ask Gemini...")
    
    if st.button("Ask Gemini", key="chat_btn") and user_message:
        with st.spinner("Thinking..."):
            try:
                response = model.generate_content(user_message)
                # सुंदर व्हाइट बॉक्स में रिस्पॉन्स दिखाना
                st.markdown(f"<div class='ai-response'><b>Gemini:</b><br><br>{response.text}</div>", unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Error: {e}")

# --- टैब 2: इमेज जनरेटर कंट्रोल पैनल ---
with tab2:
    st.markdown("<p style='color: #444746;'>Create high-quality images with AI</p>", unsafe_allow_html=True)
    
    # रैंडम प्रॉम्ट्स (पासा/डाइस फ़ीचर के लिए)
    random_prompts = [
        "A cinematic cyber-punk street of Mumbai in heavy rain, neon lights, 8k, hyper-realistic",
        "A mysterious dark palace, gothic architecture, fog, billionaire dramatic atmosphere, 3d render",
        "An ancient Indian warrior standing on top of a mountain, sunrise, anime style, highly detailed",
        "A futuristic AI robot painting on a canvas, vaporwave aesthetic, cinematic lighting, 4k",
        "Hyper-realistic portrait of a mysterious king, golden crown, glowing eyes, dark fantasy background"
    ]
    
    # डाइस और ब्रेन फीचर्स के लिए बटन्स
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("🎲 Random Prompt"):
            st.session_state.img_prompt_val = random.choice(random_prompts)
    with col_btn2:
        if st.button("🧠 Enhance Prompt"):
            if "img_prompt_val" in st.session_state and st.session_state.img_prompt_val:
                with st.spinner("Making it professional..."):
                    enhance_query = f"Expand this simple prompt into a highly detailed, cinematic, professional grade image generation prompt. Output only the enhanced prompt in English: {st.session_state.img_prompt_val}"
                    try:
                        enhanced_resp = model.generate_content(enhance_query)
                        st.session_state.img_prompt_val = enhanced_resp.text
                    except:
                        pass

    # प्रॉम्ट इनपुट एरिया
    default_prompt = st.session_state.get("img_prompt_val", "")
    img_prompt = st.text_area("Describe what you want to create:", value=default_prompt, placeholder="Type your imagination...")
    st.session_state.img_prompt_val = img_prompt

    # सेटिंग्स पैनल्स (ड्रॉपडाउन)
    col1, col2, col3 = st.columns(3)
    with col1:
        style = st.selectbox("Choose Style", ["Hyper-Realistic", "Anime", "3D Cinematic", "Cyberpunk", "Watercolor"])
    with col2:
        aspect_ratio = st.selectbox("Aspect Ratio", ["1:1 (Square)", "9:16 (Reels)", "2:3 (Ebook/Poster)", "16:9 (Landscape)"])
    with col3:
        num_images = st.selectbox("Images Count", [1, 2, 4])
        
    if st.button("Generate Art", key="img_btn") and img_prompt:
        with st.spinner("Generating..."):
            # प्रॉम्ट के साथ स्टाइल जोड़ना
            final_prompt = f"{img_prompt}, {style} style, aspect ratio {aspect_ratio}"
            encoded_prompt = requests.utils.quote(final_prompt)
            
            # ग्रिड लेआउट में इमेज दिखाना
            cols_grid = st.columns(2)
            for i in range(num_images):
                seed = random.randint(1, 99999)
                image_url = f"https://image.pollinations.ai/p/{encoded_prompt}?width=1024&height=1024&nologo=true&seed={seed}"
                
                with cols_grid[i % 2]:
                    st.image(image_url, caption=f"Design {i+1}", use_container_width=True)
