#!/usr/bin/env python3
"""WHM Komplett Handbok - PDF Generation Part 1 (Sections 1-7)"""

import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch, cm
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.lib import colors
from reportlab.platypus import (
    Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, CondPageBreak
)
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.platypus import SimpleDocTemplate
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import registerFontFamily
import hashlib

# ── Font Setup ──
pdfmetrics.registerFont(TTFont('LibSerif', '/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf'))
pdfmetrics.registerFont(TTFont('LibSerifBold', '/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf'))
pdfmetrics.registerFont(TTFont('NotoSC', '/usr/share/fonts/truetype/noto-serif-sc/NotoSerifSC-Regular.ttf'))
pdfmetrics.registerFont(TTFont('NotoSCBold', '/usr/share/fonts/truetype/noto-serif-sc/NotoSerifSC-Bold.ttf'))
pdfmetrics.registerFont(TTFont('DejaVuSans', '/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf'))
registerFontFamily('LibSerif', normal='LibSerif', bold='LibSerifBold')
registerFontFamily('NotoSC', normal='NotoSC', bold='NotoSCBold')

# ── Palette ──
ACCENT = colors.HexColor('#5532be')
TEXT_PRIMARY = colors.HexColor('#1e1d1b')
TEXT_MUTED = colors.HexColor('#908c84')
BG_SURFACE = colors.HexColor('#e9e5df')
BG_PAGE = colors.HexColor('#f1efec')

# ── Page Setup ──
PAGE_W, PAGE_H = A4
L_MARGIN = 1.0 * inch
R_MARGIN = 1.0 * inch
T_MARGIN = 0.8 * inch
B_MARGIN = 0.8 * inch
CONTENT_W = PAGE_W - L_MARGIN - R_MARGIN

# ── Styles ──
styles = {}
styles['body'] = ParagraphStyle('Body', fontName='LibSerif', fontSize=10.5, leading=16, alignment=TA_JUSTIFY, spaceAfter=6)
styles['h1'] = ParagraphStyle('H1', fontName='LibSerif', fontSize=20, leading=26, alignment=TA_LEFT, textColor=ACCENT, spaceBefore=18, spaceAfter=10)
styles['h2'] = ParagraphStyle('H2', fontName='LibSerif', fontSize=15, leading=20, alignment=TA_LEFT, textColor=TEXT_PRIMARY, spaceBefore=14, spaceAfter=8)
styles['h3'] = ParagraphStyle('H3', fontName='LibSerif', fontSize=12, leading=16, alignment=TA_LEFT, textColor=TEXT_PRIMARY, spaceBefore=10, spaceAfter=6)
styles['th'] = ParagraphStyle('TH', fontName='LibSerif', fontSize=9.5, leading=13, alignment=TA_CENTER, textColor=colors.white)
styles['td'] = ParagraphStyle('TD', fontName='LibSerif', fontSize=9, leading=12.5, alignment=TA_LEFT, wordWrap='CJK')
styles['tdc'] = ParagraphStyle('TDC', fontName='LibSerif', fontSize=9, leading=12.5, alignment=TA_CENTER)
styles['note'] = ParagraphStyle('Note', fontName='LibSerif', fontSize=9.5, leading=14, alignment=TA_LEFT, textColor=TEXT_MUTED, leftIndent=12, borderPadding=6)
styles['toc_h1'] = ParagraphStyle('TOCH1', fontName='LibSerif', fontSize=13, leftIndent=20, leading=22)
styles['toc_h2'] = ParagraphStyle('TOCH2', fontName='LibSerif', fontSize=11, leftIndent=40, leading=18)
styles['glossary'] = ParagraphStyle('Gloss', fontName='LibSerif', fontSize=10, leading=15, alignment=TA_LEFT, spaceAfter=4)

# ── TOC Template ──
class TocDocTemplate(SimpleDocTemplate):
    def afterFlowable(self, flowable):
        if hasattr(flowable, 'bookmark_name'):
            level = getattr(flowable, 'bookmark_level', 0)
            text = getattr(flowable, 'bookmark_text', '')
            key = getattr(flowable, 'bookmark_key', '')
            self.notify('TOCEntry', (level, text, self.page, key))

# ── Helpers ──
MAX_KEEP = PAGE_H * 0.4

def safe_keep(elements):
    total = sum((el.wrap(CONTENT_W, PAGE_H)[1]) for el in elements)
    if total <= MAX_KEEP:
        return [KeepTogether(elements)]
    elif len(elements) >= 2:
        return [KeepTogether(elements[:2])] + list(elements[2:])
    return list(elements)

def heading(text, style_key='h1', level=0):
    key = 'h_%s' % hashlib.md5(text.encode()).hexdigest()[:8]
    p = Paragraph('<a name="%s"/><b>%s</b>' % (key, text), styles[style_key])
    p.bookmark_name = text
    p.bookmark_level = level
    p.bookmark_text = text
    p.bookmark_key = key
    return p

def body(text):
    return Paragraph(text, styles['body'])

def note(text):
    return Paragraph('<i>%s</i>' % text, styles['note'])

def sp(h=6):
    return Spacer(1, h)

def make_table(headers, rows, col_ratios=None):
    n = len(headers)
    if col_ratios is None:
        col_ratios = [1.0/n] * n
    col_w = [r * CONTENT_W for r in col_ratios]
    data = [[Paragraph('<b>%s</b>' % h, styles['th']) for h in headers]]
    for row in rows:
        data.append([Paragraph(str(c), styles['td']) for c in row])
    t = Table(data, colWidths=col_w, hAlign='CENTER', repeatRows=1)
    style_cmds = [
        ('BACKGROUND', (0,0), (-1,0), ACCENT),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('GRID', (0,0), (-1,-1), 0.5, TEXT_MUTED),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]
    for i in range(1, len(data)):
        bg = colors.white if i % 2 == 1 else BG_SURFACE
        style_cmds.append(('BACKGROUND', (0,i), (-1,i), bg))
    t.setStyle(TableStyle(style_cmds))
    return t

