#!/usr/bin/env python3
"""WHM Komplett Handbok - PDF Generation Part 2 (Sections 8-13 + Build)"""

import os, pickle, hashlib
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
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

PAGE_W, PAGE_H = A4
L_MARGIN = 1.0 * inch
R_MARGIN = 1.0 * inch
T_MARGIN = 0.8 * inch
B_MARGIN = 0.8 * inch
CONTENT_W = PAGE_W - L_MARGIN - R_MARGIN
MAX_KEEP = PAGE_H * 0.4

# ── Styles ──
styles = {}
styles['body'] = ParagraphStyle('Body', fontName='LibSerif', fontSize=10.5, leading=16, alignment=TA_JUSTIFY, spaceAfter=6)
styles['h1'] = ParagraphStyle('H1', fontName='LibSerif', fontSize=20, leading=26, alignment=TA_LEFT, textColor=ACCENT, spaceBefore=18, spaceAfter=10)
styles['h2'] = ParagraphStyle('H2', fontName='LibSerif', fontSize=15, leading=20, alignment=TA_LEFT, textColor=TEXT_PRIMARY, spaceBefore=14, spaceAfter=8)
styles['h3'] = ParagraphStyle('H3', fontName='LibSerif', fontSize=12, leading=16, alignment=TA_LEFT, textColor=TEXT_PRIMARY, spaceBefore=10, spaceAfter=6)
styles['th'] = ParagraphStyle('TH', fontName='LibSerif', fontSize=9.5, leading=13, alignment=TA_CENTER, textColor=colors.white)
styles['td'] = ParagraphStyle('TD', fontName='LibSerif', fontSize=9, leading=12.5, alignment=TA_LEFT, wordWrap='CJK')
styles['note'] = ParagraphStyle('Note', fontName='LibSerif', fontSize=9.5, leading=14, alignment=TA_LEFT, textColor=TEXT_MUTED, leftIndent=12)
styles['toc_h1'] = ParagraphStyle('TOCH1', fontName='LibSerif', fontSize=13, leftIndent=20, leading=22)
styles['toc_h2'] = ParagraphStyle('TOCH2', fontName='LibSerif', fontSize=11, leftIndent=40, leading=18)

class TocDocTemplate(SimpleDocTemplate):
    def afterFlowable(self, flowable):
        if hasattr(flowable, 'bookmark_name'):
            level = getattr(flowable, 'bookmark_level', 0)
            text = getattr(flowable, 'bookmark_text', '')
            key = getattr(flowable, 'bookmark_key', '')
            self.notify('TOCEntry', (level, text, self.page, key))

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

# ── Load Part 1 story ──
with open('/home/z/my-project/download/whm_story_part1.pkl', 'rb') as f:
    story = pickle.load(f)

