#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
.SE Domain Registrar Comparison PDF Generator
Comprehensive comparison of companies selling .SE domains
"""

import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch, mm, cm
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY, TA_RIGHT
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, KeepTogether, CondPageBreak, HRFlowable
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import registerFontFamily

# ━━ Color Palette ━━
ACCENT       = colors.HexColor('#c35b38')
TEXT_PRIMARY  = colors.HexColor('#1a1b1d')
TEXT_MUTED    = colors.HexColor('#81878d')
BG_SURFACE   = colors.HexColor('#d6dadf')
BG_PAGE      = colors.HexColor('#edeef0')
TABLE_HEADER_COLOR = ACCENT
TABLE_HEADER_TEXT  = colors.white
TABLE_ROW_EVEN     = colors.white
TABLE_ROW_ODD      = BG_SURFACE

# ━━ Font Registration ━━
pdfmetrics.registerFont(TTFont('NotoSerifSC', '/usr/share/fonts/truetype/noto-serif-sc/NotoSerifSC-Regular.ttf'))
pdfmetrics.registerFont(TTFont('NotoSerifSCBold', '/usr/share/fonts/truetype/noto-serif-sc/NotoSerifSC-Bold.ttf'))
pdfmetrics.registerFont(TTFont('LXGWWenKai', '/usr/share/fonts/truetype/lxgw-wenkai/LXGWWenKai-Regular.ttf'))
pdfmetrics.registerFont(TTFont('LXGWWenKaiMedium', '/usr/share/fonts/truetype/lxgw-wenkai/LXGWWenKai-Medium.ttf'))
pdfmetrics.registerFont(TTFont('WenQuanYi', '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc', subfontIndex=0))
pdfmetrics.registerFont(TTFont('Carlito', '/usr/share/fonts/truetype/english/Carlito-Regular.ttf'))
pdfmetrics.registerFont(TTFont('CarlitoBold', '/usr/share/fonts/truetype/english/Carlito-Bold.ttf'))
pdfmetrics.registerFont(TTFont('DejaVuSans', '/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf'))

registerFontFamily('NotoSerifSC', normal='NotoSerifSC', bold='NotoSerifSCBold')
registerFontFamily('LXGWWenKai', normal='LXGWWenKai', bold='LXGWWenKaiMedium')
registerFontFamily('WenQuanYi', normal='WenQuanYi', bold='WenQuanYi')
registerFontFamily('Carlito', normal='Carlito', bold='CarlitoBold')
registerFontFamily('DejaVuSans', normal='DejaVuSans', bold='DejaVuSans')

# Install font fallback for mixed CJK/Latin
import sys
PDF_SKILL_DIR = "/home/z/my-project/skills/pdf"
_scripts = os.path.join(PDF_SKILL_DIR, "scripts")
if _scripts not in sys.path:
    sys.path.insert(0, _scripts)
from pdf import install_font_fallback
install_font_fallback()

# ━━ Page Setup ━━
PAGE_W, PAGE_H = A4
LEFT_MARGIN = 1.0 * inch
RIGHT_MARGIN = 1.0 * inch
TOP_MARGIN = 0.8 * inch
BOTTOM_MARGIN = 0.8 * inch
CONTENT_W = PAGE_W - LEFT_MARGIN - RIGHT_MARGIN

# ━━ Styles ━━
styles = getSampleStyleSheet()

cover_title = ParagraphStyle(
    'CoverTitle', fontName='NotoSerifSC', fontSize=36, leading=44,
    textColor=ACCENT, alignment=TA_LEFT, spaceAfter=12
)
cover_subtitle = ParagraphStyle(
    'CoverSubtitle', fontName='WenQuanYi', fontSize=16, leading=22,
    textColor=TEXT_MUTED, alignment=TA_LEFT, spaceAfter=6
)
cover_meta = ParagraphStyle(
    'CoverMeta', fontName='WenQuanYi', fontSize=11, leading=16,
    textColor=TEXT_MUTED, alignment=TA_LEFT
)
h1_style = ParagraphStyle(
    'H1Custom', fontName='NotoSerifSC', fontSize=20, leading=28,
    textColor=ACCENT, spaceBefore=18, spaceAfter=10
)
h2_style = ParagraphStyle(
    'H2Custom', fontName='NotoSerifSC', fontSize=15, leading=22,
    textColor=TEXT_PRIMARY, spaceBefore=14, spaceAfter=8
)
h3_style = ParagraphStyle(
    'H3Custom', fontName='WenQuanYi', fontSize=12, leading=18,
    textColor=TEXT_PRIMARY, spaceBefore=10, spaceAfter=6
)
body_style = ParagraphStyle(
    'BodyCustom', fontName='WenQuanYi', fontSize=10.5, leading=17,
    textColor=TEXT_PRIMARY, alignment=TA_LEFT, wordWrap='CJK',
    spaceBefore=2, spaceAfter=6
)
note_style = ParagraphStyle(
    'NoteCustom', fontName='WenQuanYi', fontSize=9.5, leading=15,
    textColor=TEXT_MUTED, alignment=TA_LEFT, wordWrap='CJK',
    spaceBefore=2, spaceAfter=4, leftIndent=12
)
header_cell_style = ParagraphStyle(
    'HeaderCell', fontName='WenQuanYi', fontSize=9, leading=13,
    textColor=TABLE_HEADER_TEXT, alignment=TA_CENTER, wordWrap='CJK'
)
cell_style = ParagraphStyle(
    'CellStyle', fontName='WenQuanYi', fontSize=8.5, leading=12,
    textColor=TEXT_PRIMARY, alignment=TA_CENTER, wordWrap='CJK'
)
cell_left_style = ParagraphStyle(
    'CellLeftStyle', fontName='WenQuanYi', fontSize=8.5, leading=12,
    textColor=TEXT_PRIMARY, alignment=TA_LEFT, wordWrap='CJK'
)
cell_small_style = ParagraphStyle(
    'CellSmallStyle', fontName='WenQuanYi', fontSize=7.5, leading=10.5,
    textColor=TEXT_PRIMARY, alignment=TA_CENTER, wordWrap='CJK'
)
caption_style = ParagraphStyle(
    'CaptionStyle', fontName='WenQuanYi', fontSize=9, leading=14,
    textColor=TEXT_MUTED, alignment=TA_CENTER, spaceBefore=3, spaceAfter=6
)
bullet_style = ParagraphStyle(
    'BulletStyle', fontName='WenQuanYi', fontSize=10, leading=16,
    textColor=TEXT_PRIMARY, alignment=TA_LEFT, wordWrap='CJK',
    leftIndent=20, bulletIndent=8, spaceBefore=2, spaceAfter=3
)

# ━━ Helper Functions ━━
def P(text, style=body_style):
    return Paragraph(text, style)

def HP(text, style=header_cell_style):
    return Paragraph(text, style)

def CP(text, style=cell_style):
    return Paragraph(text, style)

def CLP(text, style=cell_left_style):
    return Paragraph(text, style)

def make_table(data, col_widths, caption_text=None):
    """Create a styled table with optional caption."""
    t = Table(data, colWidths=col_widths, hAlign='CENTER')
    style_cmds = [
        ('BACKGROUND', (0, 0), (-1, 0), TABLE_HEADER_COLOR),
        ('TEXTCOLOR', (0, 0), (-1, 0), TABLE_HEADER_TEXT),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('GRID', (0, 0), (-1, -1), 0.4, TEXT_MUTED),
    ]
    # Alternating row colors
    for i in range(1, len(data)):
        bg = TABLE_ROW_EVEN if i % 2 == 1 else TABLE_ROW_ODD
        style_cmds.append(('BACKGROUND', (0, i), (-1, i), bg))
    t.setStyle(TableStyle(style_cmds))

    elements = [Spacer(1, 12), t]
    if caption_text:
        elements.append(Spacer(1, 4))
        elements.append(P(caption_text, caption_style))
    elements.append(Spacer(1, 12))
    return elements

# ━━ Document Build ━━
output_path = "/home/z/my-project/download/se_doman_registratorer_jamforelse.pdf"

doc = SimpleDocTemplate(
    output_path,
    pagesize=A4,
    leftMargin=LEFT_MARGIN,
    rightMargin=RIGHT_MARGIN,
    topMargin=TOP_MARGIN,
    bottomMargin=BOTTOM_MARGIN,
    title=".SE-doman Registratorer Jamforelse",
    author="Z.ai",
    creator="Z.ai"
)

story = []

# ━━ COVER PAGE ━━
story.append(Spacer(1, 120))
story.append(P('<b>.SE-doman</b>', cover_title))
story.append(P('<b>Registratorer</b>', cover_title))
story.append(P('<b>Jamforelse</b>', cover_title))
story.append(Spacer(1, 24))
story.append(HRFlowable(width="60%", thickness=2, color=ACCENT, spaceAfter=16))
story.append(P('Komplett guide till alla företag som säljer .SE-domäner', cover_subtitle))
story.append(P('Priser, funktioner, skillnader och rekommendationer', cover_subtitle))
story.append(Spacer(1, 40))
story.append(P('Maj 2026', cover_meta))
story.append(P('Utarbetad av Z.ai', cover_meta))
story.append(PageBreak())

# ━━ SECTION 1: INTRODUCTION ━━
story.append(P('<b>1. Om .SE-domäner</b>', h1_style))
story.append(Spacer(1, 6))

story.append(P(
    '.SE är Sveriges nationella toppdomän och förvaltas av Internetstiftelsen (The Swedish Internet Foundation). '
    'Till skillnad från många andra toppdomäner har .SE inbyggt dataskydd för privatpersoner, vilket innebär att '
    'personuppgifter inte visas i WHOIS-registret. Detta gör att WHOIS Privacy som separat betaltjänst är överflödig '
    'för .SE-domäner. Internetstiftelsen tar ut en registriesavgift på 135 kr/år per domän (från januari 2025), '
    'vilket utgör minimikostnaden — ingen registrator kan erbjuda .SE-domäner under detta pris lönsamt utan att ta förlust.',
    body_style
))
story.append(Spacer(1, 6))

story.append(P('<b>1.1 Vad betyder .SE-ackrediterad?</b>', h2_style))
story.append(P(
    'Ett företag som är .SE-ackrediterad (certifierad registrator) har ett direkt avtal med Internetstiftelsen '
    'och kan registrera .SE-domäner utan mellanhänder. Icke-ackrediterade företag är återförsäljare som går '
    'via en ackrediterad registrator, vilket kan innebära högre priser, långsammare hantering och färre '
    'funktioner. Att välja en ackrediterad registrator ger direkt tillgång till registret, snabbare '
    'domänändringar och oftast bättre priser eftersom inget mellanhandsmarkör läggs på.',
    body_style
))
story.append(Spacer(1, 6))

story.append(P('<b>1.2 WHOIS Privacy — Inte nödvändig för .SE</b>', h2_style))
story.append(P(
    'Internetstiftelsen skyddar redan personuppgifter för privatpersoner och enskilda firmor enligt GDPR. '
    'För företag/organisationer visas organisationsnamnet men personliga kontaktuppgifter döljs normalt. '
    'Många registratorer marknadsför "gratis WHOIS Privacy" för .SE-domäner, men detta är en tjänst som '
    'redan är inbyggd i registret och kostar inget extra. Du bör inte betala额外t för denna funktion.',
    body_style
))
story.append(Spacer(1, 6))

story.append(P('<b>1.3 Viktiga funktioner att jämföra</b>', h2_style))
story.append(P(
    'När du väljer registrator för .SE-domäner finns flera funktioner som kan skilja sig åt mellan leverantörerna. '
    'Auto-DNSSEC innebär att domänens DNS automatiskt signeras kryptografiskt, vilket skyddar mot DNS-kapning och '
    'förfalskade DNS-svar. Snapback (backorder) är en tjänst som automatiskt försöker registrera en domän när den '
    'löper ut och blir tillgänglig — användbart för eftertraktade domännamn. Registry Lock är den högsta '
    'säkerhetsnivån för en domän, där ändringar kräver manuell verifiering direkt med Internetstiftelsen, '
    'vilket förhindrar obehöriga överföringar eller ändringar.',
    body_style
))
story.append(Spacer(1, 6))

story.append(P('<b>1.4 Transfer (överföring) av .SE-domäner</b>', h2_style))
story.append(P(
    'En viktig skillnad mellan .SE och många andra toppdomäner (som .COM) är att en transfer av en .SE-domän '
    'inte inkluderar en 1-årig förnyelse. För .COM-domäner får du ofta ett extra år när du flyttar domänen, '
    'men för .SE måste förnyelsen betalas separat. Det innebär att det totala priset för att flytta en .SE-domän '
    'kan vara högre än det första transferpriset antyder. Vissa registratorer erbjuder gratis transfer men '
    'debiterar sedan förnyelseavgiften, medan andra tar betalt för både transfer och förnyelse.',
    body_style
))

# ━━ SECTION 2: MAIN PRICING TABLE ━━
story.append(P('<b>2. Prisjämförelse — Svenska registratorer</b>', h1_style))
story.append(Spacer(1, 6))

story.append(P(
    'Nedan följer en komplett prisjämförelse för alla större företag som säljer .SE-domäner. '
    'Alla priser anges i svenska kronor (SEK) inklusive moms där angivet. Priserna är uppdaterade '
    'så långt möjligt baserat på tillgänglig information från respektive företags webbplats.',
    body_style
))

# Main pricing table
pricing_data = [
    [
        HP('Foretag'), HP('Registrering<br/>(kr/ar)'), HP('Transfer<br/>(kr)'),
        HP('Förnyelse<br/>(kr/ar)'), HP('.SE-<br/>ackrediterad'), HP('Auto-<br/>DNSSEC')
    ],
    [CLP('<b>HostUp</b>'), CP('99 (169 ar 2+)'), CP('Gratis'), CP('169'), CP('Ja'), CP('Ja')],
    [CLP('<b>Inleed</b>'), CP('89 (179 ar 2+)'), CP('Gratis'), CP('179'), CP('Ja'), CP('Ja')],
    [CLP('<b>FS Data</b>'), CP('~56 (exkl moms)'), CP('Gratis'), CP('~113 inkl moms'), CP('Troligen'), CP('Okand')],
    [CLP('<b>EgenSajt</b>'), CP('229'), CP('Gratis'), CP('229'), CP('Ja'), CP('Ja')],
    [CLP('<b>Oderland</b>'), CP('229'), CP('229'), CP('229'), CP('Ja'), CP('Ja')],
    [CLP('<b>Webb.se</b>'), CP('225'), CP('225'), CP('225'), CP('Ja'), CP('Ja')],
    [CLP('<b>Miss Hosting</b>'), CP('9 kampanj'), CP('Gratis'), CP('219 exkl moms'), CP('Nej'), CP('Okand')],
    [CLP('<b>Loopia</b>'), CP('9 kampanj'), CP('~177'), CP('289 exkl moms'), CP('Ja'), CP('Ja')],
    [CLP('<b>Simply.com</b>'), CP('~209'), CP('Gratis'), CP('~209'), CP('Ja'), CP('Ja')],
    [CLP('<b>Websupport</b>'), CP('129 kampanj'), CP('279'), CP('299'), CP('Ja'), CP('Ja')],
    [CLP('<b>Strato</b>'), CP('6 kampanj'), CP('Okand'), CP('~90'), CP('Nej'), CP('Okand')],
    [CLP('<b>Polar55</b>'), CP('5 kampanj'), CP('29'), CP('289'), CP('Nej'), CP('Okand')],
    [CLP('<b>One.com</b>'), CP('Gratis m. hosting'), CP('Okand'), CP('~280'), CP('Nej'), CP('Okand')],
]

col_w = [CONTENT_W * r for r in [0.18, 0.20, 0.14, 0.20, 0.14, 0.14]]
for el in make_table(pricing_data, col_w, 'Tabell 1: Prisjamforelse for .SE-domaner hos svenska foretag (priser i SEK)'):
    story.append(el)

story.append(P(
    '<b>Observera:</b> Kampanjpriser (5-9 kr första året) är förlustintäktspriser som markant höjs vid förnyelse. '
    'Loopia debiterar dessutom 108 kr/år för LoopiaDNS om du inte har hosting hos dem, vilket gör det verkliga '
    'årspriset 397 kr/år för en domän utan hosting. Strato kan ha obligatoriska DNS-tillägg som höjer det '
    'effektiva priset. FS Data priser (exkl. moms) kan vara från före 2025 års prisökning.',
    note_style
))

# ━━ SECTION 3: FEATURE COMPARISON ━━
story.append(P('<b>3. Funktionsjämförelse</b>', h1_style))
story.append(Spacer(1, 6))

story.append(P(
    'Utöver priset skiljer sig registratorerna åt i vilka funktioner som ingår vid köp av en .SE-domän. '
    'Följande tabell visar vilka funktioner som ingår gratis, vilka som kostar extra och vilka som saknas.',
    body_style
))

feature_data = [
    [
        HP('Foretag'), HP('DNS-<br/>hantering'), HP('Epost-<br/>vidarebef.'),
        HP('URL-<br/>vidarebef.'), HP('Snapback'), HP('Registry<br/>Lock'),
        HP('Gratis<br/>SSL'), HP('Svenskt<br/>stod')
    ],
    [CLP('<b>HostUp</b>'), CP('Ja'), CP('Nej'), CP('Nej'), CP('375 kr'), CP('Gratis'), CP('Nej'), CP('Ja')],
    [CLP('<b>Inleed</b>'), CP('Ja'), CP('Endast m. hosting'), CP('Ja'), CP('Nej'), CP('Okand'), CP('Nej'), CP('Ja')],
    [CLP('<b>EgenSajt</b>'), CP('Ja'), CP('Ja'), CP('Ja'), CP('Ja'), CP('Okand'), CP('Ja'), CP('Ja')],
    [CLP('<b>Oderland</b>'), CP('Ja'), CP('M. hosting'), CP('M. hosting'), CP('Nej'), CP('Okand'), CP('Ja'), CP('Ja')],
    [CLP('<b>Webb.se</b>'), CP('Ja'), CP('Ja'), CP('Ja'), CP('Okand'), CP('Okand'), CP('Okand'), CP('Ja')],
    [CLP('<b>Miss Hosting</b>'), CP('Ja'), CP('M. hosting'), CP('M. hosting'), CP('Ja'), CP('Okand'), CP('Nej'), CP('Ja')],
    [CLP('<b>Loopia</b>'), CP('108 kr/ar extral'), CP('M. DNS'), CP('M. DNS'), CP('Nej'), CP('499 kr'), CP('Nej'), CP('Ja')],
    [CLP('<b>Simply.com</b>'), CP('Ja'), CP('Ja'), CP('Ja'), CP('Nej'), CP('Okand'), CP('Ja'), CP('Ja')],
    [CLP('<b>Websupport</b>'), CP('Ja'), CP('M. hosting'), CP('M. hosting'), CP('Nej'), CP('Okand'), CP('Ja'), CP('Ja')],
    [CLP('<b>FS Data</b>'), CP('Ja'), CP('Ja'), CP('Ja'), CP('Okand'), CP('Okand'), CP('Nej'), CP('Ja')],
    [CLP('<b>Strato</b>'), CP('Tillagg?'), CP('M. hosting'), CP('Ja'), CP('Nej'), CP('Okand'), CP('Ja'), CP('Begransat')],
    [CLP('<b>Polar55</b>'), CP('Ja'), CP('M. hosting'), CP('Ja'), CP('Nej'), CP('Okand'), CP('Nej'), CP('Begransat')],
]

col_w2 = [CONTENT_W * r for r in [0.16, 0.12, 0.13, 0.12, 0.11, 0.12, 0.11, 0.12]]
for el in make_table(feature_data, col_w2, 'Tabell 2: Funktionsjamforelse for .SE-domaner'):
    story.append(el)

story.append(P(
    'DNS-hantering innebär möjlighet att hantera DNS-poster (A, MX, CNAME etc.) utan kostnad. '
    'E-postvidarebefordran låter dig skicka e-post från din .SE-domän till en annan adress. '
    'URL-vidarebefordran omdirigerar besökare från din domän till en annan webbadress. '
    'Snapback/backorder är en tjänst som automatiskt försöker registrera en domän som löpt ut. '
    'Registry Lock är högsta säkerhetsnivå som kräver manuell verifiering för alla ändringar.',
    note_style
))

# ━━ SECTION 4: INTERNATIONAL REGISTRARS ━━
story.append(P('<b>4. Internationella registratorer</b>', h1_style))
story.append(Spacer(1, 6))

story.append(P(
    'Utöver de svenska företagen finns flera internationella registratorer som säljer .SE-domäner. '
    'Dessa är inte .SE-ackrediterade utan agerar återförsäljare via ackrediterade registratorer. '
    'Priserna är ofta betydligt högre och funktionerna mer begränsade, men de kan vara aktuella '
    'om du redan använder dessa plattformar för andra domäner och vill ha allt på ett ställe.',
    body_style
))

intl_data = [
    [
        HP('Foretag'), HP('Land'), HP('Registrering<br/>(kr/ar)'), HP('Förnyelse<br/>(kr/ar)'),
        HP('.SE-<br/>ackrediterad'), HP('Svenskt<br/>stod'), HP('Notering')
    ],
    [CLP('<b>Namecheap</b>'), CP('USA'), CP('~180'), CP('~190'), CP('Nej'), CP('Nej'), CP('Bra DNS, email redirect')],
    [CLP('<b>GoDaddy</b>'), CP('USA'), CP('~410'), CP('~508'), CP('Nej'), CP('Begransat'), CP('Dyrt, extra kostnader')],
    [CLP('<b>Hostinger</b>'), CP('Litauen'), CP('~168'), CP('~199'), CP('Nej'), CP('Begransat'), CP('Kraver hosting')],
    [CLP('<b>101domain</b>'), CP('USA'), CP('~630'), CP('~693'), CP('Nej'), CP('Nej'), CP('1500+ TLDs, specialister')],
    [CLP('<b>Europeregistry</b>'), CP('Irland'), CP('~620'), CP('~567'), CP('Nej'), CP('Nej'), CP('Europeisk ccTLD-specialist')],
    [CLP('<b>Marcaria</b>'), CP('Argentina'), CP('~575-690'), CP('~575-690'), CP('Nej'), CP('Nej'), CP('Varumarkestjanster')],
    [CLP('<b>Active24</b>'), CP('Slovakien'), CP('~320'), CP('~320'), CP('Nej'), CP('Nej'), CP('Pan-europeisk')],
]

col_w3 = [CONTENT_W * r for r in [0.16, 0.12, 0.15, 0.15, 0.12, 0.12, 0.18]]
for el in make_table(intl_data, col_w3, 'Tabell 3: Internationella registratorer som saljer .SE-domaner'):
    story.append(el)

story.append(P(
    'Internationella registratorer har oftast inget svenskt stöd, inga svenska servrar och betydligt högre priser '
    'för .SE-domäner. De kan dock vara värda att överväga om du hanterar många olika TLDs och vill ha en '
    'samlad plattform. Namecheap erbjuder den bästa kombinationen av pris och funktioner bland de internationella '
    'alternativen, med bra DNS-hantering och gratis e-postvidarebefordran.',
    note_style
))

# ━━ SECTION 5: 5-YEAR COST COMPARISON ━━
story.append(P('<b>5. Total ägandekostnad — 5-årsjämförelse</b>', h1_style))
story.append(Spacer(1, 6))

story.append(P(
    'Eftersom kampanjpriser endast gäller det första året är det viktigt att jämföra den totala kostnaden '
    'över flera år. Följande tabell visar den totala kostnaden för att äga en .SE-domän under 5 år, '
    'inklusive alla registrerings-, transfer- och förnyelseavgifter. För registratorer med gratis transfer '
    'antas att ingen extra transfer-kostnad tillkommer.',
    body_style
))

cost5_data = [
    [
        HP('Foretag'), HP('Ar 1 (kr)'), HP('Ar 2-5 / ar<br/>(kr)'), HP('5-ars total<br/>(kr)'), HP('Ranking')
    ],
    [CLP('<b>FS Data</b>'), CP('~56'), CP('~113'), CP('~508'), CP('1')],
    [CLP('<b>Inleed</b>'), CP('89'), CP('179'), CP('805'), CP('2')],
    [CLP('<b>HostUp</b>'), CP('99'), CP('169'), CP('845'), CP('3')],
    [CLP('<b>Miss Hosting</b>'), CP('9'), CP('219'), CP('885'), CP('4')],
    [CLP('<b>EgenSajt</b>'), CP('229'), CP('229'), CP('1 145'), CP('5')],
    [CLP('<b>Oderland</b>'), CP('229'), CP('229'), CP('1 145'), CP('5')],
    [CLP('<b>Webb.se</b>'), CP('225'), CP('225'), CP('1 125'), CP('5')],
    [CLP('<b>Loopia</b>'), CP('9 (+108 DNS)'), CP('289 (+108)'), CP('1 685'), CP('8')],
    [CLP('<b>Simply.com</b>'), CP('~209'), CP('~209'), CP('~1 045'), CP('5')],
    [CLP('<b>Websupport</b>'), CP('129'), CP('299'), CP('1 325'), CP('7')],
    [CLP('<b>Polar55</b>'), CP('5'), CP('289'), CP('1 161'), CP('6')],
]

col_w5 = [CONTENT_W * r for r in [0.20, 0.18, 0.22, 0.20, 0.12]]
for el in make_table(cost5_data, col_w5, 'Tabell 4: Total agandekostnad for .SE-doman over 5 ar'):
    story.append(el)

story.append(P(
    'FS Data har lägst total ägandekostnad men deras priser kan vara föråldrade (före 2025 års prisökning) — '
    ' verifiera aktuella priser direkt. Inleed och HostUp erbjuder den bästa kombinationen av lågt pris, '
    'ackreditering och kompletta funktioner. Loopia är dyrt utan hosting på grund av DNS-avgiften. '
    'Kampanjpriser från Miss Hosting och Polar55 ger låg förstaårskostnad men hög total kostnad.',
    note_style
))

# ━━ SECTION 6: DETAILED PROFILES ━━
story.append(P('<b>6. Detaljerade företagsprofiler</b>', h1_style))
story.append(Spacer(1, 6))

# HostUp
story.append(P('<b>6.1 HostUp (hostup.se)</b>', h2_style))
story.append(P(
    'HostUp är en svensk .SE-ackrediterad registrator som erbjuder .SE-domäner till konkurrenskraftiga priser. '
    'Deras förnyelsepris på 169 kr/år är ett av de lägsta på marknaden och ligger nära Internetstiftelsens '
    'registryavgift på 135 kr/år. HostUp sticker ut med att erbjuda gratis Registry Lock för .SE-domäner, '
    'vilket är en unik funktion — de flesta andra registratorer tar 499 kr eller mer för detta. De erbjuder '
    'även SmartDNSSEC som automatiskt signerar domänens DNS, samt Snapback-tjänst (backorder) till 375 kr '
    'där du bara betalar om domänen registreras. Deras DNS SmartCopy-funktion kopierar automatiskt DNS-poster '
    'vid transfer, vilket gör flyttprocessen smidigare. Däremot saknas e-postvidarebefordran och URL-'
    'vidarebefordran som gratisfunktioner vid enbar domänköp, och inget gratis SSL-certifikat ingår.',
    body_style
))

# Inleed
story.append(P('<b>6.2 Inleed (inleed.se)</b>', h2_style))
story.append(P(
    'Inleed är ett välkänt svenskt webbhotell och .SE-ackrediterad registrator med eget datacenter i Tällberg, '
    'Dalarna. Deras .SE-priser är konkurrenskraftiga med 89 kr första året och 179 kr/år i förnyelse, vilket '
    'ger en låg total ägandekostnad. Transfer är gratis. Inleed erbjuder URL-vidarebefordran (301/302 redirects) '
    'som gratisfunktion, men e-postvidarebefordran kräver hosting-abonnemang. Deras starkaste sida är att de '
    'är en komplett leverantör med hosting, VPS och domäner på samma plattform, med svenskt stöd alla dagar '
    '08:00-21:00 och Trustpilot-betyg 4.9/5. De saknar dock Snapback-tjänst och Registry Lock är inte bekräftat. '
    'Inleed är ICANN-ackrediterad, vilket innebär att de kan hantera alla typer av domäner direkt.',
    body_style
))

# EgenSajt
story.append(P('<b>6.3 EgenSajt (egensajt.se)</b>', h2_style))
story.append(P(
    'EgenSajt är en svensk .SE-ackrediterad registrator som erbjuder ett komplett funktionspaket med sina '
    '.SE-domäner. Till skillnad från många andra registratorer ingår både e-postvidarebefordran, URL-'
    'vidarebefordran och gratis Let\'s Encrypt SSL-certifikat utan extra kostnad. Priserna är enhetliga — '
    '229 kr för registrering, transfer och förnyelse — vilket gör det enkelt att beräkna kostnader utan '
    'dolda överraskningar. Snapback-tjänst finns tillgänglig. EgenSajt erbjuder dessutom 8% volymrabatt '
    'för 20+ domäner, vilket gör dem särskilt attraktiva för domänportföljer. Auto-DNSSEC stöds men kräver '
    'manuell aktivering. Deras prisläge är något högre än HostUp och Inleed, men det inkluderar fler '
    'funktioner utan extra kostnad.',
    body_style
))

# Loopia
story.append(P('<b>6.4 Loopia (loopia.se)</b>', h2_style))
story.append(P(
    'Loopia är en av Sveriges största och mest kända registratorer, .SE-ackrediterad med 24/7 svenskt stöd. '
    'Deras kampanjpris på 9 kr för första året (max 3 domäner) är lockande, men förnyelsepriset är 289 kr/år '
    '(exkl. moms, 361 kr inkl. moms) vilket är bland de högsta på marknaden. En avgörande nackdel är att '
    'LoopiaDNS kostar 108 kr/år extra om du inte har hosting hos dem, vilket gör det verkliga priset för en '
    'bar domän utan hosting till 397-469 kr/år inkl. moms — betydligt dyrare än konkurrenterna. Loopia '
    'erbjuder Registry Lock för 499 kr och har haft gratis DNSSEC sedan 2025. Deras styrka är det '
    'omfattande stödet och den etablerade plattformen, men priset för domän utan hosting är svårt att '
    'motivera jämfört med billigare alternativ.',
    body_style
))

# Miss Hosting
story.append(P('<b>6.5 Miss Hosting (misshosting.se)</b>', h2_style))
story.append(P(
    'Miss Hosting är ett svenskt företag (via Danmark) som erbjuder .SE-domäner med extremt lågt kampanjpris '
    'på 9 kr första året. Förnyelsepriset är dock 219 kr/år (exkl. moms), vilket ger 274 kr/år inkl. moms. '
    'De är inte .SE-ackrediterade utan agerar återförsäljare. Miss Hosting erbjuder Snapback-tjänst och '
    'stödjer över 1 300 TLDs. Transfer är gratis. Deras stöd är 24/7 via chat, men det svenska stödet '
    'använder Google Translate enligt uppgifter. E-post- och URL-vidarebefordran kräver hosting-abonnemang. '
    'Miss Hosting kan vara ett alternativ om du redan har hosting hos dem, men för enbar domänköp finns '
    'bättre och billigare alternativ med ackreditering.',
    body_style
))

# Oderland
story.append(P('<b>6.6 Oderland (oderland.se)</b>', h2_style))
story.append(P(
    'Oderland är en svensk .SE-ackrediterad registrator med enhetliga priser — 229 kr för registrering, '
    'transfer och förnyelse. De erbjuder gratis Let\'s Encrypt SSL och gratis Auto-DNSSEC för .SE- och .NU-'
    'domäner. E-post- och URL-vidarebefordran kräver hosting-abonnemang. Överlåtelse av domän kostar 250+25 kr '
    'per domän. Oderland är ett pålitligt val med transparenta priser, men saknar Snapback-tjänst och '
    'Registry Lock är inte bekräftat. Deras prisläge är i linje med EgenSajt, men med färre inkluderade '
    'funktioner vid enbar domänköp.',
    body_style
))

# Simply.com
story.append(P('<b>6.7 Simply.com (simply.com)</b>', h2_style))
story.append(P(
    'Simply.com är en dansk .SE-ackrediterad registrator som erbjuder .SE-domäner till cirka 209 kr/år med '
    'enheltliga priser för registrering och förnyelse. Transfer är gratis. De erbjuder komplett '
    'funktionspaket med DNS-hantering, e-postvidarebefordran, URL-vidarebefordran och gratis SSL-certifikat. '
    'Auto-DNSSEC stöds. Simply.com är certifierad registrator med direkt registrering utan mellanhänder. '
    'Deras svaga punkt är att de inte har svenskt företag (dansk) och stödet är inte på svenska, men '
    'de har liknande nordisk affärskultur och snabb hantering.',
    body_style
))

# Websupport
story.append(P('<b>6.8 Websupport (websupport.se)</b>', h2_style))
story.append(P(
    'Websupport är en del av team.blue-koncernen och .SE-ackrediterad. Deras kampanjpris är 129 kr första '
    'året, men förnyelsepriset är 299 kr/år — bland de högsta i jämförelsen. Transfer kostar 279 kr. '
    'De erbjuder komplett funktionspaket med DNS-hantering, gratis SSL och Auto-DNSSEC. E-post- och URL-'
    'vidarebefordran kräver hosting. Websupport har svenskt stöd och en modern plattform med '
    'website builder, men prisläget gör dem mindre konkurrenskraftiga för enbar domänköp. Som del av '
    'team.blue har de dock stabil infrastruktur och finansiell säkerhet.',
    body_style
))

# FS Data
story.append(P('<b>6.9 FS Data (fsdata.se)</b>', h2_style))
story.append(P(
    'FS Data är en svensk registrator med mycket låga priser — 45 kr registrering och 90 kr/år förnyelse '
    '(exkl. moms, motsvarande cirka 113 kr/år inkl. moms). Dessa priser verkar dock vara från före 2025 års '
    'prisökning hos Internetstiftelsen och kan ha uppdaterats sedan dess. FS Data inkluderar DNS-hantering, '
    'e-postvidarebefordran och URL-vidarebefordran som gratisfunktioner. De har troligen .SE-ackreditering. '
    'Verifiera aktuella priser direkt hos FS Data innan beslut. Om priserna stämmer är de det billigaste '
    'alternativet på marknaden, men deras funktionsutbud och plattform är mer begränsad än större aktörer.',
    body_style
))

# ━━ SECTION 7: COMPANIES THAT DISAPPEARED ━━
story.append(P('<b>7. Företag som fusionerats eller lagts ner</b>', h1_style))
story.append(Spacer(1, 6))

story.append(P(
    'Flera tidigare kända svenska domänregistratorer har fusionerats eller lagts ner under de senaste åren. '
    'Detta är viktigt att känna till om du har domäner hos dessa företag, eller om du hittar gamla rekommendationer '
    'på nätet som refererar till dem. Binero, som tidigare var en av Sveriges största registratorer, fusionerades '
    'med Loopia Group AB 2019 och deras webbhotellverksamhet ombildades till Websupport. Binero fokuserar numera '
    'på cloud/managed services och säljer inte längre domäner direkt. Ballou har uppgått i Miss Hosting, och '
    'Crystone har genomgått flera ägarbyten och är nu i praktiken en del av team.blue (samma koncern som '
    'Websupport och Loopia). Surftown, som var ett danskt webbhotell, verkar ha lagts ner som varumärke.',
    body_style
))

gone_data = [
    [HP('Foretag'), HP('Nuvarande status'), HP('Notering')],
    [CLP('Binero'), CLP('Fusionerat med Loopia Group → Websupport'), CLP('Säljer ej längre domäner direkt')],
    [CLP('Ballou'), CLP('Uppgått i Miss Hosting'), CLP('Domäntjänster i Miss Hosting')],
    [CLP('Crystone'), CLP('Del av team.blue'), CLP('Samma koncern som Websupport/Loopia')],
    [CLP('Surftown'), CLP('Nedlagt varumärke'), CLP('Danskt webbhotell, ej längre aktivt')],
]

col_w7 = [CONTENT_W * r for r in [0.15, 0.45, 0.40]]
for el in make_table(gone_data, col_w7, 'Tabell 5: Foretag som fusionerats eller lagts ner'):
    story.append(el)

# ━━ SECTION 8: RECOMMENDATIONS ━━
story.append(P('<b>8. Rekommendationer baserat på användningsområde</b>', h1_style))
story.append(Spacer(1, 6))

story.append(P('<b>8.1 Bäst för domän + ChemiCloud-hosting (din situation)</b>', h2_style))
story.append(P(
    'Eftersom du planerar att använda ChemiCloud för WHM/cPanel-hosting behöver du en separat .SE-registrator '
    'som kan peka domänens DNS till ChemiClouds namnservrar. I detta scenario är de viktigaste faktorerna: '
    'lågt pris, gratis DNS-hantering, gratis transfer (för framtida flytt), och Auto-DNSSEC. HostUp är det '
    'bästa valet här med 169 kr/år i förnyelse, gratis Registry Lock, Auto-DNSSEC och DNS SmartCopy vid '
    'transfer. Inleed är ett nästan lika bra alternativ med 179 kr/år och gratis transfer. Båda är .SE-'
    'ackrediterade med svenskt stöd. Du behöver inte e-post eller hosting från registratorn eftersom allt '
    'körs hos ChemiCloud.',
    body_style
))

story.append(P('<b>8.2 Bäst för stora domänportföljer (20+ domäner)</b>', h2_style))
story.append(P(
    'Om du hanterar många domäner blir volymrabatter och enhetliga priser viktiga. EgenSajt erbjuder 8% '
    'rabatt vid 20+ domäner och har enhetliga priser (229 kr) utan dolda kostnader. Simply.com erbjuder '
    'kompletta funktioner till cirka 209 kr/år. HostUp rekommenderas också tack vare lågt förnyelsepris '
    'och gratis Registry Lock som ger extra säkerhet för värdefulla domäner. För stora portföljer är det '
    'värt att överväga att dela domäner mellan två registratorer för riskspridning.',
    body_style
))

story.append(P('<b>8.3 Bäst för småföretag med allt-i-ett</b>', h2_style))
story.append(P(
    'Om du vill ha domän, e-post och hosting hos samma leverantör är Inleed ett utmärkt val med sin '
    'kompletta plattform, svenska servrar i Dalarna och svenskt stöd alla dagar. Oderland erbjuder liknande '
    'helhet med .SE-ackreditering och enhetliga priser. Loopia har den mest etablerade plattformen men '
    'är dyrare, särskilt om du inte använder deras hosting. För den som vill ha internationell '
    'närvaro kan Simply.com vara ett alternativ med danskt bolag men nordisk infrastruktur.',
    body_style
))

story.append(P('<b>8.4 Bäst budgetval</b>', h2_style))
story.append(P(
    'Om priset är den enda faktorn som spelar roll: FS Data har lägst rapporterade priser (~113 kr/år inkl. '
    'moms) men verifiera aktuella priser först. HostUp erbjuder bäst värde med 169 kr/år inklusive gratis '
    'Registry Lock och Auto-DNSSEC. Inleed följer tätt efter med 179 kr/år. Undvik kampanjpriser från '
    'Miss Hosting (9 kr första året → 274 kr/år inkl. moms därefter), Loopia (9 kr → 361+ kr/år inkl. '
    'moms och DNS-avgift) och Polar55 (5 kr → 289 kr/år) om du planerar att behålla domänen mer än ett år.',
    body_style
))

# ━━ SECTION 9: QUICK REFERENCE ━━
story.append(P('<b>9. Snabbreferens — Topp 3 per kategori</b>', h1_style))
story.append(Spacer(1, 6))

top3_data = [
    [HP('Kategori'), HP('1:a plats'), HP('2:a plats'), HP('3:e plats')],
    [CLP('Lagst fornyelsepris'), CP('FS Data (~113 kr)'), CP('HostUp (169 kr)'), CP('Inleed (179 kr)')],
    [CLP('Bast varde totalt'), CP('HostUp'), CP('Inleed'), CP('EgenSajt')],
    [CLP('Bast funktioner'), CP('EgenSajt'), CP('Simply.com'), CP('Oderland')],
    [CLP('Bast sakarhet'), CP('HostUp (gratis Registry Lock)'), CP('EgenSajt (Snapback)'), CP('Inleed')],
    [CLP('Bast for stora portfoljer'), CP('EgenSajt (8% rabatt)'), CP('HostUp'), CP('Simply.com')],
    [CLP('Bast svenskt stod'), CP('Loopia (24/7)'), CP('Inleed (dagligen)'), CP('HostUp')],
    [CLP('Lagst forsta ar'), CP('Polar55 (5 kr)'), CP('Miss Hosting (9 kr)'), CP('Loopia (9 kr)')],
]

col_w9 = [CONTENT_W * r for r in [0.24, 0.26, 0.26, 0.24]]
for el in make_table(top3_data, col_w9, 'Tabell 6: Topp 3 per kategori'):
    story.append(el)

# ━━ SECTION 10: IMPORTANT NOTES ━━
story.append(P('<b>10. Viktiga noteringar</b>', h1_style))
story.append(Spacer(1, 6))

story.append(P(
    '<b>Internetstiftelsens prisökning (januari 2025):</b> Registriesavgiften ökade från 120 kr till 135 kr/år, '
    'vilket har pressat upp priser hos de flesta registratorer. Loopia höjde sina priser igen i december 2025. '
    'Förvänta dig att fler registratorer kan komma att justera sina priser uppåt under 2026.',
    body_style
))
story.append(Spacer(1, 4))

story.append(P(
    '<b>Kampanjpriser:</b> Många svenska registratorer erbjuder extremt låga förstaårskampanjer (5-9 kr) som '
    'markant höjs vid förnyelse. Jämför alltid det ordinarie förnyelsepriset, inte kampanjpriset, när du '
    'gör ditt val. En domän som kostar 9 kr första året men 289 kr/år därefter är dyrare över tid än en '
    'domän som kostar 169 kr/år från början.',
    body_style
))
story.append(Spacer(1, 4))

story.append(P(
    '<b>Valutafluktuationer:</b> Internationella registratorers priser i SEK varierar med växelkurserna. '
    'De angivna priserna är approximationer baserade på aktuella kurser och kan avvika.',
    body_style
))
story.append(Spacer(1, 4))

story.append(P(
    '<b>DNS-vidarebefordran vs ChemiCloud:</b> Eftersom du använder ChemiCloud för hosting behöver du peka '
    'din .SE-domäns DNS till ChemiClouds namnservrar. DNS-hantering kan antingen ske hos registratorn eller '
    'hos ChemiCloud. De flesta registratorer erbjuder gratis DNS-hantering, och du kan också använda '
    'ChemiClouds DNS om du föredrar att ha allt på ett ställe.',
    body_style
))

# ━━ Build ━━
doc.build(story)
print(f"PDF generated: {output_path}")