# ── BUILD STORY ──
story = []

# ── SECTION 1: Introduktion ──
story.append(heading('1. Introduktion till WHM', 'h1', 0))
story.append(body(
    'WHM (Web Host Manager) ar din admin-panel som reseller. Det ar den plats dar du hanterar alla dina kunders cPanel-konton, '
    'staller in paket, overvakar servern och konfigurerar domaner, e-post och sakerhet. Dina restaurangkunder ser aldrig WHM '
    '— de loggar in i sitt eget cPanel-konto. WHM ar alltsa DIN arbetsyta, medan cPanel ar kundens arbetsyta.'
))
story.append(body(
    'Nar du loggar in i WHM ser du en dashboard med systemstatus (CPU, RAM, disk), senaste aktivitet, och ett sokfalt hogst upp. '
    'Sokfaltet ar det snabbaste sattet att hitta funktioner — skriv "create account" eller "spam" och WHM visar relevanta verktyg direkt. '
    'I vanster sidomeny ser du alla sektioner grupperade efter kategori, och i huvudomradet visas de enskilda funktionerna.'
))
story.append(body(
    'Det finns over 170 funktioner i WHM, men som reseller for restauranghemsidor behover du bara beharska ett tiotal av dem regelbundet. '
    'De flesta funktioner hanteras automatiskt av ChemiCloud (uppdateringar, sakerhetspatchar, serverovervakning). '
    'Denna handbok gar igenom ALLA funktioner sa att du forstar vad varje installning gor, aven de du sallan anvander.'
))

# ── SECTION 2: Account Functions ──
story.append(heading('2. Account Functions (Kontofunktioner)', 'h1', 0))
story.append(body(
    'Account Functions ar den viktigaste sektionen i WHM. Har skapar du nya kundkonton, hanterar befintliga, '
    'suspenderar ej betalande kunder och installer losenord. Nedan foljer en detaljerad genomgang av varje funktion.'
))

acct_funcs = [
    ('Create a New Account', 'Skapa ett nytt cPanel-konto for en restaurangkund. Detta ar den funktion du anvander mest. Se separat djupgenomgang i sektion 3.', 'Varje gang du far en ny kund'),
    ('List Accounts', 'Visa alla dina kunders cPanel-konton pa en skarm. Klicka pa ett konto for att logga in i deras cPanel direkt, se disk- och bandbreddsanvandning, och snabbt navigera till kontots installningar.', 'Daglig oversikt, felsokning'),
    ('Modify an Account', 'Andra installningar for ett befintligt konto: domannamn, paket, kontakt-e-post, cPanel-tema och sprak. Du kan inte andra losenord har — anvand Password Modification istallet.', 'Nar kunden vill uppgradera eller andra doman'),
    ('Manage Account Suspension', 'Suspendera (stang av) eller ateruppta ett konto. En suspenderad kund ser en "Account Suspended"-sida. Du kan aven lagga till en anledning som visas for kunden.', 'Nar kunden inte betalar'),
    ('Unsuspend Bandwidth Exceeders', 'Ateraktivera alla konton som automatiskt suspenderats for att de overskridit sin bandbreddsgrans. Detta gor att alla sadana konton far tillgang igen pa en gang.', 'Mataradsavlasning i slutet av manaden'),
    ('Terminate Accounts', 'Radera ett eller flera konton permanent. All data raderas oaterkalleligen — filer, databaser, e-post, allt. Det finns ingen aggondknapp!', 'Nar kunden lamnar for gott'),
    ('Upgrade/Downgrade an Account', 'Byt paket for en kund (t.ex. fran "Restaurang Basic" till "Restaurang Pro"). Kontoets resurser andras omedelbart till det nya paketets granser.', 'Nar kunden vill ha mer/mindre resurser'),
    ('Password Modification', 'Andra losenord for ett cPanel-konto eller for reseller-konton. Du kan aven tvinga kunden att byta losenord vid nasta inloggning.', 'Nar kunden glomt sitt losenord'),
    ('Quota Modification', 'Andra diskkvoten for ett enskilt konto utan att byta hela paketet. Anvandbart om en kund tillfalligt behover mer utrymme.', 'Tillfallig utrymmesokning'),
    ('Limit Bandwidth Usage', 'Andra den manatliga bandbreddsgransen for ett enskilt konto. Precis som Quota Modification, detta andrar bara for detta konto — inte paketet.', 'Nar en kund behover mer/mindre bandbredd'),
    ('Force Password Change', 'Tvinga en eller flera anvandare att byta losenord vid nasta inloggning. Bra sakerhetsatgard om du misstanker att ett losenord har komprometterats.', 'Sakerhetsincident'),
    ('Change Site\'s IP Address', 'Andra vilken IP-adress ett konto anvander. Detta ar sallsan anvant och bor endast goras om du vet exakt vad du gor — fel IP kan gora sajten onadig.', 'Avancerat — sallsan behov'),
    ('Email All Users', 'Skicka ett e-postmeddelande till alla cPanel-anvandare pa servern samtidigt. Anvandbart for att meddela om planerat underhall eller viktiga andringar.', 'Underhallsmeddelanden'),
    ('Manage Demo Mode', 'Konvertera ett cPanel-konto till ett demokonto. I demolage kan anvandaren se men inte andra nagon installning. Perfekt for att visa cPanel for potentiella kunder.', 'For presentationer'),
    ('Manage Shell Access', 'Hantera vilka konton som far shell/SSH-tillgang. Du kan valja mellandisabled, jailshell (begransad) eller normal shell. Rekommendera jailshell om shell behovers.', 'Nar en utvecklare ber om SSH-tillgang'),
    ('Raw Apache Log Download', 'Ladda ner Apaches raa access-logg for ett konto. Dessa loggar visar varje HTTP-forfragan till sajten i radataformat.', 'Avancerad trafikanalys'),
    ('Raw FTP Log Download', 'Ladda ner FTP-serverns raa logg for ett konto. Visar alla FTP-uppkopplingar och filoverforingar.', 'FTP-felsokning'),
    ('Raw NGINX Log Download', 'Ladda ner NGINX raa logg. ChemiCloud anvander LiteSpeed/NGINX som webbserver, sa dessa loggar kan vara relevanta.', 'Avancerad felsokning'),
    ('Rearrange an Account', 'Flytta ett konto till en annan hemkatalog pa servern. Detta andrar vilken disk kontoets filer lagras pa.', 'Sallsan — servermigration'),
    ('Reset Account Bandwidth Limit', 'Aterstall bandbreddsgransen till vad som anges i kontoets paket. Om du har andrat bandbredden manuellt, aterstaller denna funktion den till paketets standard.', 'Efter manuell bandbreddsandring'),
    ('Skeleton Directory', 'Visa soken till kontots "skeleton directory" — en mallkatalog vars innehall automatiskt kopieras till varje nytt konto. Du kan lagga standardfiler har.', 'Engangsinstallning — anpassa nya konton'),
]

