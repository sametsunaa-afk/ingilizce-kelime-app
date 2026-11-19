import streamlit as st
import json
import os
import random
import difflib
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
    .score-box {
        background-color: #FFFFFF !important;
        border-radius: 20px;
        padding: 32px 24px;
        box-shadow: 0 8px 24px rgba(27, 67, 50, 0.12);
        border: 2px solid #2D6A4F;
        text-align: center;
        margin: 20px 0;
    }
    .score-big {
        font-size: 3rem;
        font-weight: 800;
        color: #1B4332 !important;
        margin: 10px 0;
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
        {"en": "Hesitate", "tr": "tereddüt etmek, duraksamak", "ex_en": "Please do not hesitate to call me if you need help.", "ex_tr": "Yardıma ihtiyacın olursa beni aramaktan çekinme."},
        {"en": "Reluctant", "tr": "isteksiz, gönülsüz", "ex_en": "He was reluctant to admit that he was wrong.", "ex_tr": "Hatalı olduğunu kabul etmekte isteksizdi."},
        {"en": "Ambitious", "tr": "hırslı, iddialı", "ex_en": "She is an ambitious young lawyer.", "ex_tr": "O, hırslı bir genç avukattır."},
        {"en": "Compromise", "tr": "uzlaşma, orta yol (bulmak)", "ex_en": "In a marriage, both partners must learn to compromise.", "ex_tr": "Evlilikte her iki taraf da uzlaşmayı öğrenmelidir."},
        {"en": "Regret", "tr": "pişman olmak, pişmanlık", "ex_en": "I regret not studying harder for the exam.", "ex_tr": "Sınava daha sıkı çalışmadığıma pişmanım."},
        {"en": "Inevitable", "tr": "kaçınılmaz", "ex_en": "Change is an inevitable part of life.", "ex_tr": "Değişim hayatın kaçınılmaz bir parçasıdır."},
        {"en": "Persuade", "tr": "ikna etmek", "ex_en": "I finally managed to persuade him to come with us.", "ex_tr": "Sonunda onu bizimle gelmeye ikna etmeyi başardım."},
        {"en": "Feasible", "tr": "uygulanabilir, yapılabilir", "ex_en": "Your plan sounds great, but is it economically feasible?", "ex_tr": "Planın kulağa harika geliyor ama ekonomik olarak uygulanabilir mi?"},
        {"en": "Setback", "tr": "aksilik, engel, gerileme", "ex_en": "The bad weather was a major setback for the construction.", "ex_tr": "Kötü hava koşulları inşaat için büyük bir aksilik oldu."},
        {"en": "Anticipate", "tr": "öngörmek, önceden tahmin etmek", "ex_en": "We anticipate that ticket sales will increase next month.", "ex_tr": "Gelecek ay bilet satışlarının artacağını öngörüyoruz."}
    ],
    "B2": [
        {"en": "Meticulous", "tr": "titiz, özenli", "ex_en": "She is meticulous about keeping accurate records.", "ex_tr": "Doğru kayıtlar tutma konusunda çok titizdir."},
        {"en": "Ephemeral", "tr": "geçici, kısa ömürlü", "ex_en": "Fame in the social media age is often ephemeral.", "ex_tr": "Sosyal medya çağında şöhret genellikle kısa ömürlüdür."},
        {"en": "Resilient", "tr": "dirençli, dayanıklı", "ex_en": "Children are often more resilient than adults think.", "ex_tr": "Çocuklar genellikle yetişkinlerin düşündüğünden daha dayanıklıdır."},
        {"en": "Arbitrary", "tr": "keyfi, rastgele", "ex_en": "The decision seemed completely arbitrary and unfair.", "ex_tr": "Karar tamamen keyfi ve adaletsiz görünüyordu."},
        {"en": "Pragmatic", "tr": "pragmatik, gerçekçi", "ex_en": "We need a pragmatic approach to solve this budget issue.", "ex_tr": "Bu bütçe sorununu çözmek için gerçekçi bir yaklaşıma ihtiyacımız var."},
        {"en": "Redundant", "tr": "gereksiz, fazlalık", "ex_en": "Remove any redundant words to make your essay clearer.", "ex_tr": "Makaleni daha net hale getirmek için gereksiz kelimeleri çıkar."},
        {"en": "Tenuous", "tr": "zayıf, belirsiz", "ex_en": "The connection between the two events is very tenuous.", "ex_tr": "İki olay arasındaki bağlantı çok zayıf."},
        {"en": "Discern", "tr": "ayırt etmek, fark etmek", "ex_en": "It is difficult to discern the truth from his story.", "ex_tr": "Onun hikayesinden gerçeği ayırt etmek zor."},
        {"en": "Exacerbate", "tr": "kötüleştirmek, şiddetlendirmek", "ex_en": "Loud noise will only exacerbate my headache.", "ex_tr": "Yüksek gürültü baş ağrımı daha da şiddetlendirecek."},
        {"en": "Eloquent", "tr": "güzel ve etkili konuşan", "ex_en": "She gave an eloquent speech that moved the audience.", "ex_tr": "Dinleyicileri etkileyen güzel ve etkili bir konuşma yaptı."},
        {"en": "Bring about", "tr": "neden olmak, meydana getirmek", "ex_en": "New technology has brought about huge changes in education.", "ex_tr": "Yeni teknoloji eğitimde büyük değişiklikler meydana getirdi."},
        {"en": "Ubiquitous", "tr": "her yerde bulunan, yaygın", "ex_en": "Coffee shops have become ubiquitous in modern cities.", "ex_tr": "Kahve dükkanları modern şehirlerde her yerde bulunur hale geldi."},
        {"en": "Ambivalent", "tr": "kararsız, ikircikli", "ex_en": "Many people feel ambivalent about working from home.", "ex_tr": "Birçok insan evden çalışma konusunda ikircikli hissediyor."},
        {"en": "Candid", "tr": "açık sözlü, dürüst", "ex_en": "Thank you for your candid feedback on my design.", "ex_tr": "Tasarımım hakkındaki açık sözlü geri bildirimin için teşekkür ederim."},
        {"en": "Innate", "tr": "doğuştan gelen", "ex_en": "She has an innate talent for music and rhythm.", "ex_tr": "Müzik ve ritim konusunda doğuştan gelen bir yeteneği var."},
        {"en": "Dexterous", "tr": "becerikli, usta", "ex_en": "Surgeons need to be extremely dexterous with their hands.", "ex_tr": "Cerrahların ellerini son derece ustalıkla kullanmaları gerekir."},
        {"en": "Conducive", "tr": "elverişli, uygun", "ex_en": "A quiet room is more conducive to studying.", "ex_tr": "Sessiz bir oda ders çalışmak için daha elverişlidir."},
        {"en": "Pertinent", "tr": "ilgili, alakalı", "ex_en": "Please ask questions that are pertinent to the topic.", "ex_tr": "Lütfen konuyla alakalı sorular sorun."},
        {"en": "Plausible", "tr": "makul, akla yatkın", "ex_en": "Her explanation sounded completely plausible.", "ex_tr": "Açıklaması kulağa tamamen akla yatkın geliyordu."},
        {"en": "Compelling", "tr": "ikna edici, sürükleyici", "ex_en": "The lawyer presented a compelling argument.", "ex_tr": "Avukat ikna edici bir argüman sundu."}
    ]
}

