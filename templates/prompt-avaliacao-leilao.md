# Prompt: Avaliação de Lote de Veículo em Leilão — Brasil

## Como Usar

1. Abra **Claude.ai** (recomendado pela visão multimodal e raciocínio) ou Gemini Pro
2. Cole o **System Prompt** abaixo no campo de configuração do sistema (se disponível)
3. Inicie a conversa colando o **Prompt do Usuário** com os dados preenchidos
4. **Anexe todas as fotos do lote** na mesma mensagem
5. Para um novo lote: substitua tudo entre `[COLCHETES]` pelos dados do novo veículo

---

## PARTE 1 — SYSTEM PROMPT

```
Você é um especialista em avaliação de veículos de leilão no Brasil, com amplo
conhecimento em:

- Tabela FIPE e precificação do mercado de usados brasileiro
- Legislação de trânsito brasileira (CTB, Denatran, DETRAN)
- Veículos "recuperados de sinistro" e "sucata": implicações legais, de seguro
  e de revenda
- Classificações de dano veicular (Pequena Monta, Média Monta, Grande Monta)
- Exigências de vistoria INMETRO para veículos de Média e Grande Monta
- Mecânica automotiva geral e específica de veículos híbridos e elétricos
- Danos causados por enchente em veículos convencionais e híbridos (sistema de
  alta tensão, bateria HV, eCVT, chicotes elétricos, ECUs)
- Custos de transferência inter-estadual no Brasil (DETRAN, placa Mercosul)
- Estrutura de custos de leiloeiros brasileiros (comissão, taxa de depósito,
  logística, licenciamento)
- Mercado de peças e mão de obra para veículos importados no Brasil
- Riscos e oportunidades em leilões de seguradoras (Porto Seguro, Bradesco,
  Allianz, SulAmérica etc.)

Seu papel é fornecer uma análise TÉCNICA, IMPARCIAL e FINANCEIRAMENTE PRECISA
de cada lote apresentado. Nunca subestime riscos ocultos. Sempre calcule o
CUSTO TOTAL DE AQUISIÇÃO (CTA) antes de recomendar um lance máximo.

Ao analisar fotos, examine sistematicamente: lataria, vidros, interior, motor
(se visível), pneus, rodas, fluidos visíveis, chassi/longarina (se visível) e
quaisquer sinais de corrosão, mau-reparo anterior, ou dano por água/fogo.

Para veículos híbridos com dano por enchente, sinalize SEMPRE o risco da
bateria de alta tensão como item de custo incerto e potencialmente proibitivo.
```

---

## PARTE 2 — PROMPT DO USUÁRIO (Template Preenchível)

> **INSTRUÇÃO**: Substitua os campos `[ENTRE COLCHETES]` pelos dados do seu
> lote. O exemplo abaixo já está preenchido com o Prius (Lote 0215).
> Para outros veículos, substitua tudo.

---

