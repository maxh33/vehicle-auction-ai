# vehicle-auction-ai

> 🇧🇷 [Versão em Português](README.md) &nbsp;|&nbsp; [github.com/maxh33/vehicle-auction-ai](https://github.com/maxh33/vehicle-auction-ai)

AI-powered framework for analyzing salvage and damaged vehicles at Brazilian auctions (Copart Brazil, Sodré Santoro, and others).

Combines automated data collection, a parts price database, and structured prompts to help buyers make faster, better-informed bidding decisions.

---

## How it works

**Copart Brazil — automated collection:**

```
Auction lot URL (copart.com.br)
    ↓
copart_scraper.py — creates folder, extracts data, downloads HD photos
    ↓
AI analysis (Claude or Gemini) — photos + structured data + prompt
    ↓
Reports: analise-tecnica.md (damage assessment) + analise-custo.md (cost/bid)
    ↓
Decision: max bid, conditionals, or discard
```

**Other auctions (Sodré Santoro, etc.) — manual collection** *(automation planned)*:

```
Auction website
    ↓
Manual data collection (lot description, sale conditions)
    ↓
Vehicle photos (downloaded or taken during on-site inspection)
    ↓
Filled prompt template (templates/prompt-avaliacao-leilao.md)
    ↓
AI analysis — photos + raw data + prompt
    ↓
Reports saved to lot folder
```

> **Roadmap:** scrapers for Sodré Santoro, Leilão Meu, Pátio Digital, and other
> Brazilian auction houses are planned. Contributions welcome — see
> [Contributing](#contributing).

---

## Project structure

```
vehicle-auction-ai/
│
├── README.md / README.en.md           # Documentation (PT/EN)
│
├── scripts/
│   ├── copart_scraper.py              # Automated Copart lot collector
│   └── parse_pecas_olx.py             # OLX parts dump → SQLite + markdown
│
├── pecas/                             # Parts price database (per model)
│   ├── pecas.db                       # SQLite — all models in one file
│   ├── prius-zvw50-gen4/
│   │   ├── cesta-colisao.md           # AI-ready price table (collision)
│   │   ├── cesta-enchente.md          # AI-ready price table (flood)
│   │   └── raw/                       # Original OLX dumps (gitignored)
│   └── byd-dolphin-mini/
│       └── raw/
│
├── templates/                         # Reusable prompts (vehicle-agnostic)
│   └── prompt-avaliacao-leilao.md     # Master prompt for any lot analysis
│
├── guias/                             # Technical guides per vehicle model
│   └── prius-zvw50-gen4/
│       └── guia-precompra-prius-zvw50.md  # Prius Gen 4 pre-purchase checklist
│
└── lotes/                             # One subdirectory per analyzed lot
    └── 0215-toyota-prius-nga-2017/
        ├── analise-tecnica.md         # Damage assessment, risk analysis
        ├── analise-custo.md           # Cost breakdown, bid recommendation
        ├── dados-brutos/              # Raw data collected from auction site
        └── fotos/                     # Original photos (gitignored)
```

---

## Parts Price Database

The `pecas/` directory holds a centralized SQLite database of salvage yard prices collected from OLX listings, organized by vehicle model.

### Import an OLX dump

Collect a seller profile listing page from OLX (copy page text to a `.txt` file), then import:

```bash
python3 scripts/parse_pecas_olx.py pecas/prius-zvw50-gen4/raw/olx-dump.txt \
    --modelo prius-zvw50-gen4 \
    --fonte "OLX/Nevada"
```

**What the parser does:**
- Extracts listing blocks (image URLs → count → description → price)
- Filters out whole-car "sucata" listings and OLX placeholder prices (R$ 99.999+)
- Cleans descriptions (removes brand/model/year/color noise)
- Auto-categorizes: lataria, iluminacao, vidros, motor, hibrido, arrefecimento, suspensao, eletrica, seguranca, interior, escapamento
- Deduplicates by normalized description, tracking min/max/median price per part

### Export markdown for AI analysis

```bash
python3 scripts/parse_pecas_olx.py --exportar prius-zvw50-gen4
# → pecas/prius-zvw50-gen4/cesta-colisao.md
# → pecas/prius-zvw50-gen4/cesta-enchente.md
```

Generated markdown looks like:

```markdown
## Lataria

| Peça                        | Preço ref. | Min       | Max       | Anúncios | Fonte      |
|-----------------------------|-----------|-----------|-----------|----------|------------|
| Para-choque Dianteiro       | R$ 1.200  | R$ 800    | R$ 1.600  | 5        | OLX/Nevada |
| Capô                        | R$ 950    | R$ 700    | R$ 1.200  | 3        | OLX/Nevada |
```

### Check database status

```bash
python3 scripts/parse_pecas_olx.py --status
```

### Using prices in AI analysis

Include the markdown file in the AI session context:

```
@pecas/prius-zvw50-gen4/cesta-colisao.md
```

---

## Automated Collection — Copart Brazil

### Prerequisites

```bash
pip install requests
```

Environment variables in `~/.secrets` (or `.env`):

| Variable | Description |
|----------|-------------|
| `CRAWL4AI_URL` | Your Crawl4AI instance URL |
| `CRAWL4AI_USER` | BasicAuth username |
| `CRAWL4AI_PASS` | BasicAuth password |
| `GEMINI_API_KEY` | Optional — improves optional field extraction |

Requires a self-hosted [Crawl4AI](https://github.com/unclecode/crawl4ai) instance (Docker-based, runs headless Playwright to bypass Copart's Incapsula WAF).

### Usage

```bash
# Full collection (data + HD photos)
python3 scripts/copart_scraper.py https://www.copart.com.br/lot/1083986

# Data only, skip photos
python3 scripts/copart_scraper.py https://www.copart.com.br/lot/1083986 --no-photos

# Save to custom directory
python3 scripts/copart_scraper.py https://www.copart.com.br/lot/1083986 --dir /path/to/dir
```

### What it extracts

Structured fields: brand, model, trim, year, condition, title type, FIPE value, yard location, sale date, operational condition, notes, seller-specific terms link.

Photos: all in HD (1600×1200) with correct file extension auto-detected.

---

## Analyzed Lots

| Lot | Vehicle | Auction House | Date | Max Bid Rec. | Outcome |
|-----|---------|---------------|------|-------------|---------|
| 0215 | Toyota Prius NGA TOP 2017, 101.539 km, flood, Média Monta | Sodré Santoro #28139 | 2026-02-27 | R$ 16,000 | CONDITIONAL — personal use viable; sold for R$ 36,900 (above rec.) |
| 1062630 | Toyota Prius Hybrid 1.8 2016/2016, collision, Eusébio/CE | Copart Brazil | TBD | — | MONITORING — awaiting auction release |
| 1083986 | BYD Dolphin Mini 2025, collision (financed), Eusébio/CE | Copart Brazil | 2026-02-28 | — | COLLECTED — 10 HD photos via scraper; analysis pending |

---

## Specialized Guides

| Vehicle | Guide | Contents |
|---------|-------|---------|
| Toyota Prius Gen 4 (ZVW50, 2016–2022) | `guias/prius-zvw50-gen4/guia-precompra-prius-zvw50.md` | Dr. Prius app, compatible OBD dongles, HV battery checklist, known issues, recalls |

---

## Tools for On-Site Inspection (hybrid vehicles)

| Tool | Description |
|------|-------------|
| **Dr. Prius** (app) | HV battery diagnostics via OBD. Free version reads data; paid unlocks Battery Health Test |
| **Veepeak OBDCheck BLE+** | OBD dongle compatible with Dr. Prius on iOS/Android |
| **PanLong ELM327 Bluetooth** | Budget alternative OBD dongle |

> **Note:** The standard ELM327 Mini Bluetooth dongle (blue) is **not compatible** with Dr. Prius.

---

## Brazilian Market Context

- **Média Monta** — damage classification requiring INMETRO inspection report before the vehicle can be driven on public roads
- **Transferência interestadual** — requires Mercosul license plates; document delivery may exceed 30 business days
- **Leiloeiro commission** — typically 5% of hammer price (non-refundable)
- **Pre-auction fines** — buyer's responsibility (insurance may cover up to R$ 500)

---

## Requirements

- **Python 3.8+**
- `pip install requests` — only external dependency for the scraper
- Self-hosted [Crawl4AI](https://github.com/unclecode/crawl4ai) instance for Copart collection
- Claude Code or Gemini CLI for AI analysis

---

## Contributing

This framework was built for the Brazilian salvage auction market, but the core components are generic and designed to be extended.

### What contributions are welcome

| Area | Examples |
|------|---------|
| **New auction scrapers** | Sodré Santoro, Leilão Meu, Pátio Digital, Bidar, Zukerman |
| **Vehicle guides** | Pre-purchase checklists for popular models (Civic, HB20, Creta, Fiat Strada, etc.) |
| **OLX parser improvements** | Better auto-categorization keywords, support for Mercado Livre dumps |
| **Parts price data** | Additional `cesta-*.md` exports for other vehicle models |
| **Prompt template** | Improvements to the master analysis prompt (new damage types, cost scenarios) |
| **Bug reports** | Parsing edge cases, incorrect categorization, scraper failures |
| **Documentation** | Corrections, translations, usage examples |

### How to contribute

1. **Fork** the repository
2. **Create a branch** following the convention:
   - `feat/sodre-santoro-scraper` — new feature
   - `fix/olx-parser-price-edge-case` — bug fix
   - `docs/civic-pre-purchase-guide` — documentation
3. **Make your changes**, keeping these standards:
   - Python 3.8+ compatible
   - No hardcoded credentials — use environment variables
   - Minimal external dependencies (prefer stdlib)
   - Follow the existing file and folder naming conventions
4. **Open a Pull Request** with a clear description of what was changed and why

### Reporting bugs or requesting features

Open a [GitHub Issue](https://github.com/maxh33/vehicle-auction-ai/issues) describing:
- What you expected to happen
- What actually happened
- Steps to reproduce (include anonymized dump excerpts if relevant)

---

## License

MIT License — see [LICENSE](LICENSE) for full text.

Free to use, modify, and distribute. Attribution appreciated but not required.

---

<!-- seo-keywords: brazil car auction AI analysis salvage vehicle copart brazil olx scraper parts price database sqlite python claude gemini damaged car bid decision tool leilao veiculo sinistro enchente colisao prius byd dolphin hybrid electric vehicle desmanche preço peças automation -->
