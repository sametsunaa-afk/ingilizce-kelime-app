import streamlit as st
import json
import os
import random
from io import BytesIO
from gtts import gTTS

# Sayfa Ayarları
st.set_page_config(
    page_title="VocabMaster | B1 & B2",
    page_icon="🌿",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Özel CSS Tasarımı
st.markdown("""
<style>
    .stApp {
        background-color: #F4F7F5 !important;
        color: #1B4332 !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .main-title {
        color: #1B4332 !important;
        text-align: center;
        font-weight: 800;
        font-size: 2.2rem;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        color: #2D6A4F !important;
        text-align: center;
        font-size: 1rem;
        font-weight: 500;
        margin-bottom: 1.5rem;
    }
    p, label, .stCaption, div[data-testid="stCaptionContainer"] {
        color: #2D6A4F !important;
        font-weight: 500;
    }
    .word-card {
        background-color: #FFFFFF !important;
        border-radius: 20px;
        padding: 28px 22px;
        box-shadow: 0 8px 24px rgba(27, 67, 50, 0.1);
        border-top: 6px solid #2D6A4F;
        text-align: center;
        margin-bottom: 20px;
    }
    .lang-badge {
        display: inline-block;
        background-color: #EBF5EE;
        color: #2D6A4F !important;
        font-size: 0.82rem;
        font-weight: 700;
        padding: 4px 14px;
        border-radius: 20px;
        margin-bottom: 12px;
        border: 1px solid #B7E4C7;
    }
    .word-main {
        color: #1B4332 !important;
        font-size: 2rem;
        font-weight: 700;
        margin-bottom: 10px;
        line-height: 1.3;
    }
    .sentence-main {
        color: #1B4332 !important;
        font-size: 1.35rem;
        font-weight: 600;
        margin: 14px 0;
        line-height: 1.45;
    }
    .word-answer {
        color: #1B4332 !important;
        font-size: 1.35rem;
        font-weight: 700;
        background-color: #D8F3DC !important;
        padding: 10px 20px;
        border-radius: 12px;
        display: inline-block;
        margin-top: 10px;
    }
    .example-box {
        background-color: #EBF5EE !important;
        border-left: 5px solid #2D6A4F;
        padding: 16px;
        border-radius: 10px;
        text-align: left;
        margin-top: 20px;
    }
    .example-en {
        color: #1B4332 !important;
        font-size: 1.05rem;
        font-weight: 600;
        font-style: italic;
    }
    .example-tr {
        color: #40916C !important;
        font-size: 0.95rem;
        margin-top: 6px;
    }
    div.stButton > button {
        background-color: #2D6A4F !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.6rem 1.2rem !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        transition: all 0.2s ease-in-out !important;
        width: 100%;
        box-shadow: 0 4px 6px rgba(45, 106, 79, 0.2) !important;
    }
    div.stButton > button p {
        color: #FFFFFF !important;
    }
    div.stButton > button:hover {
        background-color: #1B4332 !important;
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(27, 67, 50, 0.3) !important;
    }
    div.stButton > button:disabled {
        background-color: #A3B18A !important;
        opacity: 0.75;
    }
    .stTextInput input, .stTextArea textarea {
        background-color: #FFFFFF !important;
        color: #1B4332 !important;
        border: 2px solid #74C69D !important;
        border-radius: 12px !important;
        font-size: 1.05rem !important;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        justify-content: center;
        flex-wrap: wrap;
        border-bottom: 2px solid #B7E4C7;
        padding-bottom: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #D8F3DC !important;
        border-radius: 10px !important;
        color: #1B4332 !important;
        font-weight: 700 !important;
        padding: 8px 16px !important;
        border: 1px solid #95D5B2 !important;
    }
    .stTabs [data-baseweb="tab"] p {
        color: #1B4332 !important;
        font-weight: 700 !important;
    }
    .stTabs [aria-selected="true"] {
        background-color: #2D6A4F !important;
        border-color: #1B4332 !important;
    }
    .stTabs [aria-selected="true"] p {
        color: #FFFFFF !important;
    }
    .stTabs [data-baseweb="tab-highlight"] {
        background-color: #1B4332 !important;
    }
</style>
""", unsafe_allow_html=True)

DATA_FILE = "kelimeler.json"

INITIAL_DATA = {
    "B1": [
        {"en": "Reckless", "tr": "pervasız, düşüncesizce riskli", "ex_en": "He was fined for reckless driving on the highway.", "ex_tr": "Otoyolda pervasızca araç kullanmaktan ceza yedi."},
        {"en": "Overlook", "tr": "gözden kaçırmak", "ex_en": "It is easy to overlook small details when you are tired.", "ex_tr": "Yorgun olduğunda küçük detayları gözden kaçırmak kolaydır."},
        {"en": "Deliberately", "tr": "kasıtlı olarak, bile bile", "ex_en": "She deliberately left her phone at home to enjoy the peace.", "ex_tr": "Huzurun tadını çıkarmak için telefonunu kasıtlı olarak evde bıraktı."},
        {"en": "Thorough", "tr": "titiz, eksiksiz, kapsamlı", "ex_en": "The police carried out a thorough investigation.", "ex_tr": "Polis kapsamlı bir soruşturma yürüttü."},
        {"en": "Assumption", "tr": "varsayım", "ex_en": "We shouldn't make assumptions without seeing the evidence.", "ex_tr": "Kanıtları görmeden varsayımlarda bulunmamalıyız."},
        {"en": "Conceal", "tr": "gizlemek, saklamak", "ex_en": "He tried to conceal his disappointment behind a smile.", "ex_tr": "Hayal kırıklığını bir gülümsemenin arkasına gizlemeye çalıştı."},
        {"en": "Crucial", "tr": "hayati, kritik, çok önemli", "ex_en": "Drinking enough water is crucial for your health.", "ex_tr": "Yeterince su içmek sağlığınız için hayati önem taşır."},
        {"en": "Scrutinize", "tr": "dikkatle incelemek, didik didik etmek", "ex_en": "Lawyers will scrutinize every word of the contract.", "ex_tr": "Avukatlar sözleşmenin her kelimesini dikkatle inceleyecek."},
        {"en": "Vulnerable", "tr": "savunmasız, kırılgan", "ex_en": "Young birds are very vulnerable to predators.", "ex_tr": "Yavru kuşlar yırtıcılara karşı çok savunmasızdır."},
        {"en": "Consequence", "tr": "sonuç (çoğu zaman olumsuz)", "ex_en": "Every action has a consequence.", "ex_tr": "Her eylemin bir sonucu vardır."},
        {"en": "Own up (to)", "tr": "suçunu itiraf etmek, kabullenmek", "ex_en": "Nobody owned up to breaking the window.", "ex_tr": "Kimse camı kırdığını itiraf etmedi."},
        {"en": "Cover up", "tr": "örtbas etmek", "ex_en": "The company tried to cover up the financial scandal.", "ex_tr": "Şirket finansal skandalı örtbas etmeye çalıştı."},
        {"en": "Jump to conclusions", "tr": "aceleyle yargıya varmak", "ex_en": "Don't jump to conclusions before hearing her side of the story.", "ex_tr": "Hikayenin bir de onun tarafını dinlemeden aceleyle yargıya varma."},
        {"en": "Take something into account", "tr": "hesaba katmak, göz önünde bulundurmak", "ex_en": "You must take traffic into account when planning your trip.", "ex_tr": "Seyahatini planlarken trafiği hesaba katmalısın."},
        {"en": "Draw a conclusion", "tr": "sonuca varmak, sonuç çıkarmak", "ex_en": "It is too early to draw a conclusion from these results.", "ex_tr": "Bu sonuçlardan bir çıkarım yapmak için henüz çok erken."},
        {"en": "Get rid of", "tr": "-den kurtulmak, atmak", "ex_en": "I need to get rid of these old clothes.", "ex_tr": "Bu eski kıyafetlerden kurtulmam gerekiyor."},
        {"en": "Go through", "tr": "gözden geçirmek, incelemek", "ex_en": "Let's go through the presentation one more time.", "ex_tr": "Sunumu bir kez daha gözden geçirelim."},
        {"en": "Make an effort", "tr": "çaba göstermek", "ex_en": "You have to make an effort if you want to learn English.", "ex_tr": "İngilizce öğrenmek istiyorsan çaba göstermelisin."},
        {"en": "Take the blame", "tr": "suçu üstlenmek", "ex_en": "The manager decided to take the blame for the team's mistake.", "ex_tr": "Müdür, ekibin hatası için suçu üstlenmeye karar verdi."},
        {"en": "Come to light", "tr": "gün yüzüne çıkmak, ortaya çıkmak", "ex_en": "New evidence has recently come to light.", "ex_tr": "Son zamanlarda yeni kanıtlar gün yüzüne çıktı."},
        {"en": "Hesitate", "tr": "tereddüt etmek, duraksamak", "ex_en": "Please do not hesitate to call me if you need help.", "ex_tr": "Yardıma ihtiyacın olursa beni aramaktan çekinme (tereddüt etme)."},
        {"en": "Reluctant", "tr": "isteksiz, gönülsüz", "ex_en": "He was reluctant
