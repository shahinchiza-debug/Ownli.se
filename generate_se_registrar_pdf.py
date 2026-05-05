#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
.SE Domain Registrar Comparison - Comprehensive Feature Guide
Generates a professional PDF with all registrar features.
"""

import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch, mm
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, KeepTogether, CondPageBreak
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import registerFontFamily

# ━━ Color Palette ━━
PAGE_BG       = colors.HexColor('#f0f2f2')
SECTION_BG    = colors.HexColor('#f0f1f2')
CARD_BG       = colors.HexColor('#e8eaeb')
TABLE_STRIPE  = colors.HexColor('#eef0f1')
HEADER_FILL   = colors.HexColor('#526a77')
COVER_BLOCK   = colors.HexColor('#45555e')
BORDER        = colors.HexColor('#acbec6')
ICON          = colors.HexColor('#588196')
ACCENT        = colors.HexColor('#ca5129')
ACCENT_2      = colors.HexColor('#63c14a')
TEXT_PRIMARY   = colors.HexColor('#1b1d1e')
TEXT_MUTED     = colors.HexColor('#777d81')
SEM_SUCCESS   = colors.HexColor('#418256')
SEM_WARNING   = colors.HexColor('#947a44')
SEM_ERROR     = colors.HexColor('#8e443e')
SEM_INFO      = colors.HexColor('#4b6885')

# ━━ Font Registration ━━
pdfmetrics.registerFont(TTFont('NotoSerifSC', '/usr/share/fonts/truetype/noto-serif-sc/NotoSerifSC-Regular.ttf'))
pdfmetrics.registerFont(TTFont('NotoSerifSC-Bold', '/usr/share/fonts/truetype/noto-serif-sc/NotoSerifSC-Bold.ttf'))
pdfmetrics.registerFont(TTFont('LiberationSerif', '/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf'))
pdfmetrics.registerFont(TTFont('LiberationSerif-Bold', '/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf'))
pdfmetrics.registerFont(TTFont('LiberationSans', '/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf'))
pdfmetrics.registerFont(TTFont('DejaVuSans', '/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf'))
registerFontFamily('NotoSerifSC', normal='NotoSerifSC', bold='NotoSerifSC-Bold')
registerFontFamily('LiberationSerif', normal='LiberationSerif', bold='LiberationSerif-Bold')
registerFontFamily('LiberationSans', normal='LiberationSans', bold='LiberationSans')
registerFontFamily('DejaVuSans', normal='DejaVuSans', bold='DejaVuSans')

# Install font fallback for mixed CJK/Latin text
import sys
_scripts = '/home/z/my-project/skills/pdf/scripts'
if _scripts not in sys.path:
    sys.path.insert(0, _scripts)
from pdf import install_font_fallback
install_font_fallback()

# ━━ Page Setup ━━
PAGE_W, PAGE_H = A4
LEFT_MARGIN = 0.7 * inch
RIGHT_MARGIN = 0.7 * inch
TOP_MARGIN = 0.7 * inch
BOTTOM_MARGIN = 0.8 * inch
AVAILABLE_WIDTH = PAGE_W - LEFT_MARGIN - RIGHT_MARGIN

OUTPUT_DIR = '/home/z/my-project/download'
os.makedirs(OUTPUT_DIR, exist_ok=True)
BODY_PDF = os.path.join(OUTPUT_DIR, 'se_registrar_body.pdf')
FINAL_PDF = os.path.join(OUTPUT_DIR, 'se_domän_registratorer_jämförelse.pdf')

# ━━ Styles ━━
styles = {}

styles['title'] = ParagraphStyle(
    name='Title', fontName='LiberationSerif', fontSize=22, leading=28,
    textColor=TEXT_PRIMARY, alignment=TA_LEFT, spaceAfter=6
)
styles['h1'] = ParagraphStyle(
    name='H1', fontName='LiberationSerif', fontSize=18, leading=24,
    textColor=HEADER_FILL, alignment=TA_LEFT, spaceBefore=18, spaceAfter=8
)
styles['h2'] = ParagraphStyle(
    name='H2', fontName='LiberationSerif', fontSize=14, leading=20,
    textColor=ICON, alignment=TA_LEFT, spaceBefore=14, spaceAfter=6
)
styles['body'] = ParagraphStyle(
    name='Body', fontName='LiberationSerif', fontSize=10.5, leading=16,
    textColor=TEXT_PRIMARY, alignment=TA_JUSTIFY, spaceAfter=6
)
styles['body_left'] = ParagraphStyle(
    name='BodyLeft', fontName='LiberationSerif', fontSize=10.5, leading=16,
    textColor=TEXT_PRIMARY, alignment=TA_LEFT, spaceAfter=6
)
styles['bullet'] = ParagraphStyle(
    name='Bullet', fontName='LiberationSerif', fontSize=10.5, leading=16,
    textColor=TEXT_PRIMARY, alignment=TA_LEFT, leftIndent=18, spaceAfter=4,
    bulletIndent=6
)
styles['small'] = ParagraphStyle(
    name='Small', fontName='LiberationSerif', fontSize=9, leading=13,
    textColor=TEXT_MUTED, alignment=TA_LEFT, spaceAfter=4
)
styles['caption'] = ParagraphStyle(
    name='Caption', fontName='LiberationSerif', fontSize=9, leading=12,
    textColor=TEXT_MUTED, alignment=TA_CENTER, spaceBefore=3, spaceAfter=6
)
styles['th'] = ParagraphStyle(
    name='TH', fontName='LiberationSans', fontSize=8.5, leading=11,
    textColor=colors.white, alignment=TA_CENTER
)
styles['td'] = ParagraphStyle(
    name='TD', fontName='LiberationSans', fontSize=8, leading=11,
    textColor=TEXT_PRIMARY, alignment=TA_CENTER
)
styles['td_left'] = ParagraphStyle(
    name='TDLeft', fontName='LiberationSans', fontSize=8, leading=11,
    textColor=TEXT_PRIMARY, alignment=TA_LEFT
)
styles['td_bold'] = ParagraphStyle(
    name='TDBold', fontName='LiberationSans', fontSize=8, leading=11,
    textColor=TEXT_PRIMARY, alignment=TA_LEFT
)
styles['note'] = ParagraphStyle(
    name='Note', fontName='LiberationSerif', fontSize=8.5, leading=13,
    textColor=TEXT_MUTED, alignment=TA_LEFT, spaceAfter=4, leftIndent=12
)

def P(text, style_key='body'):
    return Paragraph(text, styles[style_key])

def make_table(data, col_widths, has_header=True):
    """Create a styled table."""
    t = Table(data, colWidths=col_widths, hAlign='CENTER')
    style_cmds = [
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('GRID', (0, 0), (-1, -1), 0.5, BORDER),
    ]
    if has_header:
        style_cmds.extend([
            ('BACKGROUND', (0, 0), (-1, 0), HEADER_FILL),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ])
        for i in range(1, len(data)):
            bg = colors.white if i % 2 == 1 else TABLE_STRIPE
            style_cmds.append(('BACKGROUND', (0, i), (-1, i), bg))
    t.setStyle(TableStyle(style_cmds))
    return t

# ━━ Content ━━
story = []

# --- Title Page Content (no cover in ReportLab, cover via HTML) ---
story.append(Spacer(1, 12))
story.append(P('<b>.SE Domain Registratorer - Komplett Jamforelse</b>', 'title'))
story.append(Spacer(1, 6))
story.append(P('Alla funktioner och priser for registratorer som säljer .se-domäner', 'body_left'))
story.append(Spacer(1, 6))
story.append(P('Mars 2026 | Priser kan andras', 'small'))
story.append(Spacer(1, 18))

# --- Background Section ---
story.append(P('<b>Viktigt om .SE-domäner</b>', 'h1'))
story.append(Spacer(1, 4))

story.append(P('<b>WHOIS-sekretess - Inbyggt i .SE</b>', 'h2'))
story.append(P(
    'Internetstiftelsen (som driver .se-topdomänen) döljer automatiskt personuppgifter i WHOIS-sökningar '
    'för alla .se-domäner, i enlighet med GDPR. Du behöver inte betala extra for WHOIS-sekretess / ID Protection '
    'for .se-domäner. Detta innebär att din integritet är skyddad från dag ett, oavsett vilken registrator du väljer. '
    'När någon gör en WHOIS-sökning på din .se-domän visas inte ditt namn, din e-postadress, ditt telefonnummer '
    'eller din hemadress. Detta skiljer sig markant från t.ex. .com-domäner där personuppgifterna är synliga '
    'for allmänheten om du inte aktivt köper WHOIS Privacy-tjänsten.'
))
story.append(Spacer(1, 6))

story.append(P('<b>DNSSEC for .SE</b>', 'h2'))
story.append(P(
    'Internetstiftelsen stöder automatisk DNSSEC-provisionering via CDS-poster, vilket möjliggör nyckelhantering '
    'utan manuell registratorinteraktion. DNSSEC signerar kryptografiskt dina DNS-svar, vilket förhindrar '
    'DNS-förfalskning (spoofing) och skyddar besökare från att hamna på falska webbplatser. Manga svenska '
    'registratorer erbjuder automatisk DNSSEC-signering utan extra kostnad. DNSSEC rekommenderas starkt '
    'for alla .se-domäner, särskilt for företagskritiska webbplatser där säkerhet är avgörande.'
))
story.append(Spacer(1, 6))

story.append(P('<b>Registry-Lock for .SE</b>', 'h2'))
story.append(P(
    'Registry-Lock är den högsta säkerhetsnivån du kan sätta på en domän. Den låser domänen på registernivå '
    '(hos Internetstiftelsen), inte bara hos din registrator. Detta innebär att även om någon får tillgång '
    'till ditt konto hos registratorn kan de inte flytta eller ändra domänen utan att också kringgå registrets lås. '
    'Registry-Lock förhindrar: domänöverföring, ändring av namnservrar, ändring av DNSSEC-nycklar och '
    'ändring av registrantuppgifter. Det är en betaltjänst som erbjuds av Internetstiftelsen, men inte alla '
    'registratorer erbjuder det vidare till sina kunder. HostUp är den enda registratorn som erbjuder '
    'gratis Registry-Lock for .se-domäner.'
))
story.append(Spacer(1, 6))

story.append(P('<b>Snapback / Backorder for .SE</b>', 'h2'))
story.append(P(
    'När en .se-domän löper ut går den genom en raderingsprocess. Snapback/backorder är en bevakningstjänst '
    'som automatiskt försöker registrera domänen i samma ögonblick den blir ledig, innan någon annan hinner '
    'ta den. Detta är användbart om du vill ha en domän som snart löper ut, om du råkat låta din egen domän '
    'löpa ut och vill ha tillbaka den, eller om du bevakar en specifik domän som någon annan inte förnyat. '
    'Om flera personer har snapback på samma domän går den oftast till auktion. Inte alla registratorer '
    'erbjuder denna tjänst for .se-domäner.'
))
story.append(Spacer(1, 18))

# --- Legend ---
story.append(P('<b>Teckenförklaring</b>', 'h2'))
legend_data = [
    [P('<b>Tecken</b>', 'th'), P('<b>Betydelse</b>', 'th')],
    [P('Ja', 'td'), P('Inkluderat utan extra kostnad', 'td_left')],
    [P('Kostnad', 'td'), P('Tillgängligt mot extra avgift', 'td_left')],
    [P('Nej', 'td'), P('Ej tillgängligt / stöds ej', 'td_left')],
    [P('Ej behov', 'td'), P('Inte nödvändigt (.SE döljer redan uppgifter)', 'td_left')],
    [P('?', 'td'), P('Ej bekräftat / oklart', 'td_left')],
]
legend_table = make_table(legend_data, [60, AVAILABLE_WIDTH - 60])
story.append(Spacer(1, 6))
story.append(legend_table)
story.append(Spacer(1, 18))

# ═══════════════════════════════════════════════
# MAIN COMPARISON TABLE - Swedish Registrars
# ═══════════════════════════════════════════════
story.append(P('<b>Svenska Registratorer</b>', 'h1'))
story.append(Spacer(1, 6))

se_header = [
    P('<b>Funktion</b>', 'th'),
    P('<b>Loopia</b>', 'th'),
    P('<b>Binero /<br/>Websupport</b>', 'th'),
    P('<b>Oderland</b>', 'th'),
    P('<b>Miss<br/>Hosting</b>', 'th'),
    P('<b>INFS</b>', 'th'),
    P('<b>Domainname<br/>shop</b>', 'th'),
    P('<b>Simply.com</b>', 'th'),
]

col_w = AVAILABLE_WIDTH
c0 = col_w * 0.14  # Feature name
c_each = (col_w - c0) / 7  # 7 registrars

se_data = [se_header]

rows = [
    ('Forstår pris', '289 SEK', '~289 SEK', '229 SEK', '139 SEK', '228 SEK', '275 NOK', '$19.90'),
    ('Förnyelsepris', '289 SEK', '~289 SEK', '229 SEK', '264 SEK', '228 SEK', '275 NOK', '$19.90'),
    ('Overföring', 'Inkl. 1 år', 'Inkl. 1 år', '275 SEK', 'Gratis', '228 SEK', 'Inkl. 1 år', 'Gratis'),
    ('WHOIS-sekretess', 'Ej behov', 'Ej behov', 'Ej behov', 'Ej behov', 'Ej behov', 'Ej behov', 'Ej behov'),
    ('Auto-DNSSEC', 'Ja', 'Ja', 'Ja', '?', 'Ja', 'Ja', 'Ja'),
    ('Snapback', 'Nej', 'Nej', 'Nej', 'Nej', 'Nej', 'Nej', 'Ja'),
    ('Registry-Lock', '?', '?', '?', '?', '?', '?', '?'),
    ('DNS-hantering', 'Ja*', 'Ja', 'Ja', 'Ja', 'Ja', 'Ja', 'Ja'),
    ('Epost-vidarebefodran', 'Kostnad', 'Kostnad', 'Kostnad', 'Kostnad', '22 SEK/man', 'Ja', 'Ja'),
    ('URL-vidarebefodran', 'Ja', 'Ja', 'Ja', 'Ja', 'Ja', 'Ja', 'Ja'),
    ('API', 'Ja', '?', '?', '?', '?', '?', 'Ja'),
    ('2FA', '?', '?', '?', '?', '?', '?', '?'),
    ('Gratis SSL', 'Nej', 'Nej', 'Nej', 'Ja**', 'Nej', 'Nej', 'Nej'),
    ('Endast domän', 'Ja', 'Ja', 'Ja', 'Ja', 'Ja', 'Ja', 'Ja'),
]

for feature, *values in rows:
    row = [P('<b>' + feature + '</b>', 'td_bold')]
    for v in values:
        row.append(P(v, 'td'))
    se_data.append(row)

se_table = make_table(se_data, [c0] + [c_each] * 7)
story.append(se_table)
story.append(Spacer(1, 4))
story.append(P('* Loopia: DNS hantering 108 SEK/ar utan webbhotell. ** Miss Hosting: SSL inkluderas endast med webbhotell.', 'note'))
story.append(Spacer(1, 18))

# ═══════════════════════════════════════════════
# INTERNATIONAL REGISTRARS
# ═══════════════════════════════════════════════
story.append(P('<b>Internationella Registratorer</b>', 'h1'))
story.append(Spacer(1, 6))

intl_header = [
    P('<b>Funktion</b>', 'th'),
    P('<b>Namecheap</b>', 'th'),
    P('<b>GoDaddy</b>', 'th'),
    P('<b>Hostinger</b>', 'th'),
    P('<b>Gandi</b>', 'th'),
    P('<b>HostUp</b>', 'th'),
    P('<b>Active24</b>', 'th'),
]

c0_i = col_w * 0.14
c_each_i = (col_w - c0_i) / 6

intl_data = [intl_header]

intl_rows = [
    ('Forstår pris', '~$18.98', '$43.99', '$23.99', '~$28.37', '9.90 EUR', '~20 EUR'),
    ('Förnyelsepris', '~$18.98', '~$43.99+', '$23.99', '~$28.37', '13.50 EUR', '~20 EUR'),
    ('Overföring', '~$18.98', 'EJ STOD', '~$23.99', '~$28.37', '9.90 EUR', 'Inkl. 1 år'),
    ('WHOIS-sekretess', 'Ej behov', 'Ej behov', 'Ej behov', 'Ej behov', 'Ej behov', 'Ej behov'),
    ('Auto-DNSSEC', 'Ja', 'Ja', 'Ja', 'Ja', 'Ja', 'Ja'),
    ('Snapback', '?', 'Nej', '?', '?', 'Nej', '?'),
    ('Registry-Lock', '?', '?', '?', '?', 'Ja (gratis)', '?'),
    ('DNS-hantering', 'Ja', 'Ja', 'Ja', 'Ja', 'Ja', 'Ja'),
    ('Epost-vidarebefodran', 'Ja', 'Kostnad', '?', 'Ja', '?', '?'),
    ('URL-vidarebefodran', 'Ja', 'Ja', 'Ja', 'Ja', '?', '?'),
    ('API', 'Ja (20+ dom)', 'Ja (50+ dom)', '?', 'Ja', '?', 'Ja (via Ascio)'),
    ('2FA', 'Ja', 'Ja', 'Ja', 'Ja', '?', '?'),
    ('Gratis SSL', 'Nej', 'Nej', 'Ja', 'Ja', 'Nej', 'Nej'),
    ('Endast domän', 'Ja', 'Ja', 'Ja', 'Ja', 'Ja', 'Ja'),
]

for feature, *values in intl_rows:
    row = [P('<b>' + feature + '</b>', 'td_bold')]
    for v in values:
        row.append(P(v, 'td'))
    intl_data.append(row)

intl_table = make_table(intl_data, [c0_i] + [c_each_i] * 6)
story.append(intl_table)
story.append(Spacer(1, 4))
story.append(P('GoDaddy: Stoder EJ inkommande overforing av .se-domäner. HostUp: Ända registratorn med gratis Registry-Lock for .SE.', 'note'))
story.append(Spacer(1, 18))

# ═══════════════════════════════════════════════
# NOT SUPPORTED / SPECIAL CASES
# ═══════════════════════════════════════════════
story.append(P('<b>Registratorer som EJ stoder .SE</b>', 'h1'))
story.append(Spacer(1, 6))

nosupport_data = [
    [P('<b>Registrator</b>', 'th'), P('<b>Orsak</b>', 'th'), P('<b>Kommentar</b>', 'th')],
    [P('Cloudflare', 'td'), P('Stoder ej .SE', 'td_left'), P('Kan anvandas for DNS/CDN med .se-domäner registrerade annorstädes', 'td_left')],
    [P('Hetzner', 'td'), P('Stoder ej .SE', 'td_left'), P('Begränsat TLD-utbud (t.ex. .de, .com, .eu)', 'td_left')],
    [P('SiteGround', 'td'), P('Kräver webbhotell', 'td_left'), P('Domänregistrering endast tillsammans med webbhotell', 'td_left')],
    [P('One.com', 'td'), P('Kopplat till hotell', 'td_left'), P('Domänregistrering mojlig men optimerad for webbhotellkunder', 'td_left')],
]
ns_table = make_table(nosupport_data, [col_w * 0.18, col_w * 0.25, col_w * 0.57])
story.append(ns_table)
story.append(Spacer(1, 18))

# ═══════════════════════════════════════════════
# DETAILED REGISTRAR PROFILES
# ═══════════════════════════════════════════════
story.append(P('<b>Detaljerade Registratorprofiler</b>', 'h1'))
story.append(Spacer(1, 8))

profiles = [
    {
        'name': '1. Loopia (loopia.se)',
        'desc': 'Sveriges största .SE-registrator med över 30% marknadsandel, ackrediterad sedan 1999. '
                'Loopia är den dominerande aktören på den svenska domänmarknaden och erbjuder pålitlig '
                'drift med ett väletablerat API. Standardpris är 289 SEK/år exkl. moms (361,25 SEK inkl. moms), '
                'med kampanjpris för de första 3 .se-domänerna ner till cirka 10 SEK/år. DNS-hantering utan '
                'webbhotell kostar 108 SEK/år extra, vilket gör det verkliga domänpriset cirka 397 SEK/år om du '
                'inte använder tredjeparts-DNS. LoopiaAPI bygger på XML-RPC och stöder domänsökning, '
                'registrering och DNS-zonhantering med max 60 anrop/minut och 15 domänsökningar/minut.',
    },
    {
        'name': '2. Binero / Websupport (binero.se)',
        'desc': 'Numera en del av Websupport/Team Blue-koncernen. Binero var historiskt en pionjär inom '
                'gratis automatisk DNSSEC-signering för .se-domäner och var en av de första svenska '
                'registratorerna att erbjuda detta. Priset ligger på cirka 289 SEK/år, i linje med Websupports '
                'prissättning. Sedan sammanslagningen med Websupport har domäntjänsterna blivit mindre '
                'framträdande i produktportföljen, med ökat fokus på molntjänster via Binero Cloud. '
                'Tidigare kampanjer har erbjudit .se-domäner for så lite som 15 SEK.',
    },
    {
        'name': '3. Oderland (oderland.se)',
        'desc': 'Ackrediterad .SE-registrator med konkurrenskraftig prissättning och gratis DNSSEC. '
                'Till 229 SEK/år exkl. moms får du både domänregistrering och FreeDNS inkluderat, '
                'vilket gör Oderland till ett av de bättre priserna för ackrediterade .SE-registratorer '
                'när man vill ha domän och DNS i samma paket. DNSSEC for .SE och .NU är gratis sedan '
                'maj 2020. Overföring kostar 250 SEK plus 25 SEK per domän for ägarbyte. Oderland '
                'erbjuder över 500 TLDs och kör ibland kampanjer for specifika domändelser.',
    },
    {
        'name': '4. Miss Hosting (misshosting.se)',
        'desc': 'Budgetvänlig registrator med aggressiv förstårprissättning på 139 SEK/år, men förnyelsen '
                'hoppar upp till 264 SEK/år. Gratis domänöverföring är en fördel. Miss Hosting är en del av '
                'Miss Group och erbjuder över 1300 TLDs. WHOIS-skydd marknadsförs som inkluderat, vilket '
                'är överflödigt for .SE-domäner. Kampanjer har erbjudit .se-domäner for så lite som 10 SEK '
                'forsta året. DNS-paket ingår och URL-vidarebefodran finns, men epost-vidarebefodran '
                'kräver sannolikt webbhotellstillägg.',
    },
    {
        'name': '5. INFS / Registrera Domän (infs.se)',
        'desc': 'Certifierad .SE-registrator med transparent prissättning på 228 SEK/år exkl. moms '
                '(285 SEK inkl. moms). Samma pris for registrering, förnyelse och överföring är noterbart. '
                'Ett unikt erbjudande är eposttillägget "Endast E-post" for 22 SEK/manad, vilket är perfekt '
                'for domänkunder som behöver epost utan webbhotell. Återställning av raderad domän kostar '
                '0 SEK och administrativa kontaktuppdateringar är gratis. Deras varumärke Webb.se '
                'annonserar ett RESTful API for domän/webbhotell/SSL-hantering.',
    },
    {
        'name': '6. Domainnameshop (domainnameshop.com)',
        'desc': 'Norsk registrator som stoder .SE till 275 NOK/år (cirka 25 USD). Solid renomme med '
                '4,9/5 i betyg baserat på 158 recensioner. DNS-hantering, DNSSEC, epost-vidarebefodran '
                'och URL-vidarebefodran ingår alla. Over 400 TLDs tillgängliga. Support via chatt, epost '
                'och telefon. Priset är i mitten for .SE-domäner men funktionsuppsättningen är komplett.',
    },
    {
        'name': '7. Simply.com (simply.com)',
        'desc': 'Fullständigt dansk registrator med RESTful JSON API, backorder och auto-DNSSEC. '
                'Simply.com utmärker sig med den mest kompletta funktionsuppsättningen for domänkunder: '
                'gratis överföring, gratis DNS med geografiskt separerade namnservrar, automatisk DNSSEC-signering, '
                'RESTful JSON API (endpoint: api.simply.com/2/), epost-vidarebefodran, URL-vidarebefodran med '
                'SEO-vänlig 301-redirect, OCH backorder/snapback-tjänst. Allt till $19,90/år. '
                'Surf Town har fusionerats in i Simply.com-varumärket.',
    },
    {
        'name': '8. Namecheap (namecheap.com)',
        'desc': 'Populär internationell registrator med solid funktionsuppsättning till cirka $18,98/år. '
                'Inkluderar gratis epost-vidarebefodran och URL-vidarebefodran med domänen. API tillgängligt '
                'for konton med 20+ domäner eller via särskild ansökan. Starka säkerhetsfunktioner med '
                '2FA (TOTP, U2F/FIDO2). DNSSEC stöds via DS-posthantering for anpassad DNS. WHOIS Privacy '
                'ingår gratis (överflödigt for .SE). PremiumDNS finns som betaltillägg. 24/7 support.',
    },
    {
        'name': '9. Gandi (gandi.net)',
        'desc': 'Funktionsrik europeisk registrator med "batteries included"-filosofi till cirka $28,37/år. '
                'Inkluderar obegränsad epost-alias/vidarebefodran, HTTPS-vidarebefodran, avancerad DNS-hantering '
                '(LiveDNS API), och 1 gratis SSL-certifikat. Komplett gratis API for domäner, DNS, webbhotell, '
                'epost och SSL. 2FA med säkerhetsnyckel/U2F/TOTP. Over 750 domändelser tillgängliga. '
                'Gandi är en av de bästa registratorerna for domänkunder som vill ha allt inkluderat '
                'utan dolda kostnader. Nu en del av Your.Online-koncernen.',
    },
    {
        'name': '10. HostUp (hostup.se)',
        'desc': 'Ackrediterad .SE- och .NU-registrator med det lägsta förnyelsepriset som hittats: '
                '9,90 EUR forsta året och 13,50 EUR/år i förnyelse. Unikt erbjudande: gratis Registry-Lock '
                'for .SE-domäner, vilket ingen annan registrator erbjuder utan extra kostnad. Inkluderar '
                'SmartDNSSEC och DNS SmartCopy for enkla överföringar. Betyg 4,7/5. HostUp är det '
                'klart billigaste alternativet for .SE-domäner och den enda registratorn med gratis '
                'Registry-Lock - en betydande säkerhetsfunktion for högvärdedomäner.',
    },
    {
        'name': '11. GoDaddy (godaddy.com) - EJ REKOMMENDERAD for .SE',
        'desc': 'Världens största registrator, MEN med stora begränsningar for .SE-domäner: du kan '
                'INTE överföra .SE-domäner TILL GoDaddy, backorder stöds ej for .SE, och priset är '
                'högst på $43,99/år. GoDaddys förnyelsepriser tenderar dessutom att öka över tid. '
                'DNS-hantering och DNSSEC stöds, API kräver 50+ domäner. Epost-vidarebefodran är '
                'extra betaltjänst. Av alla registratorer i denna jamforelse är GoDaddy det sämsta '
                'valet specifikt for .SE-domäner.',
    },
]

for profile in profiles:
    story.append(P('<b>' + profile['name'] + '</b>', 'h2'))
    story.append(P(profile['desc']))
    story.append(Spacer(1, 8))

# ═══════════════════════════════════════════════
# SUMMARY RANKINGS
# ═══════════════════════════════════════════════
story.append(Spacer(1, 6))
story.append(P('<b>Sammanfattning - Ranking</b>', 'h1'))
story.append(Spacer(1, 8))

story.append(P('<b>Billigast .SE - Första året</b>', 'h2'))
price1_data = [
    [P('<b>Plats</b>', 'th'), P('<b>Registrator</b>', 'th'), P('<b>Pris</b>', 'th'), P('<b>Kommentar</b>', 'th')],
    [P('1', 'td'), P('HostUp', 'td'), P('9,90 EUR (~110 SEK)', 'td'), P('Lägst pris + gratis Registry-Lock', 'td_left')],
    [P('2', 'td'), P('Miss Hosting', 'td'), P('139 SEK', 'td'), P('Kampanjpris; förnyelse 264 SEK', 'td_left')],
    [P('3', 'td'), P('Simply.com', 'td'), P('$19,90 (~210 SEK)', 'td'), P('Komplett funktionsuppsättning', 'td_left')],
    [P('4', 'td'), P('Oderland', 'td'), P('229 SEK', 'td'), P('Gratis DNS + DNSSEC', 'td_left')],
    [P('5', 'td'), P('INFS', 'td'), P('228 SEK', 'td'), P('Transparent prissättning', 'td_left')],
]
price1_table = make_table(price1_data, [col_w*0.08, col_w*0.18, col_w*0.25, col_w*0.49])
story.append(Spacer(1, 6))
story.append(price1_table)
story.append(Spacer(1, 14))

story.append(P('<b>Billigast .SE - Förnyelse (årligen)</b>', 'h2'))
price2_data = [
    [P('<b>Plats</b>', 'th'), P('<b>Registrator</b>', 'th'), P('<b>Pris</b>', 'th'), P('<b>Kommentar</b>', 'th')],
    [P('1', 'td'), P('HostUp', 'td'), P('13,50 EUR (~145 SEK)', 'td'), P('Lägsta förnyelsepris', 'td_left')],
    [P('2', 'td'), P('Simply.com', 'td'), P('$19,90 (~210 SEK)', 'td'), P('Inga dolda kostnader', 'td_left')],
    [P('3', 'td'), P('Oderland', 'td'), P('229 SEK', 'td'), P('Inkl. FreeDNS', 'td_left')],
    [P('4', 'td'), P('INFS', 'td'), P('228 SEK', 'td'), P('Samma pris registrering/förnyelse', 'td_left')],
    [P('5', 'td'), P('Namecheap', 'td'), P('~$18,98 (~200 SEK)', 'td'), P('Bra funktioner', 'td_left')],
]
price2_table = make_table(price2_data, [col_w*0.08, col_w*0.18, col_w*0.25, col_w*0.49])
story.append(Spacer(1, 6))
story.append(price2_table)
story.append(Spacer(1, 14))

story.append(P('<b>Bäst for domänregistrering utan webbhotell</b>', 'h2'))
feature1_data = [
    [P('<b>Plats</b>', 'th'), P('<b>Registrator</b>', 'th'), P('<b>Starkaste funktioner</b>', 'th')],
    [P('1', 'td'), P('Simply.com', 'td'), P('Gratis överföring, auto-DNSSEC, API, epost, URL, backorder - allt inkluderat', 'td_left')],
    [P('2', 'td'), P('Gandi', 'td'), P('Gratis epost, URL, SSL, API, 2FA - "batteries included" (högre pris)', 'td_left')],
    [P('3', 'td'), P('Namecheap', 'td'), P('Gratis epost/URL, 2FA, API - solid internationell registrator', 'td_left')],
]
feature1_table = make_table(feature1_data, [col_w*0.08, col_w*0.18, col_w*0.74])
story.append(Spacer(1, 6))
story.append(feature1_table)
story.append(Spacer(1, 14))

story.append(P('<b>Bäst säkerhet</b>', 'h2'))
security_data = [
    [P('<b>Kategori</b>', 'th'), P('<b>Registrator</b>', 'th'), P('<b>Funktion</b>', 'th')],
    [P('Registry-Lock', 'td'), P('HostUp', 'td'), P('Enda registratorn med gratis Registry-Lock for .SE', 'td_left')],
    [P('2FA', 'td'), P('Namecheap, Gandi, GoDaddy, Hostinger', 'td'), P('Stark autentisering for kontosäkerhet', 'td_left')],
    [P('DNSSEC', 'td'), P('Simply.com, Binero, Oderland', 'td'), P('Automatisk DNSSEC-signering gratis', 'td_left')],
]
security_table = make_table(security_data, [col_w*0.15, col_w*0.35, col_w*0.50])
story.append(Spacer(1, 6))
story.append(security_table)
story.append(Spacer(1, 14))

story.append(P('<b>Bäst API</b>', 'h2'))
api_data = [
    [P('<b>Plats</b>', 'th'), P('<b>Registrator</b>', 'th'), P('<b>API-typ</b>', 'th'), P('<b>Kommentar</b>', 'th')],
    [P('1', 'td'), P('Gandi', 'td'), P('Komplett REST API', 'td'), P('Domäner, DNS, SSL, epost - allt via API', 'td_left')],
    [P('2', 'td'), P('Simply.com', 'td'), P('RESTful JSON API', 'td'), P('Väldokumenterat med HTTP Basic Auth', 'td_left')],
    [P('3', 'td'), P('Loopia', 'td'), P('XML-RPC API', 'td'), P('Väletablerat; 60 anrop/min, 15 sökningar/min', 'td_left')],
]
api_table = make_table(api_data, [col_w*0.08, col_w*0.15, col_w*0.22, col_w*0.55])
story.append(Spacer(1, 6))
story.append(api_table)
story.append(Spacer(1, 14))

# ═══════════════════════════════════════════════
# KEY TAKEAWAYS
# ═══════════════════════════════════════════════
story.append(P('<b>Viktiga slutsatser</b>', 'h1'))
story.append(Spacer(1, 8))

takeaways = [
    'For absolut billigast .SE-domän: HostUp till 9,90 EUR/år forsta året, 13,50 EUR/år i förnyelse - OCH inkluderar gratis Registry-Lock. Detta är det mest kostnadseffektiva alternativet på marknaden.',
    'For basta funktioner med enbart domän: Simply.com erbjuder det mest kompletta paketet (API, DNSSEC, epost-vidarebefodran, URL-vidarebefodran, backorder) till $19,90/år utan dolda kostnader.',
    'WHOIS-sekretess är inget problem: .SE döljer redan personuppgifter på registernivå. Betala aldrig extra for detta for .se-domäner.',
    'DNSSEC bor aktiveras: De flesta svenska registratorer erbjuder det gratis. Se till att din valda registrator stoder automatisk DNSSEC-signering.',
    'Registry-Lock är sällsynt: HostUp är den enda registratorn som erbjuder gratis Registry-Lock for .SE. Om säkerhet är paramount for högvärdedomäner är detta mycket betydelsefullt.',
    'Undvik GoDaddy for .SE: Inga inkommande överföringar, inga backorders och premiumprissättning ($43,99/år). Det finns ingen anledning att välja GoDaddy for .se-domäner.',
    'Cloudflare och Hetzner stoder ej .SE: Använd dem for DNS/CDN istället, med din domän registrerad hos en annan registrator.',
]

for i, t in enumerate(takeaways, 1):
    story.append(P('<b>' + str(i) + '.</b> ' + t))
    story.append(Spacer(1, 4))

# ━━ Build ━━
doc = SimpleDocTemplate(
    BODY_PDF,
    pagesize=A4,
    leftMargin=LEFT_MARGIN,
    rightMargin=RIGHT_MARGIN,
    topMargin=TOP_MARGIN,
    bottomMargin=BOTTOM_MARGIN,
)

# Page number footer
def add_page_number(canvas, doc):
    canvas.saveState()
    canvas.setFont('LiberationSerif', 8)
    canvas.setFillColor(TEXT_MUTED)
    page_num = canvas.getPageNumber()
    text = f"Sida {page_num}"
    canvas.drawCentredString(PAGE_W / 2, 25, text)
    canvas.restoreState()

doc.build(story, onFirstPage=add_page_number, onLaterPages=add_page_number)
print(f"Body PDF generated: {BODY_PDF}")
