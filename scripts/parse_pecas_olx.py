#!/usr/bin/env python3
"""
parse_pecas_olx.py — Parser de dumps OLX para banco SQLite de preços de peças

Uso:
    # Importar dump
    python3 scripts/parse_pecas_olx.py pecas/prius-zvw50-gen4/raw/olx-nevada-2026-02.txt \\
        --modelo prius-zvw50-gen4 --fonte "OLX/Nevada"

    # Exportar cesta markdown
    python3 scripts/parse_pecas_olx.py --exportar prius-zvw50-gen4

    # Ver resumo do banco
    python3 scripts/parse_pecas_olx.py --status
"""

import re
import sqlite3
import argparse
import unicodedata
from pathlib import Path
from datetime import date
from statistics import median

BASE_DIR = Path(__file__).parent.parent
DB_PATH = BASE_DIR / 'pecas' / 'pecas.db'


# ─── Categorização ─────────────────────────────────────────────────────────────

CATEGORY_KEYWORDS = {
    'hibrido': [
        'inversor', 'conversor', 'bateria hv', 'bateria hibrida',
        'bateria pack', 'bateria assoalho', 'pack bateria',
        'modulo hv', 'hvac', 'compressor eletrico', 'motor eletrico', 'transaxle',
        'modulo hibrido', 'hv battery', 'inverter', 'mpx',
        'motor ev ', 'motor eletrico ', 'motor electrico',
    ],
    'motor': [
        'motor', 'cambio', 'diferencial', 'virabrequim', 'arvore comando',
        'carter', 'bloco', 'cabecote', 'injetor', 'bomba combustivel',
        'bomba oleo', 'alternador', 'valvula egr', 'egr',
        'coletor admissao', 'coletor escape', 'coletor de ar',
        'turbina', 'embreagem', 'volante motor', 'correia dentada', 'tensor', 'polia',
        'bomba de agua', 'bomba dagua', 'bomba agua',
        'bomba vacuo', 'bomba de vacuo',
        'caixa filtro', 'filtro de ar', 'resonador', 'ressonador', 'caixa ressonador',
        'valvula recirculacao', 'tbi', 'corpo borboleta', 'corpo tbi',
        'flauta injecao', 'rail de injecao', 'tanque combustivel', 'tanque de combustivel',
        'tampa valvula', 'trambulador', 'tranbulador',
        'compressor ar condicionado', 'compressor de ar',
    ],
    'lataria': [
        'para-choque', 'parachoque', 'capo', 'capô', 'paralama', 'friso',
        'longarina', 'assoalho', 'coluna', 'teto solar', 'frente completa',
        'aleta', 'passarroda', 'arco passarroda', 'spoiler', 'difusor',
        'moldura grade', 'grade frontal', 'grade churrasqueira', 'painel traseiro',
        'aerofólio', 'aerofolio', 'aba lateral',
        'acabamento sup tampa tras', 'acabamento superior tampa traseira',
        'acabamento tampa traseira', 'acabamento tampa porta-malas',
        'acabamento tampa porta malas', 'cortina teto',
        'proteção traseira', 'protecao traseira',
    ],
    'iluminacao': [
        'farol', 'lanterna', 'pisca', 'luz de freio', 'refletor', 'lente farol',
        'milha', 'neblina', 'led', 'xenon', 'mascara farol', 'chicote lanterna',
        'lampada', 'modulo farol', 'luz teto cortesia', 'luz de cortesia',
        'luz cortesia',
    ],
    'vidros': [
        'vidro', 'parabrisa', 'vigia', 'luna', 'retrovisor',
        'mecanismo limpador', 'braco limpador', 'limpador para-brisa',
    ],
    'suspensao': [
        'amortecedor', 'bandeja', 'cubo roda', 'mola', 'barra estabilizadora',
        'estabilizador', 'pivo', 'manga eixo', 'manga de eixo', 'tulipa',
        'semi-eixo', 'semi eixo', 'bucha', 'rolamento', 'link',
        'caixa direcao', 'caixa de direcao', 'barra direcao', 'terminal direcao',
        'batente', 'coxim torre', 'torre telescopio', 'balanca dianteira',
        'braco facao', 'braco traseiro', 'braco de suspensao',
        'roda ', 'rodas ', 'roda e pneu', 'pinca dianteira', 'pinca de freio',
        'freio dianteiro', 'pedal de freio', 'pedal freio',
        'tambor', 'disco de freio', 'disco freio',
    ],
    'arrefecimento': [
        'radiador', 'condensador', 'ventoinha', 'resfriador', 'intercooler',
        'reservatorio', 'mangueira agua', 'mangueira arrefecimento',
        'coxim radiador', 'suporte radiador', 'tampa reservatorio',
    ],
    'eletrica': [
        'sensor abs', 'sensor rotacao', 'sensor temperatura', 'sensor oxigenio',
        'sensor pressao', 'modulo abs', 'modulo injecao', 'central eletrica',
        'ecm', 'tcm', 'ecu', 'computador', 'chicote', 'sonda lambda',
        'interruptor', 'chave ignicao', 'miolo chave',
        'fusivel', 'rele', 'sensor',
        'central de injecao', 'central eletrica', 'central eletronica',
        'modulo amplificador', 'amplificador de som', 'amplificador som',
        'modulo controle', 'modulo eletronico', 'modulo central',
        'smartkey', 'smart key', 'chave presenca', 'chave de presenca',
        'chave aproximacao', 'chave de aproximacao',
        'modulo imobilizador', 'central imobilizacao',
        'fecho eletrico', 'modulo mpx',
        'tela central', 'central multimidia', 'multimidia', 'display',
        'painel velocidade', 'painel de velocidade',
        'kit code', 'kit de codigo', 'modulo chave',
    ],
    'seguranca': [
        'airbag', 'cinto seguranca', 'modulo airbag', 'bolsa airbag',
        'cortina airbag', 'kit air bag', 'kit airbag',
    ],
    'interior': [
        'banco', 'forro porta', 'tapete', 'volante', 'console central',
        'quebra sol', 'alavanca cambio', 'macaneta interna', 'puxador',
        'apoio braco', 'porta luva', 'tablier', 'tabelie', 'revestimento',
        'forro teto', 'painel instrumento', 'painel de instrumento',
        'painel controle', 'painel climatico', 'painel climatizador',
        'acabamento painel', 'painel central',
        'botao', 'comando', 'trava', 'fechadura',
        'alto-falante', 'alto falante', 'antena', 'modulo janela',
        'motor janela', 'coxim cambio', 'tweeter', 'caixa de som',
        'cortina tampao', 'tampao bagageiro', 'tampao estepe',
        'cobertura estepe', 'cobertura membro', 'espelho interno',
        'carregador inducao', 'carregador sem fio', 'carregador por inducao',
        'bancada completa', 'conjunto bancos', 'painel completo',
        'painel central completo',
    ],
    'escapamento': [
        'escapamento', 'catalisador', 'silencioso', 'cano escape', 'tubo escape',
        'flexivel escape',
    ],
}