```
Preciso avaliar um lote de leilão de veículo no Brasil. Analise as fotos
anexadas e os dados abaixo para me dar um relatório completo.

═══════════════════════════════════════════════
 DADOS DO LOTE
═══════════════════════════════════════════════

Leiloeiro: Sodré Santoro (JUCESP 192)
Leilão nº: 28139
Lote: 0215
Data do leilão: 27/02/2026
Vendedor/Comitente: Porto Seguro Seguros

Veículo: Toyota Prius NGA TOP
Ano fab./modelo: 2017/2017
Cor: Preta
KM: 101.539
Combustível: Híbrido (gasolina/elétrico)
Câmbio: Automático
Ar-condicionado: Sim
Blindagem: Não
Kit Gás: Ausente
Chave de ignição: Sim

Danos declarados: "Câmbio Danificado – veículo de enchente"
Classificação de dano: Média Monta
Estado do chassi: Íntegro (conforme descrição)
Origem: Seguro (sinistro de seguradora)

IPVA 2026: PAGO pelo vendedor (válido até entrega do documento)
Licenciamento 2026: Responsabilidade do comprador
Multas anteriores ao leilão até R$ 500,00: Responsabilidade do comprador
Documentação: Será entregue o ATPV-e em até 30 dias úteis

Local físico do bem: Rodovia Castelo Branco KM 148 – Cesário Lange/SP

═══════════════════════════════════════════════
 REFERÊNCIA DE MERCADO
═══════════════════════════════════════════════

Tabela FIPE (verificar em fipe.org.br):
Modelo: Toyota Prius 1.8 16V (2017) — aproximadamente R$ [CONSULTAR FIPE ATUAL]
Nota: consulte a tabela FIPE para o mês atual antes de preencher.

Valor de mercado estimado para veículo sem sinistro e em bom estado: R$ [FIPE]
Valor de mercado estimado COM sinistro/recuperado (desconto 25-40%): R$ [CALCULAR]

═══════════════════════════════════════════════
 ESTRUTURA DE CUSTOS DO LEILOEIRO
═══════════════════════════════════════════════

Comissão do leiloeiro: 5% sobre o valor do lance
Taxa de depósito (veículo leve): R$ 1.900,00 (fixa)
Taxa de logística Porto Seguro: R$ 250,00 (obrigatória)

Forma de cálculo do total pago ao leiloeiro:
  Total = Lance + (Lance × 5%) + R$ 1.900 + R$ 250

Exemplos:
  Lance R$ 9.500 → Total R$ 12.179
  Lance R$ 12.000 → Total R$ 15.050
  Lance R$ 15.000 → Total R$ 18.650

═══════════════════════════════════════════════
 DADOS DO COMPRADOR
═══════════════════════════════════════════════

Cidade/Estado do comprador: Londrina – Paraná (PR)
Distância até o bem: ~560 km (Cesário Lange/SP → Londrina/PR)
Intenção de uso: [USO PRÓPRIO / REVENDA / REFORMA E REVENDA]

═══════════════════════════════════════════════
 CUSTOS ADICIONAIS ESTIMADOS (Londrina/PR)
═══════════════════════════════════════════════

Frete (Cesário Lange/SP → Londrina/PR): R$ 800 – R$ 1.500
Licenciamento 2026 (SP): R$ 200 – R$ 350
Transferência inter-estadual DETRAN-PR: R$ 310
Placa Mercosul (obrigatória troca inter-estado): R$ 200 – R$ 350
Despachante: R$ 500 – R$ 1.200
Laudo cautelar (recomendado): R$ 300 – R$ 600
Vistoria INMETRO (obrigatória – Média Monta): R$ 300 – R$ 500

Subtotal custos adicionais (estimativa): R$ 2.610 – R$ 4.810

═══════════════════════════════════════════════
 ALERTAS TÉCNICOS PRÉ-IDENTIFICADOS
═══════════════════════════════════════════════

1. VEÍCULO HÍBRIDO DE ENCHENTE: O "câmbio" do Prius é um sistema eCVT
   integrado com dois motores elétricos e a bateria de alta tensão (HV).
   Avaliar especialmente o risco de dano à bateria HV e ao inversor.

2. MÉDIA MONTA: Exige aprovação em vistoria INMETRO antes de circular.
   Custo adicional + risco de reprovação.

3. ORIGEM SEGURO: Alta probabilidade de constar "Recuperado de Sinistro"
   no documento. Verificar antes de arrematar.

4. TRANSFERÊNCIA INTER-ESTADUAL: SP → PR exige placa Mercosul nova e
   processo completo no DETRAN-PR. Prazo de 60 dias para regularizar.

═══════════════════════════════════════════════
 SOLICITAÇÃO DE ANÁLISE
═══════════════════════════════════════════════

Com base nas fotos anexadas e nos dados acima, forneça:

1. ANÁLISE VISUAL (foto a foto ou por área):
   - Danos externos visíveis (lataria, vidros, rodas, pneus)
   - Interior (estofado, painel, sinais de água/lama/mofo)
   - Compartimento do motor (se visível)
   - Sinais de corrosão, oxidação ou dano estrutural
   - Qualidade das fotos: o que NÃO é possível ver e por quê isso é risco

2. ANÁLISE DOCUMENTAL:
   - Red flags nos dados do lote
   - Probabilidade de constar "Recuperado de Sinistro" no documento
   - Itens de responsabilidade do comprador que merecem atenção
   - Inconsistências entre descrição e fotos (se houver)

3. MAPA DE CUSTOS TOTAL (tabela):
   Calcule o Custo Total de Aquisição (CTA) para três cenários de lance:
   - Cenário A (lance atual): R$ 9.500
   - Cenário B (lance moderado): R$ [sugerir com base na análise]
   - Cenário C (lance máximo recomendado): R$ [calcular]

   Para cada cenário, liste: lance + comissão/depósito/logística + frete +
   documentação + reparo estimado (mínimo e máximo) = CTA mínimo e máximo.

4. AVALIAÇÃO DE RISCOS:
   - Risco documental (sinistro, restrições): BAIXO / MÉDIO / ALTO
   - Risco técnico/mecânico: BAIXO / MÉDIO / ALTO / CRÍTICO
   - Risco financeiro (estourar orçamento): BAIXO / MÉDIO / ALTO / CRÍTICO
   - Risco de revenda (liquidez): BAIXO / MÉDIO / ALTO (se aplicável)
   - Risco específico bateria HV (híbrido + enchente): detalhar

5. VEREDICTO FINAL:
   - Vale a pena? SIM / NÃO / CONDICIONAL (especificar condição)
   - Lance máximo recomendado (com margem de segurança de 20%): R$ ___
   - Custo total esperado até o veículo regularizado e em uso: R$ ___
   - Justificativa objetiva em 3-5 linhas
   - O que fazer ANTES de dar o lance (vistoria presencial, consulta DETRAN etc.)
```

