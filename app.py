import streamlit as st
import json
import os
import random
from io import BytesIO
from gtts import gTTS
from google import genai
from google.genai import types

# Sayfa Ayarları
st.set_page_config(
    page_title="VocabMaster | B1 & B2 AI",
    page_icon="🌿",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Gemini API İstemcisi Başlatma
@st.cache_resource
def get_ai_client():
    api_key = st.secrets.get("GEMINI_API_KEY", os.environ.get("GEMINI_API_KEY", ""))
    if api_key:
        return genai.Client(api_key=api_key)
    return None

client = get_ai_client()

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
        {"en": "Reluctant", "tr": "isteksiz, gönülsüz", "ex_en": "He was reluctant to admit that he was wrong.", "ex_tr": "Hatalı olduğunu kabul etmekte isteksizdi."},
        {"en": "Ambitious", "tr": "hırslı, iddialı", "ex_en": "She is an ambitious young lawyer.", "ex_tr": "O, hırslı bir genç avukattır."},
        {"en": "Compromise", "tr": "uzlaşma, orta yol (bulmak)", "ex_en": "In a marriage, both partners must learn to compromise.", "ex_tr": "Evlilikte her iki taraf da uzlaşmayı öğrenmelidir."},
        {"en": "Regret", "tr": "pişman olmak, pişmanlık", "ex_en": "I regret not studying harder for the exam.", "ex_tr": "Sınava daha sıkı çalışmadığıma pişmanım."},
        {"en": "Inevitable", "tr": "kaçınılmaz", "ex_en": "Change is an inevitable part of life.", "ex_tr": "Değişim hayatın kaçınılmaz bir parçasıdır."},
        {"en": "Persuade", "tr": "ikna etmek", "ex_en": "I finally managed to persuade him to come with us.", "ex_tr": "Sonunda onu bizimle gelmeye ikna etmeyi başardım."},
        {"en": "Feasible", "tr": "uygulanabilir, yapılabilir", "ex_en": "Your plan sounds great, but is it economically feasible?", "ex_tr": "Planın kulağa harika geliyor ama ekonomik olarak uygulanabilir mi?"},
        {"en": "Setback", "tr": "aksilik, engel, gerileme", "ex_en": "The bad weather was a major setback for the construction.", "ex_tr": "Kötü hava koşulları inşaat için büyük bir aksilik oldu."},
        {"en": "Anticipate", "tr": "öngörmek, önceden tahmin etmek", "ex_en": "We anticipate that ticket sales will increase next month.", "ex_tr": "Gelecek ay bilet satışlarının artacağını öngörüyoruz."},
        {"en": "Turn down", "tr": "reddetmek, geri çevirmek", "ex_en": "She turned down the job offer because the salary was low.", "ex_tr": "Maaş düşük olduğu için iş teklifini geri çevirdi."},
        {"en": "Take up", "tr": "(bir uğraşa) başlamak", "ex_en": "I decided to take up photography in my free time.", "ex_tr": "Boş zamanlarımda fotoğrafçılığa başlamaya karar verdim."},
        {"en": "Put off", "tr": "ertelemek", "ex_en": "Never put off until tomorrow what you can do today.", "ex_tr": "Bugün yapabileceğin işi asla yarına erteleme."},
        {"en": "Come up with", "tr": "(fikir/çözüm) bulmak", "ex_en": "We need to come up with a good marketing strategy.", "ex_tr": "İyi bir pazarlama stratejisi bulmamız gerekiyor."},
        {"en": "Make up your mind", "tr": "karar vermek", "ex_en": "I can't make up my mind which shirt to buy.", "ex_tr": "Hangi gömleği alacağıma karar veremiyorum."},
        {"en": "Take a risk", "tr": "risk almak", "ex_en": "Sometimes you have to take a risk to achieve success.", "ex_tr": "Bazen başarıya ulaşmak için risk almalısın."},
        {"en": "Look forward to", "tr": "dört gözle beklemek", "ex_en": "I am really looking forward to our summer vacation.", "ex_tr": "Yaz tatilimizi gerçekten dört gözle bekliyorum."},
        {"en": "Settle down", "tr": "yerleşik düzene geçmek", "ex_en": "After traveling for years, he decided to settle down in Samsun.", "ex_tr": "Yıllarca seyahat ettikten sonra Samsun'da yerleşik düzene geçmeye karar verdi."},
        {"en": "Pay off", "tr": "karşılığını vermek, meyvesini vermek", "ex_en": "All her hard work finally paid off when she passed the exam.", "ex_tr": "Sınavı geçtiğinde tüm sıkı çalışması nihayet meyvesini verdi."},
        {"en": "Weigh up", "tr": "tartmak, artısını eksisini düşünmek", "ex_en": "We need to weigh up the pros and cons before deciding.", "ex_tr": "Karar vermeden önce artılarını ve eksilerini tartmalıyız."},
        {"en": "Remarkable", "tr": "dikkate değer, olağanüstü", "ex_en": "She has made remarkable progress in English.", "ex_tr": "İngilizcede dikkate değer bir ilerleme kaydetti."},
        {"en": "Preserve", "tr": "korumak, muhafaza etmek", "ex_en": "We must work together to preserve the environment.", "ex_tr": "Çevreyi korumak için birlikte çalışmalıyız."},
        {"en": "Fragile", "tr": "kırılgan, narin", "ex_en": "Be careful with that box; the glasses inside are fragile.", "ex_tr": "O kutuya dikkat et; içindeki bardaklar kırılgan."},
        {"en": "Genuine", "tr": "gerçek, hakiki, sahte olmayan", "ex_en": "Is this bag made of genuine leather?", "ex_tr": "Bu çanta hakiki deriden mi yapılmış?"},
        {"en": "Reveal", "tr": "ortaya çıkarmak, açığa vurmak", "ex_en": "The journalist refused to reveal his source.", "ex_tr": "Gazeteci kaynağını açıklamayı reddetti."},
        {"en": "Restore", "tr": "restore etmek, eski haline getirmek", "ex_en": "They spent years restoring the old castle.", "ex_tr": "Eski kaleyi restore etmek için yıllar harcadılar."},
        {"en": "Estimate", "tr": "tahmin etmek, tahmin", "ex_en": "Experts estimate that the project will take two years.", "ex_tr": "Uzmanlar projenin iki yıl süreceğini tahmin ediyor."},
        {"en": "Invaluable", "tr": "paha biçilemez, çok değerli", "ex_en": "Your advice has been invaluable to me.", "ex_tr": "Tavsiyelerin benim için paha biçilemezdi."},
        {"en": "Heritage", "tr": "(kültürel) miras", "ex_en": "We should protect our national heritage.", "ex_tr": "Ulusal mirasımızı korumalıyız."},
        {"en": "Widespread", "tr": "yaygın", "ex_en": "The use of smartphones is widespread around the world.", "ex_tr": "Akıllı telefon kullanımı dünya çapında yaygındır."},
        {"en": "Dig up", "tr": "kazıp çıkarmak", "ex_en": "Archaeologists dug up ancient coins in the area.", "ex_tr": "Arkeologlar bölgede antik sikkeler kazıp çıkardı."},
        {"en": "Set up", "tr": "kurmak", "ex_en": "He wants to set up his own 3D printing business.", "ex_tr": "Kendi 3D baskı işini kurmak istiyor."},
        {"en": "Carry out", "tr": "yürütmek, gerçekleştirmek", "ex_en": "Scientists are carrying out experiments in the lab.", "ex_tr": "Bilim insanları laboratuvarda deneyler yürütüyor."},
        {"en": "Hand over", "tr": "teslim etmek, devretmek", "ex_en": "The thief was forced to hand over the stolen money.", "ex_tr": "Hırsız çaldığı parayı teslim etmek zorunda kaldı."},
        {"en": "Break into", "tr": "(bir yere) zorla girmek", "ex_en": "Someone tried to break into our house last night.", "ex_tr": "Dün gece birisi evimize zorla girmeye çalıştı."},
        {"en": "Pull down", "tr": "yıkmak", "ex_en": "They are going to pull down the old cinema building.", "ex_tr": "Eski sinema binasını yıkacaklar."},
        {"en": "Keep an eye on", "tr": "göz kulak olmak", "ex_en": "Can you keep an eye on my bag for a minute?", "ex_tr": "Bir dakikalığına çantama göz kulak olabilir misin?"},
        {"en": "Make headlines", "tr": "manşetlere çıkmak", "ex_en": "The actor's sudden marriage made headlines worldwide.", "ex_tr": "Aktörün ani evliliği dünya çapında manşetlere çıktı."},
        {"en": "Draw attention to", "tr": "dikkat çekmek", "ex_en": "The campaign aims to draw attention to climate change.", "ex_tr": "Kampanya iklim değişikliğine dikkat çekmeyi amaçlıyor."},
        {"en": "Put on display", "tr": "sergilemek", "ex_en": "The museum put the rare paintings on display.", "ex_tr": "Müze nadir tabloları sergiledi."}
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
        {"en": "Carry out", "tr": "gerçekleştirmek, yürütmek", "ex_en": "The engineers will carry out safety tests tomorrow.", "ex_tr": "Mühendisler yarın güvenlik testleri gerçekleştirecek."},
        {"en": "Come up with", "tr": "bulmak, ortaya çıkarmak", "ex_en": "He always comes up with creative solutions.", "ex_tr": "Her zaman yaratıcı çözümler bulur."},
        {"en": "Give in", "tr": "pes etmek, boyun eğmek", "ex_en": "Don't give in to pressure; stick to your principles.", "ex_tr": "Baskıya boyun eğme; ilkelerine bağlı kal."},
        {"en": "Hold back", "tr": "kendini tutmak, geri durmak", "ex_en": "She couldn't hold back her tears during the movie.", "ex_tr": "Film sırasında gözyaşlarını tutamadı."},
        {"en": "Look into", "tr": "araştırmak, incelemek", "ex_en": "The manager promised to look into the customer's complaint.", "ex_tr": "Müdür müşterinin şikayetini inceleyeceğine söz verdi."},
        {"en": "Put off", "tr": "ertelemek", "ex_en": "They had to put off the meeting until next week.", "ex_tr": "Toplantıyı gelecek haftaya kadar ertelemek zorunda kaldılar."},
        {"en": "Rule out", "tr": "olasılığı ortadan kaldırmak", "ex_en": "The doctor has not ruled out the possibility of an infection.", "ex_tr": "Doktor enfeksiyon olasılığını henüz ortadan kaldırmadı."},
        {"en": "Set out", "tr": "yola çıkmak, girişmek", "ex_en": "They set out early in the morning to avoid traffic.", "ex_tr": "Trafikten kaçınmak için sabah erkenden yola çıktılar."},
        {"en": "Stem from", "tr": "kaynaklanmak", "ex_en": "Most of his problems stem from a lack of confidence.", "ex_tr": "Sorunlarının çoğu özgüven eksikliğinden kaynaklanıyor."},
        {"en": "Ubiquitous", "tr": "her yerde bulunan, yaygın", "ex_en": "Coffee shops have become ubiquitous in modern cities.", "ex_tr": "Kahve dükkanları modern şehirlerde her yerde bulunur hale geldi."},
        {"en": "Ambivalent", "tr": "kararsız, ikircikli", "ex_en": "Many people feel ambivalent about working from home.", "ex_tr": "Birçok insan evden çalışma konusunda ikircikli hissediyor."},
        {"en": "Tumultuous", "tr": "çalkantılı, gürültülü", "ex_en": "The country went through a tumultuous period of reform.", "ex_tr": "Ülke çalkantılı bir reform döneminden geçti."},
        {"en": "Candid", "tr": "açık sözlü, dürüst", "ex_en": "Thank you for your candid feedback on my design.", "ex_tr": "Tasarımım hakkındaki açık sözlü geri bildirimin için teşekkür ederim."},
        {"en": "Innate", "tr": "doğuştan gelen", "ex_en": "She has an innate talent for music and rhythm.", "ex_tr": "Müzik ve ritim konusunda doğuştan gelen bir yeteneği var."},
        {"en": "Dexterous", "tr": "becerikli, usta", "ex_en": "Surgeons need to be extremely dexterous with their hands.", "ex_tr": "Cerrahların ellerini son derece ustalıkla kullanmaları gerekir."},
        {"en": "Conducive", "tr": "elverişli, uygun", "ex_en": "A quiet room is more conducive to studying.", "ex_tr": "Sessiz bir oda ders çalışmak için daha elverişlidir."},
        {"en": "Pertinent", "tr": "ilgili, alakalı", "ex_en": "Please ask questions that are pertinent to the topic.", "ex_tr": "Lütfen konuyla alakalı sorular sorun."},
        {"en": "Apathy", "tr": "ilgisizlik, kayıtsızlık", "ex_en": "Voter apathy led to a low turnout in the election.", "ex_tr": "Seçmen ilgisizliği seçimde düşük katılıma yol açtı."},
        {"en": "Anomaly", "tr": "anomali, sapma", "ex_en": "Scientists noticed a strange anomaly in the test results.", "ex_tr": "Bilim insanları test sonuçlarında garip bir sapma fark etti."},
        {"en": "Account for", "tr": "açıklamak", "ex_en": "How do you account for the missing files?", "ex_tr": "Kayıp dosyaları nasıl açıklıyorsun?"},
        {"en": "Break down", "tr": "bozulmak, incelemek", "ex_en": "Our car broke down on the way to the airport.", "ex_tr": "Havaalanına giderken arabamız bozuldu."},
        {"en": "Call off", "tr": "iptal etmek", "ex_en": "The match was called off due to heavy rain.", "ex_tr": "Maç şiddetli yağmur nedeniyle iptal edildi."},
        {"en": "Cut back on", "tr": "azaltmak", "ex_en": "I'm trying to cut back on sugar and caffeine.", "ex_tr": "Şekeri ve kafeini azaltmaya çalışıyorum."},
        {"en": "Delve into", "tr": "derinlemesine incelemek", "ex_en": "The book delves into the history of ancient civilizations.", "ex_tr": "Kitap antik uygarlıkların tarihini derinlemesine inceliyor."},
        {"en": "Fall through", "tr": "suya düşmek", "ex_en": "Our vacation plans fell through at the last minute.", "ex_tr": "Tatil planlarımız son dakikada suya düştü."},
        {"en": "Get around to", "tr": "nihayet vakit ayırmak", "ex_en": "I finally got around to reading the book you lent me.", "ex_tr": "Bana ödünç verdiğin kitabı okumaya nihayet vakit ayırabildim."},
        {"en": "Iron out", "tr": "(sorunu) çözmek", "ex_en": "We still need to iron out a few minor details.", "ex_tr": "Hala birkaç küçük detayı çözmemiz gerekiyor."},
        {"en": "Keep up with", "tr": "ayak uydurmak", "ex_en": "It's hard to keep up with the rapid changes in technology.", "ex_tr": "Teknolojideki hızlı değişimlere ayak uydurmak zor."},
        {"en": "Weigh up", "tr": "tartmak, değerlendirmek", "ex_en": "You should weigh up all your options carefully.", "ex_tr": "Tüm seçeneklerini dikkatlice değerlendirmelisin."},
        {"en": "Discrepancy", "tr": "aksaklık, tutarsızlık", "ex_en": "There is a discrepancy between the two financial reports.", "ex_tr": "İki finansal rapor arasında bir tutarsızlık var."},
        {"en": "Complaint", "tr": "şikayet", "ex_en": "If the service is poor, you should make a formal complaint.", "ex_tr": "Hizmet kötüyse resmi bir şikayette bulunmalısın."},
        {"en": "Cope with", "tr": "üstesinden gelmek", "ex_en": "Exercise helps me cope with stress.", "ex_tr": "Egzersiz stresle başa çıkmama (üstesinden gelmeme) yardımcı oluyor."},
        {"en": "Ambiguity", "tr": "belirsizlik, muğlaklık", "ex_en": "Write clear instructions to avoid any ambiguity.", "ex_tr": "Herhangi bir belirsizlikten kaçınmak için net talimatlar yazın."},
        {"en": "Merger", "tr": "birleşme", "ex_en": "The merger of the two banks created a financial giant.", "ex_tr": "İki bankanın birleşmesi finansal bir dev yarattı."},
        {"en": "Vaguely", "tr": "belirsiz bir şekilde", "ex_en": "I vaguely remember meeting him at a conference years ago.", "ex_tr": "Onunla yıllar önce bir konferansta tanıştığımı hayal meyal (belirsiz bir şekilde) hatırlıyorum."},
        {"en": "Thrive", "tr": "gelişmek, serpilmek", "ex_en": "Small businesses can thrive with the right online strategy.", "ex_tr": "Küçük işletmeler doğru çevrimiçi stratejiyle gelişebilir."},
        {"en": "Friction", "tr": "sürtünme, anlaşmazlık", "ex_en": "There is some friction between the sales and marketing teams.", "ex_tr": "Satış ve pazarlama ekipleri arasında biraz sürtünme var."},
        {"en": "Feud", "tr": "kavga, kan davası", "ex_en": "The bitter feud between the two families lasted for decades.", "ex_tr": "İki aile arasındaki şiddetli kavga onlarca yıl sürdü."},
        {"en": "Adamant", "tr": "kararlı, ısrarcı", "ex_en": "She was adamant that she would not change her mind.", "ex_tr": "Fikrini değiştirmeyeceği konusunda kararlıydı."},
        {"en": "Deceptive", "tr": "aldatıcı, yanıltıcı", "ex_en": "Appearances can often be deceptive.", "ex_tr": "Görünüşler çoğu zaman aldatıcı olabilir."},
        {"en": "Daunting", "tr": "göz korkutucu, zorlu", "ex_en": "Learning a new language can seem like a daunting task.", "ex_tr": "Yeni bir dil öğrenmek göz korkutucu bir görev gibi görünebilir."},
        {"en": "Skeptical", "tr": "şüpheci", "ex_en": "I am skeptical about products that promise instant results.", "ex_tr": "Anında sonuç vaat eden ürünlere karşı şüpheciyim."},
        {"en": "Fabricate", "tr": "uydurmak", "ex_en": "He fabricated an excuse for being late to work.", "ex_tr": "İşe geç kalmak için bir bahane uydurdu."},
        {"en": "Subside", "tr": "yatışmak, azalmak", "ex_en": "We waited for the storm to subside before leaving.", "ex_tr": "Yola çıkmadan önce fırtınanın dinmesini bekledik."},
        {"en": "Glean", "tr": "(bilgi) edinmek, toplamak", "ex_en": "I gleaned some useful tips from the workshop.", "ex_tr": "Atölye çalışmasından bazı faydalı ipuçları edindim."},
        {"en": "Plausible", "tr": "makul, akla yatkın", "ex_en": "Her explanation sounded completely plausible.", "ex_tr": "Açıklaması kulağa tamamen akla yatkın geliyordu."},
        {"en": "Compelling", "tr": "ikna edici, sürükleyici", "ex_en": "The lawyer presented a compelling argument.", "ex_tr": "Avukat ikna edici bir argüman sundu."},
        {"en": "Reluctant", "tr": "isteksiz, gönülsüz", "ex_en": "Many consumers are reluctant to pay higher prices.", "ex_tr": "Birçok tüketici daha yüksek fiyatlar ödemeye isteksizdir."},
        {"en": "Back down", "tr": "geri adım atmak", "ex_en": "Neither side was willing to back down in the argument.", "ex_tr": "Tartışmada hiçbir taraf geri adım atmaya istekli değildi."},
        {"en": "Bring up", "tr": "(bir konuyu) gündeme getirmek", "ex_en": "Please don't bring up politics at the dinner table.", "ex_tr": "Lütfen akşam yemeği masasında siyaseti gündeme getirme."},
        {"en": "Come across", "tr": "rastlamak / izlenim vermek", "ex_en": "I came across an old photo while cleaning my room.", "ex_tr": "Odamı temizlerken eski bir fotoğrafa rastladım."},
        {"en": "Deal with", "tr": "ele almak, halletmek", "ex_en": "We have more urgent matters to deal with right now.", "ex_tr": "Şu anda halletmemiz gereken daha acil meseleler var."},
        {"en": "Figure out", "tr": "çözmek, anlamak", "ex_en": "I can't figure out how this software works.", "ex_tr": "Bu yazılımın nasıl çalıştığını çözemiyorum."},
        {"en": "Get away with", "tr": "yanına kar kalmak", "ex_en": "He cheated on the test and got away with it.", "ex_tr": "Sınavda kopya çekti ve yanına kar kaldı."},
        {"en": "Hold up", "tr": "geciktirmek / geçerliliğini korumak", "ex_en": "Sorry I'm late; I was held up in heavy traffic.", "ex_tr": "Geciktiğim için üzgünüm; yoğun trafikte geciktim."},
        {"en": "Lead to", "tr": "yol açmak, neden olmak", "ex_en": "Eating too much junk food can lead to health problems.", "ex_tr": "Çok fazla abur cubur yemek sağlık sorunlarına yol açabilir."},
        {"en": "Make up for", "tr": "telafi etmek", "ex_en": "I bought her flowers to make up for forgetting our anniversary.", "ex_tr": "Yıldönümümüzü unuttuğumu telafi etmek için ona çiçek aldım."},
        {"en": "Point out", "tr": "belirtmek, işaret etmek", "ex_en": "She pointed out several mistakes in my report.", "ex_tr": "Raporumdaki birkaç hataya işaret etti."},
        {"en": "Once in a blue moon", "tr": "kırk yılda bir", "ex_en": "I live abroad now, so I only see my cousins once in a blue moon.", "ex_tr": "Artık yurt dışında yaşıyorum, bu yüzden kuzenlerimi kırk yılda bir görüyorum."},
        {"en": "Cupboard (British)", "tr": "dolap (İngiliz İngilizcesi)", "ex_en": "Put the plates back in the kitchen cupboard.", "ex_tr": "Tabakları mutfak dolabına geri koy."},
        {"en": "Cabinet (USA)", "tr": "dolap (Amerikan İngilizcesi)", "ex_en": "The medicine is kept in the bathroom cabinet.", "ex_tr": "İlaçlar banyo dolabında saklanır."}
    ]
}

