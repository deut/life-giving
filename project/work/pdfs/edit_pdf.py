from io import BytesIO
from pathlib import Path

from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import Color
from reportlab.lib.utils import ImageReader
from PIL import Image, ImageEnhance, ImageFilter, ImageDraw


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "work/pdfs/edited-source.pdf"
OUTPUT = ROOT / "outputs/zhyttiedaina_brandbook_page12_cream_qr.pdf"
USER_LOGO = ROOT / "work/pdfs/extracted/p6-1-Im2.png"
UPSCALED_LOGO = ROOT / "outputs/zhyttiedaina_logo_upscaled_4096.png"
PAGE1_CIRCLE_LOGO = ROOT / "work/pdfs/page1-logo-circle.png"
PAGE6_LOGO = ROOT / "work/pdfs/page6-logo-new-sharp.png"

pdfmetrics.registerFont(TTFont("RobotoFix", str(ROOT / "fonts/Roboto-Regular.ttf")))
pdfmetrics.registerFont(TTFont("RobotoBoldFix", str(ROOT / "fonts/Roboto-Bold.ttf")))

PINK = Color(0.973, 0.847, 0.858)
BLACK = Color(0.105, 0.088, 0.083)
WHITE = Color(1, 1, 1)
OFFWHITE = Color(0.965, 0.955, 0.925)
LIGHTGRAY = Color(0.91, 0.91, 0.89)
CORAL = Color(0.937, 0.447, 0.353)
DEEP_CORAL = Color(0.710, 0.290, 0.245)
TERRACOTTA = Color(0.769, 0.475, 0.431)
MIST = Color(0.965, 0.894, 0.878)
GRAPHITE = Color(0.243, 0.169, 0.161)


def rect(c, x, top, width, height, page_h, color):
    c.setFillColor(color)
    c.setStrokeColor(color)
    c.rect(x, page_h - top - height, width, height, fill=1, stroke=0)


def text(c, x, top, value, size, page_h, font="RobotoFix", color=BLACK):
    c.setFillColor(color)
    c.setFont(font, size)
    c.drawString(x, page_h - top - size * 0.82, value)


def centered(c, cx, top, value, size, page_h, font="RobotoFix", color=BLACK):
    c.setFont(font, size)
    c.setFillColor(color)
    c.drawCentredString(cx, page_h - top - size * 0.82, value)


def multiline(c, x, top, lines, size, leading, page_h, font="RobotoFix", color=BLACK):
    for i, line in enumerate(lines):
        text(c, x, top + i * leading, line, size, page_h, font, color)


def header(c, page_no, section, page_h):
    c.setFillColor(PINK)
    c.rect(0, 0, 1440, page_h, fill=1, stroke=0)
    text(c, 81, 52, f"Сторінка {page_no:02d}", 25, page_h)
    c.setFillColor(Color(1, 0.30, 0.27))
    c.rect(81, page_h - 91, 80, 7, fill=1, stroke=0)
    c.setFont("RobotoBoldFix", 25)
    c.setFillColor(BLACK)
    c.drawRightString(1360, page_h - 52 - 20.5, section)


def rule(c, x=81, top=91, width=82, page_h=810):
    rect(c, x, top, width, 7, page_h, CORAL)


def pill(c, x, top, value, page_h):
    c.setFillColor(MIST); c.roundRect(x, page_h-top-34, 142, 34, 17, fill=1, stroke=0)
    centered(c, x+71, top+8, value, 14, page_h, "RobotoBoldFix", GRAPHITE)


def source_image(page_index, image_index=0):
    src_reader = PdfReader(str(SOURCE))
    return ImageReader(BytesIO(src_reader.pages[page_index].images[image_index].data))


def build_page1_logo_overlay(width, height):
    stream=BytesIO(); c=canvas.Canvas(stream,pagesize=(width,height))
    cx, cy, radius = 1165, height - 405, 198
    c.drawImage(ImageReader(str(PAGE1_CIRCLE_LOGO)),cx-radius,cy-radius,
                width=radius*2,height=radius*2,preserveAspectRatio=True,mask='auto')
    c.save(); stream.seek(0)
    return PdfReader(stream).pages[0]


def build_page1(width, height):
    logo_src = ROOT / "work/pdfs/extracted/p6-1-Im2.png"
    logo_circle = ROOT / "work/pdfs/page1-logo-circle.png"
    if not logo_circle.exists():
        im = Image.open(logo_src).convert("RGB").resize((1536, 1536), Image.Resampling.LANCZOS)
        im = im.filter(ImageFilter.UnsharpMask(radius=1.0, percent=80, threshold=3))
        mask = Image.new("L", im.size, 0)
        ImageDraw.Draw(mask).ellipse((10, 10, 1526, 1526), fill=255)
        rgba = im.convert("RGBA"); rgba.putalpha(mask); rgba.save(logo_circle, optimize=True)
    stream=BytesIO(); c=canvas.Canvas(stream,pagesize=(width,height))
    rect(c,0,0,width,height,height,PINK)
    text(c,82,55,"Брендбук 2026",18,height,"RobotoFix",GRAPHITE)
    c.setFont("RobotoFix",18); c.setFillColor(GRAPHITE); c.drawRightString(1358,height-55-14.8,"Версія 1.0")
    text(c,105,178,"Брендбук",62,height,"RobotoBoldFix",GRAPHITE)
    multiline(c,108,263,["ГРОМАДСЬКОЇ ОРГАНІЗАЦІЇ","«ЖИТТЄДАЙНА»"],20,32,height,"RobotoBoldFix",GRAPHITE)
    rule(c,108,345,100,height)
    multiline(c,108,382,["Сила жінки — у праві на безпеку,","гідність і власний вибір."],24,36,height,"RobotoFix",GRAPHITE)
    # Recreate the original layered cover motif without a rectangular image edge.
    c.drawImage(source_image(0,0),785,height-720,width=610,height=610,preserveAspectRatio=True,mask='auto')
    c.setStrokeColor(WHITE); c.setLineWidth(4); c.circle(1090,height-405,190,fill=0,stroke=1)
    c.drawImage(ImageReader(str(logo_circle)),900,height-595,width=380,height=380,preserveAspectRatio=True,mask='auto')
    text(c,82,742,"НАШ ПРОСТІР · УКРАЇНА",14,height,"RobotoBoldFix",GRAPHITE)
    c.setFont("RobotoBoldFix",14); c.setFillColor(GRAPHITE); c.drawRightString(1358,height-742-11.5,"LIVE-GIVING.ORG.UA")
    c.save(); stream.seek(0); return PdfReader(stream).pages[0]