# ── SECTION 8: Server Configuration ──
story.append(heading('8. Server Configuration (Serverkonfiguration)', 'h1', 0))
story.append(body('Denna sektion innehaller installningar for hela servern. Manga av dessa gor du en gang vid uppstart och dor sedan inte om. ChemiCloud har redan konfigurerat de viktigaste installningarna, men du bor forsta vad de gor sa att du kan fatta egna beslut vid behov.'))
server_funcs = [
    ('Basic WebHost Manager Setup', 'Grundlaggande installningar: kontakt-e-post, namnservrar (ns1/ns2.chemicloud.com), standard-tema (Jupiter), standard-sprak och hemkatalog. Gor denna installning FORSTA gangen du loggar in i WHM.', 'Engangsinstallning vid uppstart'),
    ('Change Root Password', 'Andra root-losenordet for servern. Detta ar det viktigaste losenordet — det ger full atkomst till ALLT. Andra regelbundet och anvand alltid ett starkt losenord.', 'Regelbundet — var 3-6 manad'),
    ('CloudLinux Manager', 'Hantera CloudLinux LVE (Lightweight Virtual Environment) granser. CloudLinux isolerar varje konto sa att ett konto inte kan forbruka alla serverresurser. Du kan justera CPU-, minne- och IO-granser per konto.', 'Om en kund far "Resource Limit" fel'),
    ('Configure cPanel Analytics', 'Aktivera eller avaktivera cPanels inbyggda analysfunktioner som skickar anonymiserad anvandningsdata till cPanel LLC. De flesta avaktiverar detta av integritetsskal.', 'Avaktivera for maximal integritet'),
    ('Configure cPanel Cron Jobs', 'Hantera cPanels interna cron-jobb (schemalagda uppgifter). Dessa skoter automatiska uppgifter som backup, statistikberakning och certifikatförnyelse. Normalt behover du inte andra har.', 'Sallsan — ChemiCloud skoter'),
    ('Enable Quotas on a Virtuozzo VPS', 'Aktivera diskkvoter pa Virtuozzo-baserade VPS. ChemiCloud anvander KVM, sa denna funktion ar inte relevant for dig.', 'Ej relevant for ChemiCloud KVM'),
    ('Initial Quota Setup', 'Initialisera diskkvotsystemet. Detta bor redan vara gjort av ChemiCloud. Kor endast om diskkvoter inte fungerar.', 'Bara vid quota-problem'),
    ('Link Server Nodes', 'Lanka samman servrar for att dela e-posthantering. Avancerad funktion for stora driftmiljoer med separata webb- och e-postservrar.', 'Avancerat — sallsan behov'),
    ('Server Profile', 'Valj serverprofil: "Standard" (allt installerat), "DNS" (endast DNS), "Mail" (endast e-post). For din reseller-server ar Standard ratt profil.', 'Engangsinstallning — Standard'),
    ('Statistics Software Configuration', 'Konfigurera vilka statistikprogram som ska kora: AWStats, Webalizer, Analog, ModLogan. AWStats ar mest detaljerat och rekommenderas. Du kan aven stalla in hur ofta statistiken ska uppdateras.', 'Aktivera AWStats for alla domaner'),
    ('Terminal in WHM', 'Inbyggd terminal i WHM for att kora kommandon direkt pa servern. Anvandbart for avancerad felsokning utan extern SSH-klient.', 'Avancerad felsokning'),
    ('Tweak Settings', 'Over 100 fininstallningar i 18 kategorier. Se separat genomgang i sektion 8.1.', 'Vid specifika behov'),
]
story.append(make_table(['Funktion', 'Forklaring', 'Nar du behover den'], server_funcs, [0.22, 0.55, 0.23]))
story.append(sp(8))

# Tweak Settings
story.append(heading('8.1 Tweak Settings — Kategorier och viktiga installningar', 'h2', 1))
story.append(body('Tweak Settings ar en samling av over 100 fininstallningar uppdelade i 18 kategorier. De flesta behover du aldrig andra, men har ar de viktigaste kategorierna och installningarna du bor känna till:'))
tweak_cats = [
    ('Mail', 'Max emails per timme per doman, SpamAssassin pa/av, Spam Box pa/av, e-postarkivering, mailformat (mdbox/maildir), autentiseringsinstallningar. De viktigaste: stall "Max hourly emails per domain" till 100-500 och aktivera Spam Box.'),
    ('Domains', 'Tillat oregistrerade domaner, auto-lagg till A-poster for namnservrar, aktivera DKIM/SPF/DMARC for nya konton, Thunderbird/Outlook autodiscover. Viktigast: aktivera DKIM/SPF/DMARC for nya konton.'),
    ('Security', 'Krav SSL for cPanel/WHM, Cookie IP-validering, jailshell, losenordsstyrka, kärndumpar, signaturvalidering. Viktigast: "Require SSL for cPanel Services" = On, Cookie IP validation = Strict.'),
    ('PHP', 'cPanel PHP max execution time, memory limit, max POST size, max upload size, PHP loader (ionCube). Viktigast: memory limit 128 MB, max upload 64 MB for restaurangbilder.'),
    ('Display', 'Standardtema, antal konton per sida, visa disk- och filanvandning. Du kan andra "Number of accounts per page" om du har manga kunder.'),
    ('SQL', 'Krav pa anvandarnamnsprefix for databaser (rekommenderas), tillat fjarratkomst. Viktigast: "Require username prefix" = On for sakerhet.'),
    ('Stats and Logs', 'Konfigurera statistik- och logginstallningar: hur ofta loggar roterar, vilka program som kors, lagringstid. Normalt behover du inte andra har.'),
    ('System', 'Vilka anvandare som kan logga in i cPanel, Apache-portar, ChkServd-intervall (hur ofta tjhanster overvakas). Viktigast: "Accounts that can access cPanel" = Root+Owner+User.'),
]
story.append(make_table(['Kategori', 'Viktiga installningar'], tweak_cats, [0.12, 0.88]))