def load_words():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(INITIAL_DATA, f, ensure_ascii=False, indent=4)
        return INITIAL_DATA
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

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

# --- YAPAY ZEKA YARDIMCI ÇAĞRI FONKSİYONU ---
def call_gemini_json(prompt, schema, temperature=0.5):
    models_to_try = ["gemini-3.8-flash", "gemini-3-flash-preview", "gemini-2.5-flash-lite"]
    last_error = None
    for model_name in models_to_try:
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=schema,
                    temperature=temperature
                )
            )
            return json.loads(response.text)
        except Exception as e:
            last_error = e
            continue
    raise last_error

def ai_generate_sentence(word_obj, level, direction):
    """Seçilen gizli kelimeyi içeren yeni bir İngilizce veya Türkçe cümle üretir."""
    if not client:
        return {
            "source_sentence": word_obj["ex_en"] if direction == "SENT_EN_TO_TR" else word_obj["ex_tr"],
            "reference_translation": word_obj["ex_tr"] if direction == "SENT_EN_TO_TR" else word_obj["ex_en"]
        }
    
    clean_en = word_obj["en"].split("(")[0].strip()
    prompt = f"""
    Sen bir İngilizce öğretmenisin. Öğrencinin seviyesi: {level}.
    Hedef İngilizce kelime/kalıp: "{clean_en}" (Türkçe anlamı: "{word_obj['tr']}").
    
    Bu hedef kelimeyi/kalıbı doğal ve öğretici bir bağlamda içeren, {level} seviyesine uygun YENİ ve kısa/orta uzunlukta tek bir cümle oluştur.
    Eğer yön "SENT_EN_TO_TR" ise source_sentence İngilizce, reference_translation Türkçe olsun.
    Eğer yön "SENT_TR_TO_EN" ise source_sentence Türkçe (içinde hedef kelimenin Türkçe anlamı doğal olarak geçsin), reference_translation ise hedef İngilizce kelimeyi ("{clean_en}") doğru formda içeren İngilizce cümle olsun.
    İstenen yön: {direction}
    """
    schema = {
        "type": "OBJECT",
        "properties": {
            "source_sentence": {"type": "STRING"},
            "reference_translation": {"type": "STRING"}
        },
        "required": ["source_sentence", "reference_translation"]
    }
    try:
        return call_gemini_json(prompt, schema, temperature=0.8)
    except Exception:
        return {
            "source_sentence": word_obj["ex_en"] if direction == "SENT_EN_TO_TR" else word_obj["ex_tr"],
            "reference_translation": word_obj["ex_tr"] if direction == "SENT_EN_TO_TR" else word_obj["ex_en"]
        }