# Priority order for auto-categorization (more specific / easily confused first)
CAT_PRIORITY = [
    'hibrido', 'seguranca', 'motor', 'arrefecimento', 'escapamento',
    'lataria', 'iluminacao', 'vidros', 'suspensao', 'eletrica', 'interior', 'outros',
]

# Display order in exported markdown (logical reading order for collision assessment)
CAT_ORDER = [
    'lataria', 'iluminacao', 'vidros', 'motor', 'hibrido', 'arrefecimento',
    'suspensao', 'eletrica', 'seguranca', 'interior', 'escapamento', 'outros',
]

CAT_LABELS = {
    'lataria': 'Lataria',
    'iluminacao': 'Iluminação',
    'vidros': 'Vidros',
    'motor': 'Motor / Transmissão',
    'hibrido': 'Sistema Híbrido',
    'arrefecimento': 'Arrefecimento',
    'suspensao': 'Suspensão / Direção',
    'eletrica': 'Elétrica / Eletrônica',
    'seguranca': 'Segurança',
    'interior': 'Interior',
    'escapamento': 'Escapamento',
    'outros': 'Outros',
}


# ─── Helpers ───────────────────────────────────────────────────────────────────

def normalize_text(text):
    """Lowercase, remove accents, collapse whitespace."""
    text = text.lower().strip()
    nfkd = unicodedata.normalize('NFKD', text)
    text = ''.join(c for c in nfkd if not unicodedata.combining(c))
    return re.sub(r'\s+', ' ', text).strip()


