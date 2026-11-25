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
        {"en": "Reckless", "tr": "pervasız, düşüncesizce riskli", "ex_en": "Reckless behavior can lead to serious problems.", "ex_tr": "Pervasız davranışlar ciddi sorunlara yol açabilir."},
        {"en": "Overlook", "tr": "gözden kaçırmak", "ex_en": "It is easy to overlook small details when you are in a hurry.", "ex_tr": "Acele ederken küçük ayrıntıları gözden kaçırmak kolaydır."},
        {"en": "Deliberately", "tr": "kasıtlı olarak, bile bile", "ex_en": "She deliberately ignored the message.", "ex_tr": "Mesajı kasıtlı olarak görmezden geldi."},
        {"en": "Thorough", "tr": "titiz, eksiksiz, kapsamlı", "ex_en": "They did a thorough check before starting.", "ex_tr": "Başlamadan önce kapsamlı bir kontrol yaptılar."},
        {"en": "Assumption", "tr": "varsayım", "ex_en": "That assumption turned out to be wrong.", "ex_tr": "Bu varsayımın yanlış olduğu ortaya çıktı."},
        {"en": "Conceal", "tr": "gizlemek, saklamak", "ex_en": "He tried to conceal the truth from everyone.", "ex_tr": "Gerçeği herkesten gizlemeye çalıştı."},
        {"en": "Crucial", "tr": "hayati, kritik, çok önemli", "ex_en": "Good planning is crucial for success.", "ex_tr": "İyi planlama başarı için çok önemlidir."},
        {"en": "Scrutinize", "tr": "dikkatle incelemek, didik didik etmek", "ex_en": "They will scrutinize every part of the report.", "ex_tr": "Raporun her kısmını dikkatle inceleyecekler."},
        {"en": "Vulnerable", "tr": "savunmasız, kırılgan", "ex_en": "The system is vulnerable to sudden changes.", "ex_tr": "Sistem ani değişikliklere karşı savunmasızdır."},
        {"en": "Consequence", "tr": "sonuç (çoğu zaman olumsuz)", "ex_en": "Every choice has a consequence.", "ex_tr": "Her seçimin bir sonucu vardır."},
        {"en": "Own up (to)", "tr": "suçunu itiraf etmek, kabullenmek", "ex_en": "He finally owned up to his mistake.", "ex_tr": "Sonunda hatasını itiraf etti."},
        {"en": "Cover up", "tr": "örtbas etmek", "ex_en": "They tried to cover up the problem.", "ex_tr": "Sorunu örtbas etmeye çalıştılar."},
        {"en": "Jump to conclusions", "tr": "aceleyle yargıya varmak", "ex_en": "Don't jump to conclusions before knowing all the facts.", "ex_tr": "Tüm gerçekleri öğrenmeden aceleyle yargıya varma."},
        {"en": "Take something into account", "tr": "hesaba katmak, göz önünde bulundurmak", "ex_en": "We need to take every detail into account.", "ex_tr": "Her ayrıntıyı hesaba katmamız gerekiyor."},
        {"en": "Draw a conclusion", "tr": "sonuca varmak, sonuç çıkarmak", "ex_en": "It is hard to draw a conclusion right now.", "ex_tr": "Şu anda bir sonuca varmak zor."},
        {"en": "Get rid of", "tr": "-den kurtulmak, atmak", "ex_en": "It's time to get rid of old files.", "ex_tr": "Eski dosyalardan kurtulma zamanı."},
        {"en": "Go through", "tr": "gözden geçirmek, incelemek", "ex_en": "Let's go through the list together.", "ex_tr": "Listeyi birlikte gözden geçirelim."},
        {"en": "Make an effort", "tr": "çaba göstermek", "ex_en": "You should make an effort to improve.", "ex_tr": "Gelişmek için çaba göstermelisin."},
        {"en": "Take the blame", "tr": "suçu üstlenmek", "ex_en": "Nobody wanted to take the blame.", "ex_tr": "Kimse suçu üstlenmek istemedi."},
        {"en": "Come to light", "tr": "gün yüzüne çıkmak, ortaya çıkmak", "ex_en": "New facts came to light yesterday.", "ex_tr": "Dün yeni gerçekler gün yüzüne çıktı."},
        {"en": "Hesitate", "tr": "tereddüt etmek, duraksamak", "ex_en": "Don't hesitate to ask if you need anything.", "ex_tr": "Bir şeye ihtiyacın olursa sormaktan çekinme."},
        {"en": "Reluctant", "tr": "isteksiz, gönülsüz", "ex_en": "He seemed reluctant to answer.", "ex_tr": "Cevap vermekte isteksiz görünüyordu."},
        {"en": "Ambitious", "tr": "hırslı, iddialı", "ex_en": "She has an ambitious plan for this year.", "ex_tr": "Bu yıl için iddialı bir planı var."},
        {"en": "Compromise", "tr": "uzlaşma, orta yol (bulmak)", "ex_en": "Both sides reached a fair compromise.", "ex_tr": "İki taraf adil bir uzlaşmaya vardı."},
        {"en": "Regret", "tr": "pişman olmak, pişmanlık", "ex_en": "I don't want to regret this decision later.", "ex_tr": "Daha sonra bu karardan pişman olmak istemiyorum."},
        {"en": "Inevitable", "tr": "kaçınılmaz", "ex_en": "Change is inevitable over time.", "ex_tr": "Zamanla değişim kaçınılmazdır."},
        {"en": "Persuade", "tr": "ikna etmek", "ex_en": "Can you persuade him to join us?", "ex_tr": "Onu bize katılmaya ikna edebilir misin?"},
        {"en": "Feasible", "tr": "uygulanabilir, yapılabilir", "ex_en": "Is this idea feasible in practice?", "ex_tr": "Bu fikir pratikte uygulanabilir mi?"},
        {"en": "Setback", "tr": "aksilik, engel, gerileme", "ex_en": "The delay was a minor setback.", "ex_tr": "Gecikme küçük bir aksilikti."},
        {"en": "Anticipate", "tr": "öngörmek, önceden tahmin etmek", "ex_en": "We didn't anticipate such a quick response.", "ex_tr": "Bu kadar hızlı bir yanıt öngörmemiştik."},
        {"en": "Turn down", "tr": "reddetmek, geri çevirmek", "ex_en": "She turned down the offer politely.", "ex_tr": "Teklifi kibarca geri çevirdi."},
        {"en": "Take up", "tr": "(bir uğraşa) başlamak", "ex_en": "He decided to take up a new hobby.", "ex_tr": "Yeni bir uğraşa başlamaya karar verdi."},
        {"en": "Put off", "tr": "ertelemek", "ex_en": "Let's not put off the meeting again.", "ex_tr": "Toplantıyı yine ertelemeyelim."},
        {"en": "Come up with", "tr": "(fikir/çözüm) bulmak", "ex_en": "They came up with a smart solution.", "ex_tr": "Akıllıca bir çözüm buldular."},
        {"en": "Make up your mind", "tr": "karar vermek", "ex_en": "Have you made up your mind yet?", "ex_tr": "Henüz kararını verdin mi?"},
        {"en": "Take a risk", "tr": "risk almak", "ex_en": "Sometimes you have to take a risk.", "ex_tr": "Bazen risk alman gerekir."},
        {"en": "Look forward to", "tr": "dört gözle beklemek", "ex_en": "I look forward to seeing you soon.", "ex_tr": "Seni yakında görmeyi dört gözle bekliyorum."},
        {"en": "Settle down", "tr": "yerleşik düzene geçmek", "ex_en": "They want to settle down in a quiet town.", "ex_tr": "Sakin bir kasabada yerleşik düzene geçmek istiyorlar."},
        {"en": "Pay off", "tr": "karşılığını vermek, meyvesini vermek", "ex_en": "Hard work usually pays off in the end.", "ex_tr": "Sıkı çalışma sonunda genellikle karşılığını verir."},
        {"en": "Weigh up", "tr": "tartmak, artısını eksisini düşünmek", "ex_en": "We should weigh up the pros and cons first.", "ex_tr": "Önce artıları ve eksileri tartmalıyız."},
        {"en": "Remarkable", "tr": "dikkate değer, olağanüstü", "ex_en": "She made remarkable progress this month.", "ex_tr": "Bu ay dikkate değer bir ilerleme kaydetti."},
        {"en": "Preserve", "tr": "korumak, muhafaza etmek", "ex_en": "We must preserve old traditions.", "ex_tr": "Eski gelenekleri korumalıyız."},
        {"en": "Fragile", "tr": "kırılgan, narin", "ex_en": "Handle this package carefully; it is fragile.", "ex_tr": "Bu paketi dikkatli taşı; kırılgan."},
        {"en": "Genuine", "tr": "gerçek, hakiki, sahte olmayan", "ex_en": "This is a genuine piece of work.", "ex_tr": "Bu gerçek bir eser."},
        {"en": "Reveal", "tr": "ortaya çıkarmak, açığa vurmak", "ex_en": "The results will reveal the truth.", "ex_tr": "Sonuçlar gerçeği ortaya çıkaracak."},
        {"en": "Restore", "tr": "restore etmek, eski haline getirmek", "ex_en": "Workers are trying to restore the old building.", "ex_tr": "Çalışanlar eski binayı eski haline getirmeye çalışıyor."},
        {"en": "Estimate", "tr": "tahmin etmek, tahmin", "ex_en": "It is difficult to estimate the exact cost.", "ex_tr": "Tam maliyeti tahmin etmek zor."},
        {"en": "Invaluable", "tr": "paha biçilemez, çok değerli", "ex_en": "Her advice was invaluable to the team.", "ex_tr": "Tavsiyeleri ekip için paha biçilemezdi."},
        {"en": "Heritage", "tr": "(kültürel) miras", "ex_en": "Protecting our cultural heritage is important.", "ex_tr": "Kültürel mirasımızı korumak önemlidir."},
        {"en": "Widespread", "tr": "yaygın", "ex_en": "The new habit has become widespread.", "ex_tr": "Yeni alışkanlık yaygın hale geldi."},
        {"en": "Dig up", "tr": "kazıp çıkarmak", "ex_en": "They dug up old records during research.", "ex_tr": "Araştırma sırasında eski kayıtları kazıp çıkardılar."},
        {"en": "Set up", "tr": "kurmak", "ex_en": "We set up a simple system for tracking.", "ex_tr": "Takip için basit bir sistem kurduk."},
        {"en": "Carry out", "tr": "yürütmek, gerçekleştirmek", "ex_en": "The team carried out the plan smoothly.", "ex_tr": "Ekip planı sorunsuz şekilde yürüttü."},
        {"en": "Hand over", "tr": "teslim etmek, devretmek", "ex_en": "He handed over the keys at the end of the day.", "ex_tr": "Günün sonunda anahtarları teslim etti."},
        {"en": "Break into", "tr": "(bir yere) zorla girmek", "ex_en": "Someone tried to break into the office at night.", "ex_tr": "Gece birisi ofise zorla girmeye çalıştı."},
        {"en": "Pull down", "tr": "yıkmak", "ex_en": "They decided to pull down the damaged wall.", "ex_tr": "Hasarlı duvarı yıkmaya karar verdiler."},
        {"en": "Keep an eye on", "tr": "göz kulak olmak", "ex_en": "Could you keep an eye on the bag for a minute?", "ex_tr": "Çantaya bir dakikalığına göz kulak olabilir misin?"},
        {"en": "Make headlines", "tr": "manşetlere çıkmak", "ex_en": "The story made headlines across the country.", "ex_tr": "Haber ülke genelinde manşetlere çıktı."},
        {"en": "Draw attention to", "tr": "dikkat çekmek", "ex_en": "The report draws attention to key issues.", "ex_tr": "Rapor temel sorunlara dikkat çekiyor."},
        {"en": "Put on display", "tr": "sergilemek", "ex_en": "The best works were put on display.", "ex_tr": "En iyi eserler sergilendi."}
    ],
    "B2": [
        {"en": "Meticulous", "tr": "titiz, özenli", "ex_en": "She is meticulous about every small detail.", "ex_tr": "Her küçük ayrıntı konusunda titizdir."},
        {"en": "Ephemeral", "tr": "geçici, kısa ömürlü", "ex_en": "Trends in this area are often ephemeral.", "ex_tr": "Bu alandaki trendler genellikle kısa ömürlüdür."},
        {"en": "Resilient", "tr": "dirençli, dayanıklı", "ex_en": "They built a resilient structure against pressure.", "ex_tr": "Baskıya karşı dayanıklı bir yapı kurdular."},
        {"en": "Arbitrary", "tr": "keyfi, rastgele", "ex_en": "The rule felt completely arbitrary.", "ex_tr": "Kural tamamen keyfi hissettirdi."},
        {"en": "Pragmatic", "tr": "pragmatik, gerçekçi", "ex_en": "We took a pragmatic approach to the problem.", "ex_tr": "Soruna gerçekçi bir yaklaşımla yaklaştık."},
        {"en": "Redundant", "tr": "gereksiz, fazlalık", "ex_en": "We removed redundant steps from the process.", "ex_tr": "Süreçteki gereksiz adımları kaldırdık."},
        {"en": "Tenuous", "tr": "zayıf, belirsiz", "ex_en": "The link between the two claims is tenuous.", "ex_tr": "İki iddia arasındaki bağ zayıf."},
        {"en": "Discern", "tr": "ayırt etmek, fark etmek", "ex_en": "It takes time to discern real differences.", "ex_tr": "Gerçek farkları ayırt etmek zaman alır."},
        {"en": "Exacerbate", "tr": "kötüleştirmek, şiddetlendirmek", "ex_en": "Ignoring it will only exacerbate the issue.", "ex_tr": "Görmezden gelmek sorunu daha da kötüleştirecek."},
        {"en": "Eloquent", "tr": "güzel ve etkili konuşan", "ex_en": "He gave an eloquent explanation of his view.", "ex_tr": "Görüşünü güzel ve etkili bir şekilde açıkladı."},
        {"en": "Bring about", "tr": "neden olmak, meydana getirmek", "ex_en": "Small changes can bring about big results.", "ex_tr": "Küçük değişiklikler büyük sonuçlar meydana getirebilir."},
        {"en": "Carry out", "tr": "gerçekleştirmek, yürütmek", "ex_en": "They carried out the task on schedule.", "ex_tr": "Görevi planlanan zamanda gerçekleştirdiler."},
        {"en": "Come up with", "tr": "bulmak, ortaya çıkarmak", "ex_en": "She came up with a fresh angle.", "ex_tr": "Yeni bir bakış açısı buldu."},
        {"en": "Give in", "tr": "pes etmek, boyun eğmek", "ex_en": "They refused to give in to pressure.", "ex_tr": "Baskıya boyun eğmeyi reddettiler."},
        {"en": "Hold back", "tr": "kendini tutmak, geri durmak", "ex_en": "He held back from making a hasty comment.", "ex_tr": "Aceleci bir yorum yapmaktan kendini tuttu."},
        {"en": "Look into", "tr": "araştırmak, incelemek", "ex_en": "We will look into this matter carefully.", "ex_tr": "Bu konuyu dikkatle araştıracağız."},
        {"en": "Put off", "tr": "ertelemek", "ex_en": "They had to put off the release.", "ex_tr": "Yayınlamayı ertelemek zorunda kaldılar."},
        {"en": "Rule out", "tr": "olasılığı ortadan kaldırmak", "ex_en": "We cannot rule out other possibilities yet.", "ex_tr": "Henüz diğer olasılıkları dışlayamayız."},
        {"en": "Set out", "tr": "yola çıkmak, girişmek", "ex_en": "They set out early in the morning.", "ex_tr": "Sabah erken saatte yola çıktılar."},
        {"en": "Stem from", "tr": "kaynaklanmak", "ex_en": "Most of the confusion stems from unclear terms.", "ex_tr": "Kafa karışıklığının çoğu belirsiz ifadelerden kaynaklanıyor."},
        {"en": "Ubiquitous", "tr": "her yerde bulunan, yaygın", "ex_en": "Smartphones have become ubiquitous.", "ex_tr": "Akıllı telefonlar her yerde bulunur hale geldi."},
        {"en": "Ambivalent", "tr": "kararsız, ikircikli", "ex_en": "He felt ambivalent about moving away.", "ex_tr": "Uzaklaşma konusunda ikircikli hissediyordu."},
        {"en": "Tumultuous", "tr": "çalkantılı, gürültülü", "ex_en": "It was a tumultuous period for everyone.", "ex_tr": "Herkes için çalkantılı bir dönemdi."},
        {"en": "Candid", "tr": "açık sözlü, dürüst", "ex_en": "I appreciate your candid feedback.", "ex_tr": "Açık sözlü geri bildirimin için teşekkür ederim."},
        {"en": "Innate", "tr": "doğuştan gelen", "ex_en": "She seems to have an innate sense of rhythm.", "ex_tr": "Doğuştan gelen bir ritim duygusuna sahip görünüyor."},
        {"en": "Dexterous", "tr": "becerikli, usta", "ex_en": "He is remarkably dexterous with tools.", "ex_tr": "Aletler konusunda son derece becerikli."},
        {"en": "Conducive", "tr": "elverişli, uygun", "ex_en": "A calm environment is conducive to focus.", "ex_tr": "Sakin bir ortam odaklanmaya elverişlidir."},
        {"en": "Pertinent", "tr": "ilgili, alakalı", "ex_en": "Please stick to pertinent points.", "ex_tr": "Lütfen konuyla alakalı noktalara bağlı kalın."},
        {"en": "Apathy", "tr": "ilgisizlik, kayıtsızlık", "ex_en": "Public apathy made the change harder.", "ex_tr": "Kayıtsızlık değişimi daha zor hale getirdi."},
        {"en": "Anomaly", "tr": "anomali, sapma", "ex_en": "The data showed a clear anomaly.", "ex_tr": "Veriler net bir sapma gösterdi."},
        {"en": "Account for", "tr": "açıklamak", "ex_en": "This factor accounts for the difference.", "ex_tr": "Bu etken farkı açıklıyor."},
        {"en": "Break down", "tr": "bozulmak, incelemek", "ex_en": "Let's break down the steps one by one.", "ex_tr": "Adımları tek tek inceleyelim."},
        {"en": "Call off", "tr": "iptal etmek", "ex_en": "They decided to call off the event.", "ex_tr": "Etkinliği iptal etmeye karar verdiler."},
        {"en": "Cut back on", "tr": "azaltmak", "ex_en": "I need to cut back on screen time.", "ex_tr": "Ekran süresini azaltmam gerekiyor."},
        {"en": "Delve into", "tr": "derinlemesine incelemek", "ex_en": "We will delve into the details later.", "ex_tr": "Ayrıntıları daha sonra derinlemesine inceleyeceğiz."},
        {"en": "Fall through", "tr": "suya düşmek", "ex_en": "The original plan fell through at the last minute.", "ex_tr": "İlk plan son dakikada suya düştü."},
        {"en": "Get around to", "tr": "nihayet vakit ayırmak", "ex_en": "I finally got around to organizing the notes.", "ex_tr": "Notları düzenlemeye nihayet vakit ayırdım."},
        {"en": "Iron out", "tr": "(sorunu) çözmek", "ex_en": "We still need to iron out a few details.", "ex_tr": "Hâlâ birkaç ayrıntıyı çözmemiz gerekiyor."},
        {"en": "Keep up with", "tr": "ayak uydurmak", "ex_en": "It is hard to keep up with every update.", "ex_tr": "Her güncellemeye ayak uydurmak zor."},
        {"en": "Weigh up", "tr": "tartmak, değerlendirmek", "ex_en": "Take time to weigh up both options.", "ex_tr": "Her iki seçeneği değerlendirmek için zaman ayır."},
        {"en": "Discrepancy", "tr": "aksaklık", "ex_en": "There was a small discrepancy in the numbers.", "ex_tr": "Sayılar arasında küçük bir aksaklık vardı."},
        {"en": "Complaint", "tr": "şikayet", "ex_en": "They received a complaint about the delay.", "ex_tr": "Gecikmeyle ilgili bir şikayet aldılar."},
        {"en": "Cope with", "tr": "üstesinden gelmek", "ex_en": "Good habits help you cope with stress.", "ex_tr": "İyi alışkanlıklar stresin üstesinden gelmene yardımcı olur."},
        {"en": "Ambiguity", "tr": "belirsizlik, şüpheci oluş", "ex_en": "We should avoid ambiguity in instructions.", "ex_tr": "Talimatlarda belirsizlikten kaçınmalıyız."},
        {"en": "Merger", "tr": "birleşme", "ex_en": "The merger was announced last week.", "ex_tr": "Birleşme geçen hafta duyuruldu."},
        {"en": "Vaguely", "tr": "belirsiz bir şekilde", "ex_en": "I vaguely remember hearing that name.", "ex_tr": "O ismi duyduğumu belirsiz bir şekilde hatırlıyorum."},
        {"en": "Thrived", "tr": "gelişme", "ex_en": "The project thrived under clear leadership.", "ex_tr": "Proje net bir liderlik altında gelişti."},
        {"en": "Friction", "tr": "sürtünme", "ex_en": "Too much friction slows down progress.", "ex_tr": "Fazla sürtünme ilerlemeyi yavaşlatır."},
        {"en": "Feud", "tr": "kavga", "ex_en": "The long feud finally ended.", "ex_tr": "Uzun süren kavga nihayet sona erdi."},
        {"en": "Adamant", "tr": "kararlı, ısrarcı", "ex_en": "She remained adamant about her decision.", "ex_tr": "Kararı konusunda kararlı kaldı."},
        {"en": "Deceptive", "tr": "aldatıcı, yanıltıcı", "ex_en": "First impressions can sometimes be deceptive.", "ex_tr": "İlk izlenimler bazen yanıltıcı olabilir."},
        {"en": "Daunting", "tr": "göz korkutucu, zorlu", "ex_en": "Starting from scratch can feel daunting.", "ex_tr": "Sıfırdan başlamak göz korkutucu gelebilir."},
        {"en": "Skeptical", "tr": "şüpheci", "ex_en": "He was skeptical about the quick promise.", "ex_tr": "Hızlı vaade karşı şüpheciydi."},
        {"en": "Fabricate", "tr": "uydurmak", "ex_en": "Nobody should fabricate excuses.", "ex_tr": "Kimse bahane uydurmamalı."},
        {"en": "Subside", "tr": "yatışmak, azalmak", "ex_en": "The noise finally began to subside.", "ex_tr": "Gürültü sonunda azalmaya başladı."},
        {"en": "Glean", "tr": "(bilgi) edinmek, toplamak", "ex_en": "We gleaned useful insights from the notes.", "ex_tr": "Notlardan faydalı bilgiler edindik."},
        {"en": "Plausible", "tr": "makul, akla yatkın", "ex_en": "Her explanation sounds quite plausible.", "ex_tr": "Açıklaması oldukça makul görünüyor."},
        {"en": "Compelling", "tr": "ikna edici, sürükleyici", "ex_en": "They made a compelling case for the change.", "ex_tr": "Değişiklik için ikna edici bir gerekçe sundular."},
        {"en": "Reluctant", "tr": "isteksiz, gönülsüz", "ex_en": "He was reluctant to share the details.", "ex_tr": "Ayrıntıları paylaşmakta isteksizdi."},
        {"en": "Back down", "tr": "geri adım atmak", "ex_en": "Neither side wanted to back down.", "ex_tr": "Hiçbir taraf geri adım atmak istemedi."},
        {"en": "Bring up", "tr": "(bir konuyu) gündeme getirmek", "ex_en": "She brought up the topic during the meeting.", "ex_tr": "Toplantı sırasında konuyu gündeme getirdi."},
        {"en": "Come across", "tr": "rastlamak/izlenim vermek", "ex_en": "I came across an interesting article today.", "ex_tr": "Bugün ilginç bir makaleye rastladım."},
        {"en": "Deal with", "tr": "ele almak, halletmek", "ex_en": "We will deal with this issue right away.", "ex_tr": "Bu sorunu hemen ele alacağız."},
        {"en": "Figure out", "tr": "çözmek, anlamak", "ex_en": "It took a few minutes to figure out the cause.", "ex_tr": "Nedeni anlamak birkaç dakika sürdü."},
        {"en": "Get away with", "tr": "yanına kar kalmak", "ex_en": "They shouldn't get away with breaking rules.", "ex_tr": "Kuralları çiğnemek yanlarına kar kalmamalı."},
        {"en": "Hold up", "tr": "geçerliliğini korumak/geciktirmek", "ex_en": "Traffic held us up on the way.", "ex_tr": "Yolda trafik bizi geciktirdi."},
        {"en": "Lead to", "tr": "yol açmak, neden olmak", "ex_en": "Careless habits can lead to mistakes.", "ex_tr": "Dikkatsiz alışkanlıklar hatalara yol açabilir."},
        {"en": "Make up for", "tr": "telafi etmek", "ex_en": "We can make up for the lost time tomorrow.", "ex_tr": "Kaybedilen zamanı yarın telafi edebiliriz."},
        {"en": "Point out", "tr": "belirtmek, işaret etmek", "ex_en": "He pointed out a key detail in the text.", "ex_tr": "Metindeki önemli bir ayrıntıya dikkat çekti."},
        {"en": "Once in a blue moon", "tr": "kırk yılda bir", "ex_en": "We eat out once in a blue moon.", "ex_tr": "Kırk yılda bir dışarıda yeriz."},
        {"en": "Cupboard (British)", "tr": "dolap", "ex_en": "The mugs are in the kitchen cupboard.", "ex_tr": "Kupalar mutfak dolabında."},
        {"en": "Cabinet (USA)", "tr": "dolap", "ex_en": "Check the top cabinet for extra supplies.", "ex_tr": "Ekstra malzemeler için üst dolabı kontrol et."}
    ]
}

def load_words():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(INITIAL_DATA, f, ensure_ascii=False, indent=4)
        return {
            "B1": list(INITIAL_DATA["B1"]),
            "B2": list(INITIAL_DATA["B2"])
        }
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        synced = {
            "B1": list(INITIAL_DATA["B1"]),
            "B2": list(INITIAL_DATA["B2"])
        }
        if isinstance(data, dict):
            for lvl in ["B1", "B2"]:
                base_keys = {item["en"].strip().lower() for item in synced[lvl]}
                for item in data.get(lvl, []):
                    en_val = str(item.get("en", "")).strip()
                    tr_val = str(item.get("tr", "")).strip()
                    if en_val and tr_val and en_val.lower() not in base_keys:
                        synced[lvl].append({
                            "en": en_val,
                            "tr": tr_val,
                            "ex_en": str(item.get("ex_en", "")).strip(),
                            "ex_tr": str(item.get("ex_tr", "")).strip()
                        })
                        base_keys.add(en_val.lower())
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(synced, f, ensure_ascii=False, indent=4)
        return synced
    except Exception:
        return {
            "B1": list(INITIAL_DATA["B1"]),
            "B2": list(INITIAL_DATA["B2"])
        }

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