# ── SECTION 9: Software ──
story.append(heading('9. Software (Mjukvara)', 'h1', 0))
software_funcs = [
    ('EasyApache 4', 'Bygga och hantera Apache/PHP-moduler. Du kan installera PHP-versioner, tillagga moduler som mod_security, och konfigurera PHP-handlers. For resellers bor ChemiCloud ha konfigurerat detta redan.', 'Sallsan — ChemiCloud skoter'),
    ('MultiPHP Manager (System)', 'Stalla in standard PHP-version for hela servern. Rekommenderat: PHP 8.2 eller 8.3 for WordPress. Du kan aven stalla in per doman.', 'Vid serveruppstart — stalla till 8.2/8.3'),
    ('MultiPHP Manager (User)', 'Stalla in PHP-version per doman for enskilda konton. Detta ar det verktyg du anvander nar en kunds WordPress kraver en specifik PHP-version.', 'Nar kundens sajt behover specifik PHP'),
    ('MultiPHP INI Editor', 'Andra php.ini-installningar per doman: memory_limit, upload_max_filesize, max_execution_time, post_max_size, disable_functions. Viktigt for WordPress med stora bilder.', 'Nar kundens WordPress klagar pa for lite minne'),
    ('NGINX Manager', 'Hantera NGINX som reverse proxy for Apache. ChemiCloud anvander LiteSpeed, sa denna funktion kan ha begransad relevans.', 'Sallsan — ChemiCloud anvander LiteSpeed'),
    ('PHP PEAR Packages', 'Installera PEAR-paket (PHP Extension and Application Repository). PEAR ar en aldre pakethanterare for PHP — de flesta moderna projekt anvander Composer istallet.', 'Sallsan — moderna projekt anvander Composer'),
    ('PHP PECL', 'Installera PECL-tillagg (PHP extension community library). PECL innehaller C-niva-tillagg for PHP som Redis, Memcached osv. Normalt behover du inte installera dessa.', 'Avancerat — for specifika PHP-tillagg'),
    ('Install a Perl Module', 'Installera Perl-moduler fran CPAN. Sallsan behov — de flesta moderna webbappar anvander inte Perl.', 'Mycket sallsan'),
    ('Install Distro Packages', 'Installera operativsystemspaket (yum/apt). Som reseller har du oftast inte ratt att installera OS-paket — det skoter ChemiCloud.', 'ChemiCloud skoter'),
    ('Module Installers', 'Gemensam granssnitt for att installera Perl-, PHP- och Ruby-moduler. Se enskilda funktioner ovan.', 'Sallsan'),
    ('Ruby Gem Installer', 'Installera Ruby Gems (pakethanterare for Ruby). Sallsan behov for restauranghemsidor.', 'Mycket sallsan'),
    ('System Update', 'Kora systemuppdateringar. ChemiCloud skoter automatiska uppdateringar, sa du behover normalt inte gora detta manuellt.', 'ChemiCloud skoter automatiskt'),
    ('Update Server Software', 'Uppdatera servermjukvara (Apache, PHP, MySQL osv.). Precis som System Update skoter ChemiCloud detta.', 'ChemiCloud skoter automatiskt'),
    ('Rebuild RPM Database', 'Aterbygga RPM-databasen om den har skadats. Detta ar ett felsokningsverktyg som du sallsan behover.', 'Endast vid RPM-databasfel'),
    ('WP Toolkit for WHM', 'Hantera alla WordPress-installationer pa servern fran en central plats. Du kan uppdatera, sakerhetskopiera, klona och migrera WordPress-sajter. Detta ar ett av dina viktigaste verktyg!', 'Dagligen — hantera alla restaurangers WordPress'),
]
story.append(make_table(['Funktion', 'Forklaring', 'Nar du behover den'], software_funcs, [0.20, 0.55, 0.25]))

