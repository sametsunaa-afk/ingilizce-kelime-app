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
        {"en": "Innate", "tr