def clean_description(raw_desc):
    """Remove brand/model/year/color noise from raw OLX description."""
    text = raw_desc.strip()

    # Remove brand and model tokens
    noise = [
        r'\bToyota\b', r'\bHonda\b', r'\bChevrolet\b', r'\bFord\b',
        r'\bFiat\b', r'\bVolkswagen\b', r'\bVW\b', r'\bHyundai\b',
        r'\bKia\b', r'\bBYD\b',
        r'\bPrius\b', r'\bNGA\b', r'\bHybrid\b', r'\bHíbrido\b',
        r'\bHibrido\b', r'\b1\.8\b', r'\b2\.0\b', r'\b1\.6\b',
    ]
    for p in noise:
        text = re.sub(p, '', text, flags=re.IGNORECASE)

    # Remove year patterns (2014, 2014/2015, 2014/15)
    text = re.sub(r'\b\d{4}(?:/\d{2,4})?\b', '', text)

    # Remove trailing colors
    colors = (
        r'Preto|Preta|Branco|Branca|Prata|Cinza|Azul|Vermelho|Vermelha|'
        r'Bege|Amarelo|Amarela|Verde|Dourado|Dourada|Marrom|Roxo|Roxa|'
        r'Natural|Original|Titanio|Titânio'
    )
    text = re.sub(rf'\s+(?:{colors})\s*$', '', text, flags=re.IGNORECASE)

    # Collapse whitespace
    text = re.sub(r'\s+', ' ', text).strip()

    # Title-case for display
    return text.title() if text else ''


def auto_categorize(norm_desc):
    """Return category string based on normalized description keywords."""
    for cat in CAT_PRIORITY[:-1]:  # skip 'outros'
        for kw in CATEGORY_KEYWORDS.get(cat, []):
            if kw in norm_desc:
                return cat
    return 'outros'


def parse_price(price_str):
    """Parse 'R$ 1.499' or 'R$ 299' → float."""
    price_str = price_str.strip()
    if price_str.upper().startswith('R$'):
        price_str = price_str[2:].strip()
    # Brazilian format: period = thousands sep, comma = decimal sep
    price_str = price_str.replace('.', '').replace(',', '.')
    try:
        value = float(price_str)
        return value if value > 0 else None
    except ValueError:
        return None


def format_brl(value):
    """Format float as 'R$ 1.499' (Brazilian thousands separator)."""
    if value is None:
        return '—'
    return 'R$ ' + f'{value:,.0f}'.replace(',', '.')


# ─── Parsing ───────────────────────────────────────────────────────────────────

def parse_dump(filepath):
    """
    Parse OLX dump file.

    OLX listing block pattern (after the store header):
        https://img.olx.com.br/...  ← one or more image URLs
        (blank)
        N                           ← image count
        Description of part         ← piece name (with model/year noise)
        R$ price                    ← price line
        Profissional / Particular
        (blank)
        City - State
        (blank)
        Date
        (blank)
        Adicionar aos favoritos

    Strategy: find every 'R$ ' line, take the preceding non-empty
    non-image non-number line as the description.
    """
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        lines = [ln.rstrip('\n') for ln in f.readlines()]

    listings = []
    for i, line in enumerate(lines):
        stripped = line.strip()
        if not stripped.startswith('R$ '):
            continue

        price = parse_price(stripped)
        if price is None:
            continue

        # Walk backwards to find description
        desc = None
        for j in range(i - 1, max(0, i - 8), -1):
            prev = lines[j].strip()
            if not prev:
                continue
            if prev.startswith('https://') or prev.startswith('http://'):
                break  # crossed into image block — no description found
            if re.match(r'^\d+$', prev):
                continue  # image count line — skip
            desc = prev
            break

        if desc:
            # Filter out whole-car "sucata" listings
            desc_norm = normalize_text(desc)
            if 'sucata' in desc_norm:
                continue
            listings.append((desc, price))

    return listings


# ─── Database ──────────────────────────────────────────────────────────────────