# ── SECTION 10: SSL/TLS ──
story.append(heading('10. SSL/TLS', 'h1', 0))
story.append(body('SSL/TLS-kryptering ar ett MASTE for alla hemsidor idag. Utan HTTPS varnar webblasaren besokarna, Google sanker din ranking i sokresultat, och restaurangens besokare misstror sidan. ChemiCloud inkluderar gratis Let\'s Encrypt SSL-certifikat som fornyas automatiskt. Har ar de 7 SSL-funktionerna:'))
ssl_funcs = [
    ('Generate an SSL Certificate and Signing Request', 'Skapa ett nytt SSL-certifikat och en Certificate Signing Request (CSR). En CSR anvands nar du vill kopa ett betalt SSL-certifikat fran en certifikatutfardare. For de flesta restauranger racker gratis Let\'s Encrypt.', 'Bara nar du behov ett betalt certifikat'),
    ('Install an SSL Certificate on a Domain', 'Installera ett SSL-certifikat manuellt pa en doman. Du klistrar in certifikatet och den privata nyckeln. Let\'s Encrypt installeras automatiskt, sa du behover bara detta for betalda certifikat.', 'For betalda SSL-certifikat'),
    ('Manage AutoSSL', 'Hantera automatisk SSL-certifikat-utfordning och fornyelse. Let\'s Encrypt ar standardleverantor och fornyar certifikat var 90:e dag automatiskt. Du kan se vilka domaner som har certifikat och vilka som saknar. Kontrollera att AutoSSL ar aktiverat!', 'Kontrollera att Let\'s Encrypt AutoSSL ar pa'),
    ('Manage SSL Hosts', 'Visa alla SSL-certifikat installerade pa servern med detaljer: doman, utfardare, utgangsdatum, typ. Bra oversikt for att se vilka certifikat som snart loser giltighet.', 'Oversikt av alla certifikat'),
    ('Purchase and Install an SSL Certificate', 'Kopa ett SSL-certifikat direkt fran cPanel Market (integrerad tjhst). Vanligtvis onodigt eftersom Let\'s Encrypt ar gratis och tillrackligt for restauranghemsidor.', 'Sallsan — Let\'s Encrypt racker'),
    ('SSL Storage Manager', 'Hantera lagrade SSL-certifikat och nycklar. Du kan radera gamla certifikat, verifiera nycklar och se vilka certifikat som ar kopplade till vilka domaner.', 'Radera gamla certifikat'),
    ('SSL/TLS Configuration', 'Globala SSL-installningar: protokollversioner (TLS 1.2, 1.3), chiffer, SNI-konfiguration. Viktigt: avaktivera gamla osakra protokoll som SSLv3 och TLS 1.0/1.1.', 'Sakerhardskonfiguration — avaktivera gamla protokoll'),
]
story.append(make_table(['Funktion', 'Forklaring', 'Nar du behover den'], ssl_funcs, [0.20, 0.55, 0.25]))

# ── SECTION 11: Backup ──
story.append(heading('11. Backup (Sakerhetskopior)', 'h1', 0))
backup_funcs = [
    ('Backup Configuration', 'Konfigurera automatiska sakerhetskopior: typ (full/inkrementell), schema (dagligen/veckovis), lagringsplats (lokal/fjarr), komprimering, uteslutna filer. ChemiCloud skoter basen med 30 dagars historik, men du kan finjustera.', 'Engangsinstallning — kontrollera att backup ar pa'),
    ('Backup Restoration', 'Aterstalla ett helt cPanel-konto fran en sakerhetskopia. Du valjer datum och vilka delar som ska aterstallas (filer, databaser, e-post, DNS). Detta ar livforsakringen nar nagot gar fel!', 'Nar en kund raderat nagot av misstag'),
    ('Backup System Migration', 'Migrera sakerhetskopior fran ett annat system (t.ex. fran en annan hostingleverantor). Anvandbart nar du flyttar kunder fran en gammal server.', 'Vid migration fran annan server'),
    ('Backup User Selection', 'Valj vilka cPanel-konton som ska inkluderas i automatiska sakerhetskopior. Som standard backas alla konton upp, men du kan utesluta specifika konton om du vill.', 'Avaktivera backup for testkonton'),
    ('File and Directory Restoration', 'Aterstalla enskilda filer och mappar fran sakerhetskopia, istallet for hela kontot. Detta ar mycket snabbare och mer precist an att aterstalla allt.', 'Nar en specifik fil raderats eller skadats'),
]
story.append(make_table(['Funktion', 'Forklaring', 'Nar du behover den'], backup_funcs, [0.20, 0.55, 0.25]))

# ── SECTION 12: All Other Sections ──
story.append(heading('12. Ovriga sektioner', 'h1', 0))

story.append(heading('12.1 Account Information', 'h2', 1))
ai = [('List Accounts', 'Visa alla konton med doman, IP, paket och diskbandbreddsanvandning.'), ('List Parked Domains', 'Lista alla parkerade domaner (alias) pa servern.'), ('List Subdomains', 'Lista alla underdomaner pa servern.'), ('List Suspended Accounts', 'Visa alla suspenderade konton och anledningen till suspenderingen.'), ('Show Accounts Over Quota', 'Visa konton som overskridit sin diskkvot.'), ('View Bandwidth Usage', 'Visa bandbreddsanvandning for alla konton.')]
story.append(make_table(['Funktion', 'Forklaring'], ai, [0.25, 0.75]))