---

## PARTE 3 — CHECKLIST PRÉ-LANCE

Use esta lista antes de arrematar qualquer veículo de leilão:

- [ ] Consultei a Tabela FIPE do mês atual para este modelo/ano
- [ ] Verifiquei débitos e restrições no site do DETRAN de origem (SP)
- [ ] Consultei o histórico no site do SENATRAN / RENAVAM
- [ ] Verifiquei se há recall pendente (consulta pelo RENAVAM/VIN em recalls.denatran.gov.br)
- [ ] Calculei o CTA completo (não apenas o lance)
- [ ] Pesquisei preços de peças críticas (bateria HV, câmbio, etc.) para este modelo
- [ ] Pesquisei oficinas especializadas em Londrina/PR para este modelo
- [ ] Li as condições de venda do leiloeiro integralmente
- [ ] Sei o prazo para retirada do veículo (e custo de estadia após o prazo)
- [ ] Tenho orçamento de contingência de pelo menos 30% sobre o reparo estimado

---

## PARTE 4 — DADOS ESPECÍFICOS PARA OUTROS LOTES

Para reutilizar este prompt com outro veículo, substitua no Prompt do Usuário:

| Campo | O que preencher |
|-------|----------------|
| Leiloeiro / Leilão / Lote | Dados do novo leilão |
| Vendedor/Comitente | Quem está vendendo |
| Dados do veículo | Marca, modelo, ano, KM, cor, itens |
| Danos declarados | Exatamente como consta no lote |
| Classificação de dano | Pequena / Média / Grande Monta (ou "não informado") |
| IPVA / Licenciamento | Quem paga cada item |
| Estrutura de custos | 5% comissão + taxa de depósito do leiloeiro específico |
| Frete | Calcule pela distância atual |
| Alertas técnicos | Adapte aos riscos do novo modelo/tipo de dano |

---

## NOTAS DE REFERÊNCIA

### Classificação de Dano (DENATRAN)
| Classificação | Critério | Exigência |
|---------------|----------|-----------|
| Pequena Monta | Danos leves, reparáveis sem comprometer estrutura | Vistoria comum |
| Média Monta | Danos moderados, sem destruição total | Vistoria INMETRO obrigatória |
| Grande Monta | Danos severos, estrutura comprometida | Vistoria INMETRO + possível rejeição |
| Sucata | Irrecuperável para circulação | Somente para desmanche |

### Comissão Sodré Santoro (Veículos)
| Item | Valor |
|------|-------|
| Comissão leiloeiro | 5% do lance |
| Taxa de depósito – moto | R$ 500 |
| Taxa de depósito – veículo leve | R$ 1.900 |
| Taxa de depósito – pesado | R$ 4.500 |
| Logística Porto Seguro (este lote) | R$ 250 |

### Custos de Transferência SP → PR (Londrina)
| Item | Valor estimado |
|------|---------------|
| Taxa de transferência inter-estadual DETRAN-PR | R$ 310 |
| Placa Mercosul (obrigatória) | R$ 200–350 |
| Licenciamento 2026 SP | R$ 200–350 |
| Despachante | R$ 500–1.200 |
| Laudo cautelar (recomendado) | R$ 300–600 |
| Vistoria INMETRO – Média Monta | R$ 300–500 |

### Risco Bateria HV – Toyota Prius 2017 (Enchente)
| Componente | Custo estimado de substituição |
|------------|-------------------------------|
| Bateria HV (pack completo) | R$ 15.000–40.000 |
| Inversor/conversor | R$ 5.000–12.000 |
| eCVT / Power Split Device | R$ 5.000–15.000 |
| ECU híbrida | R$ 3.000–8.000 |
| Chicotes e sensores | R$ 1.500–5.000 |
| **Pior caso total** | **R$ 30.000–70.000** |

> **Atenção**: Sem vistoria presencial por especialista em híbridos, o risco
> real da bateria HV é DESCONHECIDO. Este é o fator que pode tornar o Prius
> inviável financeiramente mesmo com lance baixo.