story.append(make_table(
    ['Funktion', 'Beskrivning', 'Nar du behover den'],
    acct_funcs,
    [0.22, 0.55, 0.23]
))
story.append(sp(12))

# ── SECTION 3: Create a New Account - Deep Dive ──
story.append(heading('3. Create a New Account — Detaljerad genomgang', 'h1', 0))
story.append(body(
    'Detta ar den viktigaste funktionen i WHM. Varje gang du far en ny restaurangkund ska du anvanda denna funktion '
    'for att skapa deras cPanel-konto. Har gar jag igenom VARJE falt och VARJE installning i formularet, sa att du forstar '
    'exakt vad varje installning gor och vad du bor valja.'
))

# Domain Information
story.append(heading('3.1 Domain Information (Domaninformation)', 'h2', 1))
domain_info = [
    ('Domain', 'Textfalt + radio', 'Falt for domannamnet (t.ex. restaurang.se). Du kan aven valja "Choose a domain later" vilket ger ett tillfalligt namn pa .cpanel.site. I praktiken skriver du alltid in domannamnet direkt — du vill ju att kundens hemsida ska fungera direkt.'),
    ('Username', 'Textfalt', 'Max 16 tecken, endast gemener och siffror, kan inte borja med siffra eller "test". Detta blir aven kontoets huvudanvandare och namnet pa hemkatalogen (t.ex. /home/restaur1/). Kort och beskrivande ar bast.'),
    ('Password', 'Textfalt + generator', 'Losnord for kontot. Anvand Password Generator for att skapa ett starkt losenord (minst 16 tecken, blandade teckenslag). Skriv ALDRIG ett svagt losenord.'),
    ('Re-type Password', 'Textfalt', 'Bekrafta losenordet. Maste matcha faltet ovan.'),
    ('Strength', 'Matar', 'Visar losenordsstyrkan pa en skala 0-100. Gron = acceptabel styrka. Om losenordet inte nar den kravda styrkan kan du inte skapa kontot.'),
    ('Email', 'Textfalt', 'Kundens kontakt-e-postadress. Hit skickas aviseringar om diskkvot, bandbredd och servermeddelanden. Anvand kundens riktiga e-post, inte din egen.'),
]
story.append(make_table(['Falt', 'Typ', 'Forklaring'], domain_info, [0.15, 0.15, 0.70]))
story.append(sp(10))

# Package Section
story.append(heading('3.2 Package (Paketval)', 'h2', 1))
story.append(body(
    'Har valjer du vilket resurspaket som ska tilldelas det nya kontot. Ett paket bestammer hur mycket diskutrymme, '
    'bandbredd, e-postkonton, databaser osv. kunden far. Du kan antingen valja ett befintligt paket fran en dropdown '
    'eller klicka i "Select package options manually" for att stalla in alla resurser manuellt for just detta konto.'
))
story.append(body(
    'Om du valjer manuella installningar kan du aven kryssa i "Save Manual Settings as a Package" for att spara dem som '
    'ett nytt paket som du sedan kan anvanda for framtida konton. Detta ar praktiskt om du vill skapa ett paket anpassat '
    'for en specifik kundkategori.'
))
story.append(sp(6))

# Manual Resource Options
story.append(heading('3.3 Manual Resource Options (Resursinstallningar)', 'h2', 1))
story.append(body(
    'Dessa falt visas nar du klickar i "Select package options manually". Samma falt finns aven i Add a Package. '
    'Har gar jag igenom varje resurs och forklarar vad det betyder i praktiken for din restaurangkund.'
))

