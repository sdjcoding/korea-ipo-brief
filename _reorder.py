"""One-shot reorder of sections in index.html.

New order:
  1. Hero
  PART 1 - AI Market Opportunity
  2. (was 6) E-commerce Market
  3. (was 7) Opportunity (incl. AI Paid Market spotlight)
  PART 2 - IPO Capital Opportunity
  4. (was 2) Why Now / 3 capital observations
  5. (was 3) Capital Markets
  6. (was 4) Listing Tracks
  7. (was 5) Path Mapping
  8. Comparables
  9. Case Study
  10. Foreign Issuer Path
  11. Timeline
  12. CTA

Also updates inline section_num display numbers and cross-section references.
"""
import re
from pathlib import Path

p = Path(__file__).parent / "index.html"
src = p.read_text(encoding="utf-8")

# Locate section boundaries by comment markers
marker_re = re.compile(r"<!--\s*={10,}\s*\d+\.\s*[^=]+?\s*={10,}\s*-->")
markers = list(marker_re.finditer(src))
assert len(markers) == 12, f"expected 12 section markers, got {len(markers)}"

# Locate end of section 12 = start of FOOTER comment
footer_re = re.compile(r"<!--\s*={10,}\s*FOOTER\s*={10,}\s*-->")
footer_m = footer_re.search(src)
assert footer_m, "FOOTER marker not found"

prefix = src[: markers[0].start()]
suffix = src[footer_m.start() :]

# Slice sections by their comment markers
sections = []  # list of (name_keyword, raw_text)
for i, m in enumerate(markers):
    start = m.start()
    end = markers[i + 1].start() if i + 1 < len(markers) else footer_m.start()
    raw = src[start:end]
    sections.append(raw)

def find_section(keyword):
    for s in sections:
        if keyword in s[: 200]:  # only check first 200 chars (the marker line)
            return s
    raise ValueError(f"section with keyword {keyword!r} not found")

hero       = find_section("HERO")
why_now    = find_section("WHY NOW")
capital    = find_section("CAPITAL MARKETS")
tracks     = find_section("LISTING TRACKS")
recommend  = find_section("RECOMMENDATION")
ecommerce  = find_section("E-COMMERCE")
opportunity= find_section("OPPORTUNITY")
comparable = find_section("COMPARABLES")
case       = find_section("CASE STUDY")
foreign    = find_section("FOREIGN ISSUER")
timeline   = find_section("TIMELINE")
cta        = find_section("CTA")

# new_order: [(new_num, section_text)]
ordered = [
    ("01", hero),
    ("02", ecommerce),
    ("03", opportunity),
    ("04", why_now),
    ("05", capital),
    ("06", tracks),
    ("07", recommend),
    ("08", comparable),
    ("09", case),
    ("10", foreign),
    ("11", timeline),
    ("12", cta),
]

# In each section, replace the FIRST inline section-num span value with the new number.
# Pattern: <span class="section-num text-coral-500 text-sm">OLD</span>
section_num_re = re.compile(
    r'(<span class="section-num text-coral-500 text-sm">)(\d{2})(</span>)'
)
def replace_first_section_num(text, new_num):
    def repl(m):
        return f"{m.group(1)}{new_num}{m.group(3)}"
    return section_num_re.sub(repl, text, count=1)

# Some sections (Hero, CTA) use a different label format ("11 / NEXT STEP", "12 / CONTACT").
cta_label_re = re.compile(r'(text-xs section-num text-coral-500 mb-4">)\d+(\s*/\s*[A-Z]+)')

new_sections = []
for new_num, text in ordered:
    text = replace_first_section_num(text, new_num)
    if "CONTACT" in text or "NEXT STEP" in text:
        text = cta_label_re.sub(lambda m: f"{m.group(1)}{new_num}{m.group(2)}", text, count=1)
    new_sections.append(text)

# Update cross-references that point to old section numbers.
# Why Now's card #2 says "（详见第 04 节）" pointing to Listing Tracks (was 04, now 06)
joined = "".join(new_sections)
joined = joined.replace("详见第 04 节", "详见第 06 节")
# Why Now's card #3 says "见第 09 节" pointing to Case Study — stays at 09, no change needed.

# Compose final file
out = prefix + joined + suffix
p.write_text(out, encoding="utf-8")
print(f"Reordered. New file size: {len(out)} bytes")
print(f"Section count: {len([m for m in marker_re.finditer(out)])}")
