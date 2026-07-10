# Pain Hunt — červenec 2026

Cíl: najít skutečný, ověřený problém s „blue ocean" charakterem (nepřesycený trh),
ze kterého lze udělat byznys pro sólo technického zakladatele
(scraping, datové pipeline, AI integrace — viz toto repo).

Metodika: deep-research workflow (88 sub-agentů: fan-out search → fetch → extrakce
falzifikovatelných tvrzení → adversariální verifikace 3 hlasy na tvrzení) +
nezávislá manuální validace každé hypotézy proti primárním zdrojům.
Tvrzení označená **[3-0]** přežila tři nezávislé pokusy o vyvrácení.

---

## Vítěz: synchronizace dodavatelských ceníků do e-shopu („PriceList Pilot")

**Pain:** Malé e-shopy (mimo dropshipping) dostávají od velkoobchodních dodavatelů
ceníky v XLSX/CSV/PDF/e-mailech. Každá aktualizace znamená hodiny ručního přepisování,
tiché úniky marže (dodavatel zdraží, prodejní cena zůstane) a prodej zboží,
které dodavatel mezitím vyřadil.

### Důkazy poptávky (ověřeno)

1. **Ekonomika „člověk jako náplast za software"** — na Upwork a Fiverr existují celé
   kategorie freelancerů na „product upload" z dodavatelských podkladů, typicky
   $10–70 za zakázku, nabízené jako opakovaná služba:
   - https://www.upwork.com/hire/product-upload-freelancers/
   - https://www.fiverr.com/categories/business/ecommerce-management/product-upload
2. **Bolest z první ruky** — Shopify Community: obchodník s 3 000 produkty
   a 150 značkami řeší, jak měsíčně aktualizovat ceny podle dodavatelských ceníků:
   - https://community.shopify.com/t/how-to-only-update-cost-and-prices-according-to-supplier-list/295931
3. **Poptávka po monitoringu cen/dostupnosti obecně je masivní** — changedetection.io:
   ~32,3k hvězd na GitHubu, placený hosting $8.99/měs; price-drop a restock alerty
   jsou explicitně hlavní use-case **[3-0]**:
   - https://github.com/dgtlmoon/changedetection.io

### Slabiny konkurence (ověřeno z jejich vlastních recenzí/dokumentace)

- **Stock Sync (Shopify)** — vyžaduje strukturované feedy a ruční mapování sloupců;
  recenze: „extrémně složitý setup", rozbité aktualizace („update rozházel celý obchod"),
  pomalá podpora, zdražování limitů:
  https://apps.shopify.com/stock-sync/reviews
- **Dropshipping nástroje (AutoDS, Syncee, Spocket)** — fungují jen s jejich
  marketplace katalogy / podporovanými dodavateli, ne s vlastním velkoobchodem
  („marketplace lock-in").
- **Parsery dokumentů (Docparser, Parseur)** — řeší PDF→tabulka, ne průběžný
  sync do obchodu, ne marže, ne diff.
- **Enterprise procurement (Prokuria, Pricefx)** — cena a složitost mimo segment.
- **Shoptet (CZ/SK)** — nativní importy vyžadují čistý XML/CSV feed z URL/e-mailu;
  chaos reálných ceníků (PDF, měnící se struktura XLSX) neřeší.

**Blue-ocean segment:** klasický malý retailer s vlastními (často lokálními)
velkoobchodními dodavateli a „špinavými" ceníky. Dropshipping je obsloužen,
enterprise je obsloužen, tento segment platí freelancery.

### Proč to sedí zakladateli

- Ověřená lekce ScrapingBee **[3-0]**: po dvou neúspěších uspěli tam, kde měli
  hlubokou doménovou expertízu a věděli, kdo je zákazník
  (https://www.failory.com/interview/scrapingbee). Scraping/parsing/AI pipeline
  je přesně tato doména; toto repo je zárodek engine.
- Ověřená lekce College Conductor **[3-0]**: rychlost k první hodnotě rozhoduje;
  „nudný" známý stack zkrátil reimplementaci z 2 let na 2 týdny
  (https://dev.to/mblayman/a-failed-saas-postmortem-2ek5).
  MVP: nahraješ ceník → vidíš diff a dopad na marže → export/push. Hodnota v první session.
- ScrapingBee: $1M ARR bootstrapped, distribuce přes obsah/SEO — replikovatelné sólo
  **[3-0]** (https://www.scrapingbee.com/journey-to-one-million-arr/).

### Doména

`pricelistpilot.com` — volná, $11.25/rok (ověřeno přes Vercel domain check, 2026-07-10).

---

## Zabití kandidáti (a proč)

| Kandidát | Verdikt | Důkaz |
|---|---|---|
| Generický monitoring cen konkurence | ČERVENÝ oceán | Spoluzakladatel ScrapingBee vlastní PricingBot opustil; Prisync, Price2Spy, … |
| Generická detekce změn webů | ČERVENÝ | changedetection.io (free/self-host), Visualping, Distill |
| Scraping API | ČERVENÝ | ScrapingBee, Zyte, Apify, Firecrawl… |
| Dotační radar CZ | ČERVENÝ | DotaceOnline (20+ let), Dotační Manager, Dotační.info, EY „Dotační hlídací pes", monitoring hospodářských komor |
| Policy-change monitoring pro marketplace prodejce | červený-oranžový | SellerSonar, SellerPulse, Sellerite; seller-tools prostor přesycený |
| EUDR compliance pro SME | oranžový + regulatorní riziko | Deadline pro SME posunut na 30. 6. 2027; SME nástroje už vznikají (eudrready.eu, EUDR Navigator); nařízení se dál „zjednodušuje" |
| AI Act čl. 50 „cookie banner pro AI" | oranžový, okno se zavírá | Čl. 50 platí od 2. 8. 2026 (ověřeno), ale DiscloAI a GetActReady už přesně toto staví; bariéra důvěry pro neznámého sólo zakladatele |
| Realitní/job inzeráty monitoring | červený | Nativní alerty portálů + hotové nástroje |

Poznámka k metodě: několik „faktů" z první ruky bylo při verifikaci vyvráceno
(např. můj předpoklad EUDR deadline 30. 6. 2026 byl špatně — posunuto o rok;
1M pageviews ScrapingBee nebylo použitelné jako demand signál). Bez adversariální
verifikace by šly do rozhodnutí chybné vstupy.

---

## Další krok

Landing page: `landing/index.html` (EN/CZ). CTA: early-access e-mail.
Validace: zveřejnit, nasměrovat trafik (Shopify/WooCommerce komunity, CZ e-commerce
skupiny, obsah/SEO), měřit konverzi na waitlist před psaním kódu produktu.
