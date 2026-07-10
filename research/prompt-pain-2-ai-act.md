# Prompt: Pain #2 — „Cookie banner pro AI" (EU AI Act, čl. 50)

Zkopíruj celý blok níže do nové Claude Code session.

---

Jsi mozek operace pro validaci a launch micro-SaaS nápadu. Pracuj autonomně,
všechna fakta ověřuj proti primárním zdrojům (adversariálně: aktivně se snaž
každé tvrzení vyvrátit, než ho použiješ). Nikdy nepoužívej vymyšlené
statistiky, fake reference ani nepodložená tvrzení. Piš mi česky.

## Nápad k validaci

**„Cookie banner pro AI"** — widget + scanner pro splnění transparentních
povinností EU AI Act, článek 50, pro malé firmy a agentury:

- sken webu: detekce AI chatbotů, AI generovaného obsahu a míst, kde vzniká
  povinnost transparentnosti
- jeden script tag: vloží compliantní disclosure („komunikujete s AI"),
  označení AI obsahu ve strojově čitelném formátu, deepfake labeling
- audit log jako důkaz pro dozorový orgán

## Ověřená fakta, ze kterých vycházej (znovu si je ověř, ať nejsou zastaralá)

1. Čl. 50 AI Act platí od **2. 8. 2026**; pokuty do €15M / 3 % obratu.
   Zdroje: https://artificialintelligenceact.eu/article/50/ ,
   https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-50 ,
   https://datamatters.sidley.com/2026/06/24/eu-ai-act-transparency-obligations-preparing-for-compliance-by-2-august-2026/
2. Povinnosti: informovat uživatele o interakci s AI (nejpozději při prvním
   kontaktu), strojově čitelné značení generovaného obsahu, deepfake
   disclosure. Komise vydává guidelines + Code of Practice on Transparency:
   https://digital-strategy.ec.europa.eu/en/policies/code-practice-ai-generated-content
3. Známá konkurence (k datu 10. 7. 2026 — ověř, jak se pohnula):
   - **DiscloAI** (https://discloai.com/) — widget, auto-detekce Intercom,
     Crisp, Tidio, Zendesk, Drift, LiveChat; audit log; EN-generic
   - **GetActReady** (https://getactready.com/) — checklisty a klasifikátory
   - **EU AI Compass** — implementation packy (obsah, ne SaaS)
   - GRC suity (Vanta, OneTrust) — enterprise, mimo SMB segment
4. Analogie trhu: GDPR cookie lišty stvořily Cookiebot/CookieYes/Usercentrics
   (masový trh z jedné právní povinnosti + jednoho script tagu).

## Co musíš zvalidovat, než se cokoli postaví (kill kritéria)

1. **Ochota platit v SMB**: kdo reálně koupí? Prozkoumej, jestli platícím
   zákazníkem nemají být spíš **agentury** (spravují desítky klientských
   webů = jeden nákup, N instalací). Hledej důkazy: fóra agentur, WordPress
   komunity, cenové benchmarky cookie-consent nástrojů.
2. **Enforcement realita**: kdo a jak bude čl. 50 vymáhat (market
   surveillance authorities per stát). Pokud enforcement vypadá bezzubě,
   trh potáhne jen „compliance theater" — ověř, jestl to stačilo cookie
   nástrojům před prvními pokutami.
3. **Diferenciace proti DiscloAI** — kandidátní blue-ocean klíny (vyber a
   ověř aspoň jeden):
   - lokalizace CZ/SK/DE/PL: právní texty v místním jazyce, místní právní
     reference, prodej přes místní agentury a hosting firmy
   - distribuce: oficiální **WordPress plugin directory** (DiscloAI tam
     ověř), **Shoptet doplňky** (CZ/SK e-shopy s AI chatboty), Webnode/Wix
   - agency dashboard: multi-site správa, white-label reporty
4. **Časování**: povinnost platí od 2. 8. 2026 — jsme PO deadlinu, což mění
   messaging z „připrav se" na „jsi v prodlení". Ověř, jestli po deadlinu
   poptávka roste (Google Trends, zprávy o prvních kontrolách).

Pokud validace projde (aspoň 2 nezávislé důkazy ochoty platit + funkční
klín proti DiscloAI), pokračuj. Pokud ne, napiš proč a zastav se.

## Co pak postavit

Landing page pro validaci poptávky (žádný produkt, jen waitlist):

- Jednosouborové statické HTML, EN + CZ přepínač, světlý i tmavý režim
- Design: použij skilly **pbakaus/impeccable**, **emilkowalski/skills
  (emil-design-eng)** a **leonxlnx/taste-skill** (stáhni SKILL.md z GitHubu,
  pokud nejsou nainstalované). Tvrdá pravidla: žádné em-pomlčky v copy, hero
  subtext ≤ 20 slov, max 1 eyebrow na 3 sekce, žádné dvě po sobě jdoucí
  sekce se stejným layoutem, motion jen s účelem a exponenciálním ease-out,
  prefers-reduced-motion
- Obsah: pain-first hero (např. „Váš chatbot už porušuje AI Act."), sekce
  povinností s odkazy na oficiální zdroje, jak to funguje (scan → widget →
  audit log), férové FAQ, waitlist CTA (mailto: zdenek.brdy@email.cz)
- Sekce důkazů: pouze reálná, ověřená tvrzení s odkazy (čl. 50, deadline,
  pokuty). Žádná vymyšlená čísla, žádné fake reference
- Ověř výsledek Playwright screenshoty (light/dark/mobil) a oprav, co nesedí

## Výstupy

1. `research/pain-2-validation.md` — ověřená fakta se zdroji, vyvrácená
   tvrzení, verdikt go/no-go, zvolený klín
2. `landing-ai-act/index.html` — landing page (pokud go)
3. Commit + push (větev dle instrukcí session), návrh dalších kroků
   (doména, deploy, distribuce)

---

*Vzniklo jako výstup pain huntu 2026-07-10; vítězný pain #1 = PriceList
Pilot (viz `research/pain-hunt-2026-07.md`).*