def ai_evaluate_translation(source_sentence, user_answer, target_word_obj, direction):
    """Kullanıcının yazdığı cümleyi yazım (spelling) ve dilbilgisi kurallarına göre değerlendirir."""
    if not client:
        return {
            "is_correct": False,
            "score": 0,
            "feedback": "⚠️ Yapay zeka kontrolü için Streamlit Secrets ayarlarına GEMINI_API_KEY eklenmelidir.",
            "ideal_answer": target_word_obj["ex_en"] if direction == "SENT_TR_TO_EN" else target_word_obj["ex_tr"]
        }

    clean_en = target_word_obj["en"].split("(")[0].strip()
    if direction == "SENT_TR_TO_EN":
        criteria_note = f"""
        Kullanıcı Türkçe cümleyi İngilizceye çevirdi. 
        Arka planda test edilen hedef kelime/kalıp: '{clean_en}' (Türkçesi: '{target_word_obj['tr']}').
        EN ÖNEMLİ KRİTERLER:
        1) Hedef kelime/kalıp olan '{clean_en}' (veya cümle zamanına/gramerine uygun çekimli hali) cümlede kullanılmış ve HARFİ HARFİNE DOĞRU YAZILMIŞ (spelling hatasız) olmalı. Eğer eş anlamlı başka bir kelime yazdıysa hedef kelimeyi kullanmadığını nazikçe belirt ve puan kır.
        2) İngilizce cümle dilbilgisi (gramer, edatlar, zamanlar, kelime dizilimi) açısından kurallı ve anlamlı olmalı.
        """
    else:
        criteria_note = f"""
        Kullanıcı İngilizce cümleyi Türkçeye çevirdi.
        Arka planda test edilen hedef kelime/kalıp: '{clean_en}' (Türkçesi: '{target_word_obj['tr']}').
        EN ÖNEMLİ KRİTERLER:
        1) Hedef kelime olan '{clean_en}' kelimesinin Türkçe anlamı ('{target_word_obj['tr']}') çeviride doğru verilmiş olmalı.
        2) Türkçe cümle anlamlı, doğal ve kurallı olmalı.
        """

    prompt = f"""
    Sen titiz ama teşvik edici bir İngilizce öğretmenisin. Öğrencinin çevirisini değerlendir.
    
    Kaynak Cümle: "{source_sentence}"
    Öğrencinin Cevabı: "{user_answer}"
    
    Değerlendirme Kuralları:
    {criteria_note}
    - Küçük noktalama eksikliklerini veya büyük/küçük harf farklarını tolere et ama hedef kelimedeki harf hatalarını (spelling) ve gramer hatalarını mutlaka yakala ve puan kır.
    - Puanı 100 üzerinden ver. 75 ve üzeri ise is_correct = true olsun.
    - Geri bildirimi (feedback) Türkçe, kısa, net ve öğretici yaz (hedef kelimenin ne olduğunu da geri bildirimde belirterek doğru kullanımını göster).
    """
    schema = {
        "type": "OBJECT",
        "properties": {
            "is_correct": {"type": "BOOLEAN"},
            "score": {"type": "INTEGER"},
            "feedback": {"type": "STRING"},
            "ideal_answer": {"type": "STRING"}
        },
        "required": ["is_correct", "score", "feedback", "ideal_answer"]
    }
    try:
        return call_gemini_json(prompt, schema, temperature=0.2)
    except Exception as e:
        return {
            "is_correct": False,
            "score": 0,
            "feedback": f"Yapay zeka servisine şu an ulaşılamıyor. Lütfen birkaç saniye sonra tekrar deneyin. (Detay: {str(e)})",
            "ideal_answer": target_word_obj["ex_en"] if direction == "SENT_TR_TO_EN" else target_word_obj["ex_tr"]
        }