resource_opts = [
    ('Disk Space Quota (MB)', 'Max diskutrymme for kontoets filer, e-post, databaser och loggar. 1 GB = 1024 MB. For en restaurang med WordPress och nagra bilder racker 5 GB (5120 MB) gott. Stall till "Unlimited" endast om du litar pa kunden.', '5 GB (5120 MB) for Basic'),
    ('Monthly Bandwidth Limit (MB)', 'Max datamangd som far overforas per manad. Varje gang nagon besoker hemsidan, laddar ner en PDF eller skickar e-post forbrukas bandbredd. En restauranghemsida anvander typiskt 5-20 GB/manad.', '50 GB (51200 MB) for Basic'),
    ('Max FTP Accounts', 'Max antal FTP-anvandare. FTP anvands for att ladda upp filer till servern. Varje FTP-konto far atkomst till en specifik mapp. Du behover oftast bara 1-5 FTP-konton.', '5 for Basic'),
    ('Max Email Accounts', 'Max antal e-postkonton (t.ex. info@, bokning@, catering@). Restauranger behover oftast 5-10 e-postadresser.', '5 for Basic, 50 for Pro'),
    ('Max Quota per Email Address (MB)', 'Max storlek per enskild e-postkontos postlada. Standard ar "Unlimited". Om en kund far mycket e-post med stora bilagor kan du satta en grans for att forhindra att en postlada tar allt diskutrymme.', 'Unlimited, eller 500 MB'),
    ('Max Mailing Lists', 'Max antal Mailman-sandlistor (for nyhetsbrev). En sandlista later kunden skicka ett meddelande till manga mottagare samtidigt. De flesta restauranger anvander externa tjanker som Mailchimp istallet.', '1-5'),
    ('Max SQL Databases', 'Max antal MySQL-databaser. WordPress behover EN databas. Varje ytterligare webbapplikation (webbshop, bokningssystem) behover sin egen. Obsera: MySQL och PostgreSQL raknas separat.', '1 for Basic, 5 for Pro'),
    ('Max Sub Domains', 'Max antal underdomaner (t.ex. meny.restaurang.se, catering.restaurang.se). Varje underdoman pekar till en egen mapp pa servern.', '1-5'),
    ('Max Parked Domains', 'Max antal "parked domains" (alias). En parkerad doman visar samma innehall som huvuddomanen. Anvandbart om kunden ager bade .se och .com och vill att bada ska visa samma sajt.', '0-2'),
    ('Max Addon Domains', 'Max antal "addon domains" — extra domaner som var och en visar en egen hemsida pa samma konto. Detta later en kund ha flera separata sajttyper under ett konto.', '1 for Basic, 5 for Pro'),
    ('Max Passenger Applications', 'Max antal Passenger-appar (for Ruby on Rails, Python, Node.js). De flesta restauranger anvander bara WordPress och behover inte detta.', '0 for restauranger'),
    ('Max Hourly Email by Domain Relayed', 'Max antal e-postmeddelanden som far skickas per timme fran en doman. Detta forhindrar att ett hackat konto skickar spam. 0 = obegransat (ej rekommenderat).', '100-500 per timme'),
    ('Max % Failed/Deferred Messages', 'Max procent misslyckade/forsenade meddelanden per timme innan domanen tillfalligt blockeras fran att skicka. Forsvar mot spam-utskick fran hackade konton.', '50-75%'),
]
story.append(make_table(
    ['Resurs', 'Forklaring', 'Rekommendation'],
    resource_opts,
    [0.20, 0.58, 0.22]
))
story.append(sp(10))

# Settings Section — CRITICAL
story.append(heading('3.4 Settings (Installningar) — Detaljerade forklaringar', 'h2', 1))
story.append(body(
    'Dessa checkboxar och dropdowns ar ofta forvirrande for nyborjare. Har forklarar jag exakt vad varje installning gor, '
    'om du bor aktivera eller avaktivera den, och varfor.'
))

settings_items = [
    ('Dedicated IP', 'Checkbox', 
     'Tilldelar kontot en egen unik IP-adress istallet for att dela med andra konton. '
     'Normalt delar alla konton pa serverns delade IP-adress, vilket fungerar bra for de flesta. '
     'Du behover en dedicated IP endast om: (1) kunden vill ha en egen SSL-certifikat med unik IP (sallan nodvandigt idag med SNI), '
     '(2) kundens e-post skickas fran en IP som inte ar svartlistad pa grund av andra anvandare, '
     '(3) kunden kraver det for tekniska skal. OBS: Kan inte andras efter skapande!',
     'AV (avaktiverad) — de flesta restauranger behover inte detta'),
    ('Shell Access', 'Checkbox',
     'Ger kontoets anvandare tillgang till serverns kommandotolk (terminal) via SSH. '
     'SSH-tillgang ar kraftfullt men innebar sakerhetsrisker — en anvandare med shell-tillgang kan potenstiellt skada servern. '
     'Om du maste ge shell-tillgang, anvand jailshell (begransad miljo dar anvandaren inte kan se andras filer) '
     'istallet for normal shell. De flesta restaurangkunder behover aldrig SSH-tillgang.',
     'AV — ge endast om utvecklaren uttryckligen ber om det, och da med jailshell'),
    ('CGI Access', 'Checkbox',
     'Ger kontoets anvandare ratt att kora CGI-skript (Common Gateway Interface). '
     'CGI ar en gammal teknik fran 1990-talet som later webbservern kora program och returnera resultatet som HTML. '
     'Modern WordPress anvander INTE CGI — den kors via PHP. CGI behoves bara for mycket gamla skript eller specifika '
     'applikationer. Att aktivera CGI innebar en liten sakerhetsrisk eftersom det ger mojlighet att kora godtycklig kod pa servern.',
     'AV — WordPress och moderna webbappar behover inte CGI'),
    ('Digest Authentication for Web Disk', 'Checkbox',
     'Aktiverar digest-autentisering for Web Disk (WebDAV). Web Disk later kunden ansluta serverns filer som en natverksdisk '
     'pa sin dator. Digest-autentisering kravs nar: (1) kunden anvander Windows Vista, 7 eller 8 med sjalvsignerat SSL-certifikat, '
     '(2) vanlig autentisering inte fungerar pa grund av sakerhetsinstallningar i operativsystemet. '
     'For moderna operativsystem (Windows 10/11, macOS) behoves det sallan.',
     'AV — aktivera bara om kunden har problem med Web Disk-inloggning'),
    ('cPanel Theme', 'Dropdown',
     'Valj vilket tema kundens cPanel ska anvanda. ChemiCloud anvander "Jupiter" som standard, vilket ar det senaste och mest '
     'anvandarvanliga temat. Du bor inte andra detta om du inte har en specifik anledning.',
     'Jupiter (standard)'),
    ('Locale', 'Dropdown',
     'Valj sprak for kundens cPanel-granssnitt. Svenska finns som alternativ! For svenska restaurangkunder ar det bra att valja '
     'svenska sa att de forstar allting battre. Du kan aven andra spraket senare inne i cPanel.',
     'Svenska (sv) for svenska kunder'),
    ('Enable Apache SpamAssassin', 'Checkbox',
     'Aktiverar SpamAssassin — en automatiserad spamfilter for inkommande e-post. SpamAssassin analyserar varje inkommande '
     'meddelande och ger det en poang baserat pa hur mycket det liknar spam. Meddelanden med hog poang markeras som spam. '
     'Detta ar GRATIS och ingar i cPanel. Du bor ALLTID aktivera detta for att skydda kundens e-postfran spam.',
     'PA (aktiverad) — alltid! Skyddar mot spam'),
    ('Enable Spam Box', 'Checkbox',
     'Nar SpamAssassin ar aktiverat bestammer "Spam Box" vad som hander med meddelanden som identifieras som spam. '
     'OM AKTIVERAD: Spam levereras till en separat "spam"-mapp i kundens postlada (kan granskas senare). '
     'OM AVAKTIVERAD: Spam-meddelanden raderas direkt (kan inte aterhamtas). '
     'OBS: Spam Box kraver att SpamAssassin ar aktiverat for att fungera. '
     'Rekommendation: AKTIVERA Spam Box sa att kunden kan granska falska positiva (legitima mail som felaktigt markeras som spam) '
     'innan de raderas permanent.',
     'PA (aktiverad) — sa att kunden kan granska spam innan radering'),
]
story.append(make_table(
    ['Installning', 'Typ', 'Forklaring', 'Rekommendation'],
    settings_items,
    [0.12, 0.08, 0.60, 0.20]
))
story.append(sp(10))