story.append(heading('12.2 Database Services / SQL Services', 'h2', 1))
db_funcs = [('Change Database Root Password', 'Andra root-losenordet for MySQL/MariaDB. Gors sallsan och med forsiktighet.'), ('Change Database User Password', 'Andra losenord for en specifik databasanvandare.'), ('Configure PostgreSQL', 'Konfigurera PostgreSQL (om installerat). De flesta anvander bara MySQL.'), ('Database Map Tool', 'Koppla databaser till ratt cPanel-konto. Anvands vid migrering eller om databaser hamnat pa fel konto.'), ('Edit SQL Configuration', 'Redigera MySQL/MariaDB-konfiguration (my.cnf). Avancerat — andra bara om du vet vad du gor.'), ('Manage Database Users', 'Hantera databasanvandare och deras rattigheter.'), ('Manage Databases', 'Hantera databaser: skapa, radera, reparera.'), ('Manage MySQL Profiles', 'Hantera MySQL-profiler for att ansluta till fjarrdatabaser. Avancerat.'), ('MySQL/MariaDB Upgrade', 'Uppgradera databasservern. ChemiCloud skoter detta.'), ('Repair a MySQL Database', 'Reparera en skadad databas. Forsta atgarden vid databasfel.'), ('Show MySQL Processes', 'Visa aktiva databasprocesser. For att identifiera langsamma fragor eller lasningar.'), ('Reset MySQL Root Password', 'Aterstall root-losenordet for MySQL. Anvands om du har glomt det.')]
story.append(make_table(['Funktion', 'Forklaring'], db_funcs, [0.25, 0.75]))

story.append(heading('12.3 IP Functions', 'h2', 1))
ip_funcs = [('Add a New IP Address', 'Lagg till en ny IP-adress pa servern. ChemiCloud skoter IP-tilldelning.'), ('Assign IPv6 Address', 'Tilldela IPv6-adresser. Framtidens standard men sallsan nodvandigt idag.'), ('Configure Remote Service IPs', 'Konfigurera IP-adresser for fjarrtjhster (t.ex. MySQL, DNS). Avancerat.'), ('IP Migration Wizard', 'Migrera konton fran en IP till en annan. Anvands vid IP-andringar.'), ('Rebuild the IP Address Pool', 'Aterbygg poolen av tillgangliga IP-adresser. Felsokningsverktyg.'), ('Show IP Address Usage', 'Visa vilka IP-adresser som anvands och av vilka konton.'), ('Show/Edit Reserved IPs', 'Hantera reserverade IP-adresser som inte ska tilldelas automatiskt.')]
story.append(make_table(['Funktion', 'Forklaring'], ip_funcs, [0.25, 0.75]))

story.append(heading('12.4 Resellers', 'h2', 1))
story.append(body('Som reseller hanterar du dina kunder direkt. Dessa funktioner ar mest relevanta om du sjalv har under-resellers (nagon som sacker hemsidor via dig). De viktigaste ar: Edit Reseller Nameservers (stall in dina namnservrar), Reseller Center (oversikt over reseller-konton), och View Reseller Usage (se resursanvandning).'))

story.append(heading('12.5 Service Configuration', 'h2', 1))
svc = [('Apache Configuration', 'Hantera Apache-webbserverns konfiguration: Global Configuration, Include Editor, DirectoryIndex Priority. Avancerat.'), ('Exim Configuration Manager', 'Konfigurera Exim e-postserver: sakerhet, autentisering, ACL:er, rutning. Avancerat men viktigt for e-postleverans.'), ('FTP Server Configuration', 'Konfigurera FTP-servern (portar, passivt lasge, TLS). Normalt behover du inte andra har.'), ('Nameserver Selection', 'Valj vilken DNS-server som ska anvandas: BIND, PowerDNS, MyDNS. ChemiCloud har redan valt ratt.'), ('PHP Configuration Editor', 'Redigera server-wide php.ini. Mer detaljerad an MultiPHP INI Editor.'), ('Service Manager', 'Aktivera/avaktivera och hantera overvakning av tjhster (Apache, MySQL, Exim, FTP, SSH osv.). Om en tjhst kraschar kan den automatiskt startas om.')]
story.append(make_table(['Funktion', 'Forklaring'], svc, [0.25, 0.75]))

story.append(heading('12.6 Plugins (ChemiCloud-tillagg)', 'h2', 1))
plugins = [('Comet Backup', 'ChemiClouds backup-system. Hantera och overvaka automatiska sakerhetskopior. 30 dagars historik ingar.'), ('Configure ClamAV Scanner', 'Konfigurera ClamAV antivirus-skanner. Kan skanna filer och e-post efter virus. Kompletterar Imunify360.'), ('Server Monitoring (360 Monitoring)', 'Overvaka serverns tillganglighet och prestanda. Aviseringar via e-post om servern gar ner eller presterar daligt.'), ('WP Toolkit for WHM', 'Hantera alla WordPress-installationer centralt. Uppdatera, sakerhetskopiera, klona och migrera WordPress-sajter. Ett av dina viktigaste verktyg!')]
story.append(make_table(['Plugin', 'Forklaring'], plugins, [0.20, 0.80]))