# --- SESSION STATE YÖNETİMİ ---
if "words_db" not in st.session_state:
    st.session_state.words_db = load_words()

if "current_level" not in st.session_state:
    st.session_state.current_level = "B1"

if "card_index" not in st.session_state:
    st.session_state.card_index = 0

if "card_mode" not in st.session_state:
    st.session_state.card_mode = random.choice(["EN_TO_TR", "TR_TO_EN", "SENT_EN_TO_TR", "SENT_TR_TO_EN"])

if "card_ai_sentence" not in st.session_state:
    st.session_state.card_ai_sentence = None

if "card_ai_eval" not in st.session_state:
    st.session_state.card_ai_eval = None

if "show_meaning" not in st.session_state:
    st.session_state.show_meaning = False

if "quiz_score" not in st.session_state:
    st.session_state.quiz_score = 0

if "quiz_total" not in st.session_state:
    st.session_state.quiz_total = 0

if "quiz_question" not in st.session_state:
    st.session_state.quiz_question = None

def reset_card_state(new_index, level):
    st.session_state.card_index = new_index
    st.session_state.show_meaning = False
    st.session_state.card_ai_eval = None
    mode = random.choice(["EN_TO_TR", "TR_TO_EN", "SENT_EN_TO_TR", "SENT_TR_TO_EN"])
    st.session_state.card_mode = mode
    if mode in ["SENT_EN_TO_TR", "SENT_TR_TO_EN"]:
        word_obj = st.session_state.words_db[level][new_index]
        with st.spinner("🤖 Yapay zeka cümle hazırlıyor..."):
            st.session_state.card_ai_sentence = ai_generate_sentence(word_obj, level, mode)
    else:
        st.session_state.card_ai_sentence = None

