#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WHM & cPanel Lathund - Praktisk snabbreferens for RestWeb Webhotell
Body PDF generation via ReportLab
"""

import sys, os, hashlib
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch, mm, cm
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, CondPageBreak, KeepTogether, HRFlowable
)
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import registerFontFamily

# ============================================================
# FONT REGISTRATION
# ============================================================
pdfmetrics.registerFont(TTFont('LiberationSerif', '/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf'))
pdfmetrics.registerFont(TTFont('LiberationSerif-Bold', '/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf'))
pdfmetrics.registerFont(TTFont('LiberationSans', '/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf'))
pdfmetrics.registerFont(TTFont('LiberationSans-Bold', '/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf'))
pdfmetrics.registerFont(TTFont('DejaVuSans', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'))
pdfmetrics.registerFont(TTFont('DejaVuSans-Bold', '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'))
pdfmetrics.registerFont(TTFont('DejaVuMono', '/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf'))

registerFontFamily('LiberationSerif', normal='LiberationSerif', bold='LiberationSerif-Bold')
registerFontFamily('LiberationSans', normal='LiberationSans', bold='LiberationSans-Bold')
registerFontFamily('DejaVuSans', normal='DejaVuSans', bold='DejaVuSans-Bold')

# ============================================================
# COLOR PALETTE (from cascade)
# ============================================================
PAGE_BG       = colors.HexColor('#f2f2f0')
SECTION_BG    = colors.HexColor('#efefed')
CARD_BG       = colors.HexColor('#efeeec')
TABLE_STRIPE  = colors.HexColor('#f5f5f3')
HEADER_FILL   = colors.HexColor('#504933')
COVER_BLOCK   = colors.HexColor('#847854')
BORDER        = colors.HexColor('#cbc6b5')
ICON          = colors.HexColor('#968757')
ACCENT        = colors.HexColor('#5126d2')
ACCENT_2      = colors.HexColor('#4bcf8d')
TEXT_PRIMARY   = colors.HexColor('#1d1c1a')
TEXT_MUTED     = colors.HexColor('#828078')
SEM_SUCCESS   = colors.HexColor('#3a8051')
SEM_WARNING   = colors.HexColor('#987c44')
SEM_ERROR     = colors.HexColor('#8f4842')
SEM_INFO      = colors.HexColor('#476f98')

TABLE_HEADER_COLOR = HEADER_FILL
TABLE_HEADER_TEXT  = colors.white
TABLE_ROW_EVEN     = colors.white
TABLE_ROW_ODD      = TABLE_STRIPE

# ============================================================
# PAGE DIMENSIONS
# ============================================================
PAGE_W, PAGE_H = A4
LEFT_MARGIN = 1.0 * inch
RIGHT_MARGIN = 1.0 * inch
TOP_MARGIN = 0.8 * inch
BOTTOM_MARGIN = 0.8 * inch
CONTENT_W = PAGE_W - LEFT_MARGIN - RIGHT_MARGIN

# ============================================================
# STYLES
# ============================================================
FONT_BODY = 'LiberationSerif'
FONT_HEAD = 'LiberationSans'

style_h1 = ParagraphStyle(
    name='H1', fontName=FONT_HEAD, fontSize=20, leading=26,
    textColor=ACCENT, spaceBefore=18, spaceAfter=10,
    alignment=TA_LEFT
)
style_h2 = ParagraphStyle(
    name='H2', fontName=FONT_HEAD, fontSize=15, leading=20,
    textColor=HEADER_FILL, spaceBefore=14, spaceAfter=8,
    alignment=TA_LEFT
)
style_h3 = ParagraphStyle(
    name='H3', fontName=FONT_HEAD, fontSize=12, leading=16,
    textColor=TEXT_PRIMARY, spaceBefore=10, spaceAfter=6,
    alignment=TA_LEFT
)
style_body = ParagraphStyle(
    name='Body', fontName=FONT_BODY, fontSize=10.5, leading=16,
    textColor=TEXT_PRIMARY, spaceBefore=0, spaceAfter=6,
    alignment=TA_LEFT
)
style_body_indent = ParagraphStyle(
    name='BodyIndent', fontName=FONT_BODY, fontSize=10.5, leading=16,
    textColor=TEXT_PRIMARY, spaceBefore=0, spaceAfter=4,
    leftIndent=20, alignment=TA_LEFT
)
style_step = ParagraphStyle(
    name='Step', fontName=FONT_BODY, fontSize=10.5, leading=16,
    textColor=TEXT_PRIMARY, spaceBefore=2, spaceAfter=4,
    leftIndent=24, alignment=TA_LEFT
)
style_tip = ParagraphStyle(
    name='Tip', fontName=FONT_BODY, fontSize=10, leading=15,
    textColor=SEM_INFO, spaceBefore=4, spaceAfter=6,
    leftIndent=16, borderPadding=6,
    backColor=colors.HexColor('#f0f5fa'),
    alignment=TA_LEFT
)
style_warning = ParagraphStyle(
    name='Warning', fontName=FONT_BODY, fontSize=10, leading=15,
    textColor=SEM_WARNING, spaceBefore=4, spaceAfter=6,
    leftIndent=16, borderPadding=6,
    backColor=colors.HexColor('#faf5ed'),
    alignment=TA_LEFT
)
style_bullet = ParagraphStyle(
    name='Bullet', fontName=FONT_BODY, fontSize=10.5, leading=16,
    textColor=TEXT_PRIMARY, spaceBefore=1, spaceAfter=2,
    leftIndent=28, firstLineIndent=-14, alignment=TA_LEFT
)
style_th = ParagraphStyle(
    name='TH', fontName=FONT_HEAD, fontSize=10, leading=14,
    textColor=TABLE_HEADER_TEXT, alignment=TA_CENTER
)
style_td = ParagraphStyle(
    name='TD', fontName=FONT_BODY, fontSize=9.5, leading=14,
    textColor=TEXT_PRIMARY, alignment=TA_LEFT
)
style_td_c = ParagraphStyle(
    name='TDC', fontName=FONT_BODY, fontSize=9.5, leading=14,
    textColor=TEXT_PRIMARY, alignment=TA_CENTER
)
style_caption = ParagraphStyle(
    name='Caption', fontName=FONT_BODY, fontSize=9, leading=13,
    textColor=TEXT_MUTED, alignment=TA_CENTER,
    spaceBefore=3, spaceAfter=6
)
style_toc_h1 = ParagraphStyle(
    name='TOCH1', fontName=FONT_HEAD, fontSize=13, leading=20,
    leftIndent=20, textColor=ACCENT
)
style_toc_h2 = ParagraphStyle(
    name='TOCH2', fontName=FONT_BODY, fontSize=11, leading=18,
    leftIndent=40, textColor=TEXT_PRIMARY
)

# ============================================================
# HELPER FUNCTIONS
# ============================================================
def P(text, style=style_body):
    return Paragraph(text, style)

def H1(text):
    key = 'h_%s' % hashlib.md5(text.encode()).hexdigest()[:8]
    p = Paragraph('<a name="%s"/><b>%s</b>' % (key, text), style_h1)
    p.bookmark_name = text
    p.bookmark_level = 0
    p.bookmark_text = text
    p.bookmark_key = key
    return p

def H2(text):
    key = 'h_%s' % hashlib.md5(text.encode()).hexdigest()[:8]
    p = Paragraph('<a name="%s"/><b>%s</b>' % (key, text), style_h2)
    p.bookmark_name = text
    p.bookmark_level = 1
    p.bookmark_text = text
    p.bookmark_key = key
    return p

def H3(text):
    return Paragraph('<b>%s</b>' % text, style_h3)

def Bullet(text):
    return Paragraph('&#8226; %s' % text, style_bullet)

def Step(num, text):
    return Paragraph('<b>Steg %d:</b> %s' % (num, text), style_step)

def Tip(text):
    return Paragraph('<b>Tips:</b> %s' % text, style_tip)

def Warning(text):
    return Paragraph('<b>Viktigt:</b> %s' % text, style_warning)

def make_table(headers, rows, col_widths=None):
    """Create a styled table with Paragraph cells."""
    available = CONTENT_W
    if col_widths is None:
        col_widths = [available / len(headers)] * len(headers)
    else:
        # Scale to fit
        total = sum(col_widths)
        if total < available * 0.85:
            scale = (available * 0.92) / total
            col_widths = [w * scale for w in col_widths]

    data = []
    header_row = [Paragraph('<b>%s</b>' % h, style_th) for h in headers]
    data.append(header_row)
    for row in rows:
        data.append([Paragraph(str(c), style_td) for c in row])

    t = Table(data, colWidths=col_widths, hAlign='CENTER')
    style_cmds = [
        ('BACKGROUND', (0, 0), (-1, 0), TABLE_HEADER_COLOR),
        ('TEXTCOLOR', (0, 0), (-1, 0), TABLE_HEADER_TEXT),
        ('GRID', (0, 0), (-1, -1), 0.5, BORDER),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]
    for i in range(1, len(data)):
        bg = TABLE_ROW_EVEN if i % 2 == 1 else TABLE_ROW_ODD
        style_cmds.append(('BACKGROUND', (0, i), (-1, i), bg))
    t.setStyle(TableStyle(style_cmds))
    return t

def hr():
    return HRFlowable(width="90%", thickness=0.5, color=BORDER, spaceAfter=8, spaceBefore=8)


# ============================================================
# TOC DOC TEMPLATE
# ============================================================
class TocDocTemplate(SimpleDocTemplate):
    def afterFlowable(self, flowable):
        if hasattr(flowable, 'bookmark_name'):
            level = getattr(flowable, 'bookmark_level', 0)
            text = getattr(flowable, 'bookmark_text', '')
            key = getattr(flowable, 'bookmark_key', '')
            self.notify('TOCEntry', (level, text, self.page, key))

# ============================================================
# BUILD DOCUMENT
# ============================================================
OUTPUT = '/home/z/my-project/download/lathund/body.pdf'

doc = TocDocTemplate(
    OUTPUT,
    pagesize=A4,
    leftMargin=LEFT_MARGIN,
    rightMargin=RIGHT_MARGIN,
    topMargin=TOP_MARGIN,
    bottomMargin=BOTTOM_MARGIN,
    title='WHM & cPanel Lathund',
    author='RestWeb',
    creator='Z.ai',
    subject='Praktisk snabbreferens for webbhotell for restauranger'
)

story = []

# ── TABLE OF CONTENTS ──────────────────────────────────────
story.append(Paragraph('<b>Innehall</b>', style_h1))
toc = TableOfContents()
toc.levelStyles = [style_toc_h1, style_toc_h2]
story.append(toc)
story.append(PageBreak())

# ════════════════════════════════════════════════════════════
# DEL 1: KOM IGANG MED WHM
# ════════════════════════════════════════════════════════════
story.append(H1('Del 1: Kom igang med WHM'))

story.append(P(
    'WHM (Web Host Manager) ar din kommandocentral som reseller. Har skapar du kundkonton, '
    'overvakar servern, hanterar paket och installerar SSL-certifikat. Det ar inte kunderna som '
    'ser WHM - det ar bara du som administrator. Kunderna loggar in i cPanel, som ar deras '
    'eget kontrollpanel. Tanken med den har lathunden ar att du snabbt ska hitta de funktioner '
    'du anvander oftast, utan att behova leta igenom hundratals menyalternativ.'
))

story.append(H2('Logga in i WHM'))
story.append(P(
    'Du loggar in via din ChimCloud-kontrollpanel eller direkt via webblasaren. '
    'URL-formatet ar: <b>https://din-server-ip:2087</b> eller via den specifika lanken som '
    'ChemiCloud ger dig nar du skapar ditt reseller-konto. Anvand de inloggningsuppgifter '
    'som ChemiCloud tillhandahaller. Nar du loggar in forsta gangen kommer du att se en '
    'initial setup-guide som ber dig bekrasta din kontaktinformation och namnservrar. '
    'Du kan hoppa over de flesta av dessa steg och gora installningarna senare.'
))

story.append(H2('WHM-hemskarmen - vad du ser'))
story.append(P(
    'Efter inloggning möter du WHM-hemskarmen med en sÖkpanel Överst och snabblÄnkar nedanfÖr. '
    'SÖkfÄltet ar din basta van - skriv "create" sa far du direkt "Create a New Account". '
    'Skriv "package" sa far du "Add a Package". Du behOver inte memorera menysystemet; '
    'anvand sOket. Till vanster har du en sidomeny med alla funktioner grupperade i '
    'kategorier. De viktigaste kategorierna for dig ar: Account Functions, Packages, '
    'SSL/TLS, DNS Functions och Email.'
))

story.append(make_table(
    ['Kategori', 'Vad du gor har', 'Hur ofta'],
    [
        ['Account Functions', 'Skapa/avsluta kundkonton, hantera konton', 'Varje ny kund'],
        ['Packages', 'Skapa och redigera hostingpaket', 'Engangs + vid behov'],
        ['SSL/TLS', 'Installera SSL, hantera certifikat', 'Per kund + fornyelse'],
        ['DNS Functions', 'Lagg till DNS-zoner, andra DNS-poster', 'Per kund + vid flytt'],
        ['Email', 'Spam-filter, e-postroutning, MX-poster', 'Vid problem'],
        ['Server Configuration', 'Tweak Settings, PHP-konfiguration', 'Sallan'],
        ['Resellers', 'Hantera reseller-behorigheter', 'Aldrig (du ar ensam)'],
        ['Backup', 'Konfigurera och overvaka backup', 'Engangs + test'],
        ['Service Status', 'Kolla om Apache, MySQL, e-post fungerar', 'Vid problem'],
    ],
    [120, 220, 110]
))

# ════════════════════════════════════════════════════════════
# DEL 2: STEG-FOR-STEG - NY KUND
# ════════════════════════════════════════════════════════════
story.append(Spacer(1, 12))
story.append(H1('Del 2: Skapa en ny restaurangkund - steg for steg'))

story.append(P(
    'Detta ar det arbetsflode du kommer gora allra mest. Varje gang en ny restaurang '
    'blir kund foljer du dessa steg fran borjan till slut. Processen tar ungefar 20-30 '
    'minuter nar du vant dig vid den. Har nedan gar vi igenom varje steg i detalj sa '
    'att du vet exakt vad som ska goras och varfor.'
))

story.append(H2('Steg 1: Skapa ett hostingpaket'))
story.append(P(
    'Fore du kan skapa ett kundkonto behover du ett "Package" (paket). Ett paket '
    'definierar hur mycket diskutrymme, bandbredd, e-postkonton, databaser osv. som '
    'kontot far. Tank pa detta som en mall - du skapar paket en gang och anvander dem '
    'for varje ny kund. For din restaurangverksamhet rekommenderar vi tre paket som '
    'motsvarar dina tre prisnivaer.'
))
story.append(Step(1, 'I WHM, sok "Add a Package" eller navigera till Home > Packages > Add a Package'))
story.append(Step(2, 'Fyll i paketnamnet, till exempel "Smakprov", "Huvudratt" eller "Dessert"'))
story.append(Step(3, 'Stall in resursgranser enligt tabellen nedan'))
story.append(Step(4, 'Klicka "Add" for att spara paketet'))

story.append(Spacer(1, 8))
story.append(make_table(
    ['Instollning', 'Smakprov', 'Huvudratt', 'Dessert'],
    [
        ['Diskutrymme (MB)', '1000', '3000', 'Obegransat'],
        ['Bandbredd (MB)', '5000', '15000', 'Obegransat'],
        ['Max e-postkonton', '3', '10', 'Obegransat'],
        ['Max databaser', '1', '3', 'Obegransat'],
        ['Max subdomaner', '0', '2', '5'],
        ['Max parkerade domaner', '0', '1', '3'],
        ['Max addon-domoner', '0', '1', '3'],
        ['FTP-konton', '1', '3', 'Obegransat'],
        ['cPanel-tema', 'jupiter', 'jupiter', 'jupiter'],
    ],
    [110, 90, 90, 90]
))

story.append(Tip(
    'Du kan alltid andra ett paket senare via "Edit a Package". Andringen galler alla '
    'konton som anvander paketet. Om du vill ha en unik konfiguration for en specifik '
    'kund kan du aven overstyra paketinstallningarna nar du skapar kontot.'
))

story.append(H2('Steg 2: Skapa cPanel-kontot'))
story.append(P(
    'Nu ska du skapa sjalva kundkontot. Detta ger restaurangen sin egen cPanel-inloggning '
    'där de kan hantera e-post, filer och installera WordPress. Du behöver domännamnet, '
    'ett användernamn och ett losenord. Se till att domänen redan ar registrerad hos '
    'din .SE-registrator (HostUp eller Inleed) och pekar mot ChemiClouds namnservrar.'
))
story.append(Step(1, 'Sok "Create a New Account" i WHM'))
story.append(Step(2, 'Fyll i domannamnet (t.ex. restaurangkungen.se)'))
story.append(Step(3, 'Valj anvandarnamn (automatiskt genererat baserat pa domänen, max 8 tecken)'))
story.append(Step(4, 'Stall in ett starkt losenord eller klicka "Password Generator"'))
story.append(Step(5, 'Valj e-postadress for kontot (for att ta emot systemmeddelanden)'))
story.append(Step(6, 'Valj paket fran listan (t.ex. "Huvudratt")'))
story.append(Step(7, 'Under "Settings" - se avsnittet "Viktiga installningar" nedan'))
story.append(Step(8, 'Klicka "Create" for att skapa kontot'))

story.append(Spacer(1, 6))
story.append(P(
    '<b>Den viktigaste installningen i detta steg ar "Choose how the domain should route":</b> '
    'Valj alltid <b>Local Mail Exchanger</b> om e-posten for domänen ska hanteras av din '
    'server (vilket ar standard). Om kunden anvander extern e-post (t.ex. Google Workspace) '
    'valjer du <b>Remote Mail Exchanger</b>. Fel val har leder till att e-post inte '
    'levereras korrekt, sa dubbelkolla alltid med kunden fore du skapar kontot.'
))

story.append(H2('Steg 3: Konfigurera DNS'))
story.append(P(
    'Nar kontot ar skapat maste domänens DNS peka ratt. ChemiCloud tillhandahaller '
    'namnservrar som du staller in hos din .SE-registrator. De brukar heta nagot i stil '
    'med ns1.rs8-va.serverhostgroup.com och ns2.rs8-va.serverhostgroup.com. Du staller '
    'in dessa hos HostUp/Inleed nar du hanterar domänen. Dessutom maste du se till att '
    'A-poster och MX-poster ar korrekta i WHM. I de flesta fall skapas dessa automatiskt '
    'nar du skapar kontot, men du kan verifiera dem via WHM > DNS Functions > Edit DNS Zone.'
))

story.append(H2('Steg 4: Installera SSL-certifikat'))
story.append(P(
    'Varje restauranghemsida maste ha HTTPS. Lyckligtvis erbjuder ChemiCloud gratis '
    'Let\'s Encrypt SSL-certifikat. Nar kontot ar skapat och DNS ar konfigurerat '
    'korrekt gar du till WHM > SSL/TLS > Install an SSL Certificate on a Domain. '
    'Klicka "Autofill by Domain" sa fyller systemet i uppgifterna automatiskt. '
    'Klicka sedan "Install". Certifikatet fornyas automatiskt var 90:e dag. '
    'Om autofill inte fungerar beror det oftast pa att DNS inte har propagerat '
    'än - vanta 1-2 timmar och forsok igen.'
))

story.append(H2('Steg 5: Installera WordPress'))
story.append(P(
    'De flesta restauranghemsidor byggs med WordPress. Den snabbaste vägen ar via '
    'cPanel > Software > Softaculous Apps Installer. Du loggar in i kundens cPanel '
    '(antingen via WHM > Account Information > List Accounts och klickar cPanel-ikonen, '
    'eller direkt via https://doman.se:2083). I Softaculous valjer du WordPress, '
    'fyller i administratörsuppgifter och klickar "Install". Installationen tar '
    'under 1 minut. Efter installationen far kunden en inloggningslank till '
    'wp-admin dar de (eller du) kan borja bygga hemsidan.'
))

story.append(H2('Steg 6: Skapa e-postkonton'))
story.append(P(
    'I kundens cPanel gar du till Email > Email Accounts. Klicka "Create" och fyll i '
    'e-postadressen (t.ex. info@restaurangkungen.se), stall in ett losenord och valj '
    'lagringsgrans. De vanligaste e-postadresserna for restauranger ar: info@, '
    'bokning@, kontakt@ och namnet på ägaren/kocken. Du kan aven stalla in e-post '
    'forwarders (vidarebefodring) och autoresponders (autosvar) har. For att kunden '
    'ska kunna lasa e-post kan de anvanda webbmejl via cPanel eller stalla in kontot '
    'i Outlook, Gmail eller sin telefon via IMAP/SMTP.'
))

story.append(H2('Steg 7: Verifiera allt fungerar'))
story.append(P(
    'Innan du överlämnar kontot till kunden, ga igenom denna snabbkontroll: '
    '(1) Besok domänen och bekräfta att sidan laddas, (2) Klicka pa HTTPS-laset i '
    'webblasaren och bekräfta att certifikatet ar giltigt, (3) Logga in i cPanel '
    'och bekräfta att WordPress ar installerat, (4) Skicka ett testmejl till en av '
    'e-postadresserna och bekräfta att det kommer fram, (5) Logga in i WordPress '
    'wp-admin och bekräfta att allt fungerar. Nar allt ar klart skickar du kunden '
    'deras inloggningsuppgifter via e-post.'
))


# ════════════════════════════════════════════════════════════
# DEL 3: VIKTIGA INSTALLNINGAR FÖRKLARAT
# ════════════════════════════════════════════════════════════
story.append(Spacer(1, 12))
story.append(H1('Del 3: Viktiga installningar forklarat'))

story.append(P(
    'Nar du skapar ett konto eller redigerar installningar i WHM stoter du pa manga '
    'alternativ som kan vara svåra att forsta. Har forklarar vi de vanligaste och viktigaste '
    'installningarna sa att du vet nar du ska anvanda dem och vad de betyder. De flesta '
    'av dessa kan du lama pa standardvardet, men det ar viktigt att forsta vad de gor '
    'sa att du kan fatta ratt beslut nar en kund ber om nagot specifikt.'
))

# CGI Access
story.append(H2('CGI Access'))
story.append(P(
    '<b>Vad det ar:</b> CGI (Common Gateway Interface) ar en aldre teknik som later '
    'program och skript kOras pa servern och leverera dynamiskt innehall till webblasaren. '
    'CGI-skript skrivs oftast i Perl eller Bash och placeras i en mapp som heter cgi-bin '
    'inuti kundens hemkatalog. I modern webbhotellning anvands CGI mycket sallsan eftersom '
    'PHP, Python och Node.js har tagit over som de dominerande serversidorna teknikerna. '
    'WordPress kraver inte CGI alls.'
))
story.append(P(
    '<b>Rekommendation:</b> Avaktivera CGI Access for alla kunder. Det ar en sakerhetsrisk '
    'utan nagon verklig nytta for restauranghemsidor. Om en kund nagon gang behovde CGI '
    '(mycket osannolikt) kan du alltid aktivera det senare via WHM > Account Functions > '
    'Modify an Account. Nar du skapar ett paket eller konto behover du alltsa inte bocka i '
    '"CGI Access" - lamma det avbockat som standard.'
))

# Shell Access
story.append(H2('Shell Access (SSH)'))
story.append(P(
    '<b>Vad det ar:</b> Shell access ger kunden mojlighet att logga in pa servern via SSH '
    '(Secure Shell) och exekvera kommandon direkt i terminalen. Detta ar anvandbart for '
    'avancerade anvandare som vill hantera filer, installa program eller felsoka problem '
    'via kommandoraden. For restaurangkunder ar detta normalt inte nodvandigt och utgor '
    'en potentiell sakerhetsrisk om losenordet kommer pa avvagar.'
))
story.append(P(
    '<b>Rekommendation:</b> Valj "noshell" eller "jailshell" i WHM. Jailshell ar ett '
    'kompromissalternativ som ger begransad SSH-access inom kundens egna mappar (en sa '
    'kallad "chroot-miljo"). For absolut sakerhet valjer du "noshell" som forhindrar '
    'SSH-inloggning helt. De flesta restaurangkunder kommer aldrig att behovja SSH.'
))

# SpamBox
story.append(H2('Enable Spam Box (SpamAssassin)'))
story.append(P(
    '<b>Vad det ar:</b> SpamAssassin ar serverns inbyggda spam-filter som analyserar '
    'inkommande e-post och bedomer hur troligt det ar att meddelandet ar spam. Nar '
    '"Enable Spam Box" ar aktiverat flyttas meddelanden som markerats som spam automatiskt '
    'till en separat mapp kallad "Spam" istallet for att hamna i inkorgen. Detta ar '
    'sakerre an att radera spam direkt eftersom legitima e-postmeddelanden ibland kan '
    'felaktigt markeras som spam (sa kallade "false positives"). Kunden kan da kontrollera '
    'Spam-mappen och se om nagot viktigt hamnat dar.'
))
story.append(P(
    '<b>Sa fungerar det i praktiken:</b> SpamAssassin ger varje e-post en poang baserat '
    'pa hundratals tester. Ar poangen over en viss traskel (vanligtvis 5.0) markeras '
    'meddelandet som spam. Nar Spam Box ar aktivt hamnar dessa meddelanden i mappen '
    '"Spam" som kunden kan se via webbmejl eller IMAP. Du kan justera traskelvardet '
    'via cPanel > Email > Spam Filters. Ett lagger varde = mer aggressiv filtrering '
    '(men okad risk for false positives). Ett hogre varde = mindre aggressiv (men mer '
    'spam i inkorgen). Standardvardet 5.0 ar en bra balans for de flesta anvandare.'
))
story.append(P(
    '<b>Rekommendation:</b> Aktivera Spam Box for alla kunder. Det ar en av de mest '
    'praktiska installningarna for e-posthantering och dina restaurangkunder kommer '
    'att uppskatta att deras inkorg inte fylls med skrappost. Du aktiverar det antingen '
    'i paketinstallningarna eller via WHM > Account Functions > Modify an Account.'
))

# More settings
story.append(H2('Fler viktiga installningar'))

settings_data = [
    ['Maximum Upload Size', 'Storsta filstorlek som kan laddas upp via cPanel File Manager eller webb. Standard ar ofta lagt. Ok till 256 MB for restauranger som vill ladda upp hogkvalitativa bilder.', '256 MB'],
    ['Max Email per Hour', 'Hur manga e-postmeddelanden kontot far skicka per timme. Forhindrar att hackade konton skickar mass-spam. Standard ar oftast 100-200.', '200/timme'],
    ['Max FTP Accounts', 'Antal FTP-konton kunden kan skapa. Varje FTP-konto ger tillgang till filerna. De flesta restauranger behovjer bara 1-2.', '3'],
    ['Dedicated IP', 'En unik IP-adress bara for detta konto. Kravs normalt inte langsre for SSL (SNI loste detta). Bara nodvandigt for specialfall.', 'Nej'],
    ['Apache mod_userdir', 'Later kunden se sin hemsida via en temporar URL fore DNS ar konfigurerat. Anvandbart under uppbyggnad.', 'Ja'],
    ['Locale', 'Sprakinstollning for cPanel. Valj "sv" for svenska om kunden onskar det, annars engelska.', 'en (eller sv)'],
    ['Mail Routing', 'Bestammer hur e-post ruttas. "Local" = servern hanterar e-post. "Remote" = extern e-posttjanst (Google, etc). "Auto" = systemet bestammer.', 'Auto'],
]

story.append(make_table(
    ['Installning', 'Forklaring', 'Rekommendation'],
    settings_data,
    [100, 250, 100]
))


# ════════════════════════════════════════════════════════════
# DEL 4: E-POSTHANTERING
# ════════════════════════════════════════════════════════════
story.append(Spacer(1, 12))
story.append(H1('Del 4: E-posthantering i djupet'))

story.append(P(
    'E-post ar en av de vanligaste orsakerna till att kunder hör av sig. Restauranger '
    'beror pa sin e-post for att ta emot bokningar, leveransordrar och kundfragor. '
    'Har gar vi igenom de viktigaste e-postfunktionerna och hur du konfigurerar dem '
    'for att ge kunderna en palettlig e-postupplevelse utan problem.'
))

story.append(H2('Skapa e-postkonton i cPanel'))
story.append(P(
    'I kundens cPanel gar du till Email > Email Accounts. Har kan du skapa, redigera '
    'och radera e-postkonton. For varje konto stalljer du in e-postadress, losenord '
    'och lagringsgrans. Standard lagringsgrans ar oftast 250 MB vilket rattar for de '
    'flesta restauranger. Om kunden far manga stora bilagor kan du oka den. Det finns '
    'aven en "Manage Suspension"-funktion som later dig tillfalligt avaktivera ett '
    'e-postkonto utan att radera det, vilket ar anvandbart om nagon slutat pa restaurangen '
    'men kunden vill spara e-posten for framtiden.'
))

story.append(H2('E-postautentisering: SPF och DKIM'))
story.append(P(
    'SPF (Sender Policy Framework) och DKIM (DomainKeys Identified Mail) ar tva '
    'viktiga autentiseringsmetoder som hindrar andra fran att skicka e-post som '
    'utger sig for att komma fran din kunds doman. Utan dessa ar det stor risk att '
    'kundens e-post hamnar i mottagarens spam-mapp. ChemiCloud har ofta dessa '
    'forkonfigurerade, men du bör verifiera att de ar aktiva for varje kund.'
))
story.append(P(
    '<b>SPF</b> ar en DNS-post som anger vilka servrar som ar tillatna att skicka '
    'e-post fran domanen. Exempel: "v=spf1 +a +mx +ip4:server-ip ~all". Detta '
    'bettyder att bara din server och domanens MX-post far skicka e-post fran '
    'domanen. Andra avsandare markeras som misstankta (~all) eller avvisas (-all).'
))
story.append(P(
    '<b>DKIM</b> lgger till en digital signatur i varje utgende e-post. Mottagarens '
    'server kan verifiera signaturen mot en offentlig nyckel i DNS. Detta garanterar '
    'att e-posten inte har andrats under transport och att den faktiskt kommer fran '
    'din server. Du aktiverar DKIM via cPanel > Email > Email Deliverability. '
    'Klicka pa "Manage" bredvid domanen och aktivera DKIM. Systemet skapar automatiskt '
    'de nodvandiga DNS-posterna.'
))

story.append(H2('E-postroutning'))
story.append(P(
    'E-postroutningen bestammer vad som hander med e-post som skickas till kundens '
    'doman. Det finns tre alternativ i WHM/cPanel:'
))
story.append(Bullet(
    '<b>Local Mail Exchanger:</b> Servern hanterar all e-post internt. Detta ar '
    'standardalternativet nar kunden anvander cPanel for sin e-post. Alla '
    'inkommande meddelanden levereras till lokala e-postkonton.'
))
story.append(Bullet(
    '<b>Remote Mail Exchanger:</b> E-post hanteras av en extern tjanst som Google '
    'Workspace, Microsoft 365 eller en annan e-postleverantor. All inkommande '
    'e-post vidarebefodras till den externa servern via MX-poster i DNS.'
))
story.append(Bullet(
    '<b>Backup Mail Exchanger:</b> Denna server fungerar som backup om den primara '
    'e-postservern ar nere. Sallan anvand for restaurangkunder.'
))
story.append(P(
    'Om du stalljer in fel e-postroutning kommer e-posten inte att levereras '
    'korrekt. Om kunden till exempel anvander Google Workspace men routningen '
    'ar installd pa "Local", hamnar all e-post pa din server istallet for hos '
    'Google. Dubbelkolla alltid med kunden fore du valjer routning.'
))

story.append(H2('Autoresponders och Forwarders'))
story.append(P(
    '<b>Autoresponders</b> skickar automatiskt ett svarsmeddelande nar nagon skickar '
    'e-post till en viss adress. Perfekt for restauranger som vill bekrasta att de har '
    'fattit meddelandet: "Tack for ditt meddelande! Vi laser alla e-post och svara '
    'inom 24 timmar." Du staller in detta via cPanel > Email > Autoresponders. '
    'Valj e-postadressen, skriv svarsmeddelandet och stall in tidsintervall.'
))
story.append(P(
    '<b>Forwarders</b> vidarebefodrar all e-post fran en adress till en annan. '
    'Anvandbart om restaurangagaren vill ha all e-post fran info@, bokning@ och '
    'kontakt@ samlad i en enda inkorg. Du staller in forwarders via cPanel > Email > '
    'Forwarders. Du kan aven skapa "Domain Forwarders" som vidarebefodrar all e-post '
    'for en hel doman till en annan doman.'
))


# ════════════════════════════════════════════════════════════
# DEL 5: WORDPRESS & SSL
# ════════════════════════════════════════════════════════════
story.append(Spacer(1, 12))
story.append(H1('Del 5: WordPress och SSL'))

story.append(P(
    'WordPress drivar over 40% av alla hemsidor pa internet och ar den dominerande '
    'plattformen for restauranghemsidor. Som webbhotellagare behover du beharska '
    'WordPress-installation, SSL-konfiguration och de vanligaste WordPress-problemen. '
    'Har ger vi dig de konkreta stegen och de viktigaste installningarna.'
))

story.append(H2('Installera WordPress via Softaculous'))
story.append(P(
    'Softaculous ar en en-klicks-installator som finns i varje cPanel-konto. Den '
    'gör WordPress-installation enkel och snabb. Gå till cPanel > Software > '
    'Softaculous Apps Installer > WordPress. Fyll i installtionsformularet med '
    'domanen, administratörsuppgifter och databasinstallningar. Lamma databasinstallningarna '
    'pa standard - Softaculous skapar databasen automatiskt. Valj att installera '
    'pa huvuddomänen (inte en subdoman). Under "Advanced Options" kan du valja att '
    'automatiskt uppdatera WordPress, teman och tillagg - detta rekommenderas for '
    'sakerhetens skull. Installationen tar under 60 sekunder.'
))

story.append(H2('Installera SSL-certifikat (Let\'s Encrypt)'))
story.append(P(
    'SSL-certifikat ar nu obligatoriskt for alla hemsidor. Let\'s Encrypt erbjuder '
    'gratis certifikat som fornyas automatiskt. Installationen ar enkel men kraver '
    'att DNS ar korrekt konfigurerat forst. Utan ratt DNS-peking kan certifikatet '
    'inte valideras och installationen misslyckas. Ga till WHM > SSL/TLS > Install '
    'an SSL Certificate on a Domain. Skriv in domannamnet och klicka "Autofill by '
    'Domain". Systemet hamtar automatiskt certifikatet fran Let\'s Encrypt och '
    'installerar det. Klicka "Install". Om allt gick bra ser du en grön bekräftelse.'
))
story.append(Warning(
    'Om autofill inte fungerar, kontrollera att domänen pekar mot ratt IP-adress '
    'via DNS. Anvand verktyget "DNS Check" eller kolla via nslookup/dig. '
    'DNS-propagering kan ta upp till 48 timmar (oftast 1-2 timmar). Vanta och '
    'forsok igen. Avaktivera inte HTTPS-omdirigering fore certifikatet ar installerat.'
))

story.append(H2('Automatisk HTTPS-omdirigering'))
story.append(P(
    'Nar SSL ar installerat maste du se till att all trafik omdirigeras fran HTTP '
    'till HTTPS. Detta gor du i WordPress genom att ga till Installningar > Generellt '
    'och andra bade "WordPress-adress" och "Webbplatsadress" fran http:// till https://. '
    'De flesta moderna WordPress-teman och tillagg hanterar resten automatiskt. Om inte '
    'kan du lagg till en regel i .htaccess-filen som tvingar HTTPS. ChemiCloud har '
    'ofta en "Force HTTPS"-funktion inbyggd i cPanel under SSL/TLS > Force HTTPS.'
))

story.append(H2('WordPress sakerhet'))
story.append(P(
    'Som webbhotellagare ar du ansvarig for serverns sakerhet, men kunden ansvarar for '
    'sin WordPress-installation. Du bor anda rekommendera foljande sakerhetsatgarder '
    'till alla restaurangkunder: hall WordPress, teman och tillagg uppdaterade, anvand '
    'starka losenord for administratorkontot, installera ett sakerhetstillagg som Wordfence '
    'eller Sucuri, begransna inloggningsforsok med ett tillagg som Limit Login Attempts, '
    'och gor regelbundna backup av bade filer och databas. ChemiClouds CloudLinux-miljo '
    'ger ett extra sakerhetslager genom att isolera varje konto sa att ett hackat konto '
    'inte kan paverka andra kunder.'
))


# ════════════════════════════════════════════════════════════
# DEL 6: DNS-HANTERING
# ════════════════════════════════════════════════════════════
story.append(Spacer(1, 12))
story.append(H1('Del 6: DNS-hantering'))

story.append(P(
    'DNS (Domain Name System) ar systemet som oversatter domannamn till IP-adresser. '
    'Utan ratt DNS-installningar kommer ingen att kunna hitta kundens hemsida eller '
    'skicka e-post till rätt server. Som webbhotellagare behover du forsta de viktigaste '
    'DNS-posterna och hur du konfigurerar dem. De flesta installningar skapas automatiskt '
    'nar du skapar ett konto i WHM, men du behover ofta lagga till eller andra poster '
    'for att peka domaner, konfigurera e-post eller stalla in underdomaner.'
))

story.append(H2('De viktigaste DNS-posterna'))

dns_data = [
    ['A-post', 'Mappar ett domannamn till en IPv4-adress', 'restaurangkungen.se > 192.168.1.100', 'Obligatorisk for hemsida'],
    ['AAAA-post', 'Mappar ett domannamn till en IPv6-adress', 'Samma som A men for IPv6', 'Valfri, ej nodvandig'],
    ['CNAME', 'Alias som pekar en subdoman till en annan doman', 'www > restaurangkungen.se', 'Rekommenderas for www'],
    ['MX-post', 'Bestammer vilken server som hanterar e-post', 'restaurangkungen.se > mail.restaurangkungen.se', 'Obligatorisk for e-post'],
    ['TXT-post', 'Textbaserad information (SPF, DKIM, etc.)', 'SPF: "v=spf1 +a +mx ~all"', 'Kravs for e-postsakerhet'],
    ['NS-post', 'Anger namnservrarna for domänen', 'ns1.chemicloud.com', 'Installas hos registratorn'],
    ['SRV-post', 'Anger port och prioritet for specifika tjanster', 'Anvands sallsan av restauranger', 'Bara vid behov'],
]

story.append(make_table(
    ['Posttyp', 'Vad den gor', 'Exempel', 'Kommentar'],
    dns_data,
    [60, 150, 150, 90]
))

story.append(H2('Andra DNS-poster i WHM'))
story.append(P(
    'For att redigera DNS-poster gar du till WHM > DNS Functions > Edit DNS Zone. '
    'Valj domanen och klicka "Edit". Har kan du lagga till, andra och radera poster. '
    'Var forsiktig med att andra befintliga poster - en felaktig A-post kan gora '
    'hemsidan onåbar och en felaktig MX-post kan stoppa all e-post. Gör alltid en '
    'anteckning om vad som fanns fore du andrade sa att du kan aterstalla om nagot '
    'gar fel. Nar du sparar installningarna propagrerar DNS-installningarna inom '
    'nagra minuter till nagra timmar beroende pa TTL (Time To Live) for posten.'
))

story.append(Tip(
    'Anvand kommandot "dig" eller onlinetjanster som dnschecker.org for att verifiera '
    'att DNS-posterna ar korrekta fran utsidan. Bara for att det ser ratt ut i WHM '
    'betyder det inte att det har propagrerat till hela internet än.'
))


# ════════════════════════════════════════════════════════════
# DEL 7: BACKUP OCH SAKERHET
# ════════════════════════════════════════════════════════════
story.append(Spacer(1, 12))
story.append(H1('Del 7: Backup och sakerhet'))

story.append(P(
    'Backup ar den viktigaste sakerhetsatgarden du kan gora. Om nagot gar fel - en '
    'kund raderar sina filer av misstag, en hacker forstor hemsidan eller en uppdatering '
    'gar snett - ar det backupen som raddar situationen. ChemiCloud erbjuder automatisk '
    'backup som del av deras hostingpaket, men du bor forsta hur det fungerar och hur du '
    'aterstarllar data nar det behövs. Dessutom bor du ha en plan for vad du gor om '
    'nagot gar fel med en kunds hemsida.'
))

story.append(H2('ChemiClouds backup-system'))
story.append(P(
    'ChemiCloud kör automatisk daglig backup av alla konton via JetBackup. Som kund i '
    'cPanel kan du nšja dina backups via cPanel > Files > JetBackup. Har kan du bladda '
    'bland tillgangliga backups, valja en datum och aterstalla hela kontot eller enskilda '
    'filer och databaser. Backups sparas i upp till 30 dagar beroende pa ditt paket. '
    'For extra sakerhet kan du aven ladda ner en full backup till din egen dator. Ga till '
    'cPanel > Files > JetBackup > Full Backup och klicka "Download". Detta skapar en '
    'komplett arkivfil med alla filer, databaser och e-postmeddelanden.'
))

story.append(H2('Manuell backup via WHM'))
story.append(P(
    'Som administratör kan du ocksa skapa manuela backups via WHM > Backup > Backup '
    'Wizard. Detta ar anvandbart om du ska gora en stor andring pa en kunds konto och '
    'vill ha en extra sakerhetskopia fore. Du kan aven stalla in automatiska '
    'backup-schema via WHM > Backup > Backup Configuration. Har kan du valja hur ofta '
    'backup ska goras (dagligen, veckovis, manadsvis), vilka konton som ska backas upp '
    'och var backupfilerna ska lagras. ChemiCloud har oftast redan konfigurerat detta '
    'at dig, sa du behover normalt inte andra dessa installningar.'
))

story.append(H2('Imunify360 - automatiskt sakerhetsskydd'))
story.append(P(
    'ChemiCloud inkluderar Imunify360, en avancerad sakerhetslosning som automatiskt '
    'blockerar skadlig trafik, malware och brute-force-attacker. Som webbhotellagare '
    'behöver du normalt inte gora nagot - Imunify360 kors i bakgrunden och skyddar '
    'alla konton. Om en kunds hemsida blir hackad kommer Imunify360 att detektera '
    'och isolera hotet automatiskt. Du kan granska hothandelser via WHM > Plugins > '
    'Imunify360. Har ser du en lista over blockerade attacker, smittade filer och '
    'andra sakerhetshandelser. For daglig drift behover du inte oroa dig for Imunify360 '
    '- det skoter sig sjalvt.'
))


# ════════════════════════════════════════════════════════════
# DEL 8: FELSÖKNING
# ════════════════════════════════════════════════════════════
story.append(Spacer(1, 12))
story.append(H1('Del 8: Felsokning - vanliga problem'))

story.append(P(
    'Har samlar vi de vanligaste problemen som restaurangkunder stoter pa och hur du '
    'losar dem snabbt. De flesta problem ar enkla att fixa om du vet var du ska leta. '
    'Nyckeln ar att systematiskt utesluta orsaker: Forst kontrollera DNS, sedan SSL, '
    'sedan e-postkonfiguration, och slutligen WordPress sjalvt. I de flesta fall ar '
    'det en enkel installning som ar fel, inte ett tekniskt fel pa servern.'
))

troubleshoot_data = [
    ['Hemsidan syns inte', 'DNS pekar fel eller har inte propagrerat', 'Kontrollera A-post i WHM > Edit DNS Zone. Anvand dnschecker.org for att verifiera. Vanta om DNS nyligen andrats.'],
    ['HTTP istallet for HTTPS', 'SSL-certifikat saknas eller ar felkonfigurerat', 'Installera Let\'s Encrypt via WHM. Andra WordPress-URL till https://. Aktivera Force HTTPS i cPanel.'],
    ['E-post hamnar i spam', 'SPF/DKIM saknas eller ar felkonfigurerade', 'Aktivera SPF och DKIM via cPanel > Email Deliverability. Lagg till rat DNS-poster.'],
    ['Kan inte logga in i cPanel', 'Fel losenord eller konto avstängt', 'Aterstall losenord via WHM > Password Modification. Kontrollera om kontot ar suspended.'],
    ['WordPress vit skarm', 'PHP-fel eller minnesbrist', 'Aktivera WP_DEBUG i wp-config.php. Oka PHP-minne via cPanel > MultiPHP INI Editor till 256M.'],
    ['Långsam hemsida', 'Stora bilder, manga tillagg, cacheproblem', 'Optimera bilder, installera WP Super Cache, kontrollera antalet aktiva tillagg.'],
    ['Kan inte skicka e-post', 'SMTP-instollningar fel eller portar blockerade', 'Kontrollera SMTP-portar (465 for SSL, 587 for TLS). Verifiera losenord.'],
    ['"Error establishing database connection"', 'Databasuppgifter fel eller databasen nere', 'Kontrollera wp-config.php. Aterstall databaslosenord via cPanel > MySQL Databases.'],
]

story.append(make_table(
    ['Problem', 'Mojlig orsak', 'Losning'],
    troubleshoot_data,
    [100, 150, 200]
))

story.append(H2('Nar du inte hinner sjalv'))
story.append(P(
    'ChemiCloud erbjuder 24/7 support via live-chatt och supportärenden. Om du stoter pa '
    'ett problem du inte kan losa sjalv, tveka inte att kontakta dem. De ar specialiserade '
    'pa cPanel/WHM och kan ofta losa problemet inom nagra minuter. Nar du kontaktar supporten, '
    'inkludera alltid: domannamnet, en beskrivning av problemet, vad du redan har provat, '
    'och eventuella felmeddelanden. Ju mer information du ger, desto snabbare kan de hjalpa. '
    'Du nar dem via ChemiCloud-kontrollpanelen eller via deras webbplats.'
))


# ════════════════════════════════════════════════════════════
# DEL 9: CHECKLISTA FOR NY KUND
# ════════════════════════════════════════════════════════════
story.append(Spacer(1, 12))
story.append(H1('Del 9: Checklista for varje ny kund'))

story.append(P(
    'Anvand denna checklista varje gang du far en ny restaurangkund. Den sakerstaller '
    'att inget steg glöms och att kunden far en komplett och fungerande produkt fran '
    'forsta dagen. Skriv ut denna sida och bocka av varje steg nar du gar igenom processen. '
    'Med tiden kommer du att memorera stegen, men under de forsta veckorna ar checklistan '
    'en oslagbar hjalpare.'
))

checklist_data = [
    ['1', 'Registrera doman (.se) hos HostUp/Inleed', 'Forsta steget - gor detta fore allt annat'],
    ['2', 'Stall in namnservrar hos registratorn', 'Peka mot ChemiClouds namnservrar'],
    ['3', 'Skapa/uppdatera hostingpaket i WHM', 'Valj ratt paket: Smakprov/Huvudratt/Dessert'],
    ['4', 'Skapa cPanel-konto i WHM', 'Create a New Account, valj ratt paket och installningar'],
    ['5', 'Verifiera DNS-poster i WHM', 'A-post, MX-post, CNAME for www, SPF, DKIM'],
    ['6', 'Installera SSL-certifikat', 'Let\'s Encrypt via WHM, verifiera med HTTPS-laset'],
    ['7', 'Installera WordPress via Softaculous', 'I cPanel, stall in admin-uppgifter och auto-uppdatering'],
    ['8', 'Skapa e-postkonton', 'info@, bokning@, osv. Aktivera Spam Box'],
    ['9', 'Konfigurera e-postautentisering', 'SPF och DKIM via cPanel > Email Deliverability'],
    ['10', 'Stall in HTTPS-omdirigering', 'Andra WordPress-URL till https://, aktivera Force HTTPS'],
    ['11', 'Testa allt', 'Hemsida laddar, HTTPS fungerar, e-post kommer fram'],
    ['12', 'Skicka inloggningsuppgifter till kunden', 'cPanel-URL, WordPress-admin, e-postuppgifter'],
]

story.append(make_table(
    ['#', 'Uppgift', 'Kommentar'],
    checklist_data,
    [25, 200, 225]
))


# ════════════════════════════════════════════════════════════
# DEL 10: SNABBREFERENS - VANLIGA VAGAR I WHM
# ════════════════════════════════════════════════════════════
story.append(Spacer(1, 12))
story.append(H1('Del 10: Snabbreferens - vanliga vagar i WHM'))

story.append(P(
    'Har ar en snabbreferens over de vanligaste funktionerna i WHM och exakt var du '
    'hittar dem. Anvand sokfaltet i WHM for snabbast access - skriv det som star i '
    'kolumnen "Sokterm" sa far du direkt ratt funktion. Detta ar den lista du kommer '
    'att ha igang varje gang du jobbar i WHM.'
))

ref_data = [
    ['Skapa nytt konto', 'Create a New Account', 'Account Functions', 'Nar du far en ny kund'],
    ['Skapa paket', 'Add a Package', 'Packages', 'Engangs + vid behov'],
    ['Andra paket', 'Edit a Package', 'Packages', 'Andra resursgranser'],
    ['Lista alla konton', 'List Accounts', 'Account Information', 'Oversikt alla kunder'],
    ['Aterstall losenord', 'Password Modification', 'Account Functions', 'Kunden glomt losenord'],
    ['Avsluta konto', 'Terminate Account', 'Account Functions', 'Kunden slutar - var forsiktig!'],
    ['Installera SSL', 'Install an SSL Certificate', 'SSL/TLS', 'Ny kund + fornyelse'],
    ['Hantera SSL-status', 'Manage SSL Hosts', 'SSL/TLS', 'Oversikt alla certifikat'],
    ['Redigera DNS', 'Edit DNS Zone', 'DNS Functions', 'Andra A/MX/CNAME-poster'],
    ['Lagg till DNS-zon', 'Add a DNS Zone', 'DNS Functions', 'Ny doman pa befintligt konto'],
    ['E-postroutning', 'Email Routing', 'Email', 'Local vs Remote'],
    ['Spam-instollningar', 'Tweak Settings', 'Server Configuration', 'Globala e-postregler'],
    ['Serverstatus', 'Server Status', 'Server Status', 'Kolla om nagot ar nere'],
    ['PHP-version', 'MultiPHP Manager', 'Software', 'Andra PHP-version per doman'],
    ['Backup', 'Backup Wizard', 'Backup', 'Skapa/aterstalla backup'],
    ['WordPress Toolkit', 'WordPress Toolkit', 'Software (cPanel)', 'Hantera alla WP-installationer'],
    ['Softaculous', 'Softaculous', 'Software (cPanel)', 'Installera appar med ett klick'],
]

story.append(make_table(
    ['Funktion', 'Sokterm i WHM', 'Menykategori', 'Nar du anvander den'],
    ref_data,
    [90, 120, 100, 140]
))

story.append(Spacer(1, 18))
story.append(P(
    '<b>Kom ihag:</b> Du behover inte kunna alla funktioner i WHM. De tio funktionerna ovan '
    'tacker 95% av allt du gor som webbhotellagare for restauranger. De ovriga funktionerna '
    'kan du lara dig allteftersom behov uppstar. ChimClouds support ar alltid tillganglig '
    'for hjalp med de mer avancerade installningarna.'
))


# ── BUILD ──────────────────────────────────────────────────
doc.multiBuild(story)
print(f'Body PDF generated: {OUTPUT}')