story.append(heading('12.7 Server Status', 'h2', 1))
status = [('Apache Status', 'Visa Apaches realtidsstatus: aktiva anslutningar, forfragan, arbetarprocesser.'), ('Daily Process Log', 'Visa vilka konton som anvant mest CPU och minne under dagen. Viktigt for att identifiera resurskravande kunder.'), ('Server Information', 'Visa serverns hardvaruspecifikationer: CPU, RAM, disk, OS-version, Perl/PHP-versioner.'), ('Service Status', 'Visa status for alla tjhster: Apache, MySQL, Exim, FTP, DNS, SSH. Gront = OK, rtt = problem.'), ('Task Queue Monitor', 'Overvaka bakgrundsjobb som kors pa servern (backup, statistik, certifikatförnyelse).')]
story.append(make_table(['Funktion', 'Forklaring'], status, [0.22, 0.78]))

story.append(heading('12.8 Ovriga sektioner (kort beskrivning)', 'h2', 1))
other = [('Clusters', 'Hantera DNS- och konfigurationskluster for redundans mellan servrar. Avancerat, sallsan behov for resellers.'), ('cPanel', 'Hantera cPanel-teman, plugins, nyhetsmeddelanden och uppdateringar. Customization ar viktigast — branda cPanel med din logga.'), ('Development', 'API-verktyg, hook-hantering, API-tokens for automatisering. For utvecklare som vill automatisera WHM-uppgifter.'), ('Locales', 'Hantera sprakfiler for WHM/cPanel. Svenska finns som standard, men du kan anpassa oversattningar.'), ('Market', 'Hantera cPanel Market for att salja SSL-certifikat och domen registrering direkt i cPanel. Sallsan anvant.'), ('Networking Setup', 'Andra hostname och resolver-konfiguration. Bor redan vara installt av ChemiCloud.'), ('Restart Services', 'Starta om enskilda tjhster (Apache, MySQL, DNS osv.) utan att starta om hela servern. Anvandbart vid konfigurationsandringar.'), ('Server Contacts', 'Konfigurera kontakt-e-post och aviseringar for serverhahndelser. Contact Manager ar viktigast — stall in din e-post.'), ('Support', 'Skapa supportarenden hos cPanel/ChemiCloud och ge supportpersonal tillgang till din server for felsokning.'), ('System Health', 'Overvaka serverprocesser, disk och systemresurser. Process Manager later dig doda processer som forbrukar for mycket.'), ('System Reboot', 'Starta om hela servern. Gors BARA som sista utvag — foretra da att starta om enskilda tjhster istallet.')]
story.append(make_table(['Sektion', 'Beskrivning'], other, [0.18, 0.82]))