def build_page2(width, height):
    stream=BytesIO(); c=canvas.Canvas(stream,pagesize=(width,height)); header(c,2,"Зміст",height)
    text(c,82,120,"Зміст",54,height,"RobotoBoldFix",GRAPHITE); rule(c,82,183,85,height)
    multiline(c,82,225,["Цей документ описує візуальну та змістову","ідентичність ГО «Життєдайна»: хто ми, що","говоримо і як виглядаємо в кожній точці контакту."],20,31,height,"RobotoFix",GRAPHITE)
    rect(c,80,365,540,150,height,Color(.96,.77,.75)); rect(c,80,365,8,150,height,DEEP_CORAL)
    multiline(c,112,395,["Дотримання цих правил робить організацію","впізнаваною — у громаді, у грантовій заявці","та в соціальних мережах."],22,35,height,"RobotoBoldFix",GRAPHITE)
    items=[("01","Про організацію"),("02","Місія та візія"),("03","Цінності бренду"),("04","Логотип"),("05","Типографіка"),("06","Колірна палітра"),("07","Комунікація та носії")]
    for i,(n,label) in enumerate(items):
        top=128+i*77; text(c,760,top,n,18,height,"RobotoBoldFix",CORAL); text(c,835,top,label,23,height,"RobotoBoldFix",GRAPHITE)
        c.setStrokeColor(CORAL); c.setLineWidth(2); c.line(760,height-top-38,1355,height-top-38)
    c.save(); stream.seek(0); return PdfReader(stream).pages[0]


def build_page3(width, height):
    stream=BytesIO(); c=canvas.Canvas(stream,pagesize=(width,height)); header(c,3,"01. Про організацію",height)
    text(c,82,120,"Жіноча організація, яка діє поруч",43,height,"RobotoBoldFix",GRAPHITE); rule(c,82,174,90,height)
    paras=[
      ["ГО «Життєдайна» — жіноча громадська організація, створена", "для підтримки та посилення жінок, дітей і молоді, особливо тих,", "хто опинився у складних життєвих обставинах, постраждав від", "війни, домашнього та гендерно зумовленого насильства."],
      ["Ми працюємо на перетині прав людини, гендерної рівності,", "захисту від насильства, правової та психологічної підтримки,", "жіночого лідерства і розвитку громад."],
      ["Організація поєднує професійну експертизу, практичну", "допомогу та розвиток спроможності людей і громад. Ми не лише", "реагуємо на проблеми, а й допомагаємо людям відновлювати", "впевненість у собі, знати свої права, приймати рішення та", "ставати активними учасницями змін."]]
    y=225
    for lines in paras: multiline(c,82,y,lines,18.5,29,height,"RobotoFix",GRAPHITE); y+=len(lines)*29+25
    # The content field is divided at the golden ratio: 61.8% text / 38.2% directions.
    rect(c,910,215,450,480,height,CORAL)
    centered(c,1135,248,"НАПРЯМИ РОБОТИ",16,height,"RobotoBoldFix",WHITE)
    topics=["Захист прав жінок і дітей","Протидія насильству","Психологічна підтримка","Жіноче лідерство","Правова допомога","Робота з громадами"]
    for i,t in enumerate(topics):
        yy=300+i*58; rect(c,940,yy,390,42,height,Color(.98,.90,.88)); text(c,965,yy+11,t,16,height,"RobotoBoldFix",GRAPHITE)
    c.save(); stream.seek(0); return PdfReader(stream).pages[0]


def build_page4(width, height):
    stream=BytesIO(); c=canvas.Canvas(stream,pagesize=(width,height)); header(c,4,"02. Місія та візія",height)
    text(c,82,120,"Наша місія",42,height,"RobotoBoldFix",GRAPHITE); rule(c,82,172,78,height)
    multiline(c,82,210,["Створювати умови, у яких кожна жінка має", "право на безпеку, гідність, свободу вибору", "та можливість змінювати власне життя", "і свою громаду."],23.5,36,height,"RobotoBoldFix",GRAPHITE)
    c.setStrokeColor(CORAL); c.setLineWidth(3); c.line(700,height-120,700,height-690)
    text(c,745,120,"Наша візія",42,height,"RobotoBoldFix",GRAPHITE)
    multiline(c,745,195,["Україна, у якій жінки живуть у безпеці та гідності,","знають і захищають свої права, мають рівні можливості","та впливають на рішення, що визначають майбутнє","їхніх сімей, громад і країни."],22,34,height,"RobotoBoldFix",DEEP_CORAL)
    text(c,745,370,"Ми прагнемо громад, у яких:",20,height,"RobotoBoldFix",GRAPHITE)
    goals=["немає толерантності до насильства;","права людини є реальною цінністю;","жінки мають голос і вплив;","допомогу можна отримати в кризі;","різноманітність сприймається як ресурс."]
    for i,g in enumerate(goals): text(c,770,415+i*43,"•  "+g,19,height,"RobotoFix",GRAPHITE)
    c.save(); stream.seek(0); return PdfReader(stream).pages[0]


