# Pain Hunt — kompletní archiv researche (10. 7. 2026)

Doplněk k `pain-hunt-2026-07.md` (shrnutí vítěze). Tento soubor archivuje
VŠECHNY prozkoumané kandidáty s verdiktem, důkazy, dobou platnosti hodnocení
a triggery pro re-validaci. Verdikty jsou snímek k 10. 7. 2026 — každý má
omezenou trvanlivost.

## Metodika a její limity (důležité pro interpretaci)

- Deep-research workflow: 88 sub-agentů (fan-out search → fetch → extrakce
  falzifikovatelných tvrzení → adversariální verifikace 3 hlasy na tvrzení).
  Tvrzení označená **[3-0]** přežila tři nezávislé pokusy o vyvrácení.
- Limity: network policy blokovala přímé fetche většiny domén (Reddit, HN,
  Trustpilot, Medium) → většina verifikace šla přes WebSearch indexy, ne
  přímé čtení stránek. Posledních 10 agentů (včetně finální syntézy) spadlo
  na session limit; syntézu jsem dělal ručně z žurnálu.
- Poučení z procesu: 2 moje vlastní vstupní předpoklady byly při verifikaci
  vyvráceny (EUDR deadline, ScrapingBee pageviews jako demand signál).
  Bez adversariální verifikace by šly do rozhodnutí chybné vstupy.

## Ověřená tvrzení [3-0] — trvalá znalostní báze

| Tvrzení | Zdroj | Platnost |
|---|---|---|
| changedetection.io: ~32,3k GitHub hvězd, placený hosting $8.99/měs → masivní poptávka po monitoringu změn webů | github.com/dgtlmoon/changedetection.io | čísla rostou, směr platí dlouhodobě |
| Hlavní use-casy monitoringu: pokles cen, restock, reality, joby, vládní weby | tamtéž | stabilní |
| ScrapingBee: $1M ARR bootstrapped, 2,5 roku po launchi; růst přes SEO/obsah | scrapingbee.com/journey-to-one-million-arr | historický fakt, lekce trvalá |
| Founder-market fit jako klíčový faktor (po 2 neúspěších uspěli ve vlastní doméně) | failory.com/interview/scrapingbee | lekce trvalá |
| College Conductor: 3 roky, 0 zákazníků; „nudný" stack = 2 týdny místo 2 let; speed-to-first-value rozhoduje | dev.to/mblayman/a-failed-saas-postmortem-2ek5 | lekce trvalá |
| Spoluzakladatel ScrapingBee opustil vlastní PricingBot (monitoring cen) → přesycenost niky potvrzena praktikem | failory.com/interview/scrapingbee | stabilní |

Vyvrácená tvrzení (co NEpoužívat): ScrapingBee 1M pageviews jako „search
volume signál" (marketingový self-report, 2021, vendor blog ≠ poptávka);
IEC/College Conductor „pain point" (anekdota n=1, samotný zdroj si
protiřečí); konverzní tvrzení o komunitní akvizici (v citaci není).

---

## Kandidáti: verdikt · proč · na jak dlouho

### 🏆 1. Sync dodavatelských ceníků do e-shopu (VÍTĚZ — PriceList Pilot)

- **Verdikt:** GO. Modro-oranžový oceán: segment „malý retailer s vlastními
  velkoobchodními dodavateli a špinavými ceníky (XLSX/PDF/e-mail)".
- **Proč:** (a) human-as-patch ekonomika — celé kategorie product-upload
  freelancerů na Upwork/Fiverr, $10–70/zakázka, opakovaně; (b) bolest
  z první ruky na Shopify fóru (3 000 produktů / 150 značek / měsíční
  ceníky); (c) incumbenti mají zdokumentované slabiny (Stock Sync: složitý
  setup, rozbité mapování, vyžaduje čisté feedy; AutoDS/Syncee: jen vlastní
  marketplace katalogy; Docparser/Parseur: jen parsing, ne sync; Shoptet
  nativní importy: jen čistý feed z URL/e-mailu); (d) perfektní founder fit.