# ── SECTION 13: Glossary ──
story.append(heading('13. Ordlista / Glossary', 'h1', 0))
story.append(body('Har forklarar jag alla tekniska termer du kan stota pa i WHM, i alfabetisk ordning. Dessa forklaringar ar skrivna for nagon som ar nyborjare pa webbhotell och serverhantering.'))
glossary = [
    ('Addon Domain', 'En extra doman som laggs till ett cPanel-konto och visar en helt egen hemsida. Exempel: om restaurang.se ar huvuddomanen kan catering.se vara en addon domain som visar en annan sajt pa samma konto.'),
    ('AutoSSL', 'cPanels funktion for automatisk utfordning och fornyelse av SSL-certifikat. Let\'s Encrypt ar standardleverantor. AutoSSL ser till att alla domaner alltid har ett giltigt certifikat utan manuell hantering.'),
    ('Bandbredd (Bandwidth)', 'Den mangd data som far overforas mellan servern och besokarna under en manad. Varje sidladdning, bildvisning, e-post och filnedladdning forbrukar bandbredd.'),
    ('CGI (Common Gateway Interface)', 'En gammal standard for att lata webbservern kora program och returnera resultatet som HTML. Moderna webbappar (inklusive WordPress) anvander PHP istallet och behover inte CGI.'),
    ('CloudLinux', 'Ett operativsystem som isolerar varje konto pa servern genom LVE (Lightweight Virtual Environment). Forhindrar att ett konto forbrukar alla serverresurser och paverkar andra kunder.'),
    ('cPHulk', 'cPanels inbyggda skydd mot brute-force-attacker (upprepade felaktiga inloggningsforsok). Blockerar automatiskt IP-adresser som forsoker gissa losenord.'),
    ('Cron Job', 'En schemalagd uppgift som kors automatiskt vid specifika tider. WordPress anvander cron for schemalagda inlagg, uppdateringar och sakerhetskopior.'),
    ('CSF (ConfigServer Security & Firewall)', 'En popular brandvagg for Linux-servrar. Hanterar IP-blockering, port-konfiguration, landblockering och intrangsdetektering.'),
    ('DKIM (DomainKeys Identified Mail)', 'En e-postsakerhetsstandard som lagger till en digital signatur pa utgende e-post. Mottagaren kan verifiera att meddelandet verkligen kommer fran din server och inte har manipulerats under transport.'),
    ('DMARC', 'Bygger pa SPF och DKIM och anger vad mottagaren ska gora om ett meddelande inte klarar autentiseringen (t.ex. avvisa, skicka till spam, eller skicka en rapport till avsandaren).'),
    ('DNS (Domain Name System)', 'Internets telefonkatalog som oversatter domannamn (restaurang.se) till IP-adresser (192.168.1.1). Utan DNS kan ingen hitta din hemsida.'),
    ('FTP (File Transfer Protocol)', 'Ett protokoll for att overfora filer mellan din dator och servern. Anvands for att ladda upp bilder, dokument och andra filer till hemsidan.'),
    ('Greylisting', 'En anti-spam-teknik som tillfalligt avvisar den forsta leveransforsoket fran en okand e-postserver. Legitima servers forsoker igen efter en stund, medan spam-servers ofta ger upp.'),
    ('Imunify360', 'En sakerhetsplattform som kombinerar antivirus, brandvagg, intrangsdetektering och patch-hantering. Ingars i ChemiClouds hosting.'),
    ('Inode', 'En datastruktur som representerar en fil pa filsystemet. Varje fil, mapp, e-postmeddelande och symbolisk lank anvander en inode. Om du nar inode-gransen kan du inte skapa fler filer, aven om du har diskutrymme kvar.'),
    ('Jailshell', 'En begransad version av shell/SSH dar anvandaren ar "inspad" i sin egen hemkatalog och inte kan se eller paverka andras filer. Mycket sakerre an normal shell.'),
    ('KernelCare', 'En tjhst som automatiskt applicerar sakerhetsuppdateringar for Linux-klarnan utan att behova starta om servern. Ingars i ChemiClouds hosting.'),
    ('Let\'s Encrypt', 'En gratis, automatiserad och oppen certifikatutfardare (CA) som tillhandahaller SSL/TLS-certifikat. Certifikaten ar giltiga i 90 dagar och fornyas automatiskt av AutoSSL.'),
    ('LiteSpeed', 'En hogpresterande webbserver som ersatter Apache. ChemiCloud anvander LiteSpeed som ger snabbare sidladdning, battre caching och lagre resursanvandning.'),
    ('LVE (Lightweight Virtual Environment)', 'CloudLinux teknik som skapar en isolerad miljo for varje konto med egna CPU-, minne- och IO-granser. Forhindrar att ett konto tar over hela servern.'),
    ('Maildir', 'Ett e-postlagringsformat dar varje meddelande sparas som en separat fil. Enklare men kan bli langsamt med manga meddelanden.'),
    ('MDBox', 'Ett e-postlagringsformat dar alla meddelanden i en postlada sparas i en enda fil. Mer effektivt och snabbare an Maildir for stora postlador.'),
    ('ModSecurity / WAF', 'En Web Application Firewall (WAF) som skyddar mot vanliga webbattacker som SQL injection, XSS (cross-site scripting) och filinklusion. WAF-regler kan ibland blockera legitim trafik, sa du kan behova avaktivera enskilda regler.'),
    ('MX Record', 'En DNS-post som anger vilken server som hanterar inkommande e-post for en doman. Utan ratt MX-record hamnar inte e-posten ratt.'),
    ('Parked Domain (Alias)', 'En doman som visar exakt samma innehall som huvuddomanen. Exempel: restaurang.com ar en parked domain for restaurang.se — bada visar samma hemsida.'),
    ('Passenger', 'En application server for Ruby on Rails, Python och Node.js-appar. Anvands sallsan for restauranghemsidor som typiskt kors pa WordPress/PHP.'),
    ('PTR Record / rDNS', 'Reverse DNS — oversatter en IP-adress tillbaka till ett domannamn. Mange e-posttjhster (sarskilt Gmail) kraver att din server har en giltig PTR-record for att acceptera din e-post.'),
    ('Shell Access / SSH', 'Tillgang till serverns kommandotolk via SSH-protokollet. Ger full kontroll over servern fran en terminal. Bor begransas av sakerhetsskal — anvand jailshell om nodvandigt.'),
    ('SNI (Server Name Indication)', 'En teknik som later flera SSL-certifikat dela samma IP-adress. Utan SNI behover varje SSL-certifikat en egen dedikerad IP. SNI ar standard idag och gor dedicated IP overflodigt for de flesta.'),
    ('SpamAssassin', 'En automatiserad spamfilter som analyserar inkommande e-post och ger den en poang baserat pa hur mycket det liknar spam. Hog poang = trolig spam.'),
    ('Spam Box', 'En installning i SpamAssassin som bestammer att spam-meddelanden ska flyttas till en separat "spam"-mapp istallet for att raderas. Detta later kunden granska falska positiva innan radering.'),
    ('SPF (Sender Policy Framework)', 'En DNS-baserad standard som anger vilka e-postservrar som ar tillatna att skicka e-post fran en doman. Forhindrar e-postforfalskning.'),
    ('SSH', 'Secure Shell — ett krypterat protokoll for att logga in pa en server och kora kommandon. Sakersre an vanlig Telnet/FTP.'),
    ('SSL/TLS', 'Secure Sockets Layer / Transport Layer Security — krypteringsprotokoll som skyddar kommunikationen mellan webblasaren och servern. Ser till att losenord, kreditkortsnummer och annan kanslig data inte kan avlyssnas.'),
    ('Subdoman', 'En underdoman till huvuddomanen. Exempel: meny.restaurang.se, bokning.restaurang.se. Varje subdoman kan ha eget innehall.'),
    ('TTL (Time to Live)', 'Ett varde i DNS-poster som anger hur lange andra DNS-servrar far spara posten i cache innan de maste fraga igen. Lagre TTL = snabbare uppdateringar men mer trafik. Hogre TTL = langsammare uppdateringar men mindre trafik.'),
]
for term, desc in glossary:
    story.append(Paragraph('<b>%s</b> — %s' % (term, desc), styles['body']))
    story.append(sp(3))