def load_words():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(INITIAL_DATA, f, ensure_ascii=False, indent=4)
        return INITIAL_DATA
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            if len(data.get("B1", [])) < 4 or len(data.get("B2", [])) < 4:
                return INITIAL_DATA
            return data
    except Exception:
        return INITIAL_DATA

def save_words(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

@st.cache_data(show_spinner=False)
def generate_audio(text):
    clean_text = text.split("(")[0].strip()
    tts = gTTS(text=clean_text, lang='en', slow=False)
    fp = BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)
    return fp.read()

def check_sentence_similarity(user_text, ref_text):
    u = "".join(c.lower() for c in user_text if c.isalnum() or c.isspace()).split()
    r = "".join(c.lower() for c in ref_text if c.isalnum() or c.isspace()).split()
    if not u:
        return 0.0
    ratio = difflib.SequenceMatcher(None, " ".join(u), " ".join(r)).ratio()
    return ratio

# --- SESSION STATE YÖNETİMİ ---
if "words_db" not in st.session_state:
    st.session_state.words_db = load_words()

if "current_level" not in st.session_state:
    st.session_state.current_level = "B1"

if "card_index" not in st.session_state:
    st.session_state.card_index = 0

if "cards_viewed_count" not in st.session_state:
    st.session_state.cards_viewed_count = 1

if "card_mode" not in st.session_state:
    st.session_state.card_mode = "EN_TO_TR"