- **Na jak dlouho:** okno na obsazení AI-first pozice odhadem **6–12 měsíců**.
  EagleLytics (2026) ukazuje, že gap si už někdo všiml. Rizika s časovačem:
  Shopify přidává AI import nativně (sledovat **Shopify Editions, 2× ročně**),
  Stock Sync může přidat AI mapping kdykoli.
- **Re-validace:** konkurenční sken každé **3 měsíce** během stavby
  (dotazy: „AI supplier price list import shopify", novinky Stock Sync /
  EagleLytics / Automated Commerce). Doména pricelistpilot.com volná
  k 10. 7. 2026 za $11.25 — může zmizet kdykoli, koupit hned.

### 🥈 2. „Cookie banner pro AI" — EU AI Act čl. 50 (runner-up, prompt uložen)

- **Verdikt:** PODMÍNĚNÉ GO (kill kritéria v `prompt-pain-2-ai-act.md`).
- **Proč:** regulace vynucuje poptávku (čl. 50 platí od 2. 8. 2026, pokuty
  do €15M/3 %); analogie cookie lišt (Cookiebot); konkurence existuje, ale
  malá a EN-generic (DiscloAI, GetActReady). Klín: lokalizace CZ/SK/DE +
  agentury + WordPress/Shoptet distribuce.
- **Na jak dlouho:** **nejkratší okno ze všech — jednotky měsíců.** Deadline
  je za 3 týdny; poptávkovou vlnu vyvolají první kontroly/pokuty (H2 2026).
  Pokud do ~Q4 2026 nevznikne pozice, prostor zabere DiscloAI nebo cookie
  hráči (Usercentrics/Cookiebot mohou čl. 50 přidat jako feature svých lišt
  — to je hlavní zabíječ nápadu).
- **Re-validace:** při spuštění promptu (ihned), pak při první zprávě
  o enforcementu. Trigger STOP: cookie-consent vendor ohlásí AI Act modul.

### 3. EUDR compliance pro SME (zaparkováno)

- **Verdikt:** PARK. Bolest reálná, ale deadline pro SME posunut na
  **30. 6. 2027** (velké/střední firmy 30. 12. 2026) a nařízení se dál
  „zjednodušuje" (simplification package) → regulatorní riziko; SME nástroje
  už vznikají (eudrready.eu, EUDR Navigator, Coolset).
- **Proč ne teď:** stavět na pohyblivém základě; můj původní předpoklad
  deadline 30. 6. 2026 byl vyvrácen — přesně tenhle typ chyby by zabil
  launch.
- **Na jak dlouho:** hodnocení platí do stabilizace textu nařízení.
  **Re-validace Q1 2027** (3–6 měsíců před SME deadlinem): pokud povinnosti
  přežijí zjednodušení a SME nástroje zůstanou drahé/enterprise, okno se
  znovu otevře — hlavně vertikálně (pražírny kávy, nábytek, CZ/SK importéři).
  Trigger dřívější akce: velcí odběratelé začnou tlačit DDS požadavky na
  malé dodavatele (B2B pull).

### 4. Dotační radar CZ (zabito)

- **Verdikt:** NE — červený oceán. DotaceOnline (20+ let na trhu), Dotační
  Manager („největší DB výzev"), Dotační.info (500 výzev denně, týdenní
  newsletter), EY Dotační hlídací pes, monitoring hospodářských komor.
  Konzultanti navíc rozdávají monitoring zdarma jako lead-gen.
- **Na jak dlouho:** verdikt stabilní, **re-validace nemá smysl** bez
  zásadní změny (např. nové programovací období EU 2028+ s novým chaosem,
  nebo AI-first UX gap u všech incumbentů — nepravděpodobné, EY už AI má).

### 5. Policy-change monitoring pro marketplace prodejce (zabito)

- **Verdikt:** NE. Bolest reálná (suspendace účtů bez varování — vlákna
  na Amazon Seller Central), ale seller-tools prostor je jeden
  z nejpřesycenějších v micro-SaaS (SellerSonar, SellerPulse, Sellerite AI
  TOS checker…) a policy monitoring je pro incumbenty snadný add-on.
- **Na jak dlouho:** stabilní verdikt, **12+ měsíců**. Trigger re-validace:
  velká platformní krize (masová vlna suspendací), která by vytvořila
  poptávku po nezávislém „pojištění" mimo seller-suity.