# Mail Routing
story.append(heading('3.5 Mail Routing Settings (E-postruttning)', 'h2', 1))
story.append(body(
    'Dessa inställningar bestämmer hur inkommande e-post hanteras för domänen. Detta är särskilt viktigt om restaurangen '
    'använder en extern e-posttjänst som Google Workspace eller Microsoft 365 istället för serverns inbyggda e-post.'
))

mail_routing = [
    ('Automatically Detect Configuration', 'Rekommenderat val. WHM känner automatiskt av om e-post ska hanteras lokalt eller externt baserat pa DNS-records. I de flesta fall fungerar detta perfekt.', 'Anvand alltid detta som standard'),
    ('Local Mail Exchanger', 'All e-post for domanen mottas och lagras pa DIN server. Detta ar standard nar kunden anvander cPanel for e-post (info@restaurang.se hanteras av din server).', 'Nar e-post hanteras i cPanel'),
    ('Backup Mail Exchanger', 'Din server fungerar som backup for en annan e-postserver. Om den primara e-postservern ar nere tar din server emot och sparar meddelandena tills primarservern ar tillbaka.', 'Sallsan — avancerad konfiguration'),
    ('Remote Mail Exchanger', 'E-post hanteras av en EXTERN server (t.ex. Google Workspace, Microsoft 365, ProtonMail). Din server tar INTE emot e-post for domanen — den skickas vidare till den externa servern.', 'Nar kunden anvander Google Workspace eller Microsoft 365'),
]
story.append(make_table(['Alternativ', 'Forklaring', 'Anvand nar'], mail_routing, [0.22, 0.55, 0.23]))
story.append(sp(10))

# DNS Settings
story.append(heading('3.6 DNS Settings (DNS-installningar)', 'h2', 1))
dns_settings = [
    ('Enable DKIM', 'Aktiverar DKIM (DomainKeys Identified Mail) for kontoets doman. DKIM lgger till en digital signatur pa utgende e-post sa att mottagaren kan verifiera att meddelandet verkligen kommer fran din server och inte har manipulerats. Detta ar VIKTIGT for att din kunds e-post inte ska hamna i spam-mappar hos Gmail, Outlook osv.', 'PA — alltid aktivera for nya konton'),
    ('Enable SPF', 'Aktiverar SPF (Sender Policy Framework) for domanen. SPF anger vilka e-postservrar som ar tillatna att skicka e-post fran domanen. Utan SPF kan en bedragare skicka e-post som ser ut att komma fran restaurangen. Detta ar VIKTIGT for e-postsakerhet.', 'PA — alltid aktivera for nya konton'),
    ('Enable DMARC', 'Aktiverar DMARC (Domain-based Message Authentication, Reporting and Conformance). DMARC bygger pa SPF och DKIM och anger vad mottagaren ska gora om ett meddelande inte klarar autentiseringen (t.ex. avvisa det eller skicka det till spam). Kraver att bada SPF och DKIM ar aktiverade.', 'PA — aktivera efter att SPF/DKIM fungerar'),
    ('Use nameservers at registrar', 'Ignorerar lokalt angivna namnservrar och anvander de namnservrar som ar angivna hos domanregistratorn istallet. Anvand detta OM kunden vill hantera DNS hos sin registrator (t.ex. HostUp/Inleed) istallet for i WHM.', 'Bara om kunden hanterar DNS externt'),
    ('Overwrite existing DNS zones', 'Skriver over befintliga DNS-zoner for domanen. VARNING: Detta raderar alla befintliga DNS-poster! Anvand BARA om du ar saker pa att du vill ersatta all DNS-konfiguration.', 'Bara vid full omskapande av DNS'),
]
story.append(make_table(['Installning', 'Forklaring', 'Rekommendation'], dns_settings, [0.18, 0.62, 0.20]))
story.append(sp(10))

# Reseller Settings
story.append(heading('3.7 Reseller Settings (Reseller-installningar)', 'h2', 1))
story.append(body(
    'Dessa inställningar visas när du skapar ett konto. De låter dig ge kontoägaren reseller-rättigheter, vilket '
    'innebär att de kan skapa och hantera egna cPanel-konton. För restaurangkunder ska dessa ALLTID vara avaktiverade — '
    'du vill inte att en restaurangägare ska kunna skapa egna webbhotellskonton. "Make the account own itself" innebär '
    'att reseller-kontot kan modifiera sina egna paket och resursgränser, vilket också ska vara avaktiverat för kunder.'
))