if "show_meaning" not in st.session_state:
    st.session_state.show_meaning = False

def get_next_card_mode(count):
    # Her 10 kelimede bir (10, 20, 30...) cümle yazma pratiği gelsin
    if count % 10 == 0:
        return random.choice(["SENT_EN_TO_TR", "SENT_TR_TO_EN"])
    return random.choice(["EN_TO_TR", "TR_TO_EN"])

def reset_card_state(new_index):
    st.session_state.card_index = new_index
    st.session_state.show_meaning = False
    st.session_state.cards_viewed_count += 1
    st.session_state.card_mode = get_next_card_mode(st.session_state.cards_viewed_count)

# --- 10 SORULUK QUIZ OLUŞTURUCU ---
def init_quiz_session(level):
    word_list = st.session_state.words_db[level]
    sample_size = min(10, len(word_list))
    selected_words = random.sample(word_list, sample_size)
    
    questions = []
    # Sadece 5. ve 10. sorular (indeks 4 ve 9) cümle çevirisi olsun, diğerleri kelime sorusu
    for idx, target in enumerate(selected_words):
        if idx in [4, 9]:
            q_type = random.choice(["SENT_EN_TO_TR", "SENT_TR_TO_EN"])
            source_sent = target["ex_en"] if q_type == "SENT_EN_TO_TR" else target["ex_tr"]
            ref_trans = target["ex_tr"] if q_type == "SENT_EN_TO_TR" else target["ex_en"]
            questions.append({
                "word": target,
                "q_type": q_type,
                "source_sentence": source_sent,
                "reference_translation": ref_trans,
                "answered": False,
                "is_correct": None,
                "user_input": ""
            })
        else:
            q_type = random.choice(["EN_TO_TR", "TR_TO_EN"])
            if q_type == "EN_TO_TR":
                wrong_pool = [w["tr"] for w in word_list if w["en"] != target["en"]]
                wrong_choices = random.sample(wrong_pool, min(3, len(wrong_pool)))
                correct_answer = target["tr"]
            else:
                wrong_pool = [w["en"] for w in word_list if w["tr"] != target["tr"]]
                wrong_choices = random.sample(wrong_pool, min(3, len(wrong_pool)))
                correct_answer = target["en"]
            options = wrong_choices + [correct_answer]
            random.shuffle(options)
            questions.append({
                "word": target,
                "q_type": q_type,
                "correct_answer": correct_answer,
                "options": options,
                "answered": False,
                "selected": None,
                "is_correct": None
            })
            
    st.session_state.quiz_questions = questions
    st.session_state.quiz_current_idx = 0
    st.session_state.quiz_score = 0
    st.session_state.quiz_finished = False

if "quiz_questions" not in st.session_state:
    init_quiz_session(st.session_state.current_level)

# --- ARAYÜZ BAŞLANGICI ---
st.markdown('<div class="main-title">🌿 VocabMaster</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">B1 & B2 İnteraktif Kelime ve Cümle Pratiği</div>', unsafe_allow_html=True)

col_lvl1, col_lvl2 = st.columns(2)
with col_lvl1:
    if st.button("📘 B1 Seviyesi (" + str(len(st.session_state.words_db["B1"])) + " Kelime)"):
        st.session_state.current_level = "B1"
        st.session_state.card_index = 0
        st.session_state.cards_viewed_count = 1
        st.session_state.card_mode = "EN_TO_TR"
        st.session_state.show_meaning = False
        init_quiz_session("B1")
        st.rerun()
with col_lvl2:
    if st.button("📗 B2 Seviyesi (" + str(len(st.session_state.words_db["B2"])) + " Kelime)"):
        st.session_state.current_level = "B2"
        st.session_state.card_index = 0
        st.session_state.cards_viewed_count = 1
        st.session_state.card_mode = "EN_TO_TR"
        st.session_state.show_meaning = False
        init_quiz_session("B2")
        st.rerun()

level = st.session_state.current_level
words = st.session_state.words_db[level]

st.info(f"Şu an seçili kur: **{level} Seviyesi**")

tab1, tab2, tab3, tab4 = st.tabs(["🗂️ Kelime Kartları", "🎯 10 Soruluk Quiz", "➕ Yeni Kelime Ekle", "📋 Tüm Liste"])

