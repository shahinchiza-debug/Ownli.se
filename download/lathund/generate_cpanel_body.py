#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
cPanel Jupiter Komplett Handbok - Body PDF
Alla 105 funktioner i cPanels Jupiter-tema forklarat pa svenska
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

# ── FONTS ──────────────────────────────────────────────────
pdfmetrics.registerFont(TTFont('LiberationSerif', '/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf'))
pdfmetrics.registerFont(TTFont('LiberationSerif-Bold', '/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf'))
pdfmetrics.registerFont(TTFont('LiberationSans', '/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf'))
pdfmetrics.registerFont(TTFont('LiberationSans-Bold', '/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf'))
pdfmetrics.registerFont(TTFont('DejaVuSans', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'))
pdfmetrics.registerFont(TTFont('DejaVuSans-Bold', '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'))

registerFontFamily('LiberationSerif', normal='LiberationSerif', bold='LiberationSerif-Bold')
registerFontFamily('LiberationSans', normal='LiberationSans', bold='LiberationSans-Bold')
registerFontFamily('DejaVuSans', normal='DejaVuSans', bold='DejaVuSans-Bold')

# ── PALETTE ────────────────────────────────────────────────
PAGE_BG       = colors.HexColor('#f3f3f1')
HEADER_FILL   = colors.HexColor('#726849')
ACCENT        = colors.HexColor('#217590')
TEXT_PRIMARY   = colors.HexColor('#272623')
TEXT_MUTED     = colors.HexColor('#807d76')
BORDER        = colors.HexColor('#d2cec1')
TABLE_STRIPE  = colors.HexColor('#f4f3f1')
TABLE_ROW_EVEN = colors.white
SEM_SUCCESS   = colors.HexColor('#4e9164')
SEM_WARNING   = colors.HexColor('#947c4a')
SEM_ERROR     = colors.HexColor('#a15c55')
SEM_INFO      = colors.HexColor('#4f79a3')

# ── DIMENSIONS ─────────────────────────────────────────────
PAGE_W, PAGE_H = A4
LEFT_MARGIN = 0.9 * inch
RIGHT_MARGIN = 0.9 * inch
TOP_MARGIN = 0.75 * inch
BOTTOM_MARGIN = 0.75 * inch
CONTENT_W = PAGE_W - LEFT_MARGIN - RIGHT_MARGIN

# ── STYLES ─────────────────────────────────────────────────
FB = 'LiberationSerif'
FH = 'LiberationSans'

s_h1 = ParagraphStyle(name='H1', fontName=FH, fontSize=19, leading=25, textColor=ACCENT, spaceBefore=16, spaceAfter=8, alignment=TA_LEFT)
s_h2 = ParagraphStyle(name='H2', fontName=FH, fontSize=14, leading=19, textColor=HEADER_FILL, spaceBefore=12, spaceAfter=6, alignment=TA_LEFT)
s_h3 = ParagraphStyle(name='H3', fontName=FH, fontSize=11.5, leading=16, textColor=TEXT_PRIMARY, spaceBefore=8, spaceAfter=4, alignment=TA_LEFT)
s_body = ParagraphStyle(name='Body', fontName=FB, fontSize=10, leading=15, textColor=TEXT_PRIMARY, spaceBefore=0, spaceAfter=4, alignment=TA_LEFT)
s_bullet = ParagraphStyle(name='Bullet', fontName=FB, fontSize=10, leading=15, textColor=TEXT_PRIMARY, spaceBefore=1, spaceAfter=2, leftIndent=24, firstLineIndent=-12, alignment=TA_LEFT)
s_tip = ParagraphStyle(name='Tip', fontName=FB, fontSize=9.5, leading=14, textColor=SEM_INFO, spaceBefore=3, spaceAfter=5, leftIndent=14, backColor=colors.HexColor('#f0f5fa'), alignment=TA_LEFT)
s_warn = ParagraphStyle(name='Warn', fontName=FB, fontSize=9.5, leading=14, textColor=SEM_WARNING, spaceBefore=3, spaceAfter=5, leftIndent=14, backColor=colors.HexColor('#faf5ed'), alignment=TA_LEFT)
s_th = ParagraphStyle(name='TH', fontName=FH, fontSize=9.5, leading=13, textColor=colors.white, alignment=TA_CENTER)
s_td = ParagraphStyle(name='TD', fontName=FB, fontSize=9, leading=13, textColor=TEXT_PRIMARY, alignment=TA_LEFT)
s_td_c = ParagraphStyle(name='TDC', fontName=FB, fontSize=9, leading=13, textColor=TEXT_PRIMARY, alignment=TA_CENTER)
s_caption = ParagraphStyle(name='Cap', fontName=FB, fontSize=8.5, leading=12, textColor=TEXT_MUTED, alignment=TA_CENTER, spaceBefore=2, spaceAfter=4)
s_toc1 = ParagraphStyle(name='TOC1', fontName=FH, fontSize=12, leading=19, leftIndent=20, textColor=ACCENT)
s_toc2 = ParagraphStyle(name='TOC2', fontName=FB, fontSize=10.5, leading=17, leftIndent=40, textColor=TEXT_PRIMARY)

# ── HELPERS ────────────────────────────────────────────────
def P(text, style=s_body):
    return Paragraph(text, style)

def H1(text):
    key = 'h_%s' % hashlib.md5(text.encode()).hexdigest()[:8]
    p = Paragraph('<a name="%s"/><b>%s</b>' % (key, text), s_h1)
    p.bookmark_name = text; p.bookmark_level = 0; p.bookmark_text = text; p.bookmark_key = key
    return p

def H2(text):
    key = 'h_%s' % hashlib.md5(text.encode()).hexdigest()[:8]
    p = Paragraph('<a name="%s"/><b>%s</b>' % (key, text), s_h2)
    p.bookmark_name = text; p.bookmark_level = 1; p.bookmark_text = text; p.bookmark_key = key
    return p

def H3(text):
    return Paragraph('<b>%s</b>' % text, s_h3)

def B(text):
    return Paragraph('&#8226; %s' % text, s_bullet)

def Tip(text):
    return Paragraph('<b>Tips:</b> %s' % text, s_tip)

def Warn(text):
    return Paragraph('<b>Viktigt:</b> %s' % text, s_warn)

def hr():
    return HRFlowable(width="90%", thickness=0.4, color=BORDER, spaceAfter=6, spaceBefore=6)

def T(headers, rows, cw=None):
    available = CONTENT_W
    if cw is None:
        cw = [available / len(headers)] * len(headers)
    else:
        total = sum(cw)
        if total < available * 0.85:
            s = (available * 0.92) / total
            cw = [w * s for w in cw]
    data = [[Paragraph('<b>%s</b>' % h, s_th) for h in headers]]
    for row in rows:
        data.append([Paragraph(str(c), s_td) for c in row])
    t = Table(data, colWidths=cw, hAlign='CENTER')
    cmds = [
        ('BACKGROUND', (0,0), (-1,0), HEADER_FILL),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('GRID', (0,0), (-1,-1), 0.4, BORDER),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]
    for i in range(1, len(data)):
        bg = TABLE_ROW_EVEN if i % 2 == 1 else TABLE_STRIPE
        cmds.append(('BACKGROUND', (0,i), (-1,i), bg))
    t.setStyle(TableStyle(cmds))
    return t

# ── TOC TEMPLATE ──────────────────────────────────────────
class TocDoc(SimpleDocTemplate):
    def afterFlowable(self, flowable):
        if hasattr(flowable, 'bookmark_name'):
            level = getattr(flowable, 'bookmark_level', 0)
            text = getattr(flowable, 'bookmark_text', '')
            key = getattr(flowable, 'bookmark_key', '')
            self.notify('TOCEntry', (level, text, self.page, key))

# ══════════════════════════════════════════════════════════
# BUILD DOCUMENT
# ══════════════════════════════════════════════════════════
OUTPUT = '/home/z/my-project/download/lathund/cpanel_body.pdf'

doc = TocDoc(OUTPUT, pagesize=A4,
    leftMargin=LEFT_MARGIN, rightMargin=RIGHT_MARGIN,
    topMargin=TOP_MARGIN, bottomMargin=BOTTOM_MARGIN,
    title='cPanel Jupiter Komplett Handbok', author='RestWeb', creator='Z.ai',
    subject='Komplett guide till alla funktioner i cPanels Jupiter-tema')

story = []

# ── TOC ────────────────────────────────────────────────────
story.append(Paragraph('<b>Innehall</b>', s_h1))
toc = TableOfContents()
toc.levelStyles = [s_toc1, s_toc2]
story.append(toc)
story.append(PageBreak())

# ════════════════════════════════════════════════════════════
# INTRO
# ════════════════════════════════════════════════════════════
story.append(H1('Introduktion till cPanel'))
story.append(P(
    'cPanel ar kundens kontrollpanel - det granssnitt som dina restaurangkunder ser nar de '
    'loggar in. Till skillnad fran WHM (som bara du som administratör ser) ar cPanel designat '
    'for slutanvandare. Har kan kunden hantera e-post, filer, databaser, SSL-certifikat och '
    'mycket mer. Jupiter-temat ar den senaste designen med en modern, ren layout som gor det '
    'lattare for kunder att hitta vad de soker. Som webbhotellagare ar det viktigt att du '
    'kanner till alla funktioner sa att du kan hjalpa kunderna och gora installningar at dem.'
))
story.append(P(
    'cPanel i Jupiter-temat har ungefar 105 funktioner uppdelade pa 9 huvudsektioner plus '
    'nagra snabblankar i toppen. Manga funktioner kommer du sallan att anvanda, men det ar '
    'viktigt att veta att de finns och vad de gor nar en kund fragar. I denna handbok gar '
    'vi igenom ALLA funktioner systematiskt, sektion for sektion, med svenska forklaringar '
    'och praktiska rekommendationer for din restaurangverksamhet.'
))

story.append(H2('Granssnittets huvuddelar'))
story.append(P(
    'Nar du loggar in i cPanel möter du fÖljande element: en sÖkruta hÖgst upp (anvand denna '
    'for att snabbt hitta funktioner), en rad snabblankar under sokfaltet, en sidopanel med '
    'kontoinformation och statistik till hoger, och de nio huvudsektionerna i mitten av sidan. '
    'Sokfaltet ar din basta van - skriv "email" sa far du alla e-postfunktioner, skriv "ssl" '
    'sa far du alla SSL-verktyg. Du behover inte bladdra igenom alla sektioner for att hitta '
    'vad du letar efter.'
))

story.append(T(
    ['Element', 'Beskrivning', 'Anvandning'],
    [
        ['Sokruta', 'Snabbsok efter funktioner (kortkommando: /)', 'Snabbast vag att hitta nagot'],
        ['Snabblankar', 'WordPress, Sitejet Builder, SEO, etc.', 'Vanligaste funktionerna'],
        ['Sidopanel', 'Kontoinfo, statistik, diskusage', 'Overvakning av kontot'],
        ['Huvudsektioner', 'Files, Email, Databases, etc.', 'Alla funktioner grupperade'],
        ['Aviseringar', 'Klockikonen med roda prickar', 'Varningar och felmeddelanden'],
        ['konto-meny', 'Profilikonen hogst upp', 'Byta losenord, sprak, logga ut'],
    ],
    [80, 220, 150]
))


# ════════════════════════════════════════════════════════════
# SNABBLANKAR OCH TOPPMENY
# ════════════════════════════════════════════════════════════
story.append(H1('Snabblankar och toppmeny'))
story.append(P(
    'Langst upp i cPanel, under sokfaltet, finns en rad snabblankar som ger direkt tillgang '
    'till de mest anvanda funktionerna. Dessa ar designade for att kunden snabbt ska komma '
    'till de verktyg de anvander oftast utan att behava navigera genom menyerna. Har ar de '
    'snabblankar som vanligtvis visas i Jupiter-temat:'
))

story.append(H2('WordPress Management (WP Toolkit)'))
story.append(P(
    'WP Toolkit ar en integrerad hanterare for WordPress-installationer. Har kan du installera, '
    'uppdatera, backa upp och hantera alla WordPress-sajter pa kontot fran en och samma plats. '
    'Du kan ven stalla in automatiska uppdateringar for WordPress-karnan, teman och tillagg. '
    'Verktyget visar en oversikt over alla installationer med statusindikatorer (gron = OK, '
    'gul = uppdatering tillganglig, rod = sakerhetsproblem). For restaurangkunder ar detta '
    'den absolut viktigaste snabblanken eftersom de flesta restauranghemsidor byggs med WordPress.'
))

story.append(H2('Sitejet Builder'))
story.append(P(
    'Sitejet ar en inbyggd hemsidbyggare som latar kunden skapa en enkel hemsida utan kodkunskaper. '
    'Den erbjuder drag-and-drop-redigering, fardiga mallar och responsiv design. For restauranger '
    'som vill ha en enkel narvaro pa natet utan att anlita en webbutvecklare kan Sitejet vara ett '
    'alternativ. I praktiken kommer du dock troligen att bygga kundens hemsida i WordPress, sa '
    'Sitejet ar mer av en backup-losning for kunder som vill prova sjalva.'
))

story.append(H2('Search Engine Optimization (SEO)'))
story.append(P(
    'SEO-verktyget analyserar kundens hemsida och ger tips for att forbattra synligheten i '
    'sokmotorer. Det kontrollerar faktorer som sidtitlar, metabeskrivningar, rubrikstruktur, '
    'bild-alt-texter och laddtid. Verktyget ar grundlaggande och ersatter inte ett riktigt '
    'SEO-tillagg i WordPress (som Yoast SEO), men det ger en bra snabboversikt over de mest '
    'grundlaggande SEO-kraven. For restauranger ar lokal SEO extra viktig - se till att '
    'namn, adress och telefonnummer ar konsekventa over hela natet.'
))

story.append(H2('Site Quality Monitoring'))
story.append(P(
    'Detta verktyg overvakar kundens hemsida for vanliga problem och ger en helhetsbedoming '
    'med fargindikatorer (gron/gul/rod). Det kontrollerar SEO, prestanda, tillganglighet och '
    'sakerhet. Om nagot ar fel visar verktyget exakt vad som behover atgardas. Detta ar ett '
    'bra verktyg for dig som webbhotellagare for att proaktivt upptacka problem fore kunden '
    'rinkar dem. Du kan aven stalla in e-postaviseringar sa att du far besked nar en hemsida '
    'får en rod indikator.'
))

story.append(H2('Manage Team'))
story.append(P(
    'Team-hantering latar dig skapa virtuella cPanel-konton for teammedlemmar med begransad '
    'atkomst. Du kan till exempel ge en restaurangagare atkomst till e-posthantering men inte '
    'till filhantering eller databaser. Detta ar anvandbart for större restauranger med flera '
    'anvandare som behover olika behorigheter. Varje teammedlem far en egen inloggning och kan '
    'bara se de funktioner som du har beviljat dem atkomst till.'
))

story.append(H2('Social Media Management (SocialBee)'))
story.append(P(
    'En integration med SocialBee som latar kunden hantera sociala medier fran cPanel. Kunden '
    'kan schemalagga inlagg, hantera flera konton och analysera engagemang. Detta ar en '
    'tredjepartstjanst som kraver ett separat abonnemang med SocialBee. For restauranger kan '
    'det vara ett intressant tillaggstjanst, men de flesta restaurangagare kommer att anvanda '
    'egna sociala medier-verktyg istallet. Denna funktion kan vara dold om inte ChemiCloud har '
    'aktiverat integrationen.'
))


# ════════════════════════════════════════════════════════════
# FILES
# ════════════════════════════════════════════════════════════
story.append(H1('Files - Filhantering'))

story.append(P(
    'Files-sektionen ar en av de mest centrala delarna av cPanel. Har hanterar kundens filer, '
    'skapar backup, satter losenordsskydd pa mappar och overvakar diskanvandningen. For '
    'restaurangkunder ar File Manager och Backup de viktigaste funktionerna, men du bor '
    'kanna till alla verktyg for att kunna hjalpa kunderna vid behov.'
))

story.append(H2('File Manager'))
story.append(P(
    'File Manager ar cPanels inbyggda filhanterare som fungerar som en enkel FTP-klient i '
    'webblasaren. Du kan ladda upp, ladda ner, redigera, radera och flytta filer utan att '
    'behova en separat FTP-klient. Filhanteraren visar kundens hemkatalog med undermappar som '
    'public_html (där hemsidans filer ligger), mail (e-postmeddelanden), logs (loggfiler) och '
    'flera andra systemmappar. Du kan ocksa redigera filer direkt i webblasaren med den inbyggda '
    'textedigeraren - anvandbart for snabba andringar i .htaccess eller wp-config.php utan att '
    'behova ladda ner filen forst. Filhanteraren stod ven komprimering och dekomprimering av '
    'ZIP-filer, vilket ar praktiskt nar du vill ladda upp en hel WordPress-installation pa en gang.'
))
story.append(Tip(
    'For att redigera en fil: klicka pa filen, klicka "Edit" i verktygsfaltet, bekrysta '
    'kodningsval (UTF-8 ar standard), gor andringarna och klicka "Save Changes". Anvand '
    'aldrig File Manager for stora filer - anvand FTP istallet.'
))

story.append(H2('Backup'))
story.append(P(
    'Backup-funktionen latar kunden ladda ner en fullstandig kopia av hela sitt konto som en '
    'komprimerad fil. Detta inkluderar alla filer, databaser, e-postmeddelanden, DNS-poster och '
    'cPanel-installningar. Kunden kan ven aterställa hela kontot eller enskilda delar fran en '
    'tidigare backup. ChemiCloud anvander JetBackup som ger kunden mojlighet att valja mellan '
    'olika datum for aterstallning. Nar kunden klickar pa "Download a Full Account Backup" '
    'skapas en tar.gz-fil som innehaller allt. Denna fil kan vara flera gigabyte stor for konton '
    'med manga bilder och e-postmeddelanden. Det ar viktigt att kunderna regelbundet laddar ner '
    'backup till sin egen dator som ett extra sakerhetslager utover serverns automatiska backup.'
))

story.append(H2('Backup Wizard'))
story.append(P(
    'Backup Wizard ar en guidad version av Backup-funktionen. Den leder kunden steg for steg '
    'genom processen att antingen skapa en backup eller aterstalla fran en backup. Forsta steget '
    'ar att valja "Backup" eller "Restore". Sedan valjer kunden om de vill backa upp hela kontot '
    'eller bara specifika delar (home directory, MySQL-databaser, e-postforwarders). Aterstallningen '
    'fungerar likadant - valj vad du vill aterstalla och ladda upp backupfilen. Detta ar ett mer '
    'anvandarvanligt alternativ an den vanliga Backup-funktionen for kunder som inte ar lika '
    'tekniskt bevandrade.'
))

story.append(H2('Directory Privacy'))
story.append(P(
    'Directory Privacy latar dig satta losenordsskydd pa specifika mappar i kundens konto. Nar '
    'en mapp ar losenordsskyddad maste besokaren ange ett anvandarnamn och losenord for att se '
    'innehallet. Detta ar anvandbart for att skapa en privat klientportal, ett testomrade for en '
    'ny hemsida eller skydda sensitiva filer fran allman atkomst. For att skapa ett losenordsskydd: '
    'klicka pa mappen du vill skydda, skapa en anvandare med losenord, och klicka "Save". cPanel '
    'skapar automatiskt en .htaccess- och .htpasswd-fil som hanterar autentiseringen. Du kan '
    'lagga till flera anvandare per mapp och aven ta bort atkomst for enskilda anvandare.'
))

story.append(H2('Disk Usage'))
story.append(P(
    'Disk Usage visar en detaljerad oversikt over hur kontots diskutrymme anvands. Det visar '
    'stoleken pa varje mapp, antalet filer och hur mycket utrymme som ar kvar. Detta ar '
    'anvandbart nar ett konto nar sin diskgrans och du behover ta reda pa vad som tar upp '
    'plats. Ofta ar det e-postmeddelanden med stora bilagor, gamla backup-filer eller stora '
    'bilder som forbrukar mest utrymme. Du kan sortera efter stolek for att snabbt hitta de '
    'storsta mapparna. Om kunden far slut pa utrymme kan du antingen uppgradera deras paket '
    'i WHM eller hjalpa dem att radera onodiga filer och e-post.'
))

story.append(H2('Images'))
story.append(P(
    'Images-verktyget latar kunden andra storlek pa bilder, skapa thumbnails och konvertera '
    'bildformat direkt i cPanel. Funktionen ar grundlaggande och mest anvandbar for att snabbt '
    'komprimera bilder fore uppladdning. For restauranger som ofta har stora hogkvalitativa '
    'bilder pa sin meny och sin restaurang ar det viktigt att bilderna ar optimerade for webben '
    'innan de laddas upp till WordPress. I praktiken kommer du troligen att optimerar bilderna '
    'i WordPress med ett tillagg som Smush eller Imagery istallet for att anvanda detta verktyg, '
    'men det ar bra att veta att det finns for snabba justeringar.'
))

story.append(H2('FTP Accounts'))
story.append(P(
    'FTP (File Transfer Protocol) konton latar anvandare ansluta till servern med en FTP-klient '
    'som FileZilla for att ladda upp och ner filer. Du kan skapa flera FTP-konton med olika '
    'atkomstnivaer - ett konto kan ha atkomst till hela hemkatalogen medan ett annat bara kan '
    'se public_html-mappen. Nar du skapar ett FTP-konto anger du anvandarnamn, losenord och '
    'vilken mapp kontot ska ha atkomst till. FTP-konton ar anvandbara for webbutvecklare som '
    'behöver ladda upp stora mangder filer eller for kunder som vill hantera sina filer via en '
    'skrivbordsklient istallet for File Manager. Anvand alltid SFTP (SSH File Transfer Protocol) '
    'fore vanlig FTP for extra sakerhet.'
))

story.append(H2('FTP Connections'))
story.append(P(
    'FTP Connections visar alla aktiva FTP-anslutningar till kontot. Du kan se vilken anvandare '
    'som ar ansluten, fran vilken IP-adress och vilken mapp de ar i. Detta ar anvandbart for '
    'sakerhetsovervakning - om du ser en okand IP-adress som ar ansluten via FTP kan det '
    'indikera att nagon har fatt tag pa losenordet. Du kan aven avbryta (disconnect) en aktiv '
    'anslutning direkt fran denna sida. For daglig drift anvands denna funktion sallan, men '
    'det ar bra att veta att den finns for felsokning och sakerhetskontroll.'
))

story.append(H2('Anonymous FTP'))
story.append(P(
    'Anonymous FTP latar anvandare ansluta till servern utan losenord for att ladda ner filer '
    'fran en specifik mapp. Detta anvandes for att dela stora filer med allmanheten fore tider '
    'av molnlagring och CDN-tjanster. I modern webbhotellning ar Anonymous FTP sallan nodvandigt '
    'och utgor en potentiell sakerhetsrisk. For restaurangkunder finns det ingen praktisk '
    'anvandning for denna funktion. Rekommendation ar att lamma den avaktiverad sa som den ar '
    'som standard. Om nagon fragar om den, forklara att det ar en aldre teknik som inte '
    'rekommenderas for moderna hemsidor.'
))

story.append(H2('Git Version Control'))
story.append(P(
    'Git Version Control latar kunden skapa och hantera Git-repositorier direkt i cPanel. Detta '
    'ar framttaget for utvecklare som vill anvanda Git for versionshantering av sin kod. Du kan '
    'skapa ett nytt repositorie eller klona ett befintligt fran GitHub, GitLab eller Bitbucket. '
    'cPanel visar den senaste commit-infon, grenar och filstatus. For restaurangkunder ar denna '
    'funktion normalt inte relevant - de flesta restaurangagare har inte kunskap om Git och '
    'behöver inte versionshantering. Men om du sjalv utvecklar kundens hemsida kan du anvanda '
    'Git for att hantera din kod pa ett professionellt satt.'
))

story.append(H2('Web Disk'))
story.append(P(
    'Web Disk latar kunden hantera filer pa servern som om det vore en lokal hardisk pa deras '
    'dator. Det anvander WebDAV-protokollet for att skapa en natverksdisk som visas i '
    'Filhanteraren pa Windows, Mac eller Linux. Detta ar ett alternativ till FTP som ar enklare '
    'for kunder som inte vill installera en separat FTP-klient. Du skapar en Web Disk genom att '
    'ange ett anvandarnamn, losenord och vilken mapp den ska peka pa. Sedan laddar du ner en '
    'konfigurationsfil for ditt operativsystem som automatiskt satter upp anslutningen. For '
    'restaurangkunder som vill ha ett enkelt satt att ladda upp bilder och dokument ar Web Disk '
    'ett bra alternativ som inte kraver teknisk kunskap.'
))

story.append(H2('File and Directory Restoration'))
story.append(P(
    'Denna funktion latar kunden aterstalla enskilda filer och mappar fran serverns automatiska '
    'backup utan att behova aterstalla hela kontot. Detta ar mycket anvandbart om kunden av '
    'misstag raderat en viktig fil eller om en fil har skadats. Kunden valjer datum fran '
    'backupen, bladdrar till filen och klickar "Restore". Systemet ersatter den nuvarande filen '
    'med versionen fran backupen. Detta ar mycket snabbare an att ladda ner en full backup och '
    'manuellt extrahera filen. ChemiClouds JetBackup hanterar denna funktion och sparar '
    'vanligtvis 30 dagars historik som kunden kan bladdra bland.'
))

story.append(H2('HTML Editor'))
story.append(P(
    'HTML Editor ar en enkel WYSIWYG-redigerare (What You See Is What You Get) inbyggd i '
    'File Manager. Den latar kunden redigera HTML-filer visuellt utan att behova skriva kod. '
    'Detta ar anvandbart for snabba andringar av text och bilder pa en enkel HTML-sida. For '
    'WordPress-sajter ar denna funktion sallan nodvandig eftersom WordPress har sin egen '
    'redigerare som ar mycket mer kraftfull. HTML Editor kan aven vara borttagen i nyare '
    'versioner av cPanel (v134+) dar den har ersatts av andra verktyg. Om den finns ar det '
    'ett enkelt satt for kunder att gora mindre andringar utan att logga in i WordPress.'
))

story.append(H2('Gitweb'))
story.append(P(
    'Gitweb ar ett webbgranssnitt for att bladdra i Git-repositorier. Det visar commit-historik, '
    'filinnehall och diff-jamforelser direkt i webblasaren. Detta ar ett komplement till Git '
    'Version Control-funktionen. For restaurangkunder ar denna funktion inte relevant. Den ar '
    'framforallt anvandbar for utvecklingsteam som vill granska kod utan att ha lokal tillgang '
    'till repositoriet. Liksom HTML Editor kan Gitweb vara borttaget i nyare cPanel-installationer.'
))


# ════════════════════════════════════════════════════════════
# EMAIL
# ════════════════════════════════════════════════════════════
story.append(H1('Email - E-posthantering'))

story.append(P(
    'E-postsektionen ar en av de mest anvanda delarna av cPanel. Har hanterar kunden sina '
    'e-postkonton, spam-filter, vidarebefordring, autosvar och mycket mer. For restauranger ar '
    'e-post kritiskt - de far bokningar, leveransordrar och kundfragor via e-post varje dag. '
    'Som webbhotellagare behover du beharska alla e-postfunktioner for att hjalpa kunderna '
    'och sakerstalla att deras e-post fungerar felfritt.'
))

story.append(H2('Email Accounts'))
story.append(P(
    'Email Accounts ar den viktigaste e-postfunktionen. Har skapar, redigerar och raderar kunden '
    'sina e-postkonton. For varje konto anger du e-postadress (t.ex. info@restaurang.se), ett '
    'losenord och en lagringsgrans. Du kan aven ladda ner e-post via webbmejl, se diskutrymmet '
    'som kontot anvander och andra losenordet. Sidan visar en lista over alla e-postkonton med '
    'information om lagringsanvandning. Du kan ocksa "suspendera" ett konto tillfalligt utan att '
    'radera det - anvandbart om en anstalld slutar men kunden vill spara e-posten. Klicka pa '
    '"Manage" brevid ett konto for att andra installningar eller pa "Delete" for att radera det '
    'permanent. Var forsiktig med radering - all e-post i kontot raderas och gar inte att '
    'aterstalla utan backup.'
))

story.append(H2('Address Importer'))
story.append(P(
    'Address Importer latar dig skapa manga e-postkonton eller vidarebefordrare pa en gang genom '
    'att ladda upp en CSV- eller Excel-fil. Detta ar anvandbart nar du satter upp e-post for en '
    'ny restaurang och vill skapa 10-20 konton snabbt. Filformatet ar enkelt: en kolumn med '
    'e-postadresser och en kolumn med losenord (for e-postkonton) eller destinationsadresser '
    '(for vidarebefordrare). Du kan ocksa skapa listan direkt i cPanel utan att ladda upp en '
    'fil - ange adresserna i textrutan med ett adresspar per rad. Detta sparar mycket tid '
    'jamfort med att skapa varje konto manuellt.'
))

story.append(H2('Archive'))
story.append(P(
    'Archive-funktionen latar kunden spara kopior av alla inkommande, utgaende och mailinglist-'
    'meddelanden under en angiven tidsperiod. Arkiveringen sker automatiskt och meddelandena '
    'sparas i en separat mapp som inte racker mot kontots e-postkvot. Detta ar anvandbart for '
    'restauranger som behover spara e-post for juridiska skall eller vill ha en backup av all '
    'kommunikation. Du kan stalla in hur lange meddelandena ska sparas (t.ex. 1 ar, 5 ar eller '
    'obegransat) och vilka typer av meddelanden som ska arkiveras. Arkiverade meddelanden kan '
    'sokas och lasas via webbmejl eller IMAP.'
))

story.append(H2('Autoresponders'))
story.append(P(
    'Autoresponders skickar automatiskt ett svarsmeddelande nar nagon skickar e-post till en '
    'specifik adress. Detta ar ett av de mest praktiska verktygen for restauranger. Vanliga '
    'anvandningsomraden: bekrysta att en bokning har tagits emot, meddella oppettider under '
    'helgdagar, informera om att restaurangen ar stangd for semester, eller ge en generell '
    '"tack for ditt meddelande"-bekrystelse. Du anger e-postadressen, svarsmeddelandet, '
    'start- och slutdatum och hur ofta samma avsandare ska fa autosvaret (standard ar en gang '
    'per timme). Autoresponders kan aktiveras och avaktiveras nar som helst utan att radera '
    'konfigurationen.'
))

story.append(H2('BoxTrapper'))
story.append(P(
    'BoxTrapper ar ett aggressivt spam-filter som anvander "challenge-response"-metoden. Nar '
    'nagon skickar e-post till en adress med BoxTrapper aktivt, maste avsandaren bekrysta sin '
    'identitet genom att svara pa ett automatiskt meddelande. Forst efter bekrystelsen levereras '
    'den ursprungliga e-posten. Detta ar effektivt for att blockera automatiserad spam, men det '
    'ar ocksa aggressivt och kan skrapa legitima avsandare som inte forstar bekrystelsemeddelandet. '
    'For restauranger rekommenderas INTE BoxTrapper - det ar battre att anvanda SpamAssassin '
    '(Spam Filters) som ar mer balanserat. Om en kund nagon gang ber om starkare spam-skydd '
    'kan du forklara BoxTrapper-men varna for risken att missa viktig e-post.'
))

story.append(H2('Calendar Delegation / Calendars and Contacts'))
story.append(P(
    'Dessa funktioner hanterar kalender- och kontakt.delning via CalDAV och CardDAV-protokollen. '
    'Calendar Delegation latar en anvandare ge en annan anvandare atkomst att lasa eller redigera '
    'deras kalender. Calendars and Contacts Management latar kunden skapa, radera och byta namn '
    'pa kalendrar och adressbocker. Calendars and Contacts Sharing latar kunden dela kalendrar '
    'och adressbocker med andra anvandare. Dessa funktioner kraver att kunden anvander en '
    'kalenderklient som stod CalDAV (t.ex. Apple Calendar, Thunderbird). For restauranger ar '
    'detta sallan aktuellt - de flesta anvander Google Calendar eller Outlook istallet. Men om '
    'en restaurang vill ha en integrerad kalender kopplad till sin e-post ar dessa funktioner '
    'tillgangliga.'
))

story.append(H2('Configure Greylisting'))
story.append(P(
    'Greylisting ar en spam-forsvarsteknik som tillfalligt avvisar e-post fran okanda avsandare. '
    'Nar en e-post tas emot for forsta gangen fran en okand server, avvisas den tillfalligt med '
    'en "try again later"-signal. Legitima e-postservrar kommer att forsoka igen efter nagra '
    'minuter, och da slapps meddelandet igenom. Spambotar som inte forsoker igen blockeras '
    'automatiskt. Greylisting ar aktiverat som standard och ar ett effektivt satt att minska '
    'spam utan att riskera att legitima meddelanden forsvinner. Du kan avaktivera det for '
    'specifika domaner om en kund har problem med fordrade e-postmeddelanden, men i de flesta '
    'fall borde det vara aktivt.'
))

story.append(H2('Default Address'))
story.append(P(
    'Default Address (aven kallat "catch-all") bestammer vad som hander med e-post som skickas '
    'till en adress som inte finns pa domanen. Till exempel, om nagon skickar e-post till '
    'hej@restaurang.se men det adressen inte finns, hamnar meddelandet hos default-adressen. '
    'Du kan valja mellan att kasta meddelandet (Discard), skicka ett felmeddelande till '
    'avsandaren, eller vidarebefordra till en specifik adress. For restauranger rekommenderas '
    'att stalla in "Discard with error to sender" - det ar battre att avsandaren far veta att '
    'adressen inte finns an att all spam samlas i en inkorg. Anvand INTE "Forward to" for '
    'catch-all eftersom det innebar att all spam till alla tankbara adresser vidarebefodras.'
))

story.append(H2('Email Deliverability'))
story.append(P(
    'Email Deliverability ar ett av de viktigaste verktygen for att sakerstalla att kundens '
    'e-post faktiskt levereras. Det kontrollerar automatiskt om domanen har korrekta SPF-, DKIM- '
    'och DMARC-poster i DNS. Om nagot saknas eller ar felaktigt visar verktyget exakt vad som '
    'behover lagas och ger knappar for att automatiskt reparera problemen. SPF anger vilka '
    'servrar som far skicka e-post fran domanen, DKIM signerar utgaende e-post med en digital '
    'signatur, och DMARC anger vad mottagaren ska gora om e-posten misslyckas med SPF- eller '
    'DKIM-kontrollen. For varje ny kund bor du alltid kontrollera Email Deliverability och se '
    'till att alla tre poster ar korrekta och aktiva.'
))

story.append(H2('Email Disk Usage'))
story.append(P(
    'Email Disk Usage visar hur mycket lagringsutrymme varje e-postkonto anvander. Du kan se '
    'listan over alla konton sorterad efter stolek och snabbt identifiera vilka konton som tar '
    'mest plats. Funktionen har ocksa ett verktyg for att radera gamla meddelanden baserat pa '
    'alder - till exempel radera alla meddelanden aldre an 1 ar for att frigora utrymme. Detta '
    'ar anvandbart nar en kund nar sin diskgrans och du behover hjalpa dem att rensa. For '
    'restauranger ar det vanligt att info@-kontot samlar manga ar av gamla bokningar och '
    'leveransbekrystelser som kan raderas for att frigora utrymme.'
))

story.append(H2('Email Filters'))
story.append(P(
    'Email Filters latar kunden skapa regler for att automatiskt hantera inkommande e-post '
    'for ett specifikt e-postkonto. Du kan skapa filter baserat pa avsandare, amne, broddtext, '
    'storlek och manga andra kriterier. När ett filter matchar kan du valja att leverera till '
    'en specifik mapp, vidarebefordra till en annan adress, radera meddelandet, marker som last '
    'eller applicera en regel. Vanliga anvandningsomraden for restauranger: sortera bokningar '
    'till en separat mapp, radera automatiska notiser fran sociala medier, eller vidarebefordra '
    'leveransordrar till en specifik adress. Du kan testa ett filter fore du aktiverar det for '
    'att sakerstalla att det fungerar som vantat.'
))

story.append(H2('Email Routing'))
story.append(P(
    'Email Routing bestammer hur inkommande e-post hanteras for en doman. Det finns tre '
    'alternativ: Local Mail Exchanger (servern hanterar e-posten internt), Remote Mail Exchanger '
    '(e-posten vidarebefodras till en extern server som Google Workspace), och Backup Mail '
    'Exchanger (servern agerar backup). For de flesta restauranger ar "Local Mail Exchanger" '
    'ratt val eftersom e-posten hanteras av din ChemiCloud-server. Om kunden anvander Google '
    'Workspace eller Microsoft 365 for sin e-post maste du stalla in "Remote Mail Exchanger" '
    'och se till att MX-posterna i DNS pekar mot den externa tjansten. Felaktig e-postroutning '
    'ar en av de vanligaste orsakerna till e-postproblem - dubbelkolla alltid denna installning.'
))

story.append(H2('Encryption (GnuPG)'))
story.append(P(
    'Encryption-verktyget latar kunden skapa och hantera GnuPG-nycklar for krypterad e-post. '
    'GPG-kryptering ar en metod for att skicka krypterade och signerade e-postmeddelanden som '
    'bara mottagaren kan lasa. Detta ar en avancerad sakerhetsfunktion som de flesta restaurang-'
    'kunder aldrig kommer att anvanda. Den framtsta anvandningen ar for restauranger som hanterar '
    'kansliga information (t.ex. allergiuppgifter, betalningsinformation) och vill sakerstalla '
    'att e-postkommunikationen ar krypterad. I praktiken ar det mycket sallsan som denna '
    'funktion anvands, men den finns tillganglig for kunder som behovjer den.'
))

story.append(H2('Forwarders'))
story.append(P(
    'Forwarders vidarebefodrar automatiskt all e-post fran en adress till en annan. Detta ar '
    'en av de mest anvanda e-postfunktionerna. Vanliga scenario: vidarebefodra bokning@ till '
    'agarens personliga e-post, vidarebefodra info@ till flera personer, eller samla all e-post '
    'for en doman till en enda inkorg. Du kan skapa tva typer av vidarebefordring: '
    'Account-level (en adress till en annan) och Domain-level (all e-post for en hel doman '
    'till en annan doman). Vidarebefodring sker omedelbart och behaller en kopia pa servern '
    'om du valjer "Forward to" istallet for "Pipe to a program". Forwarders ar enkla att '
    'skapa och kraver ingen teknisk kunskap - ange kalladress och destinationsadress och klicka '
    '"Add Forwarder".'
))

story.append(H2('Global Email Filters'))
story.append(P(
    'Global Email Filters fungerar likadant som Email Filters men tillampas pa ALL e-post for '
    'hela domanen, inte bara ett enskilt konto. Detta ar anvandbart nar du vill blockera en '
    'specifik avsandare for alla konton, eller sortera e-post baserat pa gemensamma kriterier. '
    'Du kan till exempel skapa ett globalt filter som raderar all e-post fran en kand '
    'spammare, eller som markerar all e-post med "invoice" i amnet som viktig. Var forsiktig '
    'med globala filter eftersom de paverkar alla konton pa domanen - ett felaktigt filter kan '
    'radera legitima meddelanden for alla anvandare. Testa alltid globala filter noga fore du '
    'aktiverar dem.'
))

story.append(H2('Mailing Lists (Mailman)'))
story.append(P(
    'Mailing Lists latar kunden skapa e-postlistor dar ett enda meddelande skickas till manga '
    'prenumeranter. Detta drivs av Mailman, en beprövad mjukvara for e-postlistor. For '
    'restauranger kan mailinglistor anvandas for att skicka nyhetsbrev, menyuppdateringar, '
    'speciella erbjudanden eller evenemangsinbjudningar. Kunder kan sjalva prenumerera och '
    'avprenumerera via en webbsida. Du anger listans namn (t.ex. nyheter@restaurang.se), '
    'losenord for administratoren och vilka installningar som ska galla (vem far skicka, '
    'kravs godkannande for prenumeration, etc.). I praktiken anvander de flesta restauranger '
    'hellre ett nyhetsbrevsverktyg som Mailchimp, men Mailing Lists ar ett gratis alternativ '
    'som finns inbyggt i cPanel.'
))

story.append(H2('Spam Filters (SpamAssassin)'))
story.append(P(
    'Spam Filters konfigurerar Apache SpamAssassin, serverns inbyggda spam-filter. SpamAssassin '
    'analyserar varje inkommande e-post och ger den en spam-poang baserat pa hundratals tester. '
    'Om poangen overstiger traskelvardet (vanligtvis 5.0) markeras meddelandet som spam. Du '
    'kan stalla in vad som ska handa med spam: flytta till en separat Spam-mapp (rekommenderas), '
    'radera automatiskt (risk for false positives) eller leverera normalt med modifiererat '
    'amne. Du kan aven vitlista (whitelist) specifika avsandare som alltid ska slappas igenom, '
    'och svartlista (blacklist) avsandare som alltid ska blockeras. For restauranger ar det '
    'viktigt att vitlista leverantorernas e-postadresser och bokningssystem sa att dessa '
    'meddelanden aldrig hamnar i spam-mappen.'
))
story.append(Warn(
    'Om du stalljer in spam-traskeln for lagt (t.ex. 2.0) kommer manga legitima meddelanden '
    'att markeras som spam. Om du stalljer in den for hogt (t.ex. 10.0) slapper du igenom '
    'mycket spam. Standardvardet 5.0 ar en bra balans. Om kunden klagar pa for mycket spam, '
    'sank traskelen gradvis. Om kunden missar viktig e-post, hoj traskelen.'
))

story.append(H2('Track Delivery'))
story.append(P(
    'Track Delivery visar en detaljerad rapport over alla e-postleveransforsok fran kontot. Du '
    'kan se om ett meddelande har levererats framgangsrikt, har forsokt levereras igen, eller '
    'har misslyckats. For misslyckade leveranser visas felmeddelandet som forklarar varfor '
    'e-posten inte kom fram. Detta ar ett ovarderligt verktyg for felsokning nar en kund '
    'sager "min e-post kommer inte fram". Du kan filtrera rapporten per avsandare, mottagare '
    'eller doman. Vanliga fel orsakade av: felaktiga MX-poster, misslyckad SPF/DKIM-validering, '
    'mottagarens server avvisar meddelandet, eller att mottagarens inkorg ar full. Med Track '
    'Delivery kan du snabbt identifiera orsaken och atgarda problemet.'
))

story.append(H2('Set Up Mail Client'))
story.append(P(
    'Set Up Mail Client gör det enkelt for kunden att konfigurera sin e-postklient (Outlook, '
    'Apple Mail, Thunderbird, etc.) genom att automatiskt generera korrekta IMAP-, POP3- och '
    'SMTP-installningar. Kunden valjer sitt e-postkonto och sin e-postklient fran listan, och '
    'cPanel visar de exakta installningarna: servernamn, portnummer, sakerhetstyp (SSL/TLS) '
    'och inloggningsuppgifter. Manga klienter kan aven ladda ner en automatisk konfigurationsfil '
    'som staller in allt med ett klick. Detta ar sarskilt anvandbart for restaurangkunder som '
    'inte ar tekniskt skickliga och behover hjalp att fa sin e-post att fungera i telefonen '
    'eller pa datorn. Du kan aven skicka installationsinstruktioner via e-post direkt fran '
    'denna sida.'
))


# ════════════════════════════════════════════════════════════
# DATABASES
# ════════════════════════════════════════════════════════════
story.append(H1('Databases - Databaser'))

story.append(P(
    'Databassektionen hanterar MySQL/MariaDB- och PostgreSQL-databaser. For restauranger ar '
    'MySQL den viktigaste databasen eftersom WordPress anvander den. De flesta restaurangkunder '
    'kommer aldrig att behovja rogra vid databassektionen - WordPress skoter all databashantering '
    'automatiskt. Men som webbhotellagare bor du veta hur du skapar databaser, anvandare och '
    'behörigheter for fall dar nagot ga snett eller nar du manuellt behover aterstalla en '
    'WordPress-databas.'
))

story.append(H2('MySQL Databases'))
story.append(P(
    'MySQL Databases ar det huvudsakliga verktyget for att skapa och hantera MySQL/MariaDB-'
    'databaser. Har kan du skapa nya databaser, skapa databasanvandare med losenord, tilldela '
    'anvandare till databaser med specifika behorigheter (SELECT, INSERT, UPDATE, DELETE, etc.), '
    'och reparera skadade databaser. Nar du installerar WordPress via Softaculous skapas '
    'databasen och anvandaren automatiskt, sa du behover normalt inte gora detta manuellt. Men '
    'om du migrerar en befintlig WordPress-sajt eller behover aterstalla en databas fran backup '
    'ar denna funktion nodvandig. Du kan aven aven kontrollera storleken pa varje databas och '
    'se vilka anvandare som har atkomst till vilka databaser.'
))

story.append(H2('MySQL Database Wizard'))
story.append(P(
    'MySQL Database Wizard ar en guidad version av MySQL Databases som leder dig steg for steg '
    'genom processen att skapa en databas, en anvandare och tilldela behorigheter. Forsta steget: '
    'skapa databasen (ange ett namn). Andra steget: skapa en anvandare (ange anvandarnamn och '
    'losenord). Tredje steget: tilldela anvandaren behorigheter (vanligtvis "ALL PRIVILEGES"). '
    'Detta ar enklare for nyborjare an att anvanda MySQL Databases direkt. For WordPress-'
    'installationer rekommenderas dock att lata Softaculous skapa databasen automatiskt for att '
    'undvika felkonfiguration.'
))

story.append(H2('MySQL Manager'))
story.append(P(
    'MySQL Manager ar ett modernare granssnitt for att hantera databaser som gradvis ersatter '
    'den aldre MySQL Databases-sidan. Den har en renare design och mer intuitiv hantering av '
    'databaser och anvandare. Funktionerna ar i grunden desamma som MySQL Databases, men '
    'granssnittet ar lattare att navigera. Du kan skapa, redigera och radera databaser och '
    'anvandare, tilldela behorigheter och overvaka diskutrymme. Om bada verktygen finns '
    'tillgangliga rekommenderas MySQL Manager for dess modernare design.'
))

story.append(H2('phpMyAdmin'))
story.append(P(
    'phpMyAdmin ar ett kraftfullt webbaserat verktyg for att hantera MySQL/MariaDB-databaser. '
    'Det ger direkt tillgang till databaserna dar du kan kora SQL-fragor, importera och '
    'exportera data, redigera tabeller, skapa nya tabeller och mycket mer. For restaurangkunder '
    'ar phpMyAdmin sallan nodvandigt, men som webbhotellagare ar det ett ovarderligt verktyg '
    'for felsokning. Vanliga anvandningsomraden: aterstalla en WordPress-databas fran en SQL-'
    'dump, andra WordPress-installningar direkt i wp_options-tabellen, eller rensa gamla '
    'revisioner och spam-kommentarer som tar upp plats. Var forsiktig med phpMyAdmin - du kan '
    'radera hela databaser med ett missklick, sa alltid skapa en backup fore du gor andringar.'
))

story.append(H2('PostgreSQL Databases / phpPgAdmin'))
story.append(P(
    'PostgreSQL ar ett alternativt databassystem som erbjuds utover MySQL/MariaDB. PostgreSQL '
    'ar mer kraftfullt for komplexa fragor och stora datamangder, men det anvands sallan for '
    'webbhotell eftersom WordPress och de flesta webbapplikationer kraver MySQL. For restaurang-'
    'kunder finns det ingen praktisk anledning att anvanda PostgreSQL. phpPgAdmin ar motsvarigheten '
    'till phpMyAdmin for PostgreSQL. Om kunden fragar om PostgreSQL kan du forklara att MySQL '
    'ar standard och rekommenderas for deras behov.'
))

story.append(H2('Remote Database Access'))
story.append(P(
    'Remote Database Access latar kunden tillata specifika IP-adresser att ansluta till '
    'MySQL/MariaDB-databaserna fran en annan server. Normalt kan databaserna bara accessas '
    'lokalt fran samma server (localhost). Om kunden har en extern applikation som behover '
    'lasa eller skriva till databasen fran en annan server maste du lagga till den externa '
    'IP-adressen har. For restauranger ar detta sallan nodvandigt. Ett exempel dar det kan '
    'vara aktuellt ar om restaurangen har ett separat bokningssystem som lagger i en annan '
    'molnmiljo och behover lasa menydata fran WordPress-databasen.'
))


# ════════════════════════════════════════════════════════════
# DOMAINS
# ════════════════════════════════════════════════════════════
story.append(H1('Domains - Domäner'))

story.append(P(
    'Domains-sektionen hanterar alla domanrelaterade funktioner: lagga till domaner, skapa '
    'subdomaner, stalla in omdirigeringar och redigera DNS-poster. For restauranger ar '
    'Zone Editor (DNS-redigering) och Domains (hantering av addon-domäner) de viktigaste '
    'funktionerna. Du kommer att anvanda dessa nar du satter upp en ny kund, pekar en doman '
    'mot ratt katalog, eller staller in DNS-poster for e-post och SSL.'
))

story.append(H2('Domains'))
story.append(P(
    'Domains ar den centrala hanteringen for alla domaner pa kontot. Har kan du se en lista '
    'over alla domaner, subdomaner och addon-domäner som ar kopplade till kontot. Du kan '
    'lagga till en ny doman, ta bort en befintlig doman, stalla in document root (vilken mapp '
    'som hemsidan ska laddas fran) och hantera omdirigeringar. Nar du lagger till en ny doman '
    'anger du domannamnet och vilken mapp som ska vara document root (standard ar public_html/ '
    'domannamn). cPanel skapar automatiskt DNS-poster och en mappstrukturen for den nya '
    'domänen. Du kan aven stalla in om domänen ska ha sin egen SSL-certifikat.'
))

story.append(H2('Dynamic DNS'))
story.append(P(
    'Dynamic DNS (DDNS) ar en funktion for domäner vars IP-adress andras regelbundet. Detta '
    'anvands framforallt for hemmaservrar och natverksenheter som inte har en fast IP-adress. '
    'For restaurangkunder ar Dynamic DNS normalt inte relevant eftersom deras hemsida hostas '
    'pa en server med fast IP-adress. Om en restaurang skulle ha en lokal server i restaurangen '
    '(t.ex. for ett punktsystem eller overvakningskameror) kan DDNS anvandas for att ge '
    'servern ett domannamn som alltid pekar mot restaurangens aktuella IP-adress.'
))

story.append(H2('Redirects'))
story.append(P(
    'Redirects latar dig stalla in omdirigeringar fran en URL till en annan. Du kan skapa '
    'permanenta (301) eller tillfalliga (302) omdirigeringar. Vanliga anvandningsomraden for '
    'restauranger: omdirigera gamla sidor till nya, omdirigera http till https, omdirigera '
    'en subdoman till en extern tjanst (t.ex. bokning.restaurang.se till ett bokningssystem), '
    'eller omdirigera en gammal doman till en ny. 301-omdirigeringar ar permanenta och '
    'sokmotorer overfor SEO-vardet till den nya URL:en. 302-omdirigeringar ar tillfalliga och '
    'borde bara anvandas for tillfalliga andamal. Du kan aven anvanda wildcards for att '
    'omdirigera alla sidor under en specifik vag till en ny plats.'
))

story.append(H2('Zone Editor'))
story.append(P(
    'Zone Editor ar det viktigaste verktyget for att redigera DNS-poster for en doman. Har kan '
    'du lagga till, redigera och radera A-, AAAA-, CNAME-, MX-, TXT-, SRV- och CAA-poster. '
    'Detta ar sarskilt viktigt nar du staller in e-postautentisering (SPF, DKIM, DMARC), '
    'pekar en subdoman mot en extern tjanst, eller verifierar domanagande for Google Search '
    'Console eller andra tjanster. Zone Editor har tre funktioner: Manage (fullstandig '
    'redigering av alla poster), +A Record (snabb lagga till A-post) och +CNAME Record '
    '(snabb lagga till CNAME-post). For avancerad redigering klickar du pa "Manage" sa far du '
    'en komplett lista over alla DNS-poster med mojlighet att lagga till, andra och radera.'
))
story.append(Tip(
    'Anvand Zone Editor for att lagga till TXT-poster for SPF, DKIM och DMARC. Gå till '
    'Email Deliverability forst - den kan automatiskt skapa dessa poster at dig. Anvand bara '
    'Zone Editor om Email Deliverability inte kan losa problemet automatiskt.'
))


# ════════════════════════════════════════════════════════════
# METRICS
# ════════════════════════════════════════════════════════════
story.append(H1('Metrics - Statistik'))

story.append(P(
    'Metrics-sektionen ger kunden insikt i hur deras hemsida anvands och hur serverresurserna '
    'forbrukas. For restauranger ar Bandwidth och Visitors de mest intressanta funktionerna, '
    'medan CPU and Concurrent Connection Usage ar viktigast for dig som webbhotellagare for '
    'att overvaka att inget konto overbelastar servern.'
))

story.append(H2('Site Quality Monitoring'))
story.append(P(
    'Site Quality Monitoring overvakar kundens hemsida for problem med SEO, prestanda och '
    'tillganglighet. Det ger en overall bedoming med fargindikatorer och specifika rekommendationer '
    'for forbattringar. Verktyget kors automatiska tester med jama mellanrum och lagrar '
    'historik sa att kunden kan se trender over tid. For dig som webbhotellagare ar detta ett '
    'bra verktyg for att proaktivt identifiera problem fore kunden rinker dem. Du kan aven '
    'stalla in e-postaviseringar for att fa besked nar en hemsidas kvalitetspoang sjunker.'
))

story.append(H2('AWStats'))
story.append(P(
    'AWStats ar en detaljerad statistikrapport over hemsidans trafik. Den visar antal '
    'besokare, sidvisningar, besokstid, de mest populara sidorna, vilka sokord som lett '
    'besokare till sajten, vilka lander besokarna kommer fran och mycket mer. AWStats ar '
    'det mest omfattande statistikverktyget i cPanel och ger en djupgande bild av '
    'hur besokarna interagerar med hemsidan. For restauranger ar det intressant att se '
    'vilka sidor som ar mest populara (meny, oppettider, kontakt), vilka sokord som '
    'leder trafik till sajten och om det finns okanda trafikkallor. AWStats uppdateras '
    'normalt en gang per dygn sa datan ar inte realtidsbaserad.'
))

story.append(H2('Bandwidth'))
story.append(P(
    'Bandwidth visar hur mycket data som har overforts till och fran kontot under den '
    'aktuella manaden. Det visas som grafer for HTTP (webbtrafik), FTP, SMTP (e-post) och '
    'POP3/IMAP (e-postnedladdning). Om kundens paket har en bandbreddsgrans (t.ex. 5 GB/manad) '
    'kan du har se hur mycket som har anvants och hur mycket som ar kvar. For restauranger ar '
    'bandbreddsanvandningen vanligtvis lag - en typisk restauranghemsida med bilder och ett '
    'par hundra besokare per dag anvander sallan mer an 1-2 GB per manad. Om bandbredden '
    'overstiger gransen kan hemsidan bli otillganglig eller langsam, sa det ar viktigt att '
    'overvaka denna statistik.'
))

story.append(H2('CPU and Concurrent Connection Usage'))
story.append(P(
    'Denna funktion visar hur mycket serverresurser kontot anvander i realtid. Den visar '
    'CPU-anvandning, minnesanvandning (RAM) och antal samtidiga processer (entry processes). '
    'Dessa granser satts av CloudLinux som isolerar varje konto och forhindrar att ett konto '
    'overbelastar servern och paverkar andra kunder. Om ett konto ofta nar sina resursgranser '
    'kan det bero pa en felkonfigurerad WordPress-installation, ett resurskravande tillagg '
    'eller en trafikspik. Vanliga orsaker till hog CPU-anvandning: WordPress-cronjobb som '
    'kors for ofta, okompilerade PHP-skript, eller bot-trafik som belastar sajten. Om du ser '
    'att ett konto ofta nar sina granser bor du undersoka orsaken och eventuellt uppgradera '
    'kundens paket.'
))

story.append(H2('Errors'))
story.append(P(
    'Errors visar de senaste posterna fran webbserverns felloggar (error log). Har kan du se '
    '404-fel (sidor som inte hittas), 500-fel (serverfel), PHP-fel och andra problem som '
    'uppstatt nar besokare forsoker komma at hemsidan. Detta ar ett ovarderbart verktyg for '
    'felsokning - om en kund rinker att en sida inte fungerar kan du har se exakt vad felmeddelandet '
    'ar. cPanel visar upp till 300 av de senaste felposterna. Vanliga fel for WordPress: '
    'PHP-fel orsakade av inkompatibla tillagg, saknade filer, och databasanslutningsfel.'
))

story.append(H2('Visitors'))
story.append(P(
    'Visitors visar detaljerad information om de senaste besok pa hemsidan, extraherad fran '
    'access-loggarna. Du kan se vilka sidor som besoktes, fran vilken IP-adress, vid vilken '
    'tidpunkt och med vilken webblasare. Detta ar mer detaljerat an AWStats men visar bara '
    'de senaste besoken (inte historisk data). For restauranger kan det vara intressant att se '
    'om besokare kommer fran mobila enheter, vilka sidor de tittar pa och hur lange de stannar. '
    'Detta ar ocksa anvandbart for sakerhetskontroll - om du ser misstankt trafik fran en '
    'specifik IP-adress kan du blockera den via IP Blocker.'
))

story.append(H2('Raw Access, Webalizer, Analog Stats'))
story.append(P(
    'Dessa ar aldre statistikverktyg som ger mindre anvandarvanliga vyer av trafikdata. Raw '
    'Access ger raa loggfiler (text) som kan analyseras med externa verktyg. Webalizer ar ett '
    'snabbt statistikprogram med grundlaggande grafer. Analog Stats ger en enkel trafikrapport. '
    'For daglig anvandning ar AWStats battre an alla dessa, men de finns tillgangliga for den '
    'som fordrar mer detaljerad eller radata. Metrics Editor latar dig valja vilka av dessa '
    'program som ska bearbeta loggfilerna for varje doman.'
))


# ════════════════════════════════════════════════════════════
# SECURITY
# ════════════════════════════════════════════════════════════
story.append(H1('Security - Sakerhet'))

story.append(P(
    'Security-sektionen innehaller alla sakerhetsrelaterade funktioner fran SSL-certifikat till '
    'IP-blockering och tvafaktorsautentisering. For restauranger ar SSL/TLS de viktigaste '
    'funktionerna - alla hemsidor maste ha HTTPS. IP Blocker och ModSecurity ar ocksa viktiga '
    'for att skydda mot skadlig trafik och brute-force-attacker.'
))

story.append(H2('SSL/TLS'))
story.append(P(
    'SSL/TLS-sektionen ar den mest anvanda sakerhetsfunktionen. Den hanterar generering av '
    'privata nycklar, Certificate Signing Requests (CSR) och installation av SSL-certifikat. '
    'For restaurangkunder ar det viktigaste flodet att installera ett Let\'s Encrypt-certifikat '
    '(vilket gor du via WHM, inte har). Men om kunden behover ett betalt certifikat fran en '
    'tredjeparts-utavnnare (t.ex. Comodo, DigiCert) skapar du forst en CSR har, skickar den '
    'till certifikatutavnnaren och installerar sedan det fardiga certifikatet har. cPanel '
    'lagrar alla nycklar och certifikat for framtida referens.'
))

story.append(H2('SSL/TLS Status'))
story.append(P(
    'SSL/TLS Status visar en oversikt over alla domäner pa kontot och deras SSL-status. '
    'Gront = certifikat aktivt och giltigt, gult = certifikat gar ut snart, rod = inget '
    'certifikat eller ogiltigt certifikat. Du kan ocksa se när certifikatet gar ut och '
    'klicka pa "Run AutoSSL" for att forsoka installera eller fornya certifikat automatiskt. '
    'AutoSSL (Let\'s Encrypt eller cPanel-certifikat) kors automatiskt med jama mellanrum, '
    'men du kan ocksa starta det manuellt har. Om en doman visar rod status beror det oftast '
    'pa att DNS inte pekar ratt - kontrollera att A-posten pekar mot ratt IP-adress.'
))

story.append(H2('SSL/TLS Certificates (tabbad vy)'))
story.append(P(
    'Detta ar en modernare version av SSL/TLS-hanteringen med ett tabbat granssnitt som '
    'innehaller fyra flikar: Certificates (installera och hantera certifikat), Private Keys '
    '(skapa och hantera privata nycklar), Certificate Signing Requests (skapa CSR for betalda '
    'certifikat) och Install and Manage SSL for your site (installera certifikat pa specifika '
    'domäner). Denna vy ger en mer oversiktlig hantering av SSL-relaterade uppgifter. For '
    'nya installationer rekommenderas denna vy over den klassiska SSL/TLS-sidan.'
))

story.append(H2('SSL/TLS Wizard'))
story.append(P(
    'SSL/TLS Wizard ar en guidad process for att kopa och installera ett SSL-certifikat. Den '
    'letar kunden steg for steg genom att valja doman, valja certifikattyp (Domain Validation, '
    'Organization Validation, Extended Validation), kopa certifikatet fran en partner och '
    'installera det automatiskt. For restauranger ar Let\'s Encrypt (gratis) tillrackligt i '
    'nasta alla fall. Betalda certifikat ar bara nodvandiga for e-handel eller om kunden '
    'onskar en hogre valideringsniva. Wizard-funktionen forenklar processen for kunder som '
    'onskar kopa ett betalt certifikat sjalva.'
))

story.append(H2('IP Blocker'))
story.append(P(
    'IP Blocker latar dig blockera specifika IP-adresser eller hela IP-intervall fran att '
    'komma at kundens hemsida. Detta ar anvandbart for att stoppa spam-botar, hackare eller '
    'ovälkomna besokare. Du anger IP-adressen (t.ex. 192.168.1.100), ett intervall (t.ex. '
    '192.168.1.0/24) eller ett domannamn (som automatiskt oversatts till IP-adresser). '
    'Blockerade besokare far ett 403 Forbidden-fel. Du kan se en lista over alla blockerade '
    'IP-adresser och ta bort blockeringar nar som helst. For restauranger kan detta anvandas '
    'for att blockera kanda spammare eller bot-natverk som skickar falska bokningar.'
))

story.append(H2('Hotlink Protection'))
story.append(P(
    'Hotlink Protection forhindrar att andra webbplatser linker direkt till bilder och andra '
    'mediafiler pa kundens server. Nar nagon "hotlinkar" en bild anvander de kundens bandbredd '
    'utan att besoka deras hemsida. Detta ar vanligt for bloggar och forum som vill visa '
    'restaurangens bilder utan tillstand. Med Hotlink Protection kan du ange vilka domäner som '
    'ar tillatna att lanka till filerna och blockera alla andra. Du kan ocksa valja att visa '
    'en alternativ bild (t.ex. en "Stjal inte bilder"-bild) istallet for den efterfragade '
    'filen. For restauranger med unika professionella bilder ar detta ett bra satt att skydda '
    'sitt innehall och sin bandbredd.'
))

story.append(H2('Leech Protection'))
story.append(P(
    'Leech Protection upptacker och begransar ovanlig aktivitet i losenordsskyddade kataloger. '
    'Om nagon delar sitt losenord med manga andra anvandare (s.k. "leeching") kan Leech '
    'Protection automatiskt blockera kontot eller skicka en avisering. Du staller in en grans '
    'for hur manga gangar ett konto kan logga in under en viss period. Om gransen overskrids '
    'kan du valja att omdirigera anvandaren till en specifik URL, inaktivera kontot eller skicka '
    'ett e-postmeddelande. For restauranger ar denna funktion sallan nodvandig, men den kan vara '
    'anvandbar om kunden har ett losenordsskyddat omrade (t.ex. en partnerportal) och vill '
    'forhindra obehorig delning av inloggningsuppgifter.'
))

story.append(H2('ModSecurity'))
story.append(P(
    'ModSecurity ar en webbapplikation-brandvagg (WAF) som analyserar inkommande HTTP-forgaringar '
    'och blockerar kanda attackmönster som SQL-injektion, cross-site scripting (XSS) och andra '
    'vanliga attacker. ModSecurity ar aktiverat som standard av ChemiCloud och bor vara aktiverat '
    'for alla domäner. Ibland kan ModSecurity falskt blockera legitima forfragingar (t.ex. om '
    'kunden forsoker spara en lang text i WordPress som innehaller kod-liknande monster). I '
    'sada fall kan du tillfalligt avaktivera ModSecurity for den specifika domänen eller '
    'lagga till en undantagsregel. Avaktivera aldrig ModSecurity permanent - det ar en viktig '
    'sakerhetskomponent som skyddar kundens hemsida mot de vanligaste attacktyperna.'
))

story.append(H2('SSH Access'))
story.append(P(
    'SSH Access ger information om hur kunden ansluter till servern via SSH (Secure Shell). '
    'Har kan kunden ladda ner SSH-nycklar, hantera kanda vardar och se anslutningsinformation. '
    'For att SSH ska fungera maste det vara aktiverat i WHM (se WHM > Account Functions > '
    'Modify an Account > Shell Access). For restaurangkunder rekommenderas normalt att SSH ar '
    'avaktiverat (noshell) eftersom de sallan behovjar kommandoradsaccess och det utgor en '
    'sakerhetsrisk. Om du sjalv behovjar SSH for att felsoka en kunds konto kan du anvanda '
    'WHM:s Terminal-funktion istallet for att ge kunden SSH-atkomst.'
))

story.append(H2('Two-Factor Authentication'))
story.append(P(
    'Two-Factor Authentication (2FA) lagger till ett extra sakerhetslager vid inloggning i '
    'cPanel. Utöver losenordet maste kunden aven ange en kod fran sin telefon (via en app '
    'som Google Authenticator eller Authy). Detta forhindrar att nagon kan logga in aven om '
    'de har fatt tag pa losenordet. For restauranger rekommenderas 2FA starkt - det ar en '
    'enkel atgard som dramatiskt okar sakerheten. Du staller in 2FA genom att skanna en QR-'
    'kod med din autentiseringsapp och sedan ange koden for att bekrasta. Efter det kravs '
    'losenord + kod vid varje inloggning. Spara atkomstkoderna (backup-koder) pa en saker '
    'plats ifall telefonen tappas eller byts ut.'
))

story.append(H2('Manage API Tokens'))
story.append(P(
    'API Tokens latar kunden skapa sakra tokens for att ansluta till cPanel-API:et utan att '
    'anvanda losenordet. Detta ar anvandbart for automatisering och integrationer - till exempel '
    'om kunden vill automatiskt skapa e-postkonton via ett externt skript eller integrera cPanel '
    'med ett affarssystem. Varje token har specifika behorigheter (lasa, skriva, etc.) och kan '
    'aterkallas nar som helst. For restauranger ar denna funktion sallan aktuell, men om du bygger '
    'en anpassad lösning for en restaurang som automatiskt hanterar e-post eller filer via API:et '
    'ar detta det sakra sattet att gora det.'
))

story.append(H2('Security Policy'))
story.append(P(
    'Security Policy latar kunden uppdatera de sakerhetsfragor som anvands for att aterstalla '
    'losenordet om de glomt det. Dessa fragor ar ett alternativ till e-postbaserad '
    'losenordsaterstallning. Kunden kan valja fragor som "Vilken stad foddes du i?" eller '
    "Vad hette ditt forsta husdjur?\" och ange svaren. Detta ar en grundlaggande sakerhetsfunktion "
    'som alla kunder bor stalla in vid kontots skapande. Om kunden glommer sitt losenord kan de '
    'svara pa sakerhetsfragorna for att fa tillgang till kontot igen. Se till att kunden valjer '
    'fragor med svar som inte ar latta att gissa fran sociala medier.'
))


# ════════════════════════════════════════════════════════════
# SOFTWARE
# ════════════════════════════════════════════════════════════
story.append(H1('Software - Mjukvara'))

story.append(P(
    'Software-sektionen hanterar PHP-konfiguration, applikationer och programmspraksmoduler. '
    'For restauranger ar MultiPHP Manager och MultiPHP INI Editor de viktigaste funktionerna - '
    'de latar dig valja PHP-version och konfigurera PHP-installningar for varje doman. Optimize '
    'Website ar ocksa anvandbart for att komprimera webbinnehall och snabba upp hemsidan.'
))

story.append(H2('MultiPHP Manager'))
story.append(P(
    'MultiPHP Manager latar dig stalla in vilken PHP-version varje doman ska anvanda. Detta ar '
    'viktigt eftersom olika WordPress-versioner och tillagg kraver olika PHP-versioner. '
    'WordPress rekommenderar PHP 8.1 eller hogre for bast prestanda och sakerhet. Om en kund '
    'har en aldre WordPress-installation med inkompatibla tillagg kan du behova anvanda en '
    'aldre PHP-version tillfalligt. Du valjer domanen fran listan, valjer PHP-version fran '
    'rullgardinsmenyn och klickar "Apply". Andringen trader i kraft omedelbart. ChemiCloud '
    'erbjuder vanligtvis PHP 7.4, 8.0, 8.1, 8.2 och 8.3 via CloudLinuxs PHP Selector. '
    'Rekommendation: anvanda den nyaste PHP-versionen som kundens WordPress och tillagg stoder.'
))

story.append(H2('MultiPHP INI Editor'))
story.append(P(
    'MultiPHP INI Editor latar dig andra PHP-konfigurationsinstallningar (php.ini) for varje '
    'doman. De viktigaste installningarna for restauranger ar: memory_limit (hur mycket minne '
    'PHP far anvanda, rekommenderas 256M for WordPress), upload_max_filesize (max filstorlek '
    'for uppladdning, rekommenderas 64M for stora bilder), post_max_size (max storlek for '
    'POST-data, bor vara minst lika stor som upload_max_filesize), max_execution_time (hur lange '
    'ett PHP-skript far kora, standard 30 sekunder), och max_input_vars (max antal indata-'
    'variabler, viktigt for stora menyer i WordPress). Du kan redigera installningarna i '
    'ett enkelt granssnitt (Basic Mode) eller direkt i php.ini-format (Editor Mode).'
))

story.append(H2('Optimize Website'))
story.append(P(
    'Optimize Website latar dig konfigurera Apache att automatiskt komprimera specifika typer '
    'av innehall fore det skickas till besokarens webblasare. Komprimering minskar filstorleken '
    'och gor att hemsidan laddar snabbare, sarskilt for besokare med langsammare internet-'
    'anslutningar. Du kan valja att komprimera all text (HTML, CSS, JavaScript) eller specifika '
    'MIME-typer. For restauranger rekommenderas att aktivera komprimering for "All text" - det '
    'ar en enkel installning som kan snabba upp hemsidan avenstbart. De flesta moderna '
    'WordPress-sajter har redan komprimering aktiverad via cachetillagg, sa denna installning '
    'ar viktigast for hemsidor som inte anvander caching.'
))

story.append(H2('Perl Modules, PHP PEAR Packages, RubyGems, Ruby on Rails'))
story.append(P(
    'Dessa funktioner hanterar installation av moduler och paket for Perl, PHP PEAR och Ruby. '
    'Perl Modules latar dig installera Perl-moduler fran CPAN-arkivet. PHP PEAR Packages '
    'hanterar PHP-paket fran PEAR-arkivet. RubyGems ar pakethanteraren for Ruby-program och '
    'bibliotek. Ruby on Rails latar dig skapa och distribuera en Rails-applikation. For '
    'restaurangkunder ar ingen av dessa funktioner relevanta - moderna restauranghemsidor byggs '
    'med WordPress (PHP) och behovjer inte dessa avancerade utvecklarverktyg. Du kan tryggt '
    'ignorera dessa funktioner om du inte sjalv utvecklar anpassade applikationer for kunderna.'
))

story.append(H2('Application Manager'))
story.append(P(
    'Application Manager latar dig distribuera applikationer med Phusion Passenger-'
    'applikationsservern. Detta ar framtaget for Ruby-, Python- och Node.js-applikationer som '
    'maste kora som bakgrundsprocesser. For restauranger ar denna funktion normalt inte '
    'relevant eftersom WordPress (PHP) inte behovjar Passenger. Men om du bygger en anpassad '
    'Node.js- eller Python-applikation for en restaurang (t.ex. ett specialiserat bokningssystem '
    'eller en realtids-meny) kan du anvanda Application Manager for att distribuera och hantera '
    'applikationen.'
))

story.append(H2('Site Software'))
story.append(P(
    'Site Software visar en lista over programvara som hostingleverantoren har gjort tillganglig '
    'for installation. Detta ar en aldre funktion som har erstatts av Softaculous och WP Toolkit. '
    'I ChemiClouds miljo ar Softaculous den primara installatören, sa Site Software ar sallan '
    'aktuellt. Om det finns nagon programvara har som inte finns i Softaculous kan det vara '
    'vardt att kolla, men for restaurangkunder ar Softaculous mer an tillrackligt for alla '
    'installationsbehov.'
))


# ════════════════════════════════════════════════════════════
# ADVANCED
# ════════════════════════════════════════════════════════════
story.append(H1('Advanced - Avancerat'))

story.append(P(
    'Advanced-sektionen innehaller tekniska verktyg for avancerade anvandare. Cron Jobs ar den '
    'vanligaste funktionen har - den latar dig schemalagga uppgifter som ska kora automatiskt. '
    'Terminal ger kommandoradsaccess direkt i webblasaren. Virus Scanner ar viktig for sakerhet. '
    'De ovriga funktionerna anvands sallan av restaurangkunder men ar bra att kanna till.'
))

story.append(H2('Cron Jobs'))
story.append(P(
    'Cron Jobs latar dig schemalagga kommandon eller skript som ska kora automatiskt vid '
    'fordefinierade tider eller intervall. For WordPress ar cron jobs sarskilt viktiga - '
    'WordPress anvander ett internt cron-system (WP-Cron) for att schemalagga uppgifter som '
    'publicering av inlagg, kontroll av uppdateringar och radering av spam-kommentarer. Du kan '
    'ocksa skapa system-cron jobs som korer PHP-skript, shell-skript eller andra kommandon. '
    'Vanliga anvandningsomraden: backa upp databasen varje natt, rensa gamla filer varje vecka, '
    'eller kora ett sakerhetsskanning. Du anger tidintervallet med cron-syntax (min timme dag '
    'manad veckodag) eller anvander de fordefinierade alternativen (var 5:e minut, en gang i '
    'timmen, etc.). Var forsiktig - felkonfigurerade cron jobs kan belasta servern och paverka '
    'andra kunder.'
))

story.append(H2('Terminal'))
story.append(P(
    'Terminal ger en kommandoterminal direkt i webblasaren. Detta ar som att ha SSH-access '
    'utan att behovja en separat klient. Du kan kora Linux-kommandon, navigera filsystemet, '
    'redigera filer med vim/nano, kora PHP-skript och mycket mer. For avancerade anvandare '
    'ar detta ett kraftfullt verktyg for felsokning och administration. For restaurangkunder '
    'ar Terminal normalt inte nodvandigt och bor vara avaktiverat av sakerhetsskal. Som '
    'webbhotellagare kan du anvanda Terminal for snabb felsokning utan att behova logga in '
    'via SSH separat. Terminal-sessionen ar bunden till kundens cPanel-session och forsvinner '
    'nar du loggar ut.'
))

story.append(H2('Virus Scanner (ClamAV)'))
story.append(P(
    'Virus Scanner anvander ClamAV for att skanna kundens konto efter malware, virus och andra '
    'sakerhetshot. Du kan skanna hela kontot, specifika mappar eller enskilda filer. Om nagot '
    'hittas visar skannern filnamnet och typen av hot, och du kan valja att radera eller '
    'karantanera filen. For restauranger ar det bra att kora en virus skanning med jama '
    'mellanrum, sarskilt om kunden har installerat manga WordPress-tillagg fran tredje part. '
    'ChemiCloud har ocksa Imunify360 som kors i bakgrunden och automatiskt detekterar malware, '
    'sa Virus Scanner ar ett komplement for manuella skanningar. Om en skanning hittar malware '
    'bor du ocksa undersoka hur det kom in (vanligtvis via sarbara tillagg eller stulna losenord).'
))

story.append(H2('Error Pages'))
story.append(P(
    'Error Pages latar kunden anpassa felsidor som besokare ser nar nagot gar fel. De vanligaste '
    'felsidorna ar 404 (sidan hittades inte), 403 (atkomst nekad), 500 (internt serverfel) och '
    '400 (felaktig forfragan). Du kan skapa egna felsidor med HTML som matchar kundens '
    'varumärke - till exempel en 404-sida som sager "Hoppsan! Den har ratten finns inte pa '
    'var meny" med en lank tillbaka till hemsidan. cPanel har en enkel HTML-redigerare for att '
    'skapa felsidor, eller sa kan du klistra in egen HTML-kod. For restauranger ar en anpassad '
    '404-sida en bra detalj som ger ett professionellt intryck.'
))

story.append(H2('Apache Handlers'))
story.append(P(
    'Apache Handlers bestammer hur Apaches webbserver ska hantera specifika filtyper. Du kan '
    'till exempel saga att .py-filer ska koras som CGI-skript eller att .shtml-filer ska '
    'processas for Server Side Includes. For restaurangkunder ar denna funktion normalt inte '
    'relevant - WordPress och PHP hanteras automatiskt av servern. Om du behovjar att lagga till '
    'en egen handler for en specifik filtyp kan du gora det har, men i praktiken behovjar '
    'du sallan rogra vid denna installning.'
))

story.append(H2('MIME Types'))
story.append(P(
    'MIME Types bestammer hur webblasaren ska hantera specifika filtyper. En MIME-typ '
    'informerar webblasaren om vilken typ av innehall en fil innehaller (t.ex. text/html for '
    'HTML-filer, image/jpeg for JPEG-bilder). Du kan lagga till egna MIME-typer for filformat '
    'som inte ar standard. For restauranger ar denna funktion sallan nodvandig - de vanligaste '
    'filtyperna (HTML, CSS, JavaScript, bilder, PDF) ar redan fordefinierade. Ett exempel dar '
    'det kan vara aktuellt ar om kunden vill servera en speciell filtyp (t.ex. .webp-bilder) '
    'som inte ar standard pa servern.'
))

story.append(H2('Indexes'))
story.append(P(
    'Indexes bestammer hur servern visar innehallet i en katalog som saknar en indexfil (t.ex. '
    'index.html eller index.php). Om indexering ar aktiverat visas en lista over filerna i '
    'katalogen. Om det ar avaktiverat far besokaren ett 403 Forbidden-fel. For sakerhetskal '
    'bor indexering normalt vara avaktiverat sa att besokare inte kan se filstrukturen. Om en '
    'kund vill att besokare ska kunna bladdra i en specifik mapp (t.ex. en mapp med nedladdnings- '
    'bara menyer i PDF-format) kan du aktivera indexering for just den mappen. Standard i '
    'cPanel ar att indexering ar avaktiverat for public_html och aktiverat for vissa undermappar.'
))

story.append(H2('Track DNS'))
story.append(P(
    'Track DNS ar ett natverksdiagnostikverktyg som latar dig kora DNS-uppslag (dig), '
    'traceroute och andra natverkskommandon direkt fran cPanel. Detta ar anvandbart for '
    'felsokning nar du vill kontrollera om en doman pekar ratt, om DNS-posterna ar korrekta '
    'eller om det finns natverksproblem mellan kundens dator och servern. Du anger domannamnet '
    'och valjer typ av uppslag. Verktyget returnerar detaljerad information om DNS-poster, '
    'sokvag och svarstider. For restauranger anvands detta sallan, men det ar ett bra verktyg '
    'for dig som webbhotellagare nar du felsoker DNS-problem for en kund.'
))

story.append(H2('API Shell'))
story.append(P(
    'API Shell latar dig kora cPanel API-funktioner interaktivt direkt i webblasaren. Detta '
    'ar ett utvecklarverktyg for att testa API-anrop och se resultatet direkt. Du kan valja '
    'mellan cPanel API 1 och cPanel API 2, ange funktionen och parametrar, och se svaret. '
    'For restaurangkunder ar denna funktion inte relevant alls. Den ar framtagen for '
    'utvecklare som bygger integrationer med cPanel-API:et. Som webbhotellagare anvander '
    'du denna funktion sallan, men den kan vara anvandbar for att testa om ett API-anrop '
    'fungerar korrekt om du bygger en anpassad losning.'
))


# ════════════════════════════════════════════════════════════
# PREFERENCES
# ════════════════════════════════════════════════════════════
story.append(H1('Preferences - Installningar'))

story.append(P(
    'Preferences-sektionen hanterar kontoinstallningar, losenord, sprak och kontaktinformation. '
    'Dessa funktioner ar grundlaggande och varje kund bor ga igenom dem vid kontots skapande.'
))

story.append(H2('Password and Security'))
story.append(P(
    'Password and Security latar kunden andra sitt cPanel-losenord. Detta ar en av de viktigaste '
    'sakerhetsatgarderna - ett starkt losenord ar forsta forsvaret mot obehorig atkomst. '
    'Kunden anger sitt nuvarande losenord och det nya losenordet tva ganger. cPanel har en '
    'inbyggd losenordsgenerator som skapar starka losenord med en blandning av bokstaver, '
    'siffror och specialtecken. Uppmundra alla kunder att anvanda losenordsgeneratorn och '
    'att spara losenordet i en losenordshanterare (t.ex. Bitwarden eller 1Password). '
    'Losenoordet maste vara minst 5 tecken (men rekommenderas vara minst 16 tecken).'
))

story.append(H2('Change Language'))
story.append(P(
    'Change Language latar kunden valja vilket sprak cPanel-granssnittet ska visas pa. '
    'Tillgangliga sprak inkluderar engelska, svenska, norska, danska, finska och manga '
    'andra. For svenska restaurangkunder kan det vara behagligt att stalla in cPanel pa '
    'svenska, men observera att inte alla funktioner ar fullstandigt oversatta. Manga '
    'tekniska termer (som "DNS", "SSL", "PHP") behalls pa engelska aven i den svenska '
    'oversattningen. Som webbhotellagare bor du kunna hjalpa kunderna baade pa svenska '
    'och engelska eftersom bada spraken kan forekomma i granssnittet.'
))

story.append(H2('Contact Information'))
story.append(P(
    'Contact Information latar kunden stalla in sin e-postadress och telefonnummer for att '
    'ta emot viktiga meddelanden fran systemet. Dessa kontaktuppgifter anvands for att skicka '
    'aviseringar om losenordsaterstallning, diskgranser som nars, SSL-certifikat som gar ut '
    'och andra viktiga händelser. Det ar kritiskt att e-postadressen ar korrekt och aktuell - '
    'om kunden inte far dessa aviseringar kan de missa viktig information som att deras hemsida '
    'snart slutar fungera. Uppmundra kunderna att aven ange ett telefonnummer for akuta '
    'situationer dar e-post inte ar tillrackligt snabbt.'
))

story.append(H2('User Manager'))
story.append(P(
    'User Manager ger en oversikt over alla underkonton som ar kopplade till cPanel-kontot: '
    'e-postkonton, FTP-konton och Web Disk-konton. Du kan se en lista over alla anvandare med '
    'deras typ, anvandarnamn och om de ar aktiva eller avstangda. Fran User Manager kan du '
    'snabbt andra losenord, avaktivera eller radera underkonton. Detta ar ett bekvamt satt att '
    'hantera alla anvandare fran en och samma plats istallet for att ga till separata sektioner '
    'for e-post, FTP och Web Disk. For restauranger med manga anstallda som behovjer egna '
    'e-postkonton ar User Manager ett praktiskt verktyg for att halla koll pa vem som har '
    'atkomst till vad.'
))

story.append(H2('Account Preferences'))
story.append(P(
    'Account Preferences latar kunden andra grundlaggande kontoinstallningar som visnings-'
    'installningar for cPanel-granssnittet. Har kan kunden valja om de vill se de grundlaggande '
    'sektionerna eller dölja dem, andra hur manga ikoner som visas per rad, och valja om '
    'snabblankarna ska visas. Dessa installningar ar kosmetiska och paverkar inte kontots '
    'funktionalitet. For nya kunder bor du lamma standardinstallningarna och lata kunden '
    'sjalv andra dem om de onskar en annan layout.'
))

story.append(H2('Manage Team (i Preferences)'))
story.append(P(
    'Manage Team i Preferences-sektionen ar samma funktion som snabblanken i toppen. Den latar '
    'kunden skapa virtuella cPanel-konton for teammedlemmar med begransad atkomst. Du kan ge '
    'en teammedlem atkomst till specifika funktioner (t.ex. bara e-posthantering eller bara '
    'filhantering) utan att ge dem full atkomst till hela cPanel-kontot. Varje teammedlem far '
    'en egen inloggning och kan bara se de sektioner och funktioner som du har beviljat dem. '
    'Detta ar anvandbart for restauranger dar flera personer behovjar atkomst till cPanel men '
    'med olika behorighetsnivaer - till exempel kan restaurangagaren ha full atkomst medan en '
    'anstalld bara kan hantera e-post och bilder.'
))


# ════════════════════════════════════════════════════════════
# SIDOPANEL OCH KONTOINFORMATION
# ════════════════════════════════════════════════════════════
story.append(H1('Sidopanel och kontoinformation'))

story.append(P(
    'Till hoger i cPanel finns en sidopanel med viktig kontoinformation och statistik. Denna '
    'panel ger en snabb oversikt over kontots status och resursanvandning. Har ar de viktigaste '
    'elementen:'
))

story.append(H2('Allman information'))
story.append(T(
    ['Falt', 'Forklaring'],
    [
        ['Current User', 'Kontots anvandarnamn (t.ex. restaurang)'],
        ['Primary Domain', 'Huvuddomanen med SSL-statusknapp'],
        ['IP Address', 'Delad eller dedikerad IP-adress'],
        ['Home Directory', 'Sokvag till kontots hemkatalog'],
        ['Last Login IP', 'IP-adress fran senaste inloggningen'],
        ['Theme', 'Aktuellt tema (Jupiter)'],
        ['Server Information', 'Lank till detaljerad serverinfo'],
    ],
    [110, 340]
))

story.append(H2('Statistikpanel'))
story.append(P(
    'Statistikpanelen visar kontots resursanvandning i realtid. De viktigaste vardeena ar: '
    'Bandwidth (dataoverforing denna manad), Disk Usage (diskutrymme anvant), File Usage '
    '(antal filer/inoder), Email Accounts (antal e-postkonton), MySQL Databases (antal '
    'databaser), och CPU/Memory/Entry Processes (CloudLinux-resursgranser). Om nagot varde '
    'nar sin grans markeras det i rodt for att du snabbt ska kunna identifiera problem. '
    'Overvaka sarskilt CPU-anvandningen - om kundens WordPress-sajt ofta nar CPU-gransen '
    'bor du undersoka orsaken (vanligtvis ett resurskravande tillagg eller mangder av '
    'bot-trafik).'
))

story.append(H2('NGINX Caching'))
story.append(P(
    'Om ChemiCloud anvander NGINX som reverse proxy (vilket ar vanligt for battré prestanda) '
    'visar sidopanelen en NGINX Caching-statusknapp. Du kan se om cachen ar aktiv eller '
    'inaktiv och klicka pa "Clear Cache" for att tomma cachen. Detta ar anvandbart nar du '
    'gor andringar pa en hemsida och andringarna inte syns direkt - det kan bero pa att '
    'NGINX serverar en cachad version av sidan. Genom att rensa cachen tvingar du NGINX att '
    'hamta den senaste versionen fran Apache/PHP. For restauranger som uppdaterar sin meny '
    'eller sina oppettider regelbundet ar det bra att veta om denna funktion.'
))


# ════════════════════════════════════════════════════════════
# SAMMANFATTNING
# ════════════════════════════════════════════════════════════
story.append(H1('Sammanfattning - vilka funktioner du faktiskt anvander'))

story.append(P(
    'cPanel har over 105 funktioner men du kommer att anvanda manga av dem sallan eller aldrig. '
    'Har ar en sammanfattning av de funktioner som ar mest relevanta for din restaurang-webbhotell-'
    'verksamhet, uppdelad i tre nivaer: dagligen, ibland och sallan.'
))

story.append(T(
    ['Niva', 'Funktion', 'Anvandning'],
    [
        ['Dagligen', 'Email Accounts', 'Skapa/hantera e-post for kunder'],
        ['Dagligen', 'WP Toolkit / Softaculous', 'Installera/hantera WordPress'],
        ['Dagligen', 'File Manager', 'Ladda upp/editera filer'],
        ['Dagligen', 'Spam Filters', 'Hantera spam-instollningar'],
        ['Ibland', 'SSL/TLS Status', 'Kontrollera certifikat'],
        ['Ibland', 'Zone Editor', 'Andra DNS-poster'],
        ['Ibland', 'Backup / File Restoration', 'Aterstalla filer/backup'],
        ['Ibland', 'MultiPHP Manager', 'Byta PHP-version'],
        ['Ibland', 'Email Deliverability', 'Fixa SPF/DKIM/DMARC'],
        ['Ibland', 'Forwarders', 'Stall in vidarebefordring'],
        ['Ibland', 'Autoresponders', 'Stall in autosvar'],
        ['Ibland', 'Redirects', 'Omdirigera URL:er'],
        ['Ibland', 'IP Blocker', 'Blockera skadliga IP'],
        ['Sallan', 'MySQL Databases', 'Hantera databaser manuellt'],
        ['Sallan', 'phpMyAdmin', 'Avancerad databasredigering'],
        ['Sallan', 'Cron Jobs', 'Schemalagga uppgifter'],
        ['Sallan', 'Error Pages', 'Anpassa felsidor'],
        ['Sallan', 'Directory Privacy', 'Losenordsskydda mappar'],
        ['Sallan', 'Terminal', 'Kommandoradsaccess'],
        ['Sallan', 'Virus Scanner', 'Skanera efter malware'],
        ['Aldrig', 'BoxTrapper', 'For aggressivt for restauranger'],
        ['Aldrig', 'Anonymous FTP', 'Sakerhetsrisk utan nytta'],
        ['Aldrig', 'Perl/Ruby/Gem-moduler', 'Ej relevant for WordPress'],
        ['Aldrig', 'API Shell', 'Endast for utvecklare'],
        ['Aldrig', 'Gitweb', 'Ej relevant for restauranger'],
    ],
    [55, 140, 255]
))

story.append(Spacer(1, 12))
story.append(P(
    'Kom ihag: Du behover inte kunna alla 105 funktioner utantill. De 12-15 funktionerna i '
    '"Dagligen" och "Ibland"-kolumnerna tacker 95% av allt du gor. De ovriga funktionerna '
    'lär du dig allteftersom behov uppstar. ChemiClouds support ar alltid tillganglig '
    'for hjalp med de mer avancerade funktionerna.'
))


# ── BUILD ──────────────────────────────────────────────────
doc.multiBuild(story)
print(f'Body PDF generated: {OUTPUT}')