# ── SECTION 4: Packages ──
story.append(heading('4. Packages (Paket)', 'h1', 0))
story.append(body(
    'Paket (packages) ar mallar for resurstilldelning. Istallet for att manuellt stalla in diskutrymme, bandbredd och '
    'e-postgranser varje gang du skapar ett konto, skapar du paket en gang och tilldelar dem. Detta sparar tid och ser '
    'till att alla konton med samma paket har identiska resurser. Nar du andrar ett paket andras ALLA konton med det paketet automatiskt.'
))

story.append(heading('4.1 Add a Package — Alla falt', 'h2', 1))
story.append(body(
    'Formularet for att skapa ett paket innehaller samma resursfalte som "Manual Resource Options" i Create a New Account '
    '(se sektion 3.3), plus nagra extra installningar. Har ar de extra falt som inte behandlats tidigare:'
))

pkg_extra = [
    ('Package Name', 'Namnet pa paketet. Detta kan INTE andras senare! Anvand beskrivande namn (t.ex. "Restaurang_Basic") och undvik prisbaserade namn ("Paket_299kr") eftersom priset kan andras men namnet inte kan andras.'),
    ('Feature List', 'Dropdown for att valja vilka cPanel-funktioner som ska vara tillgangliga for konton med detta paket. Du kan skapa egna feature lists via Feature Manager (se 4.4). Standard ar "default" som ger tillgang till allt.'),
]
story.append(make_table(['Falt', 'Forklaring'], pkg_extra, [0.18, 0.82]))

story.append(heading('4.2 Feature Manager', 'h2', 1))
story.append(body(
    'Feature Manager later dig styra exakt vilka funktioner som ska vara synliga i kundens cPanel. Du kan skapa anpassade '
    'feature lists som doltjer avanerade funktioner som kunden inte behover eller bor rora. Detta ar useful for att forenkla '
    'cPanel for restaurangkunder sa att de bara ser vad de faktiskt behover.'
))
story.append(body(
    'Det finns tre fordefinierade feature lists: "default" (alla funktioner synliga), "Mail Only" (endast e-postfunktioner, '
    'for kunder som bara anvander e-post), och "disabled" (markerar funktioner som inte ska vara tillgangliga). '
    'Du kan skapa egna feature lists med checkboxar for varje enskild cPanel-funktion — fran Email Accounts till Terminal.'
))

# ── SECTION 5: DNS Functions ──
story.append(heading('5. DNS Functions (DNS-funktioner)', 'h1', 0))
story.append(body(
    'DNS (Domain Name System) ar internets telefonkatalog — det oversatter domannamn (restaurang.se) till IP-adresser '
    '(192.168.1.1) sa att webblasaren vet var hemsidan finns. Har ar alla 14 DNS-funktioner i WHM.'
))

dns_funcs = [
    ('Add a DNS Zone', 'Skapa en ny DNS-zon for en doman. Detta gor automatiskt nar du skapar ett konto, sa du behover sallan gor detta manuellt.', 'Automatiskt vid kontoskapande'),
    ('Add an A Entry for Your Hostname', 'Lagg till en A-post for serverns hostnamn. Detta bor redan vara konfigurerat av ChemiCloud.', 'Engangsinstallning — ChemiCloud skoter'),
    ('Delete a DNS Zone', 'Radera en DNS-zon. VARNING: Detta tar bort ALLA DNS-poster for domanen och gor den onadig.', 'Nar en doman tas bort permanent'),
    ('DNS Zone Manager', 'Nyare granssnitt for att hantera DNS-zoner. Erbjuder en mer anvandarvanlig vy an Edit a DNS Zone.', 'For att redigera DNS-poster'),
    ('Edit Zone Templates', 'Redigera mallar for nya DNS-zoner. Mallen bestammer vilka DNS-poster som automatiskt skapas for nya domaner.', 'Engangsinstallning — anpassa standard-DNS'),
    ('Email DNS Record Manager', 'Hantera e-postrelaterade DNS-poster (MX, SPF, DKIM, DMARC) for alla domaner pa en gang.', 'For att aktivera SPF/DKIM for alla kunder'),
    ('Email Routing Configuration', 'Konfigurera e-postruttning for alla domaner pa en gang (Local/Remote/Backup Mail Exchanger).', 'Nar manga kunder anvander extern e-post'),
    ('Enable DKIM/SPF Globally', 'Aktivera DKIM och SPF for ALLA domaner pa servern automatiskt. Rekommenderas starkt!', 'Gor direkt vid uppstart'),
    ('Nameserver Record Report', 'Visa en rapport over alla namnserver-poster pa servern. Anvandbart for att verifiera att namnservrarna ar korrekt konfigurerade.', 'Felsokning av DNS-problem'),
    ('Park a Domain', 'Parkera en doman (skapa ett alias som visar samma innehall som en annan doman). Exempel: restaurang.com visar restaurang.se.', 'Nar kunden ager flera domaner'),
    ('Perform a DNS Cleanup', 'Rensa bort gamla, overblivna eller felaktiga DNS-poster fran servern. En god hygienatgard som kan losa mystika DNS-problem.', 'Vid DNS-felsokning'),
    ('Set Zone Time to Live (TTL)', 'Andra TTL-varde for en DNS-zon. TTL bestammer hur lange andra DNS-servrar ska spara dina DNS-poster i cache innan de fragar igen. Laggre TTL = snabbare uppdateringar men mer trafik.', 'Innan stora DNS-andringar'),
    ('Setup/Edit Domain Forwarding', 'Konfigurera domanvidarebefodran (t.ex. restaurang.com skickas vidare till restaurang.se). Detta ar en serverniva-vidarebefodran, inte en HTTP-redirect.', 'Nar en doman ska peka till en annan'),
    ('Synchronize DNS Records', 'Synkronisera DNS-poster mellan servrar i ett DNS-kluster. Anvands for redundans sa att om en server gar ner tar en annan over DNS-hanteringen.', 'Avancerat — for DNS-kluster'),
]
story.append(make_table(['Funktion', 'Forklaring', 'Nar du behover den'], dns_funcs, [0.22, 0.55, 0.23]))
story.append(sp(8))