def build_page5(width, height):
    stream=BytesIO(); c=canvas.Canvas(stream,pagesize=(width,height)); header(c,5,"03. Цінності бренду",height)
    text(c,82,112,"Наші цінності",50,height,"RobotoBoldFix",GRAPHITE)
    multiline(c,760,116,["Дев’ять принципів визначають зміст комунікації бренду:","як ми говоримо, що обіцяємо і за що відповідаємо."],19,29,height,"RobotoBoldFix",GRAPHITE)
    cards=[("Гідність","Кожна людина має право на повагу, безпеку та гідне життя."),("Рівність","Рівні права, можливості та доступ до ресурсів."),("Безпека","Безпечне середовище — фундамент відновлення."),("Справедливість","Захист прав людини та відповідальність."),("Підтримка","Ми поруч і допомагаємо відновити власну силу."),("Жіноче лідерство","Жінки — лідерки та експертки змін."),("Партнерство","Стійкі зміни створюються через довіру."),("Професійність","Знання, досвід і доказові підходи."),("Відповідальність","Перед людьми, ресурсами й результатами.")]
    xs=[82,512,942]; tops=[218,398,578]
    for i,(title_,body) in enumerate(cards):
        x=xs[i%3]; top=tops[i//3]; w=398; h=160
        # Fill the rounded card first; the body color overlays the lower field without a divider.
        c.setFillColor(MIST); c.setStrokeColor(MIST)
        c.roundRect(x,height-top-h,w,h,8,fill=1,stroke=0)
        rect(c,x,top+60,w,h-60,height,PINK)
        rect(c,x+18,top+13,34,34,height,DEEP_CORAL)
        centered(c,x+35,top+21,f"{i+1:02d}",13,height,"RobotoBoldFix",WHITE)
        text(c,x+68,top+18,title_,23,height,"RobotoBoldFix",GRAPHITE)
        words=body.split(); lines=[]; line=""
        for word in words:
            trial=(line+" "+word).strip()
            if pdfmetrics.stringWidth(trial,"RobotoFix",18)>348: lines.append(line); line=word
            else: line=trial
        if line: lines.append(line)
        multiline(c,x+24,top+82,lines,18,27,height,"RobotoFix",GRAPHITE)
        c.setFillColor(PINK); c.setStrokeColor(TERRACOTTA); c.setLineWidth(1.35)
        c.setLineJoin(0); c.setLineCap(0)
        c.roundRect(x,height-top-h,w,h,8,fill=0,stroke=1)
    c.save(); stream.seek(0); return PdfReader(stream).pages[0]


def build_page6(width, height):
    stream=BytesIO(); c=canvas.Canvas(stream,pagesize=(width,height)); header(c,6,"04. Логотип",height)
    text(c,82,112,"Жіночий профіль, поєднаний із",39,height,"RobotoBoldFix",GRAPHITE)
    text(c,82,160,"природними елементами",39,height,"RobotoBoldFix",GRAPHITE); rule(c,82,215,90,height)
    c.drawImage(ImageReader(str(PAGE6_LOGO)),95,height-650,width=410,height=410,preserveAspectRatio=True,mask='auto')
    text(c,115,675,"•  основний логотип",18,height,"RobotoFix",GRAPHITE); text(c,115,710,"•  знак + напис",18,height,"RobotoFix",GRAPHITE)
    multiline(c,700,108,["ЗНАК ПОЄДНУЄ ЖІНОЧИЙ ПРОФІЛЬ ІЗ ГІЛКАМИ", "ТА ВІНКОМ ЛИСТЯ. ПРОФІЛЬ — ЦЕ ЛЮДИНА,", "ЇЇ ГОЛОС І ВИБІР. РОСЛИННИЙ ВІНОК —", "ЖИТТЄДАЙНІСТЬ, ВІДНОВЛЕННЯ ТА ЗРОСТАННЯ,", "ЯКІ МИ ПОВЕРТАЄМО ЛЮДИНІ Й ГРОМАДІ."],16.5,27,height,"RobotoBoldFix",GRAPHITE)
    rect(c,620,275,740,435,height,PINK); c.setStrokeColor(Color(.7,.62,.6)); c.line(660,height-320,1320,height-320)
    blocks=[(660,355,"ЗНАЧЕННЯ",["Турбота без жалості:","спокійна сила, а не крихкість."]),(1010,355,"ХАРАКТЕР",["Органічна лінія, ручний штрих,","відсутність гострих кутів."]),(660,500,"КОЛІР ЗНАКА",["Темний теплий графіт #3E2B29", "на світлому чи кораловому тлі."]),(1010,500,"НАПИС",["«Життєдайна» — під знаком,", "по центру, без розрядки."])]
    for x,top,label,lines in blocks: text(c,x,top,label,15,height,"RobotoBoldFix",TERRACOTTA); multiline(c,x,top+42,lines,17,27,height,"RobotoFix",GRAPHITE)
    rect(c,660,630,660,54,height,MIST); rect(c,660,630,7,54,height,TERRACOTTA); text(c,685,648,"Для великого друку використовуйте оригінал високої роздільності.",15,height,"RobotoFix",GRAPHITE)
    c.save(); stream.seek(0); return PdfReader(stream).pages[0]


def build_page8(width, height):
    stream = BytesIO(); c = canvas.Canvas(stream, pagesize=(width, height))
    header(c, 8, "05. Типографіка", height)
    c.setFillColor(PINK); c.rect(105, 85, 1230, 625, fill=1, stroke=0)
    c.setStrokeColor(Color(.25,.25,.23)); c.setLineWidth(1)
    c.line(120, 100, 120, 700); c.line(720, 385, 720, 700); c.line(1320, 100, 1320, 700)
    text(c, 165, 112, "Бб", 104, height, "RobotoBoldFix")
    text(c, 780, 112, "Бб", 104, height, "RobotoFix")
    text(c, 165, 275, "Roboto Bold", 26, height, "RobotoBoldFix")
    text(c, 780, 275, "Roboto Regular", 26, height, "RobotoFix")
    multiline(c,165,312,["Заголовки, цитати та назви розділів. Bold 700.","Виразна сучасна ієрархія без декоративних шрифтів."],18,26,height)
    multiline(c,780,312,["Основний текст, підписи, інтерфейс і документи.","Regular 400; Bold 700 — для підзаголовків."],18,26,height)
    multiline(c,165,382,["АБВГДЕЄЖЗИІЇЙКЛМНОПРСТУФХЦЧШЩЬЮЯ","абвгдеєжзиіїйклмнопрстуфхцчшщьюя","0123456789"],23,33,height,"RobotoBoldFix")
    multiline(c,780,382,["АБВГДЕЄЖЗИІЇЙКЛМНОПРСТУФХЦЧШЩЬЮЯ","абвгдеєжзиіїйклмнопрстуфхцчшщьюя","0123456789"],23,33,height,"RobotoFix")
    c.line(165, height - 560, 1265, height - 560)
    text(c,165,582,"#1.  ·  Roboto Bold 700  ·  48/1.25",13,height,"RobotoBoldFix")
    text(c,165,617,"Право на безпеку",38,height,"RobotoBoldFix")
    text(c,610,582,"#2.  ·  Roboto Bold 700  ·  28/1.35",13,height,"RobotoBoldFix")
    centered(c,735,617,"Підтримка там, де вона",22,height,"RobotoFix"); centered(c,735,646,"потрібна",22,height,"RobotoFix")
    text(c,960,582,"Body  ·  Roboto Regular 400  ·  16/1.7",13,height,"RobotoBoldFix")
    centered(c,1110,617,"Ми надаємо правову та психологічну",17,height); centered(c,1110,646,"підтримку жінкам і дівчатам.",17,height)
    c.save(); stream.seek(0); return PdfReader(stream).pages[0]


def build_page7(width, height):
    src=ROOT/'work/pdfs/extracted/p7-0-Im9.jpg'
    crop=ROOT/'work/pdfs/extracted/p7-logo-original-sharpened.png'
    if not crop.exists():
        im=Image.open(src).convert('RGB').crop((142,80,430,360))
        im=im.resize((2304,2240),Image.Resampling.LANCZOS)
        im=im.filter(ImageFilter.UnsharpMask(radius=1.2,percent=105,threshold=4))
        im.save(crop,optimize=True)
    trimmed=ROOT/'work/pdfs/extracted/p7-logo-original-trimmed.png'
    if not trimmed.exists():
        im=Image.open(crop).convert('RGB')
        # Remove the pale scan edge, especially the strip along the right side.
        im=im.crop((14,14,im.width-36,im.height-14))
        im.save(trimmed,optimize=True)
    light_logo=ROOT/'work/pdfs/extracted/user-logo-light-v2.png'
    if not light_logo.exists():
        im=Image.open(USER_LOGO).convert('RGB')
        mask=Image.new('L',im.size,0)
        alpha=[]
        for r,g,b in im.getdata():
            lum=(r+g+b)/3
            chroma=max(r,g,b)-min(r,g,b)
            neutral=max(0.0,min(1.0,(78-chroma)/38))
            darkness=max(0.0,min(1.0,(145-lum)/55))
            alpha.append(round(255*neutral*darkness))
        mask.putdata(alpha)
        mask=mask.resize((1536,1536),Image.Resampling.LANCZOS)
        rgba=Image.new('RGBA',(1536,1536),(246,246,243,0)); rgba.putalpha(mask)
        rgba.save(light_logo,optimize=True)
    stream=BytesIO(); c=canvas.Canvas(stream,pagesize=(width,height))
    header(c,7,"04. Логотип + правила",height)
    text(c,81,100,"Версії та охоронне поле",42,height,"RobotoBoldFix")
    c.setFillColor(Color(1,.30,.27)); c.rect(81,height-155,90,7,fill=1,stroke=0)
    rect(c,80,170,1280,565,height,PINK)
    c.setStrokeColor(Color(.72,.55,.52)); c.setLineWidth(.8); c.line(105,height-190,1335,height-190)

    # Three vector-framed logo examples.
    c.drawImage(ImageReader(str(USER_LOGO)),148,height-405,width=205,height=205,preserveAspectRatio=True,mask='auto')
    rect(c,470,200,410,205,height,DEEP_CORAL)
    c.drawImage(ImageReader(str(light_logo)),580,height-398,width=190,height=190,preserveAspectRatio=True,mask='auto')
    rect(c,910,200,390,205,height,MIST)
    c.setStrokeColor(Color(.60,.36,.34)); c.setDash(5,4); c.rect(940,height-375,330,145,fill=0,stroke=1); c.setDash()
    c.drawImage(ImageReader(str(USER_LOGO)),1048,height-337,width=84,height=84,preserveAspectRatio=True,mask='auto')

    text(c,105,430,"О С Н О В Н А  ·  Н А  С В І Т Л О М У",15,height,"RobotoBoldFix",TERRACOTTA)
    multiline(c,105,465,["Тло #FBF6F3 або біле. Базовий варіант","для документів і сайту."],17,28,height)
    text(c,470,430,"М О Н О Х Р О М Н А  ·  Н А  К О Р А Л І",15,height,"RobotoBoldFix",TERRACOTTA)
    multiline(c,470,465,["Знак і напис у #F6F6F3 на глибокому коралі.","Для банерів, мерчу та темних поверхонь."],17,28,height)
    text(c,910,430,"О Х О Р О Н Н Е  П О Л Е",15,height,"RobotoBoldFix",TERRACOTTA)
    multiline(c,910,465,["Вільний простір з усіх боків — не менше висоти","напису «Життєдайна»."],17,28,height)

    c.setStrokeColor(Color(.72,.55,.52)); c.line(105,height-560,1335,height-560)
    text(c,105,585,"М І Н І М А Л Ь Н І  Р О З М І Р И",15,height,"RobotoBoldFix",TERRACOTTA)
    multiline(c,105,620,["Друк — не менше 22 мм по ширині знака.","Екран — не менше 64 px. Нижче цих значень","використовується лише знак, без напису."],16.5,27,height)
    text(c,575,585,"Н Е  М О Ж Н А",15,height,"RobotoBoldFix",TERRACOTTA)
    left=["×   розтягувати чи стискати","×   змінювати колір знака","×   розміщувати на фото без","    підкладки"]
    right=["×   обертати знак","×   додавати тінь і контур","×   пересувати знак і напис"]
    multiline(c,575,620,left,16.5,27,height)
    multiline(c,995,620,right,16.5,27,height)
    c.save(); stream.seek(0); return PdfReader(stream).pages[0]


def build_page6_overlay(width, height):
    stream=BytesIO(); c=canvas.Canvas(stream,pagesize=(width,height))
    # Replace the widely tracked serif paragraph with compact modern sans-serif.
    rect(c,625,92,815,225,height,PINK)
    paragraph = [
        "ЗНАК ПОЄДНУЄ ЖІНОЧИЙ ПРОФІЛЬ ІЗ",
        "ГІЛКАМИ ТА ВІНКОМ ЛИСТЯ. ПРОФІЛЬ —",
        "ЦЕ ЛЮДИНА, ЇЇ ГОЛОС І ВИБІР.",
        "РОСЛИННИЙ ВІНОК — ЖИТТЄДАЙНІСТЬ,",
        "ВІДНОВЛЕННЯ ТА ЗРОСТАННЯ, ЯКІ МИ",
        "ПОВЕРТАЄМО ЛЮДИНІ Й ГРОМАДІ.",
    ]
    for i, line in enumerate(paragraph):
        centered(c, 1130, 104 + i * 31, line, 18.5, height, "RobotoBoldFix", GRAPHITE)

    # Replace the raster information card only; keep the logo and page composition intact.
    rect(c,625,320,815,490,height,Color(.985,.98,.965))
    c.setStrokeColor(Color(.68,.62,.60)); c.setLineWidth(.8)
    c.line(660,height-370,1350,height-370)

    text(c,705,405,"З Н А Ч Е Н Н Я",14,height,"RobotoBoldFix",GRAPHITE)
    multiline(c,705,445,["Турбота без жалості: спокійна сила,", "а не крихкість."],18,29,height)
    text(c,1070,405,"Х А Р А К Т Е Р",14,height,"RobotoBoldFix",GRAPHITE)
    multiline(c,1070,445,["Органічна лінія, ручний штрих,", "відсутність гострих кутів."],18,29,height)

    text(c,705,525,"К О Л І Р  З Н А К А",14,height,"RobotoBoldFix",GRAPHITE)
    multiline(c,705,565,["Темний теплий графіт #3E2B29 на", "світлому або коралово-рожевому тлі."],18,29,height)
    text(c,1070,525,"Н А П И С",14,height,"RobotoBoldFix",GRAPHITE)
    multiline(c,1070,565,["«Життєдайна» — завжди під знаком,", "по центру, без розрядки."],18,29,height)

    rect(c,700,655,650,72,height,Color(.965,.90,.89))
    rect(c,700,655,7,72,height,TERRACOTTA)
    multiline(c,730,671,["Для продакшну потрібні векторні файли знака (SVG/EPS) та версія", "з прозорим тлом. Растровий градієнт не використовують для великого друку."],15.5,25,height)
    c.save(); stream.seek(0); return PdfReader(stream).pages[0]


def build_page5_overlay(width, height):
    stream=BytesIO(); c=canvas.Canvas(stream,pagesize=(width,height))
    rect(c,0,173,1360,637,height,OFFWHITE)
    cards=[
        ("Гідність",["Кожна людина має право на повагу,","безпеку та гідне життя."]),
        ("Рівність",["Рівні права, можливості та доступ до","ресурсів — незалежно від обставин."]),
        ("Безпека",["Безпечне середовище — фундамент","відновлення й самореалізації."]),
        ("Справедливість",["Захист прав людини та","відповідальність за їх порушення."]),
        ("Підтримка",["Ми поруч тоді, коли складно — і","допомагаємо відновити власну силу."]),
        ("Жіноче лідерство",["Жінки — не лише отримувачки","допомоги, а лідерки та експертки змін."]),
        ("Партнерство",["Стійкі зміни створюються разом —","через довіру та співпрацю."]),
        ("Професійність",["Знання, досвід, доказові підходи та","постійний розвиток команди."]),
        ("Відповідальність",["Перед людьми, ресурсами,","партнерами та результатами роботи."]),
    ]
    xs=[24,466,909]; tops=[183,391,607]
    for idx,(title,body) in enumerate(cards):
        x=xs[idx%3]; top=tops[idx//3]; w=426; h=190
        c.setStrokeColor(Color(.78,.62,.62)); c.setLineWidth(1.2)
        c.setFillColor(Color(.985,.965,.965)); c.roundRect(x,height-top-h,w,h,7,fill=1,stroke=1)
        c.setFillColor(Color(.95,.86,.87)); c.roundRect(x,height-top-67,w,67,7,fill=1,stroke=0)
        c.rect(x,height-top-67,w,9,fill=1,stroke=0)
        text(c,x+32,top+18,title,28,height,"RobotoBoldFix")
        multiline(c,x+32,top+90,body,18,31,height,"RobotoFix")
    c.save(); stream.seek(0); return PdfReader(stream).pages[0]


def build_page11(width, height):
    stream = BytesIO(); c = canvas.Canvas(stream, pagesize=(width, height))
    header(c, 11, "06. Колірна палітра", height)
    rect(c,82,105,1276,635,height,OFFWHITE)
    cols=[(132,CORAL,"#EF7264","Кораловий",["Основний акцент: кнопки,","лінії, заголовкові плашки."]),(377,DEEP_CORAL,"#B54A3E","Глибокий кораловий",["Тло під світлий текст:","плашки, пости, банери."]),(622,TERRACOTTA,"#C4796E","Теракотовий",["Другорядні акценти,","діаграми, стани наведення."]),(867,MIST,"#F6E4E0","Рожевий туман",["Підкладки, картки, виноски,","спокійні блоки тексту."]),(1112,GRAPHITE,"#3E2B29","Теплий графіт",["Колір знака та основного","тексту. Замінює чорний."])]
    for x,color,code,name,desc in cols:
        c.setFillColor(color); c.rect(x,500,195,190,fill=1,stroke=0)
        text(c,x,320,code,17,height,"RobotoBoldFix")
        text(c,x,350,name,20,height,"RobotoBoldFix")
        multiline(c,x,385,desc,15.5,25,height)
    c.setStrokeColor(GRAPHITE); c.setLineWidth(1); c.line(95,300,1310,300)
    text(c,95,530,"П Р О П О Р Ц І Ї",17,height,"RobotoBoldFix")
    x=95
    for width_,color in [(250,MIST),(85,CORAL),(40,DEEP_CORAL),(28,GRAPHITE)]:
        rect(c,x,570,width_,30,height,color); x+=width_
    multiline(c,95,610,["Тло 60% · рожевий туман 20% · кораловий","13% · графіт 7%."],16,25,height)
    text(c,580,530,"Н Е Й Т Р А Л Ь Н Е   Т Л О",17,height,"RobotoBoldFix")
    multiline(c,580,570,["Кремовий #FBF6F3 — тло всіх","документів; білий #FFFFFF — картки та","таблиці."],16,25,height)
    text(c,990,530,"К О Н Т Р А С Т",17,height,"RobotoBoldFix")
    multiline(c,990,570,["Світлий текст ставимо лише на","глибокий кораловий #B54A3E. На","яскравому #EF7264 — інший графіт","#3E2B29."],16,25,height)
    c.save(); stream.seek(0); return PdfReader(stream).pages[0]


def build_page12(width, height):
    stream=BytesIO(); c=canvas.Canvas(stream,pagesize=(width,height))
    header(c,12,"07. Соціальні мережі",height)
    # Compact social-media examples on a white presentation field.
    rect(c,82,105,920,635,height,OFFWHITE)
    text(c,112,125,"Соціальні мережі",42,height,"RobotoBoldFix",GRAPHITE)
    multiline(c,520,126,["Три типи публікацій: заява, анонс події та", "практична допомога. Формат 4:5, поле 40 px,", "підпис завжди внизу. Фото — лише зі згодою."],14,21,height,"RobotoFix",GRAPHITE)

    # Statement post.
    c.setFillColor(DEEP_CORAL); c.rect(112,height-675,145,430,fill=1,stroke=0)
    text(c,132,265,"Ж И Т Т Є Д А Й Н А",10,height,"RobotoBoldFix",WHITE)
    multiline(c,132,345,["Ви","маєте","право","на","безпеку"],26,31,height,"RobotoBoldFix",WHITE)
    c.setStrokeColor(WHITE); c.setLineWidth(1.2); c.line(132,height-565,165,height-565)
    multiline(c,132,582,["Безоплатна","правова та","психологічна","допомога"],12,17,height,"RobotoFix",WHITE)

    # Event post.
    text(c,300,238,"А Н О Н С    18 Ж О В Т Н Я",11,height,"RobotoBoldFix",GRAPHITE)
    c.drawImage(ImageReader(str(PAGE6_LOGO)),300,height-645,width=370,height=370,preserveAspectRatio=True,mask='auto')
    text(c,300,660,"Група підтримки для жінок",14,height,"RobotoFix",GRAPHITE)

    # Practical-help post.
    c.setStrokeColor(GRAPHITE); c.setLineWidth(.8)
    c.line(712,height-680,712,height-240); c.line(735,height-240,955,height-240)
    text(c,735,250,"Я К  О Т Р И М А Т И",13,height,"RobotoBoldFix",GRAPHITE)
    text(c,735,274,"Д О П О М О Г У",13,height,"RobotoBoldFix",GRAPHITE)
    steps=[("01",["Зателефонуйте","або напишіть нам"]),("02",["Розкажіть про ситуацію —","конфіденційно"]),("03",["Отримайте юриста","та психолога"])]
    for i,(num,lines) in enumerate(steps):
        top=330+i*112
        text(c,735,top,num,15,height,"RobotoBoldFix",DEEP_CORAL)
        multiline(c,775,top,lines,14.5,22,height,"RobotoFix",GRAPHITE)

    # Supplied QR codes, kept in their original proportions.
    qr_instagram = ROOT / "work/pdfs/qr-instagram-card-cream.png"
    qr_facebook = ROOT / "work/pdfs/qr-facebook-card-cream.png"
    c.drawImage(ImageReader(str(qr_instagram)),1092,height-375,width=225,height=225,preserveAspectRatio=True,anchor='c',mask='auto')
    c.drawImage(ImageReader(str(qr_facebook)),1092,height-675,width=225,height=225,preserveAspectRatio=True,anchor='c',mask='auto')
    centered(c,1204.5,693,"Код ЄДРПОУ 45638920",13,height,"RobotoBoldFix",GRAPHITE)
    c.save(); stream.seek(0); return PdfReader(stream).pages[0]


def build_page9(width, height):
    stream=BytesIO(); c=canvas.Canvas(stream,pagesize=(width,height)); header(c,9,"05. Типографіка + тон",height)
    text(c,82,112,"Як ми говоримо",44,height,"RobotoBoldFix",GRAPHITE); rule(c,82,166,82,height)
    statements=["Ми працюємо там, де починаються зміни — у громадах і серед жінок, які діють.","Наша команда поєднує досвід, підтримку та можливості для зростання.","Говоримо коротко й шанобливо, без драматизації — про силу, права та вибір.","Ми створюємо умови для жіночого лідерства й безпечних громад.","Кожен крок — внесок у сильніше та справедливіше суспільство.","Підтримуємо жінок, які розвивають громади та змінюють світ навколо.","У центрі нашої діяльності — співпраця, навчання та реальні дії.","Віримо в силу локальних рішень і жіночої ініціативи.","Там, де є підтримка, з’являються можливості, впевненість і зростання."]
    for i,s in enumerate(statements):
        text(c,92,220+i*49,"•",22,height,"RobotoBoldFix",CORAL)
        # compact wrap only where necessary
        if pdfmetrics.stringWidth(s,"RobotoFix",18)<=750: text(c,125,220+i*49,s,18,height,"RobotoFix",GRAPHITE)
        else:
            cut=max(j for j in range(len(s)) if pdfmetrics.stringWidth(s[:j],"RobotoFix",18)<=750 and s[j]==' ')
            text(c,125,213+i*49,s[:cut],18,height,"RobotoFix",GRAPHITE); text(c,125,236+i*49,s[cut+1:],18,height,"RobotoFix",GRAPHITE)
    examples=[("ТАК","«Ви маєте право на безпеку. Ми поруч і підкажемо наступний крок»." ,Color(.92,.96,.92)),("НІ","«Бідні жертви насильства потребують нашого порятунку»." ,Color(.98,.90,.90)),("ПРАВИЛО","Ніколи не публікуємо історій і фото без письмової згоди людини.",MIST)]
    for i,(tag,copy,bg) in enumerate(examples):
        top=205+i*172; rect(c,970,top,390,132,height,bg); text(c,995,top+18,tag,14,height,"RobotoBoldFix",DEEP_CORAL)
        words=copy.split(); lines=[]; line=""
        for word in words:
            trial=(line+" "+word).strip()
            if pdfmetrics.stringWidth(trial,"RobotoBoldFix",17)>335: lines.append(line); line=word
            else: line=trial
        if line: lines.append(line)
        multiline(c,995,top+50,lines,17,25,height,"RobotoBoldFix",GRAPHITE)
    c.save(); stream.seek(0); return PdfReader(stream).pages[0]


def build_page10(width, height):
    stream=BytesIO(); c=canvas.Canvas(stream,pagesize=(width,height)); header(c,10,"06. Колірна палітра",height)
    text(c,82,112,"Колірна палітра",45,height,"RobotoBoldFix",GRAPHITE); rule(c,82,168,88,height)
    multiline(c,82,220,["Палітра походить від логотипа: теплий кораловий градієнт,","рожевий туман і темний графіт знака. Це кольори світла","й тепла — не тривоги."],22,34,height,"RobotoFix",GRAPHITE)
    colors=[CORAL,Color(1,.25,.23),GRAPHITE,OFFWHITE,Color(.96,.51,.53)]
    xs=[125,365,605,845,1085]
    for x,col in zip(xs,colors):
        c.setFillColor(col); c.roundRect(x,height-550,165,165,28,fill=1,stroke=0)
    text(c,1110,575,"5 фірмових кольорів",19,height,"RobotoBoldFix",GRAPHITE); text(c,1110,608,"+ 1 нейтральне тло",19,height,"RobotoFix",GRAPHITE)
    rect(c,82,700,1275,55,height,MIST); text(c,110,717,"Градієнт застосовується лише як обкладинковий фон.",17,height,"RobotoBoldFix",GRAPHITE)
    c.save(); stream.seek(0); return PdfReader(stream).pages[0]


def build_page13(width, height):
    stream=BytesIO(); c=canvas.Canvas(stream,pagesize=(width,height)); header(c,13,"07. Фірмові носії",height)
    rect(c,82,112,920,610,height,PINK)
    c.drawImage(source_image(12,0),82,height-722,width=920,height=610,preserveAspectRatio=False,mask='auto')
    text(c,1060,145,"Фірмові носії",35,height,"RobotoBoldFix",GRAPHITE); rule(c,1060,193,75,height)
    multiline(c,1060,230,["Мінімум декору:","знак, назва та один","акцентний колір."],22,34,height,"RobotoBoldFix",GRAPHITE)
    multiline(c,1060,365,["Схеми нанесення для","виробника мають бути","простими й точними.","Носії — корисними для","учасниць."],19,31,height,"RobotoFix",GRAPHITE)
    pill(c,1060,575,"МЕРЧ",height); pill(c,1060,625,"ПОЛІГРАФІЯ",height)
    c.save(); stream.seek(0); return PdfReader(stream).pages[0]


def build_page14(width, height):
    stream=BytesIO(); c=canvas.Canvas(stream,pagesize=(width,height)); rect(c,0,0,width,height,height,PINK)
    text(c,82,55,"ДЯКУЄМО",17,height,"RobotoBoldFix",GRAPHITE)
    c.setFont("RobotoBoldFix",14); c.setFillColor(GRAPHITE); c.drawRightString(1358,height-55-11.5,"LIVE-GIVING.ORG.UA")
    # Mirror the opening cover: watercolor field + circular logo, without a box edge.
    c.drawImage(source_image(0,0),-75,height-720,width=690,height=690,preserveAspectRatio=True,mask='auto')
    c.setStrokeColor(WHITE); c.setLineWidth(4); c.circle(305,height-390,205,fill=0,stroke=1)
    c.drawImage(ImageReader(str(ROOT / "work/pdfs/page1-logo-circle.png")),100,height-595,width=410,height=410,preserveAspectRatio=True,mask='auto')
    multiline(c,790,155,["Дякуємо, що","розділяєте наші","цінності"],51,61,height,"RobotoBoldFix",GRAPHITE)
    multiline(c,790,390,["Брендбук — не лише про вигляд.","Це про зміст: кожен елемент айдентики", "має звучати як голос, упевненість і підтримка."],20,31,height,"RobotoFix",GRAPHITE)
    rect(c,790,520,475,2,height,TERRACOTTA)
    multiline(c,790,552,["«ЖИТТЄДАЙНА» — СИЛА ЖІНКИ", "У ПРАВІ НА ВИБІР."],18,27,height,"RobotoBoldFix",DEEP_CORAL)
    text(c,82,742,"ГО «ЖИТТЄДАЙНА» · ЛЬВІВСЬКА ОБЛАСТЬ",14,height,"RobotoBoldFix",GRAPHITE)
    c.setFont("RobotoFix",14); c.setFillColor(GRAPHITE); c.drawRightString(1358,height-742-11.5,"Брендбук · версія 1.0 · 2026")
    c.save(); stream.seek(0); return PdfReader(stream).pages[0]


def make_overlay(page_no, width, height):
    stream = BytesIO()
    c = canvas.Canvas(stream, pagesize=(width, height))

    if page_no == 1:
        pass

    elif page_no == 2:
        # Remove only the superfluous comma after "документ".
        rect(c, 300, 307, 12, 38, height, PINK)

    elif page_no == 3:
        # Add the missing full stop without repainting the line.
        text(c, 211, 455, ".", 23, height, "RobotoFix")

    elif page_no == 9:
        rect(c, 1035, 194, 350, 57, height, WHITE)
        text(c, 1053, 201, "«Ви маєте право на безпеку. Ми", 18.2, height, "RobotoBoldFix")
        text(c, 1077, 226, "поруч і підкажемо наступний крок».", 18.2, height, "RobotoBoldFix")
        rect(c, 1051, 410, 316, 57, height, WHITE)
        text(c, 1080, 417, "«Бідні жертви насильства", 18.2, height, "RobotoBoldFix")
        text(c, 1070, 442, "потребують нашого порятунку».", 18.2, height, "RobotoBoldFix")

    elif page_no == 10:
        pass

    elif page_no == 13:
        pass

    elif page_no == 14:
        rect(c, 55, 746, 270, 33, height, PINK)
        text(c, 64, 753, "ГО «ЖИТТЄДАЙНА»", 20, height, "RobotoBoldFix")
        rect(c, 1078, 743, 305, 39, height, PINK)
        text(c, 1090, 750, "Брендбук, версія 1.0, 2026", 25, height)

    c.save()
    stream.seek(0)
    return PdfReader(stream).pages[0]


reader = PdfReader(str(SOURCE))
writer = PdfWriter()
builders = {
    1: build_page1, 2: build_page2, 3: build_page3, 4: build_page4,
    5: build_page5, 6: build_page6, 7: build_page7, 8: build_page8,
    9: build_page9, 10: build_page10, 11: build_page11, 12: build_page12,
    13: build_page13, 14: build_page14,
}
for i, page in enumerate(reader.pages, 1):
    w = float(page.mediabox.width)
    h = float(page.mediabox.height)
    if i == 1:
        page.merge_page(build_page1_logo_overlay(w,h),over=True)
        writer.add_page(page)
        continue
    if i in {10, 14}:
        writer.add_page(page)
        continue
    writer.add_page(builders[i](w, h))

writer.add_metadata({
    "/Title": "Брендбук ГО «Життєдайна» — відредагована версія",
    "/Author": "ГО «Життєдайна»",
    "/Subject": "Вичитаний брендбук із чітким векторним текстом",
})
OUTPUT.parent.mkdir(parents=True, exist_ok=True)
with OUTPUT.open("wb") as f:
    writer.write(f)
print(OUTPUT)
