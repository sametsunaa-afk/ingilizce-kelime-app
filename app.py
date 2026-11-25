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
        font-size: 2rem;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        color: #2D6A4F !important;
        text-align: center;
        font-size: 0.95rem;
        font-weight: 500;
        margin-bottom: 1.2rem;
    }
    p, label, .stCaption, div[data-testid="stCaptionContainer"] {
        color: #2D6A4F !important;
        font-weight: 500;
    }
    .word-card {
        background-color: #FFFFFF !important;
        border-radius: 20px;
        padding: 24px 20px;
        box-shadow: 0 8px 24px rgba(27, 67, 50, 0.1);
        border-top: 6px solid #2D6A4F;
        text-align: center;
        margin-bottom: 16px;
    }
    .lang-badge {
        display: inline-block;
        background-color: #EBF5EE;
        color: #2D6A4F !important;
        font-size: 0.82rem;
        font-weight: 700;
        padding: 4px 14px;
        border-radius: 20px;
        margin-bottom: 10px;
        border: 1px solid #B7E4C7;
    }
    .word-main {
        color: #1B4332 !important;
        font-size: 1.9rem;
        font-weight: 700;
        margin-bottom: 8px;
        line-height: 1.3;
    }
    .example-box {
        background-color: #EBF5EE !important;
        border-left: 5px solid #2D6A4F;
        padding: 14px;
        border-radius: 10px;
        text-align: left;
        margin-top: 16px;
    }
    .example-en {
        color: #1B4332 !important;
        font-size: 1rem;
        font-weight: 600;
        font-style: italic;
    }
    .example-tr {
        color: #40916C !important;
        font-size: 0.92rem;
        margin-top: 5px;
    }
    div.stButton > button {
        background-color: #2D6A4F !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.6rem 1.1rem !important;
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
    }
    div.stButton > button:disabled {
        background-color: #A3B18A !important;
        opacity: 0.75;
    }
    .stTextInput input {
        background-color: #FFFFFF !important;
        color: #1B4332 !important;
        border: 2px solid #74C69D !important;
        border-radius: 12px !important;
        font-size: 1rem !important;
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
        padding: 8px 14px !important;
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
        {"en": "Compelling", "tr": "ikna edici, sürükleyici", "ex_tr": "The lawyer presented a compelling argument.", "ex_tr": "Avukat ikna edici bir argüman sundu."}
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
            if len(data.get("B1", [])) < 3 or len(data.get("B2", [])) < 3:
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

# --- KARIŞIK SIRALAMA VE 3 SEÇENEKLİ KART OLUŞTURUCU ---
def build_shuffled_deck(level):
    word_list = st.session_state.words_db[level]
    shuffled_words = random.sample(word_list, len(word_list))
    deck = []

    for target in shuffled_words:
        direction = random.choice(["EN_TO_TR", "TR_TO_EN"])
        if direction == "EN_TO_TR":
            wrong_pool = [w["tr"] for w in word_list if w["tr"] != target["tr"]]
            wrong_choices = random.sample(wrong_pool, min(2, len(wrong_pool)))
            correct_answer = target["tr"]
        else:
            wrong_pool = [w["en"] for w in word_list if w["en"] != target["en"]]
            wrong_choices = random.sample(wrong_pool, min(2, len(wrong_pool)))
            correct_answer = target["en"]

        options = wrong_choices + [correct_answer]
        random.shuffle(options)

        deck.append({
            "word": target,
            "direction": direction,
            "correct_answer": correct_answer,
            "options": options,
            "answered": False,
            "selected": None,
            "is_correct": None
        })

    return deck

def init_level_deck(level):
    st.session_state.deck = build_shuffled_deck(level)
    st.session_state.deck_pos = 0
    st.session_state.round_number = st.session_state.get("round_number", 1)

# --- SESSION STATE YÖNETİMİ ---
if "words_db" not in st.session_state:
    st.session_state.words_db = load_words()

if "current_level" not in st.session_state:
    st.session_state.current_level = "B1"

if "round_number" not in st.session_state:
    st.session_state.round_number = 1

if "deck" not in st.session_state:
    init_level_deck(st.session_state.current_level)

# --- ARAYÜZ BAŞLANGICI ---
st.markdown('<div class="main-title">🌿 VocabMaster</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">B1 & B2 Kelime Pratiği</div>', unsafe_allow_html=True)

col_lvl1, col_lvl2 = st.columns(2)
with col_lvl1:
    if st.button("📘 B1 Seviyesi (" + str(len(st.session_state.words_db["B1"])) + " Kelime)"):
        st.session_state.current_level = "B1"
        st.session_state.round_number += 1
        init_level_deck("B1")
        st.rerun()
with col_lvl2:
    if st.button("📗 B2 Seviyesi (" + str(len(st.session_state.words_db["B2"])) + " Kelime)"):
        st.session_state.current_level = "B2"
        st.session_state.round_number += 1
        init_level_deck("B2")
        st.rerun()

level = st.session_state.current_level
words = st.session_state.words_db[level]

st.info(f"Şu an seçili kur: **{level} Seviyesi**")

tab1, tab2, tab3 = st.tabs(["🗂️ Kelimeler", "➕ Yeni Kelime Ekle", "📋 Tüm Liste"])

# --- SEKME 1: 3 SEÇENEKLİ KARIŞIK KELİME KARTLARI ---
with tab1:
    deck = st.session_state.deck
    total_cards = len(deck)

    if total_cards > 0:
        pos = st.session_state.deck_pos
        if pos >= total_cards:
            pos = 0
            st.session_state.deck_pos = 0

        item = deck[pos]
        current_word = item["word"]
        direction = item["direction"]

        st.progress((pos + 1) / total_cards)
        st.caption(f"Tur {st.session_state.round_number} • Kelime {pos + 1} / {total_cards} (Karışık Sıra)")

        if direction == "EN_TO_TR":
            badge_text = "🇬🇧 İngilizce ➔ 🇹🇷 Türkçe"
            question_text = current_word["en"]
            prompt_text = "Doğru Türkçe karşılığı seç:"
        else:
            badge_text = "🇹🇷 Türkçe ➔ 🇬🇧 İngilizce"
            question_text = current_word["tr"]
            prompt_text = "Doğru İngilizce karşılığı seç:"

        example_html = ""
        if item["answered"] and current_word.get("ex_en"):
            example_html = (
                f'<div class="example-box">'
                f'<div class="example-en">"{current_word["ex_en"]}"</div>'
                f'<div class="example-tr">{current_word.get("ex_tr", "")}</div>'
                f'</div>'
            )

        card_html = (
            f'<div class="word-card">'
            f'<div class="lang-badge">{badge_text}</div>'
            f'<div style="font-size:0.9rem; color:#52796F; font-weight:600; margin-bottom:4px;">{prompt_text}</div>'
            f'<div class="word-main">{question_text}</div>'
            f'{example_html}'
            f'</div>'
        )
        st.markdown(card_html, unsafe_allow_html=True)

        # Seslendirme butonları
        if st.button("🔊 Kelimeyi Dinle", key=f"listen_word_{st.session_state.round_number}_{pos}"):
            st.audio(generate_audio(current_word["en"]), format="audio/mp3", autoplay=True)

        if item["answered"] and current_word.get("ex_en"):
            if st.button("🗣️ Örnek Cümleyi Dinle", key=f"listen_ex_{st.session_state.round_number}_{pos}"):
                st.audio(generate_audio(current_word["ex_en"]), format="audio/mp3", autoplay=True)

        st.write("")

        # 3 Seçenek
        for opt_i, opt in enumerate(item["options"]):
            if st.button(opt, key=f"opt_{st.session_state.round_number}_{pos}_{opt_i}", disabled=item["answered"]):
                item["answered"] = True
                item["selected"] = opt
                item["is_correct"] = (opt == item["correct_answer"])
                st.rerun()

        if item["answered"]:
            st.write("")
            if item["is_correct"]:
                st.success(f"✅ Doğru: **{item['correct_answer']}**")
            else:
                st.error(f"❌ Seçimin: {item['selected']} | Doğru cevap: **{item['correct_answer']}**")

        st.write("")
        if pos < total_cards - 1:
            if st.button("Sonraki Kelime ➡️", key=f"next_word_{st.session_state.round_number}_{pos}"):
                st.session_state.deck_pos += 1
                st.rerun()
        else:
            if st.button("🔄 Yeni Karışık Sırayla Başla", key=f"reshuffle_end_{st.session_state.round_number}"):
                st.session_state.round_number += 1
                init_level_deck(level)
                st.rerun()

        if st.button("🔀 Sırayı Şimdi Yeniden Karıştır", key=f"reshuffle_anytime_{st.session_state.round_number}_{pos}"):
            st.session_state.round_number += 1
            init_level_deck(level)
            st.rerun()

# --- SEKME 2: YENİ KELİME EKLEME ---
with tab2:
    st.markdown("### ➕ Sözlüğe Yeni Kelime Ekle")
    st.write("Öğrendiğiniz yeni kelimeleri buradan ekleyebilirsiniz.")

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
                if target_lvl == level:
                    init_level_deck(level)
                st.success(f"✅ **{new_en}** başarıyla **{target_lvl}** listesine eklendi!")
            else:
                st.warning("⚠️ Lütfen İngilizce kelime ve Türkçe anlamı alanlarını doldurun.")

# --- SEKME 3: TÜM KELİME LİSTESİ ---
with tab3:
    st.markdown(f"### 📋 {level} Seviyesi Tüm Kelimeler ({len(words)} Adet)")
    search_term = st.text_input("🔍 Kelime Ara...", placeholder="İngilizce veya Türkçe yazın...")

    for i, w in enumerate(words):
        if search_term.lower() in w["en"].lower() or search_term.lower() in w["tr"].lower():
            with st.expander(f"**{w['en']}** — {w['tr']}"):
                st.write(f"🇬🇧 *{w.get('ex_en', '')}*")
                st.write(f"🇹🇷 {w.get('ex_tr', '')}")
                if st.button("🔊 Dinle", key=f"list_audio_{level}_{i}"):
                    st.audio(generate_audio(w["en"]), format="audio/mp3", autoplay=True)