### 6. Generický monitoring (ceny konkurence / změny webů / scraping API)

- **Verdikt:** NE, všechny tři pod-trhy červené: Prisync/Price2Spy/PriceRest
  (ceny), changedetection.io free + Visualping/Distill (změny),
  ScrapingBee/Zyte/Apify/Firecrawl (API).
- **Na jak dlouho:** **trvale** — tady se dá vyhrát jen vertikálou, ne
  generikem. Repo competitor-price-monitor zůstává cenné jako engine
  a portfolio, ne jako produkt.

### 7. Reality / joby / restock monitoring (zabito bez hluboké validace)

- **Verdikt:** NE. Reality: nativní alerty portálů + hotové watchdogy.
  Joby jako sales signál: LoneScale/Mantiks a spol. Restock pro spotřebitele:
  sniper boty. B2B procurement restock: důkazy tenké, nezkoumáno do hloubky.
- **Na jak dlouho:** povrchní verdikt — pokud by se objevil konkrétní
  vertikální důkaz (např. stavebniny, healthcare supplies), stojí za
  samostatný mini-research. Jinak neřešit.

### 8. EAA přístupnost pro SMB e-shopy (zavrženo bez hloubky)

- **Verdikt:** NE teď. European Accessibility Act platí od 6/2025,
  enforcement teprve nabíhá; trh okupují overlay vendoři (accessiBe,
  UserWay) s obřím marketingem a spornou pověstí.
- **Na jak dlouho:** re-validace **při první vlně pokut pro malé e-shopy**
  (sledovat CZ ČOI / národní enforcement zprávy). Pak může vzniknout klín
  „poctivý ne-overlay audit + opravy pro Shoptet/Woo" — ale je to spíš
  služba než SaaS.

### 9. AI/GEO monitoring značek v AI odpovědích (zavrženo)

- **Verdikt:** NE — od 2025 zafinancováno (Profound, Peec, Otterly…),
  HubSpot přidal AEO. Rychle rotující prostor.
- **Na jak dlouho:** verdikt platí ~**6 měsíců**; prostor se hýbe tak
  rychle, že za půl roku může vypadat úplně jinak (konsolidace, nebo naopak
  díra v lokálních trzích). Nesledovat aktivně, jen periferně.

### 10. Nevytěžené stopy (nikdy nevaliduováno — syrové leady)

- „Boring industries" z r/SaaS monitoringu: **local permitting, funeral
  planning, industrial maintenance** — US-centrické, zdroj = Medium content
  (nízká důvěra). Validovat jen s vlastním důkazním researchem.
- **Zapier frustrace** (Trustpilot recenze, drahé tarify) — fetch blokován
  policy, nikdy dočteno. Automatizační alternativy jsou ale samy o sobě
  červený oceán (Make, n8n, Relay…).
- **Data sovereignty / local-first automatizace** pro agentury (r/SaaS gap)
  — zajímavý 2026 theme, příliš vágní na akci.

---

## Doporučené datumové kotvy (co si dát do kalendáře)

| Kdy | Co |
|---|---|
| ihned | koupit pricelistpilot.com (ověřeno volné 10. 7. 2026, $11.25/rok) |
| každé ~3 měsíce | konkurenční sken supplier-sync prostoru (Stock Sync, EagleLytics, Shopify AI import) |
| 2. 8. 2026 + první enforcement zprávy | rozhodnout o spuštění promptu pain #2 (AI Act čl. 50) |
| Shopify Editions (léto/zima) | zkontrolovat, jestli Shopify nepřidal nativní AI import ceníků |
| Q1 2027 | re-validace EUDR pro SME (deadline 30. 6. 2027) |
| při první vlně EAA pokut | re-validace přístupnostního klínu pro malé e-shopy |

## Odkazy na artefakty

- Shrnutí vítěze: `research/pain-hunt-2026-07.md`
- Prompt pro pain #2: `research/prompt-pain-2-ai-act.md`
- Landing page: `landing/index.html` (Artifact preview:
  https://claude.ai/code/artifact/d75939d6-d1cd-4726-b335-e5fd53fd3b12)
- Pages deploy workflow: `.github/workflows/pages.yml` (čeká na zapnutí
  Pages v Settings)