# Common DNS records
story.append(heading('5.1 Vanliga DNS-posttyper', 'h2', 1))
dns_types = [
    ('A', 'IPv4-adress', 'Kopplar domannamn till en IPv4-adress (t.ex. restaurang.se -> 192.168.1.1). Den vanligaste posttypen.'),
    ('AAAA', 'IPv6-adress', 'Kopplar domannamn till en IPv6-adress. Framtidens standard, men de flesta anvander fortfarande A-poster.'),
    ('CNAME', 'Alias', 'Skapar ett alias som pekar pa ett annat domannamn (t.ex. www.restaurang.se -> restaurang.se).'),
    ('MX', 'Mail Exchanger', 'Anger vilken server som hanterar inkommande e-post for domanen (t.ex. mail.restaurang.se).'),
    ('TXT', 'Text', 'Innehaller textinformation, oftast for SPF, DKIM och DMARC-verifiering. Aven anvant for Google-verifiering.'),
    ('NS', 'Name Server', 'Anger vilka namnservrar som ar auktoritativa for domanen (t.ex. ns1.chemicloud.com, ns2.chemicloud.com).'),
    ('SRV', 'Service', 'Anger platsen for en specifik tjhst (t.ex. _sip._tcp.restaurang.se). Anvands sallsan av restauranger.'),
]
story.append(make_table(['Typ', 'Namn', 'Forklaring'], dns_types, [0.08, 0.15, 0.77]))

# ── SECTION 6: Email Functions ──
story.append(heading('6. Email Functions (E-postfunktioner)', 'h1', 0))
email_funcs = [
    ('Email Deliverability', 'Kontrollera och fixa e-postleveransproblem for specifika domaner. Visar om SPF, DKIM och PTR-poster ar korrekta. Detta ar det FORSTA verktyget du ska anvanda nar en kund sier att deras mail hamnar i spam.', 'Nar kundens mail hamnar i spam'),
    ('Filter Incoming Emails by Country', 'Blockera eller tillata e-post fran specifika lander. Exempel: blockera all e-post fran lander dar du aldrig far legitim e-post ifran. Kan reducera spam markant.', 'For aggressiv spamreducering'),
    ('Filter Incoming Emails by Domain', 'Blockera eller tillata e-post fran specifika domaner. Exempel: blockera allt fran @spamdomain.com.', 'Nar specifika domaner skickar spam'),
    ('Greylisting', 'Aktivera/inaktivera greylisting for hela servern. Greylisting avvisar tillfalligt den forsta leveransforsoket fran en okand avsandare — legitim e-postservers forsoker igen efter en stund, men spam-servers ger ofta upp. Detta ar en effektiv anti-spam-atgard.', 'Aktivera som standard — kan orsaka kort forsojning av legitim e-post'),
    ('Mail Delivery Reports', 'Visa detaljerade rapporter om e-postleverans for hela servern. Du kan se vilka meddelanden som levererades, avvisades eller forsenades, och varfor. Ovaerderligt for felsokning.', 'Nar e-post inte kommer fram'),
    ('Mail Queue Manager', 'Se och hantera e-post som fastnat i ko (vantar pa att skickas). Du kan visa, radera, eller forcera ett nytt leveransforsok for enskilda meddelanden.', 'Nar e-post fastnar i ko'),
    ('Mail Troubleshooter', 'Felsok e-postproblem for en specifik adress. Skriv in avsandare och mottagare sa visar verktyget exakt vad som hande med meddelandet — om det levererades, avvisades eller forsenades.', 'For att spara upp varfor ett specifikt mail inte kom fram'),
    ('Mailbox Conversion', 'Konvertera postlador mellan format: mdbox (efficient, alla meddelanden i en fil) och maildir (ett meddelande per fil). ChemiCloud anvander normalt mdbox som ar snabbare och mer platsbesparande.', 'Sallsan — vid migration eller formatproblem'),
    ('Repair Mailbox Permissions', 'Reparera filrattigheter for en postlada. Om en kund inte kan logga in i sin e-post eller saknar meddelanden kan det bero pa felaktiga filrattigheter.', 'Nar e-postinte fungerar efter migration'),
    ('Spamd Startup Configuration', 'Konfigurera hur SpamAssassin-demonen (spamd) startar. Du kan aktivera/avaktivera spamd och stalla in minnesgranser. Normalt behover du inte andra har.', 'Avancerat — sallsan behov'),
    ('View Mail Statistics Summary', 'Visa statistik over e-posttrafik: hur manga meddelanden som skickats, tagits emot, avvisats och markerats som spam. Bra oversikt over serverns e-postshalsa.', 'Manatlig oversikt'),
    ('View Relayers', 'Visa vilka anvandare som har skickat e-post via din server (relayerat). Detta ar viktigt for att upptacka missbruk — om ett konto skickar ovanligt mycket e-post kan det vara hackat.', 'Sakerhetskontroll'),
    ('View Sent Summary', 'Visa en sammanfattning av all utgende e-post fran servern. Du kan se vilka konton som skickar mest e-post och till vilka mottagare.', 'Identifiera potentiella spam-konton'),
]
story.append(make_table(['Funktion', 'Forklaring', 'Nar du behover den'], email_funcs, [0.18, 0.58, 0.24]))

# ── SECTION 7: Security Center ──
story.append(heading('7. Security Center (Sakerhetscenter)', 'h1', 0))
story.append(body(
    'Sakerhetscenter innehaller 20 funktioner for att skydda din server och dina kunders konton. '
    'Manga av dessa hanteras automatiskt av ChemiCloud, men det ar viktigt att du forstar vad de gor sa att du kan '
    'gor medvetna val nar problem uppstar.'
))

