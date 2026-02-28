#!/usr/bin/env python3
"""
copart_scraper.py — Coleta automática de lotes Copart Brazil via Crawl4AI

Uso:
    python3 scripts/copart_scraper.py https://www.copart.com.br/lot/1083986
    python3 scripts/copart_scraper.py https://www.copart.com.br/lot/1083986 --no-photos
    python3 scripts/copart_scraper.py https://www.copart.com.br/lot/1083986 --dir /outro/caminho

Variáveis de ambiente (~/.secrets):
    CRAWL4AI_URL   URL do Crawl4AI (ex: https://crawl.maxhaider.dev)
    CRAWL4AI_USER  Usuário BasicAuth
    CRAWL4AI_PASS  Senha BasicAuth
    GEMINI_API_KEY Chave Gemini para extração LLM
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path

import requests

# ── Configuração ──────────────────────────────────────────────────────────────

CRAWL4AI_URL  = os.getenv("CRAWL4AI_URL",  "http://localhost:11235")
CRAWL4AI_USER = os.getenv("CRAWL4AI_USER", "")
CRAWL4AI_PASS = os.getenv("CRAWL4AI_PASS", "")
GEMINI_KEY    = os.getenv("GEMINI_API_KEY", "")

AUTH = (CRAWL4AI_USER, CRAWL4AI_PASS) if CRAWL4AI_USER else None

# Schema JSON para extração estruturada pelo LLM
EXTRACTION_SCHEMA = {
    "type": "object",
    "properties": {
        "codigo_lote":            {"type": "string", "description": "Código/número do lote"},
        "marca":                  {"type": "string"},
        "modelo":                 {"type": "string"},
        "versao":                 {"type": "string", "description": "Versão completa do veículo"},
        "ano_fabricacao":         {"type": "string"},
        "ano_modelo":             {"type": "string"},
        "blindado":               {"type": "string"},
        "tipo_documento":         {"type": "string"},
        "tipo_monta":             {"type": "string"},
        "condicao":               {"type": "string", "description": "Ex: COLISÃO, ENCHENTE, INCÊNDIO"},
        "valor_fipe":             {"type": "string"},
        "tipo_chassi":            {"type": "string"},
        "combustivel":            {"type": "string"},
        "final_placa":            {"type": "string"},
        "chave":                  {"type": "string"},
        "condicao_funcionamento": {"type": "string"},
        "patio":                  {"type": "string", "description": "Cidade/estado do pátio"},
        "data_venda":             {"type": "string"},
        "notas":                  {"type": "string", "description": "Texto completo do campo Notas"},
        "condicoes_especificas":  {"type": "string", "description": "Texto completo de Condições Específicas"},
        "termos_responsabilidade":{"type": "string", "description": "Texto completo dos Termos de Responsabilidade"},
        "fotos_urls": {
            "type": "array",
            "items": {"type": "string"},
            "description": "URLs das fotos do veículo, preferencialmente versões HD/full"
        }
    }
}

# ── Utilitários ───────────────────────────────────────────────────────────────

def slugify(text: str) -> str:
    """Converte texto em slug ASCII kebab-case."""
    text = text.lower().strip()
    replacements = {
        "àáâãä": "a", "èéêë": "e", "ìíîï": "i",
        "òóôõö": "o", "ùúûü": "u", "ç": "c", "ñ": "n",
    }
    for chars, replacement in replacements.items():
        for ch in chars:
            text = text.replace(ch, replacement)
    text = re.sub(r"[^\w\s-]", "", text)
    return re.sub(r"[\s_-]+", "-", text).strip("-")


def lot_code_from_url(url: str) -> str:
    """Extrai o código numérico do lote da URL."""
    m = re.search(r"/lot/(\d+)", url)
    return m.group(1) if m else "unknown"


# ── Crawl4AI ──────────────────────────────────────────────────────────────────

def check_health() -> bool:
    """Verifica se o Crawl4AI está acessível."""
    try:
        r = requests.get(f"{CRAWL4AI_URL}/health", auth=AUTH, timeout=10)
        r.raise_for_status()
        data = r.json()
        print(f"[OK] Crawl4AI {data.get('version', '')} acessível em {CRAWL4AI_URL}")
        return True
    except Exception as e:
        print(f"[ERRO] Não foi possível conectar ao Crawl4AI em {CRAWL4AI_URL}")
        print(f"       Detalhe: {e}")
        print(f"       Verifique CRAWL4AI_URL, CRAWL4AI_USER e CRAWL4AI_PASS em ~/.secrets")
        return False


def crawl_lot(url: str) -> dict:
    """
    Envia requisição ao Crawl4AI para raspar a página do lote.
    Usa LLMExtractionStrategy (Gemini) para extrair dados estruturados.
    """
    if not GEMINI_KEY:
        print("[AVISO] GEMINI_API_KEY não definido — extração LLM desativada, usando apenas markdown")

    payload = {
        "urls": [url],
        "browser_config": {
            "type": "BrowserConfig",
            "params": {
                "headless": True,
                "viewport": {"type": "dict", "value": {"width": 1280, "height": 900}},
            }
        },
        "crawler_config": {
            "type": "CrawlerRunConfig",
            "params": {
                "cache_mode": "bypass",
                "js_code": "await new Promise(r => setTimeout(r, 5000));",
                "extraction_strategy": {
                    "type": "LLMExtractionStrategy",
                    "params": {
                        "llm_config": {
                            "type": "LLMConfig",
                            "params": {
                                "provider": "gemini/gemini-2.0-flash",
                                "api_token": GEMINI_KEY or "no-key"
                            }
                        },
                        "schema": {"type": "dict", "value": EXTRACTION_SCHEMA},
                        "instruction": (
                            "Extraia todos os dados deste lote de leilão de veículos brasileiro. "
                            "Capture: código do lote, dados do veículo (marca, modelo, versão, anos, "
                            "combustível, blindagem, tipo de documento, tipo de monta, condição, "
                            "tipo de chassi, final de placa, chave, condição de funcionamento), "
                            "valor FIPE, localização do pátio, data/status da venda. "
                            "MUITO IMPORTANTE: capture o texto COMPLETO e integral das seções "
                            "'Notas', 'Condições Específicas' e 'Termos de Responsabilidade' — "
                            "esses campos contêm datas, valores e restrições críticas. "
                            "Para fotos_urls, liste as URLs das imagens do veículo, "
                            "priorizando versões em alta resolução (HD/full)."
                        )
                    }
                } if GEMINI_KEY else None,
                "screenshot": False,
            }
        }
    }

    # Remover extraction_strategy se sem chave Gemini
    if not GEMINI_KEY:
        del payload["crawler_config"]["params"]["extraction_strategy"]

    print(f"[INFO] Raspando: {url}")
    print(f"[INFO] Aguardando resposta do Crawl4AI (pode levar até 60s)...")

    try:
        r = requests.post(
            f"{CRAWL4AI_URL}/crawl",
            json=payload,
            auth=AUTH,
            timeout=180
        )
        r.raise_for_status()
        return r.json()
    except requests.exceptions.Timeout:
        print("[ERRO] Timeout — o Crawl4AI demorou mais de 3 minutos")
        sys.exit(1)
    except requests.exceptions.HTTPError as e:
        print(f"[ERRO] HTTP {e.response.status_code}: {e.response.text[:300]}")
        sys.exit(1)


# ── Parsing da resposta ───────────────────────────────────────────────────────

def parse_response(crawl_result: dict, lot_url: str) -> tuple:
    """
    Retorna (dados_estruturados: dict, image_urls: list[str], markdown: str)
    """
    # Crawl4AI pode retornar lista em "results" ou objeto direto
    if isinstance(crawl_result, list):
        result = crawl_result[0] if crawl_result else {}
    elif "results" in crawl_result:
        results = crawl_result["results"]
        result = results[0] if results else {}
    else:
        result = crawl_result

    # ── Markdown bruto
    markdown_obj = result.get("markdown", {})
    if isinstance(markdown_obj, dict):
        markdown = markdown_obj.get("raw_markdown", "") or markdown_obj.get("fit_markdown", "")
    else:
        markdown = str(markdown_obj) if markdown_obj else ""

    # ── Dados estruturados: markdown parser primeiro (confiável), LLM complementa
    # Parser de markdown é o método primário — determinístico e sem custo de API
    structured = parse_markdown(markdown, lot_url) if markdown else {}

    # Tentar enriquecer com resultado do LLM (preenche campos que o regex não capturou)
    raw_extracted = result.get("extracted_content") or result.get("extraction_result", "")
    llm_data = {}
    if isinstance(raw_extracted, str) and raw_extracted.strip():
        try:
            parsed = json.loads(raw_extracted)
            if isinstance(parsed, list) and parsed:
                llm_data = parsed[0]
            elif isinstance(parsed, dict):
                llm_data = parsed
        except json.JSONDecodeError:
            pass
    elif isinstance(raw_extracted, dict):
        llm_data = raw_extracted

    # Mesclar: LLM preenche apenas campos ainda vazios no markdown parser
    if llm_data and isinstance(llm_data, dict) and llm_data.get("marca"):
        print("[INFO] LLM complementou os dados do markdown")
        for k, v in llm_data.items():
            if v and not structured.get(k):
                structured[k] = v

    # ── URLs de fotos: extrai do markdown (mais completo que media.images)
    image_urls = extract_photo_urls(markdown)

    # Completar com media.images do Crawl4AI se necessário
    if not image_urls:
        media = result.get("media", {})
        if isinstance(media, dict):
            for img in media.get("images", []):
                src = img.get("src", "")
                if _is_copart_photo(src):
                    image_urls.append(src)

    # Converter thumbnails → full resolution
    image_urls = [_to_full_res(u) for u in image_urls]
    # Deduplicar
    seen = set()
    image_urls = [u for u in image_urls if not (u in seen or seen.add(u))]

    return structured, image_urls, markdown


def parse_markdown(markdown: str, lot_url: str) -> dict:
    """
    Extrai dados estruturados do markdown da Copart usando regex.
    Funciona mesmo sem LLM.

    Formatos presentes no markdown da Copart:
      - Label na linha, valor na próxima: "Marca: \\nBYD"
      - Label e valor na mesma linha:     "Condição: FINANCIAMENTO"
      - Link markdown:                    "Pátio do Leilão: [CIDADE - UF](...)"
    """
    F = re.IGNORECASE | re.MULTILINE

    def nxt(label: str) -> str:
        """Valor na PRÓXIMA linha após o label."""
        m = re.search(rf"^{re.escape(label)}:\s*$\s*^(.+?)$", markdown, F)
        return m.group(1).strip() if m else ""

    def same(label: str) -> str:
        """Valor na MESMA linha após o label."""
        m = re.search(rf"^{re.escape(label)}:\s+(.+?)$", markdown, F)
        return m.group(1).strip() if m else ""

    def either(label: str) -> str:
        """Tenta mesma linha, depois próxima linha."""
        return same(label) or nxt(label)

    def link_text(label: str) -> str:
        """Extrai texto de link: [TEXTO](url)"""
        m = re.search(rf"{re.escape(label)}:\s+\[([^\]]+)\]", markdown, F)
        return m.group(1).strip() if m else either(label)

    # Código: aparece como "Código: 1083986" ou "### Código 1083986"
    code = (
        same("Código") or
        re.search(r"[Cc]ódigo[:\s]+(\d{5,})", markdown).group(1)
        if re.search(r"[Cc]ódigo[:\s]+(\d{5,})", markdown) else lot_code_from_url(lot_url)
    )

    # Título para fallback: "#  2025 BYD DOLPHIN MINI"
    title_m = re.search(r"^#\s+(\d{4}\s+.+?)$", markdown, F)
    title_parts = title_m.group(1).strip().split() if title_m else []
    ano_titulo  = title_parts[0] if title_parts and title_parts[0].isdigit() else ""
    marca_titulo = title_parts[1] if len(title_parts) > 1 else ""
    modelo_titulo = " ".join(title_parts[2:]) if len(title_parts) > 2 else ""

    # Versão: linha logo após DOLPHIN MINI (ex: "Dolphin Mini EV GS5 55 kW")
    versao_m = re.search(r"^Versão:\s*$\s*^(.+?)$", markdown, F)
    versao = versao_m.group(1).strip() if versao_m else ""

    # Notas: seção delimitada no markdown
    notas_m = re.search(r"Notas?:\s*\n(.*?)(?=\n###|\nInformações de Venda|\nCaracterísticas|\Z)",
                        markdown, re.DOTALL | re.IGNORECASE)
    notas = notas_m.group(1).strip() if notas_m else ""

    # Termos/condições gerais (texto longo das cláusulas)
    termos_m = re.search(r"(3\.1\..+?)(?=\n#{1,4}\s|\Z)", markdown, re.DOTALL)
    termos = termos_m.group(1).strip() if termos_m else ""

    data = {
        "codigo_lote":            code,
        "marca":                  nxt("Marca")          or marca_titulo,
        "modelo":                 nxt("Modelo")         or modelo_titulo,
        "versao":                 versao,
        "ano_fabricacao":         nxt("Ano de Fabricação") or ano_titulo,
        "ano_modelo":             nxt("Ano Modelo")     or ano_titulo,
        "blindado":               nxt("Blindado"),
        "tipo_documento":         nxt("Tipo de Documento"),
        "tipo_monta":             nxt("Tipo de Monta"),
        "condicao":               same("Condição"),
        "valor_fipe":             same("Valor FIPE"),
        "tipo_chassi":            same("Tipo de Chassi"),
        "combustivel":            same("Combustível"),
        "final_placa":            same("Final de Placa"),
        "chave":                  same("Chave"),
        "condicao_funcionamento": same("Condição de Func."),
        "patio":                  link_text("Pátio do Leilão") or link_text("Pátio Veículo"),
        "data_venda":             either("Data da Venda"),
        "notas":                  notas,
        "condicoes_especificas":  "",
        "termos_responsabilidade": termos,
    }

    return {k: v for k, v in data.items() if v}


def extract_photo_urls(markdown: str) -> list:
    """
    Extrai URLs de fotos do markdown.
    Copart usa: brimages.copart.com.br/Repository/Fotos/{uuid}?imageType=thumbnail
    """
    # Padrão específico da Copart Brazil
    urls = re.findall(
        r'https://brimages\.copart\.com\.br/[^\s\)\]"\']+',
        markdown
    )
    # Remover duplicatas mantendo ordem
    seen = set()
    return [u for u in urls if not (u in seen or seen.add(u))]


def _to_full_res(url: str) -> str:
    """Troca ?imageType=thumbnail por ?imageType=full para obter HD."""
    return re.sub(r"[?&]imageType=\w+", "?imageType=full", url)


def _is_copart_photo(url: str) -> bool:
    """Retorna True se a URL é uma foto de veículo da Copart."""
    if not url or not url.startswith("http"):
        return False
    return "brimages.copart.com.br" in url or "copart.com" in url.lower()


# ── Pasta do lote ─────────────────────────────────────────────────────────────

def build_lot_dir(data: dict, url: str, base_dir: Path) -> Path:
    """
    Cria e retorna o diretório do lote no padrão:
    lotes/{código}-{marca}-{modelo}-{ano}/
    """
    code  = data.get("codigo_lote") or lot_code_from_url(url)
    marca = slugify(data.get("marca", "veiculo"))
    modelo = slugify(data.get("modelo", ""))
    ano   = data.get("ano_modelo") or data.get("ano_fabricacao", "")

    parts = [p for p in [code, marca, modelo, str(ano)] if p]
    folder_name = re.sub(r"-+", "-", "-".join(parts)).strip("-")

    lot_dir = base_dir / "lotes" / folder_name
    (lot_dir / "dados-brutos").mkdir(parents=True, exist_ok=True)
    (lot_dir / "fotos").mkdir(parents=True, exist_ok=True)
    return lot_dir


# ── Salvar dados ──────────────────────────────────────────────────────────────

def save_description(data: dict, lot_dir: Path, url: str):
    """Salva descricao-lote.txt no formato padrão do projeto."""

    def field(key: str, label: str) -> str:
        val = data.get(key, "")
        return f"{label}: {val}" if val else f"{label}: —"

    lines = [
        "Leiloeira: Copart Brazil",
        f"URL: {url}",
        field("codigo_lote", "Código do Lote"),
        "",
        "--- DADOS DO VEÍCULO ---",
        field("marca",                  "Marca"),
        field("modelo",                 "Modelo"),
        field("versao",                 "Versão"),
        field("ano_fabricacao",         "Ano de Fabricação"),
        field("ano_modelo",             "Ano Modelo"),
        field("blindado",               "Blindado"),
        field("combustivel",            "Combustível"),
        field("final_placa",            "Final de Placa"),
        field("chave",                  "Chave"),
        field("condicao_funcionamento", "Condição de Funcionamento"),
        "",
        "--- DANO / CLASSIFICAÇÃO ---",
        field("condicao",       "Condição"),
        field("tipo_documento", "Tipo de Documento"),
        field("tipo_monta",     "Tipo de Monta"),
        field("tipo_chassi",    "Tipo de Chassi"),
        "",
        "--- VALORES ---",
        field("valor_fipe", "Valor FIPE"),
        "",
        "--- LOCALIZAÇÃO ---",
        field("patio", "Pátio"),
        "",
        "--- STATUS DA VENDA ---",
        field("data_venda", "Data da Venda"),
        "",
        "--- NOTAS ---",
        data.get("notas", "").strip() or "(não extraído — ver pagina-raw.md)",
        "",
        "--- CONDIÇÕES ESPECÍFICAS ---",
        data.get("condicoes_especificas", "").strip() or "(não extraído — ver pagina-raw.md)",
        "",
        "--- TERMOS DE RESPONSABILIDADE ---",
        data.get("termos_responsabilidade", "").strip() or "(não extraído — ver pagina-raw.md)",
    ]

    dest = lot_dir / "dados-brutos" / "descricao-lote.txt"
    dest.write_text("\n".join(lines), encoding="utf-8")
    print(f"[OK] {dest}")


def save_markdown(markdown: str, lot_dir: Path):
    """Salva o markdown bruto da página como fallback para leitura humana."""
    if not markdown.strip():
        return
    dest = lot_dir / "dados-brutos" / "pagina-raw.md"
    dest.write_text(markdown, encoding="utf-8")
    print(f"[OK] {dest}  ({len(markdown):,} chars)")


# ── Download de fotos ─────────────────────────────────────────────────────────

def download_photos(image_urls: list, lot_dir: Path):
    """Baixa as fotos para a pasta fotos/, mantendo nome original."""
    if not image_urls:
        print("[AVISO] Nenhuma URL de foto encontrada pelo Crawl4AI")
        return

    fotos_dir = lot_dir / "fotos"
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        )
    }

    # Mapa Content-Type → extensão
    EXT = {
        "image/jpeg": ".jpg", "image/jpg": ".jpg",
        "image/png":  ".png", "image/webp": ".webp",
        "image/gif":  ".gif", "image/bmp":  ".bmp",
    }

    downloaded = skipped = errors = 0
    for url in image_urls:
        base_name = url.split("?")[0].split("/")[-1]
        if not base_name:
            continue

        # Verificar se já existe com qualquer extensão
        existing = list(fotos_dir.glob(f"{base_name}*"))
        if existing:
            skipped += 1
            continue

        try:
            r = requests.get(url, headers=headers, stream=True, timeout=30)
            if r.ok:
                # Determinar extensão pelo Content-Type
                ct = r.headers.get("Content-Type", "").split(";")[0].strip().lower()
                ext = EXT.get(ct, "")
                # Fallback: detectar pelos magic bytes
                content = r.content
                if not ext:
                    if content[:3] == b"\xff\xd8\xff":
                        ext = ".jpg"
                    elif content[:8] == b"\x89PNG\r\n\x1a\n":
                        ext = ".png"
                    elif content[:4] == b"RIFF" and content[8:12] == b"WEBP":
                        ext = ".webp"

                filename = base_name + ext
                (fotos_dir / filename).write_bytes(content)
                downloaded += 1
                print(f"  [↓] {filename}  ({len(content) // 1024} KB)")
            else:
                print(f"  [!] HTTP {r.status_code} — {base_name}")
                errors += 1
        except Exception as e:
            print(f"  [!] Erro ao baixar {base_name}: {e}")
            errors += 1

    print(f"[INFO] Fotos: {downloaded} baixadas, {skipped} já existiam, {errors} erros")


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Coleta dados e fotos de um lote Copart Brazil via Crawl4AI"
    )
    parser.add_argument("url",        help="URL do lote (ex: https://www.copart.com.br/lot/1083986)")
    parser.add_argument("--dir",      default=None, help="Diretório base do projeto")
    parser.add_argument("--no-photos",action="store_true", help="Não baixar fotos")
    args = parser.parse_args()

    # Diretório base: pai do diretório scripts/ (raiz do projeto)
    base_dir = Path(args.dir) if args.dir else Path(__file__).resolve().parent.parent

    print(f"\n=== Copart Scraper ===")
    print(f"Lote:       {args.url}")
    print(f"Projeto:    {base_dir}")
    print(f"Crawl4AI:   {CRAWL4AI_URL}")
    print()

    if not check_health():
        sys.exit(1)

    # 1. Raspar página
    crawl_result = crawl_lot(args.url)

    # 2. Parsear resposta
    structured, image_urls, markdown = parse_response(crawl_result, args.url)

    if not structured:
        print("[AVISO] LLM não retornou dados estruturados — verifique GEMINI_API_KEY")
        if not markdown:
            print("[ERRO] Crawl4AI também não retornou markdown. Resposta bruta:")
            print(json.dumps(crawl_result, indent=2, ensure_ascii=False)[:1000])
            sys.exit(1)

    # 3. Criar pasta do lote
    lot_dir = build_lot_dir(structured, args.url, base_dir)
    print(f"[INFO] Pasta: {lot_dir}")

    # 4. Salvar dados
    save_description(structured, lot_dir, args.url)
    save_markdown(markdown, lot_dir)

    # 5. Baixar fotos
    if not args.no_photos:
        print(f"\n[INFO] {len(image_urls)} URLs de fotos encontradas")
        download_photos(image_urls, lot_dir)

    print(f"\n[CONCLUÍDO] {lot_dir}")


if __name__ == "__main__":
    main()