# --- SEKME 1: KELİME KARTLARI ---
with tab1:
    if len(words) > 0:
        if st.session_state.card_index >= len(words):
            st.session_state.card_index = 0
            
        current_word = words[st.session_state.card_index]
        mode = st.session_state.card_mode
        
        progress = (st.session_state.card_index + 1) / len(words)
        st.progress(progress)
        
        kalan_yazma = 10 - (st.session_state.cards_viewed_count % 10)
        if kalan_yazma == 10:
            st.caption(f"Kart {st.session_state.card_index + 1} / {len(words)} • ✍️ **Cümle Yazma Pratiği Kartı!**")
        else:
            st.caption(f"Kart {st.session_state.card_index + 1} / {len(words)} • Sonraki yazma pratiğine {kalan_yazma} kart kaldı")

        # --- DURUM A: KELİME KARTI ---
        if mode in ["EN_TO_TR", "TR_TO_EN"]:
            if mode == "EN_TO_TR":
                badge_text = "🇬🇧 İngilizce ➔ 🇹🇷 Türkçe (Kelime)"
                question_text = current_word["en"]
                answer_text = current_word["tr"]
                hint_text = "Türkçe anlamını görmek için aşağıdaki butona dokun 👇"
            else:
                badge_text = "🇹🇷 Türkçe ➔ 🇬🇧 İngilizce (Kelime)"
                question_text = current_word["tr"]
                answer_text = current_word["en"]
                hint_text = "İngilizce karşılığını görmek için aşağıdaki butona dokun 👇"

            answer_html = f'<div class="word-answer">{answer_text}</div>' if st.session_state.show_meaning else f'<div style="color:#52796F; font-weight:500; margin-top:10px;">{hint_text}</div>'
            
            example_html = ""
            if current_word.get("ex_en"):
                if mode == "EN_TO_TR":
                    ex_tr_display = current_word.get("ex_tr", "") if st.session_state.show_meaning else "<i>(Türkçe çeviri gizli)</i>"
                    example_html = f'<div class="example-box"><div class="example-en">"{current_word["ex_en"]}"</div><div class="example-tr">{ex_tr_display}</div></div>'
                else:
                    if st.session_state.show_meaning:
                        example_html = f'<div class="example-box"><div class="example-en">"{current_word["ex_en"]}"</div><div class="example-tr">{current_word.get("ex_tr", "")}</div></div>'

            card_html = f'<div class="word-card"><div class="lang-badge">{badge_text}</div><div class="word-main">{question_text}</div>{answer_html}{example_html}</div>'
            st.markdown(card_html, unsafe_allow_html=True)

            if mode == "EN_TO_TR" or st.session_state.show_meaning:
                col_audio1, col_audio2 = st.columns(2)
                with col_audio1:
                    if st.button("🔊 Kelimeyi Dinle", key="listen_word"):
                        st.audio(generate_audio(current_word["en"]), format="audio/mp3", autoplay=True)
                with col_audio2:
                    if current_word.get("ex_en"):
                        if st.button("🗣️ Cümleyi Dinle", key="listen_sent"):
                            st.audio(generate_audio(current_word["ex_en"]), format="audio/mp3", autoplay=True)

            st.write("")
            btn_label = "🙈 Cevabı Gizle" if st.session_state.show_meaning else "👀 Cevabı Göster"
            if st.button(btn_label, key="toggle_meaning"):
                st.session_state.show_meaning = not st.session_state.show_meaning
                st.rerun()

        # --- DURUM B: HER 10 KELİMEDE BİR GELEN CÜMLE YAZMA KARTI ---
        else:
            if mode == "SENT_EN_TO_TR":
                badge_text = "✍️ Cümle Çevirisi (10 Kartta 1): 🇬🇧 İngilizce ➔ 🇹🇷 Türkçe"
                instruction = "Aşağıdaki İngilizce cümleyi Türkçeye çevir:"
                source_sentence = current_word["ex_en"]
                reference_text = current_word["ex_tr"]
            else:
                badge_text = "✍️ Cümle Çevirisi (10 Kartta 1): 🇹🇷 Türkçe ➔ 🇬🇧 İngilizce"
                instruction = "Aşağıdaki Türkçe cümleyi İngilizceye çevir:"
                source_sentence = current_word["ex_tr"]
                reference_text = current_word["ex_en"]

            card_html = f'<div class="word-card"><div class="lang-badge">{badge_text}</div><div style="font-size:0.95rem; color:#52796F; font-weight:600; margin-top:4px;">{instruction}</div><div class="sentence-main">"{source_sentence}"</div></div>'
            st.markdown(card_html, unsafe_allow_html=True)

            if mode == "SENT_EN_TO_TR":
                if st.button("🔊 Cümleyi Dinle", key="listen_ai_sent"):
                    st.audio(generate_audio(source_sentence), format="audio/mp3", autoplay=True)

            st.text_area("Çevirini buraya yaz:", key=f"card_input_{st.session_state.cards_viewed_count}", height=85, placeholder="Cümlenizi buraya yazabilirsiniz...")
            
            show_ref_key = f"show_ref_{st.session_state.cards_viewed_count}"
            if show_ref_key not in st.session_state:
                st.session_state[show_ref_key] = False

            btn_ref_label = "🙈 Doğru Cevabı Gizle" if st.session_state[show_ref_key] else "👀 Doğru Cevabı Göster"
            if st.button(btn_ref_label, key="btn_toggle_ref"):
                st.session_state[show_ref_key] = not st.session_state[show_ref_key]
                st.rerun()

            if st.session_state[show_ref_key]:
                st.info(f"💡 **Örnek Doğru Çeviri:**\n\n{reference_text}\n\n🎯 **İçerdiği Hedef Kelime:** {current_word['en']} ({current_word['tr']})")
                if mode == "SENT_TR_TO_EN":
                    if st.button("🔊 Doğru İngilizce Cümleyi Dinle", key="listen_ideal_card"):
                        st.audio(generate_audio(reference_text), format="audio/mp3", autoplay=True)

        st.write("")
        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button("⬅️ Önceki"):
                reset_card_state((st.session_state.card_index - 1) % len(words))
                st.rerun()
        with c2:
            if st.button("🎲 Rastgele"):
                reset_card_state(random.randint(0, len(words) - 1))
                st.rerun()
        with c3:
            if st.button("Sonraki ➡️"):
                reset_card_state((st.session_state.card_index + 1) % len(words))
                st.rerun()