sec_funcs = [
    ('Apache mod_userdir Tweak', 'Forhindra att anvandare kan komma at sin hemsida via ~anvandarnamn (t.ex. server.com/~restaur1). Detta ar en sakerhetsatgard som forhindrar informationlackage om anvandarnamn och kontostruktur.', 'Aktivera — forhindrar informationlackage'),
    ('Compiler Access', 'Stall in vilka anvandare som far kompilera program pa servern. Normalt ska bara root ha denna rattighet. Om du ger kompilatorstillgang till vanliga anvandare kan de potentiellt skapa och kora skadlig kod.', 'Inaktivera for alla utom root'),
    ('Configure Security Policies', 'Konfigurera sakerhetspolicys for WHM-inloggning: krav pa sakerhetsfragor, begransade IP-adresser och tidsbegransningar for root-inloggning.', 'Aktivera sakerhetsfragor for root'),
    ('cPHulk Brute Force Protection', 'Skydd mot brute-force-attacker (upprepade felaktiga inloggningsforsok). cPHulk blockerar automatiskt IP-adresser som misslyckas med inloggning for manga ganger. Hanteras automatiskt men du kan se loggar och vitlista IP-adresser.', 'Automatiskt — vitlista din egen IP om du blir blockad'),
    ('Host Access Control', 'Konfigurera TCP-wrappers for att tillata eller neka atkomst fran specifika IP-adresser eller natverk till specifika tjhster (SSH, FTP, SMTP osv.). Mer granulart an en brandvagg.', 'Avancerat — specifika IP-blockeringar'),
    ('Manage External Authentications', 'Hantera externa autentiseringstjhster (t.ex. Google, GitHub) for cPanel-inloggning. Later anvandare logga in med sitt Google-konto istallet for losenord.', 'Valfritt — extra bekvamlighet'),
    ('Manage root\'s SSH Keys', 'Skapa, importera och hantera SSH-nycklar for root-anvandaren. SSH-nycklar ar sakerre an losenord och rekommenderas for all SSH-atkomst.', 'Skapa en SSH-nyckel for root-inloggning'),
    ('Manage Sudo Group Users', 'Hantera vilka anvandare som ar i sudo-gruppen (kan kora kommandon som root med sudo). Begransa detta till bara de anvandare som verkligen behover det.', 'Bara root och trusted anvandare'),
    ('Manage Wheel Group Users', 'Hantera vilka anvandare som ar i wheel-gruppen (kan byta till root med su). Liknar sudo men ar en annan metod. Wheel-gruppen ar den traditionella UNIX-metoden.', 'Bara root och trusted anvandare'),
    ('ModSecurity Configuration', 'Globala installningar for ModSecurity WAF (Web Application Firewall). ModSecurity skyddar mot vanliga webbattacker som SQL injection, XSS och filinklusion. Du kan aktivera/avaktivera WAF globalt och valja regeluppsattning.', 'Aktivera — gor att OWASP-regler som standard'),
    ('ModSecurity Tools', 'Hantera ModSecurity-regler: visa loggar, avaktivera specifika regler som krockar med kundens webbplats, skapa egna regler. Om en kunds WordPress-plugin kraschar pga. en WAF-regel kan du avaktivera just den regeln.', 'Nar WAF blockerar legitim trafik'),
    ('ModSecurity Vendors', 'Hantera ModSecurity-leverantorer och deras regeluppsattningar. ChemiCloud inkluderar OWASP-regler. Du kan aven lagga till andra leverantorer som Comodo eller Atomic.', 'Installera OWASP-regler om inte redan installerade'),
    ('Password Strength Configuration', 'Krav pa losenordsstyrka for olika delar av systemet: cPanel, WHM, FTP, e-post, Web Disk, MySQL osv. Stall in minimikrav for att tvinga starka losenord.', 'Stall till "Strong" (65/100) for alla'),
    ('Security Advisor', 'Visar en rapport over potentiella sakerhetsproblem pa din server och rekommenderar atgarder. Detta ar ett utmarkt verktyg att kora regelbundet for att halla servern saker.', 'Kor manligen — folj rekommendationerna'),
    ('Security Questions', 'Konfigurera sakerhetsfragor for WHM-inloggning fran okanda IP-adresser. Detta ar ett extra skyddsfall forutom losenordet.', 'Aktivera for root-inloggning'),
    ('Shell Fork Bomb Protection', 'Forhindrar "fork bombs" — ett slags attack dar ett skadligt program skapar sa manga processer att servern kraschar. Detta begransnar antalet processer per anvandare.', 'Aktivera — forhindrar en klassisk attack'),
    ('SMTP Restrictions', 'Begransar vilka anvandare som far skicka e-post via SMTP. Forhindrar att skript som kors som "nobody" (okand anvandare) kan skicka e-post, vilket ar en vanlig spam-vektor.', 'Aktivera — forhindrar obehorig e-post'),
    ('SSH Password Authorization Tweak', 'Aktivera eller avaktivera losenordsbaserad SSH-inloggning. For maximal sakerhet: avaktivera losenordsinloggning och anvand BARA SSH-nycklar. Om du avaktiverar losenord maste du ha en giltig SSH-nyckel for att logga in.', 'Avaktivera for maximal sakerhet (anvand SSH-nycklar)'),
    ('Traceroute Enable/Disable', 'Tillat eller neka traceroute fran servern. Traceroute avslojar natverkstopologi som kan utnyttjas av angripare. Avaktivera for battre sakerhet.', 'Avaktivera — minskar informationlackage'),
    ('Two-Factor Authentication', 'Aktivera 2FA for WHM-inloggning. Du anvander en app som Google Authenticator for att generera tidsbegransade koder utover ditt vanliga losenord. Detta ar den viktigaste sakerhetsatgarden du kan gora!', 'AKTIVERA IMMEDIAT — det viktigaste du kan gora!'),
]
story.append(make_table(['Funktion', 'Forklaring', 'Rekommendation'], sec_funcs, [0.17, 0.60, 0.23]))

# Save part 1 story to a pickle file for part 2 to continue
import pickle
with open('/home/z/my-project/download/whm_story_part1.pkl', 'wb') as f:
    pickle.dump(story, f)

print("Part 1 done — story saved to whm_story_part1.pkl")
print(f"Story elements so far: {len(story)}")