def create_quiz_question(level):
    word_list = st.session_state.words_db[level]
    target = random.choice(word_list)
    q_type = random.choice(["EN_TO_TR", "TR_TO_EN", "SENT_EN_TO_TR", "SENT_TR_TO_EN"])
    
    if q_type in ["EN_TO_TR", "TR_TO_EN"]:
        if q_type == "EN_TO_TR":
            wrong_choices = random.sample([w["tr"] for w in word_list if w["en"] != target["en"]], 3)
            correct_answer = target["tr"]
        else:
            wrong_choices = random.sample([w["en"] for w in word_list if w["tr"] != target["tr"]], 3)
            correct_answer = target["en"]
        options = wrong_choices + [correct_answer]
        random.shuffle(options)
        return {
            "word": target,
            "q_type": q_type,
            "correct_answer": correct_answer,
            "options": options,
            "answered": False,
            "selected": None
        }
    else:
        with st.spinner("🤖 Yapay zeka cümle sorusu hazırlıyor..."):
            sent_data = ai_generate_sentence(target, level, q_type)
        return {
            "word": target,
            "q_type": q_type,
            "sent_data": sent_data,
            "answered": False,
            "ai_eval": None
        }

# --- ARAYÜZ BAŞLANGICI ---
st.markdown('<div class="main-title">🌿 VocabMaster AI</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">B1 & B2 İnteraktif Kelime ve Cümle Pratiği</div>', unsafe_allow_html=True)

