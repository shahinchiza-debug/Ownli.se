#!/usr/bin/env python3
"""
Apply Ownli renames + section removal in src/app/page.tsx:
1. Rename "WebPro" -> "Ownli" everywhere (including testimonials).
2. Rename navbar logo "Web<Pro>" markup -> "Ownli" wordmark.
3. Remove the `subscriptions` and `consultingServices` data arrays.
4. Remove the Abonnemang and Konsulttjänster JSX sections.
5. Update the "Hur det fungerar" block so it no longer references
   abonnemang or konsulttjänster.
6. Drop FAQ entries that are abonnemang/konsulttjänster-specific.

Reads from /home/z/my-project/src/app/page.tsx, applies edits in place.
"""

import re
from pathlib import Path

SRC = Path('/home/z/my-project/src/app/page.tsx')
text = SRC.read_text(encoding='utf-8')

# ---------------------------------------------------------------- 1. WebPro -> Ownli
text = text.replace('WebPro', 'Ownli')

# ---------------------------------------------------------------- 2. Navbar wordmark
# "Web<span ...>Pro</span>" -> "Ownli"  (three occurrences: navbar, footer, login; dashboard variant "Web<span ...>Pro</span>")
text = re.sub(
    r'Web(<span[^>]*>)Pro</span>',
    r'Ownli',
    text,
)

# ---------------------------------------------------------------- 3. Remove data arrays
# subscriptions + consultingServices blocks (each ends with '];\n')
def remove_block(text, name):
    pattern = re.compile(
        r'const ' + name + r' = \[\n(?:.*\n)*?\];\n',
        re.MULTILINE,
    )
    new_text, n = pattern.subn('', text)
    print(f"  removed {name}: {n} match(es)")
    return new_text

text = remove_block(text, 'subscriptions')
text = remove_block(text, 'consultingServices')

# ---------------------------------------------------------------- 4. Remove Abonnemang + Konsulttjänster JSX blocks
# Each block starts with "{/* Abonnemang */}" / "{/* Konsulttjänster */}"
# and ends at the next "{/* ... */}" comment.

def remove_jsx_block(text, comment_marker, next_marker):
    start = text.find(comment_marker)
    if start == -1:
        print(f"  WARNING: marker not found: {comment_marker!r}")
        return text
    end = text.find(next_marker, start)
    if end == -1:
        # fall back to closing the parent section: end at " {/* Hur det fungerar */}"
        end = text.find('{/* Hur det fungerar */}', start)
        if end == -1:
            print(f"  WARNING: end marker not found for {comment_marker!r}")
            return text
    removed = text[start:end]
    print(f"  removed JSX block {comment_marker!r} ({len(removed)} chars)")
    return text[:start] + text[end:]

text = remove_jsx_block(text, '{/* Abonnemang */}', '{/* Konsulttjänster */}')
text = remove_jsx_block(text, '{/* Konsulttjänster */}', '{/* Hur det fungerar */}')

# ---------------------------------------------------------------- 5. Rewrite "Hur det fungerar" copy
# Find the inner <div className="space-y-4 ...">...</div> block and replace its <p> children.
old_how = (
    '<div className="space-y-4 text-stone-600 leading-relaxed">\n'
    '                <p>Kunden köper en hemsida via ett av två alternativ. Vid <strong className="text-stone-900">direktköp</strong> äger kunden hemsidan från dag ett och väljer därefter fritt om de vill teckna ett abonnemang.</p>\n'
    '                <p>Vid <strong className="text-stone-900">2-årsalternativet</strong> betalas hemsidan av under 24 månader — under denna period ingår 700 kr/mån-abonnemanget samt en omfaktorering automatiskt i priset.</p>\n'
    '                <p>När de 24 månaderna är slut övergår full äganderätt till kunden, som då fritt väljer att fortsätta med ett abonnemang, avsluta eller ta över hosting helt på egen hand.</p>\n'
    '                <p><strong className="text-stone-900">Konsulttjänster</strong> erbjuds löpande till båda kundgrupper för arbeten som faller utanför abonnemangets scope.</p>\n'
    '              </div>'
)
new_how = (
    '<div className="space-y-4 text-stone-600 leading-relaxed">\n'
    '                <p>Du köper din hemsida via ett av två alternativ. Vid <strong className="text-stone-900">direktköp</strong> betalar du 35 000 kr och äger hemsidan fullt ut från dag ett — fri att hosta hos oss, hos någon annan eller på egen hand.</p>\n'
    '                <p>Vid <strong className="text-stone-900">avbetalning 2 år</strong> betalar du 48 000 kr fördelat på 24 månader. Under perioden ingår drift, support och en större omfaktorering. När perioden är slut övergår full äganderätt till dig.</p>\n'
    '                <p><strong className="text-stone-900">Du äger alltid din domän och din kod.</strong> Vi bygger, du bestämmer — precis som varumärket lovar: "Du äger. Vi bygger."</p>\n'
    '              </div>'
)
if old_how in text:
    text = text.replace(old_how, new_how)
    print("  rewrote 'Hur det fungerar' copy")