# ── BUILD PDF ──
output_path = '/home/z/my-project/download/whm-komplett-handbok.pdf'

doc = TocDocTemplate(
    output_path,
    pagesize=A4,
    leftMargin=L_MARGIN,
    rightMargin=R_MARGIN,
    topMargin=T_MARGIN,
    bottomMargin=B_MARGIN,
    title='WHM Komplett Handbok',
    author='RestWeb',
    creator='Z.ai',
    subject='Komplett genomgang av alla WHM-funktioner och installningar',
)

# Insert TOC at beginning (after a title)
toc_story = []
toc_story.append(Paragraph('<b>WHM Komplett Handbok</b>', ParagraphStyle('CoverTitle', fontName='LibSerif', fontSize=28, leading=36, alignment=TA_CENTER, textColor=ACCENT, spaceBefore=120)))
toc_story.append(Paragraph('Web Host Manager — Alla funktioner och installningar forklarade', ParagraphStyle('CoverSub', fontName='LibSerif', fontSize=14, leading=20, alignment=TA_CENTER, textColor=TEXT_MUTED, spaceAfter=40)))
toc_story.append(Paragraph('2026-05-15 | RestWeb', ParagraphStyle('CoverMeta', fontName='LibSerif', fontSize=11, leading=16, alignment=TA_CENTER, textColor=TEXT_MUTED, spaceAfter=60)))
toc_story.append(PageBreak())

toc = TableOfContents()
toc.levelStyles = [styles['toc_h1'], styles['toc_h2']]
toc_story.append(Paragraph('<b>Innehallsforteckning</b>', ParagraphStyle('TOCTitle', fontName='LibSerif', fontSize=18, leading=24, alignment=TA_CENTER, spaceAfter=20)))
toc_story.append(toc)
toc_story.append(PageBreak())

# Combine
full_story = toc_story + story

doc.multiBuild(full_story)
print(f"PDF generated: {output_path}")

# Add metadata
from pypdf import PdfReader, PdfWriter
reader = PdfReader(output_path)
writer = PdfWriter()
for page in reader.pages:
    writer.add_page(page)
writer.add_metadata({'/Title': 'WHM Komplett Handbok', '/Author': 'RestWeb', '/Creator': 'Z.ai', '/Subject': 'Komplett genomgang av alla WHM-funktioner och installningar'})
with open(output_path, 'wb') as f:
    writer.write(f)

import os
size_mb = os.path.getsize(output_path) / (1024*1024)
page_count = len(reader.pages)
print(f"Pages: {page_count}, Size: {size_mb:.1f} MB")