if not client:
    st.warning("⚠️ **Yapay Zeka Aktif Değil:** Cümle oluşturma ve değerlendirme özelliğinin çalışması için Streamlit Secrets ayarlarına `GEMINI_API_KEY` eklemelisiniz.")

col_lvl1, col_lvl2 = st.columns(2)
with col_lvl1:
    if st.button("📘 B1 Seviyesi (" + str(len(st.session_state.words_db["B1"])) + " Kelime)"):
        st.session_state.current_level = "B1"
        reset_card_state(0, "B1")
        st.session_state.quiz_question = create_quiz_question("B1")
        st.rerun()
with col_lvl2:
    if st.button("📗 B2 Seviyesi (" + str(len(st.session_state.words_db["B2"])) + " Kelime)"):
        st.session_state.current_level = "B2"
        reset_card_state(0, "B2")
        st.session_state.quiz_question = create_quiz_question("B2")
        st.rerun()

level = st.session_state.current_level
words = st.session_state.words_db[level]

st.info(f"Şu an seçili kur: **{level} Seviyesi**")

tab1, tab2, tab3, tab4 = st.tabs(["🗂️ Kelime Kartları", "🎯 Mini Quiz", "➕ Yeni Kelime Ekle", "📋 Tüm Liste"])

# --- SEKME 1: KELİME KARTLARI ---
with tab1:
    if len(words) > 0:
        if st.session_state.card_index >= len(words):
            st.session_state.card_index = 0
            
        current_word = words[st.session_state.card_index]
        mode = st.session_state.card_mode
        
        if mode in ["SENT_EN_TO_TR", "SENT_TR_TO_EN"] and st.session_state.card_ai_sentence is None:
            with st.spinner("🤖 Yapay zeka cümle hazırlıyor..."):
                st.session_state.card_ai_sentence = ai_generate_sentence(current_word, level, mode)
        
        progress = (st.session_state.card_index + 1) / len(words)
        st.progress(progress)
        st.caption(f"Kart {st.session_state.card_index + 1} / {len(words)}")

        # --- DURUM A: KLASİK KELİME KARTI ---
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

        # --- DURUM B: YAPAY ZEKA CÜMLE ÇEVİRİSİ KARTI (HEDEF KELİME GİZLİ) ---
        else:
            sent_data = st.session_state.card_ai_sentence
            if mode == "SENT_EN_TO_TR":
                badge_text = "✍️ Cümle Çevirisi: 🇬🇧 İngilizce ➔ 🇹🇷 Türkçe"
                instruction = "Aşağıdaki İngilizce cümleyi kurallı bir şekilde Türkçeye çevir:"
            else:
                badge_text = "✍️ Cümle Çevirisi: 🇹🇷 Türkçe ➔ 🇬🇧 İngilizce"
                instruction = "Aşağıdaki Türkçe cümleyi kurallı bir şekilde İngilizceye çevir:"

            card_html = f'<div class="word-card"><div class="lang-badge">{badge_text}</div><div style="font-size:0.95rem; color:#52796F; font-weight:600; margin-top:4px;">{instruction}</div><div class="sentence-main">"{sent_data["source_sentence"]}"</div></div>'
            st.markdown(card_html, unsafe_allow_html=True)

            if mode == "SENT_EN_TO_TR":
                if st.button("🔊 Cümleyi Dinle", key="listen_ai_sent"):
                    st.audio(generate_audio(sent_data["source_sentence"]), format="audio/mp3", autoplay=True)

            user_translation = st.text_area("Çevirini buraya yaz:", key=f"card_input_{st.session_state.card_index}", height=90, placeholder="Cümlenizi yazıp aşağıdaki kontrol butonuna basın...")
            
            if st.button("🤖 Yapay Zeka ile Kontrol Et", key="check_card_ai"):
                if user_translation.strip():
                    with st.spinner("🤖 Yapay zeka yazım ve gramer kontrolü yapıyor..."):
                        st.session_state.card_ai_eval = ai_evaluate_translation(
                            sent_data["source_sentence"],
                            user_translation.strip(),
                            current_word,
                            mode
                        )
                else:
                    st.warning("⚠️ Lütfen önce boşluğa çevirinizi yazın.")

            if st.session_state.card_ai_eval:
                ev = st.session_state.card_ai_eval
                if ev["is_correct"]:
                    st.success(f"✅ **Harika! (Puan: {ev['score']}/100)**\n\n{ev['feedback']}")
                else:
                    st.error(f"❌ **Geliştirilmeli (Puan: {ev['score']}/100)**\n\n{ev['feedback']}")
                
                if ev.get("ideal_answer"):
                    st.info(f"💡 **Örnek Doğru Çeviri:** {ev['ideal_answer']}\n\n🎯 **Test Edilen Kelime:** {current_word['en']} ({current_word['tr']})")
                    if mode == "SENT_TR_TO_EN":
                        if st.button("🔊 Doğru İngilizce Cümleyi Dinle", key="listen_ideal_card"):
                            st.audio(generate_audio(ev["ideal_answer"]), format="audio/mp3", autoplay=True)

        st.write("")
        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button("⬅️ Önceki"):
                reset_card_state((st.session_state.card_index - 1) % len(words), level)
                st.rerun()
        with c2:
            if st.button("🎲 Rastgele"):
                reset_card_state(random.randint(0, len(words) - 1), level)
                st.rerun()
        with c3:
            if st.button("Sonraki ➡️"):
                reset_card_state((st.session_state.card_index + 1) % len(words), level)
                st.rerun()