else:
    print("  WARNING: 'Hur det fungerar' block not found verbatim")

# ---------------------------------------------------------------- 6. FAQ cleanup
# Drop the abonnemang/konsult-specific questions:
#   "Vad ingår i abonnemanget Bas (300 kr/mån)?"
#   "Vad ingår i abonnemanget Plus (700 kr/mån)?"
#   "Vad är en "liten uppdatering" (500 kr) vs en "större omfaktorering" (5 000 kr)?"
#   "Kan jag byta abonnemang under tiden?"
#   "Vad händer om jag vill avsluta mitt abonnemang?"
faq_remove_patterns = [
    r"  \{ q: 'Vad ingår i abonnemanget Bas \(300 kr/mån\)\?', a: '[^']*' \},\n",
    r"  \{ q: 'Vad ingår i abonnemanget Plus \(700 kr/mån\)\?', a: '[^']*' \},\n",
    r'''  \{ q: 'Vad är en "liten uppdatering" \(500 kr\) vs en "större omfaktorering" \(5 000 kr\)\?', a: '[^']*' \},\n''',
    r"  \{ q: 'Kan jag byta abonnemang under tiden\?', a: '[^']*' \},\n",
    r"  \{ q: 'Vad händer om jag vill avsluta mitt abonnemang\?', a: '[^']*' \},\n",
]
for p in faq_remove_patterns:
    new_text, n = re.subn(p, '', text)
    if n:
        text = new_text
        print(f"  removed FAQ entry (pattern matched {n}x)")

# Add a couple of new FAQs that better fit the simplified purchase-only model.
# Insert them right after the existing "Vad händer efter avbetalningen är klar?" entry.
new_faqs = (
    "  { q: 'Ingår hosting i priset?', a: 'Direktköp (35 000 kr) är själva hemsidan — du väljer därefter hosting själv eller via oss. Vid avbetalning under 24 månader ingår drift, support och uppdateringar under hela perioden.' },\n"
    "  { q: 'Vad händer med min domän om jag vill flytta?', a: 'Du äger alltid din domän. Vill du flytta till en annan leverantör hjälper vi dig kostnadsfritt att överföra den, oavsett om du köpt direkt eller via avbetalning.' },\n"
    "  { q: 'Kan ni uppdatera hemsidan senare?', a: 'Ja. Mindre justeringar och större omfaktoreringar tar vi per uppdrag. Du får alltid en fast prisuppskattning i förväg så att du vet vad som gäller.' },\n"
)
anchor = "  { q: 'Vad händer efter avbetalningen är klar?', a: 'När de 24 månaderna är slut äger du hemsidan fullt ut. Du väljer då fritt om du vill fortsätta med ett abonnemang (Bas eller Plus), avsluta helt, eller ta över hosting på egen hand. Det är ditt val.' },\n"
if anchor in text:
    text = text.replace(anchor, anchor + new_faqs)
    print("  added 3 new FAQ entries")
    # Also rewrite the anchor itself to not reference "Bas eller Plus"
    text = text.replace(
        anchor,
        "  { q: 'Vad händer efter avbetalningen är klar?', a: 'När de 24 månaderna är slut äger du hemsidan fullt ut. Du väljer då fritt om du vill ha kvar oss som driftpartner, ta över hosting på egen hand, eller flytta till en annan leverantör. Det är ditt val.' },\n",
    )
else:
    print("  WARNING: anchor FAQ not found, did not insert new FAQs")

# Update the Priser section header copy that mentions "välj abonnemang"
text = text.replace(
    '<p className="text-lg text-stone-600">Köp din hemsida, välj abonnemang efter behov. Alla priser är exkl. moms.</p>',
    '<p className="text-lg text-stone-600">Två enkla sätt att bli ägare. Alla priser är exkl. moms.</p>',
)

# Update process step 4 description to not mention "Abonnemang"
text = text.replace(
    "{ n: '04', icon: Shield, t: 'Du äger', d: 'Vid direktköp äger du allt från dag 1. Vid avbetalning äger du allt när perioden är slut. Abonnemang väljer du fritt.' }",
    "{ n: '04', icon: Shield, t: 'Du äger', d: 'Vid direktköp äger du allt från dag 1. Vid avbetalning äger du allt när perioden är slut. Du är alltid ägare av din kod och din domän.' }",
)

# Save
SRC.write_text(text, encoding='utf-8')
print(f"Done. Wrote {SRC}")