# --- SEKME 2: 10 SORULUK MINI QUIZ ---
with tab2:
    questions = st.session_state.quiz_questions
    total_q = len(questions)
    
    # QUIZ TAMAMLANDIYSA SONUÇ EKRANI
    if st.session_state.quiz_finished:
        score = st.session_state.quiz_score
        percent = int((score / total_q) * 100)
        
        if percent >= 80:
            emoji_title = "🏆 Harika İş Çıkardın!"
            msg = "Kelime bilgin çok sağlam görünüyor!"
        elif percent >= 50:
            emoji_title = "👍 Güzel Çaba!"
            msg = "Biraz daha tekrarla mükemmel olacak."
        else:
            emoji_title = "📚 Tekrar Zamanı!"
            msg = "Kelime kartlarına biraz daha göz atıp tekrar deneyebilirsin."

        st.markdown(f"""
        <div class="score-box">
            <div style="font-size: 1.4rem; font-weight: 700; color: #2D6A4F;">{emoji_title}</div>
            <div class="score-big">{score} / {total_q}</div>
            <div style="font-size: 1.15rem; font-weight: 600; color: #1B4332;">Başarı Oranı: %{percent}</div>
            <p style="margin-top: 10px;">{msg}</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🔄 Yeni 10 Soruluk Quiz Başlat", key="restart_quiz"):
            init_quiz_session(level)
            st.rerun()

    # QUIZ DEVAM EDİYORSA
    else:
        idx = st.session_state.quiz_current_idx
        q = questions[idx]
        q_word = q["word"]
        q_type = q["q_type"]
        
        st.progress((idx + 1) / total_q)
        st.caption(f"Soru **{idx + 1} / {total_q}** • Mevcut Doğru Sayısı: **{st.session_state.quiz_score}**")
        
        # --- DURUM A: ÇOKTAN SEÇMELİ KELİME ---
        if q_type in ["EN_TO_TR", "TR_TO_EN"]:
            if q_type == "EN_TO_TR":
                q_badge = "🇬🇧 İngilizce ➔ 🇹🇷 Türkçe (Kelime)"
                q_prompt = "Bu kelimenin Türkçe karşılığı nedir?"
                q_display = q_word["en"]
            else:
                q_badge = "🇹🇷 Türkçe ➔ 🇬🇧 İngilizce (Kelime)"
                q_prompt = "Bu ifadenin İngilizce karşılığı nedir?"
                q_display = q_word["tr"]
            
            quiz_card_html = f'<div class="word-card" style="padding: 20px;"><div class="lang-badge">{q_badge}</div><div style="font-size: 0.95rem; color: #52796F; font-weight: 600;">{q_prompt}</div><div class="word-main" style="font-size: 1.9rem; margin-top: 8px;">{q_display}</div></div>'
            st.markdown(quiz_card_html, unsafe_allow_html=True)
            
            if q_type == "EN_TO_TR" or q["answered"]:
                if st.button("🔊 İngilizce Telaffuzunu Dinle", key=f"quiz_audio_{idx}"):
                    st.audio(generate_audio(q_word["en"]), format="audio/mp3", autoplay=True)
                
            st.write("")
            for opt_i, opt in enumerate(q["options"]):
                if st.button(opt, key=f"q_{idx}_opt_{opt_i}", disabled=q["answered"]):
                    q["answered"] = True
                    q["selected"] = opt
                    if opt == q["correct_answer"]:
                        q["is_correct"] = True
                        st.session_state.quiz_score += 1
                    else:
                        q["is_correct"] = False
                    st.rerun()
                    
            if q["answered"]:
                if q["is_correct"]:
                    st.success(f"✅ Doğru! Cevap: **{q['correct_answer']}**")
                else:
                    st.error(f"❌ Yanlış! Senin seçimin: {q['selected']} | Doğru cevap: **{q['correct_answer']}**")
                    
                if q_word.get("ex_en"):
                    st.info(f"💡 **Örnek Cümle:** {q_word['ex_en']}\n\n*{q_word.get('ex_tr', '')}*")
                    
                next_label = "Sonuçları Gör 🏁" if idx == total_q - 1 else "Sonraki Soruya Geç ➡️"
                if st.button(next_label, key=f"next_mc_{idx}"):
                    if idx == total_q - 1:
                        st.session_state.quiz_finished = True
                    else:
                        st.session_state.quiz_current_idx += 1
                    st.rerun()

        # --- DURUM B: CÜMLE YAZMA SORUSU (SADECE 5. VE 10. SORULAR) ---
        else:
            if q_type == "SENT_EN_TO_TR":
                q_badge = "✍️ Cümle Çevirisi: 🇬🇧 İngilizce ➔ 🇹🇷 Türkçe"
                q_prompt = "Bu İngilizce cümleyi Türkçeye çevir:"
            else:
                q_badge = "✍️ Cümle Çevirisi: 🇹🇷 Türkçe ➔ 🇬🇧 İngilizce"
                q_prompt = "Bu Türkçe cümleyi İngilizceye çevir:"

            quiz_card_html = f'<div class="word-card" style="padding: 20px;"><div class="lang-badge">{q_badge}</div><div style="font-size: 0.95rem; color: #52796F; font-weight: 600; margin-top:4px;">{q_prompt}</div><div class="sentence-main">"{q["source_sentence"]}"</div></div>'
            st.markdown(quiz_card_html, unsafe_allow_html=True)

            if q_type == "SENT_EN_TO_TR":
                if st.button("🔊 Cümleyi Dinle", key=f"quiz_sent_audio_{idx}"):
                    st.audio(generate_audio(q["source_sentence"]), format="audio/mp3", autoplay=True)

            user_ans = st.text_area("Çevirini buraya yaz:", value=q["user_input"], key=f"quiz_txt_{idx}", height=85, disabled=q["answered"])

            if not q["answered"]:
                if st.button("👀 Cevabı Kontrol Et", key=f"check_sent_{idx}"):
                    q["user_input"] = user_ans
                    q["answered"] = True
                    # Yazılan cümle boşsa veya benzerlik çok düşükse otomatik yanlış işaretle
                    sim = check_sentence_similarity(user_ans, q["reference_translation"])
                    if not user_ans.strip() or sim < 0.45:
                        q["is_correct"] = False
                    else:
                        q["is_correct"] = True
                        st.session_state.quiz_score += 1
                    st.rerun()

            if q["answered"]:
                if q["is_correct"]:
                    st.success("✅ Doğru / Çok Yakın Çeviri!")
                else:
                    if not q["user_input"].strip():
                        st.error("❌ Yanlış! Herhangi bir çeviri yazmadınız.")
                    else:
                        st.error("❌ Yanlış / Eksik Çeviri! Aşağıdaki doğru örnekle karşılaştırabilirsiniz.")

                st.info(f"💡 **Örnek Doğru Cevap:**\n\n{q['reference_translation']}\n\n🎯 **Test Edilen Kelime:** {q_word['en']} ({q_word['tr']})")
                
                # Kullanıcı kendi değerlendirmesini düzeltmek isterse diye opsiyonel buton
                col_fix1, col_fix2 = st.columns(2)
                with col_fix1:
                    if not q["is_correct"]:
                        if st.button("Aslında Doğru Yazdım (+1 Puan)", key=f"override_true_{idx}"):
                            q["is_correct"] = True
                            st.session_state.quiz_score += 1
                            st.rerun()
                with col_fix2:
                    if q["is_correct"]:
                        if st.button("Aslında Yanlış Yazdım (-1 Puan)", key=f"override_false_{idx}"):
                            q["is_correct"] = False
                            st.session_state.quiz_score -= 1
                            st.rerun()

                if q_type == "SENT_TR_TO_EN":
                    if st.button("🔊 Doğru İngilizce Cümleyi Dinle", key=f"listen_ideal_quiz_{idx}"):
                        st.audio(generate_audio(q["reference_translation"]), format="audio/mp3", autoplay=True)

                next_label = "Sonuçları Gör 🏁" if idx == total_q - 1 else "Sonraki Soruya Geç ➡️"
                if st.button(next_label, key=f"next_sent_{idx}"):
                    if idx == total_q - 1:
                        st.session_state.quiz_finished = True
                    else:
                        st.session_state.quiz_current_idx += 1
                    st.rerun()

# --- SEKME 3: YENİ KELİME EKLEME MENÜSÜ ---
with tab3:
    st.markdown("### ➕ Sözlüğe Yeni Kelime Ekle")
    st.write("Derste öğrendiğiniz yeni kelimeleri buradan sisteme ekleyebilirsiniz.")
    
    with st.form("add_word_form", clear_on_submit=True):
        target_lvl = st.selectbox("Hangi Kura Eklensin?", ["B1", "B2"], index=0 if level == "B1" else 1)
        new_en = st.text_input("İngilizce Kelime / Kalıp *", placeholder="Örn: Resilient")
        new_tr = st.text_input("Türkçe Anlamı *", placeholder="Örn: dirençli, dayanıklı")
        new_ex_en = st.text_input("Örnek İngilizce Cümle (İsteğe Bağlı)", placeholder="Örn: She is a very resilient person.")
        new_ex_tr = st.text_input("Örnek Cümlenin Türkçesi (İsteğe Bağlı)", placeholder="Örn: O çok dayanıklı bir insandır.")
        
        submitted = st.form_submit_button("💾 Kelimeyi Kaydet")
        if submitted:
            if new_en.strip() and new_tr.strip():
                final_ex_en = new_ex_en.strip() if new_ex_en.strip() else f"We learned the word '{new_en.strip()}' in our English class today."
                final_ex_tr = new_ex_tr.strip() if new_ex_tr.strip() else f"Bugün İngilizce dersimizde '{new_en.strip()}' kelimesini öğrendik."
                
                new_entry = {
                    "en": new_en.strip(),
                    "tr": new_tr.strip(),
                    "ex_en": final_ex_en,
                    "ex_tr": final_ex_tr
                }
                st.session_state.words_db[target_lvl].append(new_entry)
                save_words(st.session_state.words_db)
                st.success(f"✅ **{new_en}** başarıyla **{target_lvl}** listesine eklendi!")
            else:
                st.warning("⚠️ Lütfen en azından İngilizce kelime ve Türkçe anlamı alanlarını doldurun.")

# --- SEKME 4: TÜM KELİME LİSTESİ ---
with tab4:
    st.markdown(f"### 📋 {level} Seviyesi Tüm Kelimeler ({len(words)} Adet)")
    search_term = st.text_input("🔍 Kelime Ara...", placeholder="İngilizce veya Türkçe yazın...")
    
    for i, w in enumerate(words):
        if search_term.lower() in w["en"].lower() or search_term.lower() in w["tr"].lower():
            with st.expander(f"**{w['en']}** — {w['tr']}"):
                st.write(f"🇬🇧 *{w.get('ex_en', '')}*")
                st.write(f"🇹🇷 {w.get('ex_tr', '')}")
                if st.button("🔊 Dinle", key=f"list_audio_{level}_{i}"):
                    st.audio(generate_audio(w["en"]), format="audio/mp3", autoplay=True)