def get_db():
    """Open (or create) the SQLite database, ensure schema exists."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute('PRAGMA journal_mode=WAL')
    conn.executescript('''
        CREATE TABLE IF NOT EXISTS pecas (
            id           INTEGER PRIMARY KEY,
            modelo       TEXT NOT NULL,
            categoria    TEXT,
            descricao    TEXT NOT NULL,
            preco_min    REAL,
            preco_max    REAL,
            preco_ref    REAL,
            qtd_anuncios INTEGER DEFAULT 1,
            condicao     TEXT DEFAULT 'usado',
            fonte        TEXT,
            data_coleta  TEXT,
            observacoes  TEXT
        );

        CREATE TABLE IF NOT EXISTS cesta_padrao (
            id          INTEGER PRIMARY KEY,
            modelo      TEXT NOT NULL,
            tipo_dano   TEXT NOT NULL,
            peca_id     INTEGER REFERENCES pecas(id),
            prioridade  INTEGER,
            observacoes TEXT
        );

        CREATE UNIQUE INDEX IF NOT EXISTS idx_pecas_modelo_desc
            ON pecas(modelo, descricao);
        CREATE INDEX IF NOT EXISTS idx_pecas_modelo_cat
            ON pecas(modelo, categoria);
    ''')
    conn.commit()
    return conn


# ─── Import ────────────────────────────────────────────────────────────────────

def import_dump(filepath, modelo, fonte, data_coleta=None, preco_max=50_000):
    """Parse OLX dump and upsert records into SQLite."""
    if data_coleta is None:
        data_coleta = date.today().isoformat()

    listings = parse_dump(filepath)
    # Filter out OLX "price on request" placeholders (R$ 99.999, R$ 999.999, etc.)
    listings = [(d, p) for d, p in listings if p <= preco_max]
    print(f"Anúncios encontrados no dump: {len(listings)}")

    # Group by normalized description to consolidate prices within this batch
    from collections import defaultdict
    price_groups = defaultdict(list)   # norm_key → [prices]
    desc_map = {}                      # norm_key → cleaned_desc (first seen)

    skipped = 0
    for raw_desc, price in listings:
        cleaned = clean_description(raw_desc)
        if not cleaned or len(cleaned) < 4:
            skipped += 1
            continue
        norm_key = normalize_text(cleaned)
        price_groups[norm_key].append(price)
        if norm_key not in desc_map:
            desc_map[norm_key] = cleaned

    print(f"Peças únicas (após dedup): {len(price_groups)}")
    if skipped:
        print(f"Ignoradas (descrição inválida): {skipped}")

    conn = get_db()
    inserted = updated = 0

    for norm_key, prices in price_groups.items():
        cleaned_desc = desc_map[norm_key]
        categoria = auto_categorize(norm_key)
        preco_min = min(prices)
        preco_max = max(prices)
        preco_ref = median(prices)
        qtd = len(prices)

        # Check for existing record (exact match on stored description)
        row = conn.execute(
            'SELECT id, preco_min, preco_max, qtd_anuncios FROM pecas WHERE modelo=? AND descricao=?',
            (modelo, cleaned_desc)
        ).fetchone()

        if row:
            new_min = min(row[1], preco_min)
            new_max = max(row[2], preco_max)
            new_qtd = row[3] + qtd
            conn.execute(
                '''UPDATE pecas
                   SET preco_min=?, preco_max=?, preco_ref=?, qtd_anuncios=?
                   WHERE id=?''',
                (new_min, new_max, (new_min + new_max) / 2, new_qtd, row[0])
            )
            updated += 1
        else:
            conn.execute(
                '''INSERT OR IGNORE INTO pecas
                   (modelo, categoria, descricao, preco_min, preco_max, preco_ref,
                    qtd_anuncios, fonte, data_coleta)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                (modelo, categoria, cleaned_desc, preco_min, preco_max, preco_ref,
                 qtd, fonte, data_coleta)
            )
            inserted += 1

    conn.commit()
    conn.close()

    print(f"  Inseridas: {inserted} peças novas")
    if updated:
        print(f"  Atualizadas: {updated} peças existentes")
    print(f"  Banco: {DB_PATH}")


# ─── Export ────────────────────────────────────────────────────────────────────

def export_markdown(modelo):
    """
    Export parts for a model to markdown files.

    If cesta_padrao entries exist for the model, filters and annotates by priority.
    Otherwise, exports the full catalog ordered by category and price.

    Generates:
        pecas/{modelo}/cesta-colisao.md
        pecas/{modelo}/cesta-enchente.md
    """
    conn = get_db()

    # Check for defined cesta entries
    cesta_types = conn.execute(
        'SELECT DISTINCT tipo_dano FROM cesta_padrao WHERE modelo=?', (modelo,)
    ).fetchall()
    cesta_types = [r[0] for r in cesta_types]

    all_rows = conn.execute(
        '''SELECT p.descricao, p.categoria, p.preco_ref, p.preco_min, p.preco_max,
                  p.qtd_anuncios, p.fonte, p.data_coleta
           FROM pecas p
           WHERE p.modelo = ?
           ORDER BY p.categoria, p.preco_ref DESC''',
        (modelo,)
    ).fetchall()

    conn.close()

    if not all_rows:
        print(f"Nenhuma peça encontrada para '{modelo}'. Importe um dump primeiro.")
        return

    output_dir = BASE_DIR / 'pecas' / modelo
    output_dir.mkdir(parents=True, exist_ok=True)

    data_ref = all_rows[0][7] or date.today().isoformat()

    def build_markdown(rows, tipo_dano):
        by_cat = {}
        for row in rows:
            cat = row[1] or 'outros'
            by_cat.setdefault(cat, []).append(row)

        lines = [
            f'# Preços de Peças — {modelo}',
            '',
            f'> Tipo de dano: **{tipo_dano}** | Fonte: OLX | '
            f'Coletado: {data_ref} | Total: {len(rows)} peças',
            '',
            '---',
            '',
        ]

        for cat in CAT_ORDER:
            if cat not in by_cat:
                continue
            label = CAT_LABELS.get(cat, cat.title())
            items = by_cat[cat]
            lines += [
                f'## {label}',
                '',
                '| Peça | Preço ref. | Min | Max | Anúncios | Fonte |',
                '|------|-----------|-----|-----|----------|-------|',
            ]
            for row in items:
                desc, _, ref, pmin, pmax, qtd, fonte, _ = row
                lines.append(
                    f'| {desc} | {format_brl(ref)} | {format_brl(pmin)} | '
                    f'{format_brl(pmax)} | {qtd} | {fonte or "—"} |'
                )
            lines.append('')

        return '\n'.join(lines)

    # Export for each damage type (colisao, enchente, incendio)
    # If cesta_padrao is defined for that type, use it; otherwise use full catalog
    damage_types = cesta_types if cesta_types else ['colisao', 'enchente']

    for tipo in damage_types:
        content = build_markdown(all_rows, tipo)
        dest = output_dir / f'cesta-{tipo}.md'
        dest.write_text(content, encoding='utf-8')
        print(f"Exportado: {dest}  ({len(all_rows)} peças)")


# ─── Status ────────────────────────────────────────────────────────────────────

def show_status():
    """Print a summary of the database contents."""
    if not DB_PATH.exists():
        print("Banco não encontrado. Importe um dump primeiro.")
        return

    conn = sqlite3.connect(DB_PATH)
    modelos = conn.execute(
        'SELECT DISTINCT modelo FROM pecas ORDER BY modelo'
    ).fetchall()

    if not modelos:
        print("Banco vazio.")
        conn.close()
        return

    print(f"\n=== {DB_PATH} ===\n")

    for (modelo,) in modelos:
        count, total_anuncios, pmin, pmax = conn.execute(
            '''SELECT COUNT(*), SUM(qtd_anuncios), MIN(preco_min), MAX(preco_max)
               FROM pecas WHERE modelo=?''',
            (modelo,)
        ).fetchone()

        cats = conn.execute(
            '''SELECT categoria, COUNT(*) FROM pecas
               WHERE modelo=? GROUP BY categoria ORDER BY COUNT(*) DESC''',
            (modelo,)
        ).fetchall()

        print(f"Modelo: {modelo}")
        print(f"  Peças únicas : {count}")
        print(f"  Total anúncios: {total_anuncios}")
        print(f"  Faixa de preços: {format_brl(pmin)} — {format_brl(pmax)}")
        print(f"  Por categoria:")
        for cat, cnt in cats:
            print(f"    {cat or 'outros':<20} {cnt:>4} peças")
        print()

    conn.close()


# ─── CLI ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description='Parser de dumps OLX para banco de preços de peças',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument('arquivo', nargs='?', help='Arquivo de dump OLX para importar')
    parser.add_argument('--modelo', '-m', help='Código do modelo (ex: prius-zvw50-gen4)')
    parser.add_argument('--fonte', '-f', default='OLX',
                        help='Fonte dos dados (default: OLX)')
    parser.add_argument('--data', '-d', default=None,
                        help='Data de coleta YYYY-MM-DD (default: hoje)')
    parser.add_argument('--preco-max', type=float, default=50_000,
                        help='Preço máximo por peça em R$ (default: 50000, filtra placeholders OLX)')
    parser.add_argument('--exportar', '-e', metavar='MODELO',
                        help='Exportar markdown para o modelo')
    parser.add_argument('--status', '-s', action='store_true',
                        help='Mostrar resumo do banco')

    args = parser.parse_args()

    if args.status:
        show_status()
    elif args.exportar:
        export_markdown(args.exportar)
    elif args.arquivo:
        if not args.modelo:
            parser.error('--modelo é obrigatório ao importar um dump')
        import_dump(args.arquivo, args.modelo, args.fonte, args.data,
                    preco_max=args.preco_max)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