# --- SEKME 2: MINI QUIZ ---
with tab2:
    st.markdown(f"### 🎯 {level} Seviyesi Hızlı Test")
    st.caption(f"Toplam Skor: **{st.session_state.quiz_score} Doğru** / {st.session_state.quiz_total} Soru")
    
    if st.session_state.quiz_question is None:
        st.session_state.quiz_question = create_quiz_question(level)
        
    q = st.session_state.quiz_question
    q_word = q["word"]
    q_type = q["q_type"]
    
    # --- QUIZ DURUM A: ÇOKTAN SEÇMELİ KELİME ---
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
            if st.button("🔊 İngilizce Telaffuzunu Dinle", key="quiz_audio"):
                st.audio(generate_audio(q_word["en"]), format="audio/mp3", autoplay=True)
            
        st.write("")
        for idx, opt in enumerate(q["options"]):
            if st.button(opt, key=f"opt_{idx}", disabled=q["answered"]):
                q["answered"] = True
                q["selected"] = opt
                st.session_state.quiz_total += 1
                if opt == q["correct_answer"]:
                    st.session_state.quiz_score += 1
                st.rerun()
                
        if q["answered"]:
            if q["selected"] == q["correct_answer"]:
                st.success(f"🎉 Harika! Doğru cevap: **{q['correct_answer']}**")
            else:
                st.error(f"❌ Yanlış! Senin seçimin: {q['selected']} | Doğru cevap: **{q['correct_answer']}**")
                
            if q_word.get("ex_en"):
                st.info(f"💡 **Örnek Cümle:** {q_word['ex_en']}\n\n*{q_word.get('ex_tr', '')}*")
                
            if st.button("Sonraki Soruya Geç ➡️", key="next_quiz_mc"):
                st.session_state.quiz_question = create_quiz_question(level)
                st.rerun()

    # --- QUIZ DURUM B: YAPAY ZEKA YAZMA / CÜMLE ÇEVİRİSİ (HEDEF KELİME GİZLİ) ---
    else:
        sent_data = q["sent_data"]
        if q_type == "SENT_EN_TO_TR":
            q_badge = "✍️ Yazma Sorusu: 🇬🇧 İngilizce ➔ 🇹🇷 Türkçe"
            q_prompt = "Bu İngilizce cümleyi kurallı bir şekilde Türkçeye çevir:"
        else:
            q_badge = "✍️ Yazma Sorusu: 🇹🇷 Türkçe ➔ 🇬🇧 İngilizce"
            q_prompt = "Bu Türkçe cümleyi kurallı bir şekilde İngilizceye çevir:"

        quiz_card_html = f'<div class="word-card" style="padding: 20px;"><div class="lang-badge">{q_badge}</div><div style="font-size: 0.95rem; color: #52796F; font-weight: 600; margin-top:4px;">{q_prompt}</div><div class="sentence-main">"{sent_data["source_sentence"]}"</div></div>'
        st.markdown(quiz_card_html, unsafe_allow_html=True)

        if q_type == "SENT_EN_TO_TR":
            if st.button("🔊 Cümleyi Dinle", key="quiz_sent_audio"):
                st.audio(generate_audio(sent_data["source_sentence"]), format="audio/mp3", autoplay=True)

        quiz_user_text = st.text_area("Çevirini buraya yaz:", key=f"quiz_input_{st.session_state.quiz_total}", height=90, disabled=q["answered"])

        if not q["answered"]:
            if st.button("🤖 Cevabı Kontrol Et", key="submit_quiz_ai"):
                if quiz_user_text.strip():
                    with st.spinner("🤖 Yapay zeka cevabını inceliyor..."):
                        ev = ai_evaluate_translation(
                            sent_data["source_sentence"],
                            quiz_user_text.strip(),
                            q_word,
                            q_type
                        )
                        q["ai_eval"] = ev
                        q["answered"] = True
                        st.session_state.quiz_total += 1
                        if ev["is_correct"]:
                            st.session_state.quiz_score += 1
                        st.rerun()
                else:
                    st.warning("⚠️ Lütfen önce çevirinizi yazın.")

        if q["answered"] and q.get("ai_eval"):
            ev = q["ai_eval"]
            if ev["is_correct"]:
                st.success(f"🎉 **Tebrikler! Puan kazandın ({ev['score']}/100)**\n\n{ev['feedback']}")
            else:
                st.error(f"❌ **Hatalı veya Eksik Çeviri ({ev['score']}/100)**\n\n{ev['feedback']}")
            
            if ev.get("ideal_answer"):
                st.info(f"💡 **Örnek Doğru Çeviri:** {ev['ideal_answer']}\n\n🎯 **Test Edilen Kelime:** {q_word['en']} ({q_word['tr']})")
                if q_type == "SENT_TR_TO_EN":
                    if st.button("🔊 Doğru İngilizce Cümleyi Dinle", key="listen_ideal_quiz"):
                        st.audio(generate_audio(ev["ideal_answer"]), format="audio/mp3", autoplay=True)

            if st.button("Sonraki Soruya Geç ➡️", key="next_quiz_ai"):
                st.session_state.quiz_question = create_quiz_question(level)
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
