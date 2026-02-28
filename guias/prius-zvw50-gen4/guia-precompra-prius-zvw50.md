# Guia de Pré-Compra — Toyota Prius ZVW50 (4ª Geração, 2016–2022)

> Versão: Fevereiro 2026 | Foco: Leilão / Compra de terceiros com histórico incerto

---

## Índice

1. [Dr. Prius App — Guia Completo](#1-dr-prius-app--guia-completo)
2. [Compatibilidade de Dongles OBD](#2-compatibilidade-de-dongles-obd)
3. [Checklist Pré-Compra Presencial](#3-checklist-pré-compra-presencial)
4. [Prius Gen 3 × Gen 4 — O que melhorou](#4-prius-gen-3--gen-4--o-que-melhorou)
5. [Problemas Conhecidos do Gen 4 (ZVW50)](#5-problemas-conhecidos-do-gen-4-zvw50)

---

## 1. Dr. Prius App — Guia Completo

### O que é

**Dr. Prius** é o aplicativo mais completo disponível para diagnóstico da bateria de alta tensão (HV) de veículos Toyota/Lexus híbridos. Desenvolvido especificamente para Prius, ele acessa ECUs que aplicativos OBD genéricos não conseguem ler, entregando dados detalhados da bateria NiMH/Li-ion.

Disponível para **Android** (Google Play) e **iOS** (App Store).

### Versão Gratuita × Versão Paga

| Função | Gratuita | Paga (~US$ 11,99 / ~R$ 65–70) |
|--------|----------|-------------------------------|
| Download e instalação | ✅ | ✅ |
| Leitura de PIDs da bateria HV (tensões, temperaturas) | ✅ | ✅ |
| Visualização de dados brutos em tempo real | ✅ | ✅ |
| Leitura de DTCs (códigos de falha) | ✅ | ✅ |
| **Battery Health Test (BHT)** | ❌ | ✅ |
| Teste de expectativa de vida da bateria | ❌ | ✅ |
| Diagnóstico avançado de células | ❌ | ✅ |

> **Atenção:** A licença paga tem **limite de 3 usos**. Use com sabedoria — idealmente apenas no veículo que for comprar.

### Como usar para avaliar a bateria HV antes de comprar

1. **Conecte o dongle OBD** à porta OBD-II (abaixo do volante, lado esquerdo)
2. Abra o Dr. Prius e conecte ao adaptador
3. Ligue o veículo em **READY mode** (não precisa dar partida — só pressionar o botão de ignição com freio)
4. Na tela principal, verifique os **block voltages** — as tensões de cada bloco da bateria
5. Se tiver a versão paga, execute o **Battery Health Test (BHT)**

### Interpretando os resultados

| Indicador | O que é | Valores saudáveis |
|-----------|---------|------------------|
| **SOH%** (State of Health) | Saúde geral da bateria em % da capacidade original | Acima de 70% = ok; abaixo de 60% = próxima de substituição |
| **Block Voltages** | Tensão de cada bloco de células | Devem ser uniformes. Variação > 0,5V entre blocos = alerta |
| **Internal Resistance** | Resistência interna de cada bloco | Valores altos = células degradadas |
| **Temperature** | Temperatura dos módulos | Deve ser uniforme e não excessivamente alta |
| **DTCs** | Códigos de falha ativos ou históricos | P0A80 = célula degradada; P3000 series = problema HV |

> **Código P0A80** ("Replace Hybrid Battery Pack") é o mais crítico. Se aparecer, a bateria está com módulos degradados. Substituição completa custa R$ 3.000–8.000+ dependendo da procedência.

---

## 2. Compatibilidade de Dongles OBD

### ⚠️ Dongle do usuário: ELM327 Mini Bluetooth (azul translúcido)

**VEREDICTO: NÃO COMPATÍVEL com Dr. Prius.**

O site oficial **priusapp.com/obd.html** lista explicitamente:

> **"No Name Junk (blue transparent)"** — categoria: **NOT COMPATIBLE**
>
> *"appears to support switching between ECUs, but it failed to retrieve any battery-related information from both Prius Gen2 and Gen3. This is definitely one of the worst adapters, as it doesn't even support most of the basic OBD commands from v1.2 all the way to v2.3"*

Este dongle não funciona para Dr. Prius. Não adianta tentar configurações alternativas — a limitação é de hardware/firmware.

### Por que clones baratos falham (explicação técnica)

O Dr. Prius precisa trocar entre diferentes ECUs do veículo usando o comando **`AT SH`** (Set Message Header). Este comando define o cabeçalho CAN para comunicar com ECUs específicas (como a do Battery Management System).

Clones baratos (especialmente os translúcidos azuis/vermelhos de marcas sem nome) **não implementam corretamente o `AT SH`**, então:
- Conseguem ler PIDs genéricos do motor (RPM, temperatura)
- Mas **não conseguem acessar a ECU da bateria HV**
- Resultado: Dr. Prius conecta, mas não obtém dados da bateria

Este é o motivo de 90% das incompatibilidades relatadas por usuários.

### Dongles compatíveis com Dr. Prius

| Adaptador | Compatibilidade | Sistema | Preço estimado (USD) |
|-----------|----------------|---------|---------------------|
| **Veepeak OBDCheck BLE+** | ✅ Totalmente compatível | Android + iOS | US$ 25–35 |
| **PanLong** (versão preta ou azul — **NÃO a vermelha**) | ✅ Compatível | Android + iOS | US$ 15–20 |
| **NEXAS Bluetooth 5.0** | ✅ Compatível | Android + iOS | US$ 20–30 |
| **BAFX 34t5** | ✅ Compatível | Android apenas | US$ 20–25 |
| OBDLink MX+ | ✅ Com ressalvas | Android + iOS | US$ 80–100 |
| ELM327 Mini azul translúcido | ❌ **NÃO COMPATÍVEL** | — | — |
| ELM327 Mini vermelho | ❌ NÃO COMPATÍVEL | — | — |
| Clones genéricos sem marca | ❌ Geralmente falham | — | — |

### Onde comprar no Brasil

- **AliExpress**: Veepeak OBDCheck BLE+ (verificar se é o original com foto do produto — deve ser preto, não azul)
- **Mercado Livre**: PanLong versão preta/azul (buscar "PanLong OBD Bluetooth" — evitar a versão vermelha)
- **Amazon Brasil**: Veepeak costuma ter estoque (mais caro, mas entrega rápida e garantia)

> **Dica**: Para compra em leilão onde você tem tempo limitado com o veículo, prefira alugar o serviço de um mecânico com scanner Toyota específico, ou levar alguém de confiança com o equipamento certo.

---

## 3. Checklist Pré-Compra Presencial

> Use este checklist durante a visita ao veículo. Itens marcados com 🔴 são críticos — problema aqui pode inviabilizar a compra.

### A) Sistema Híbrido (mais crítico)

- [ ] 🔴 **Ligar em READY mode**: painel acende normalmente, sem ícone de exclamação laranja "!"
- [ ] 🔴 **Ícone "!" laranja**: ausente — se presente, indica falha no sistema HV (pode ser grave)
- [ ] **Modo EV funcional**: pressionar botão EV Mode, veículo deve circular ~1–2 km sem ligar motor a combustão
- [ ] **Frenagem regenerativa**: ao frear suavemente, painel de fluxo de energia deve mostrar "CHG" (carregando bateria)
- [ ] **Fluido do inversor**: verificar reservatório próprio (diferente do radiador do motor) — deve estar no nível e transparente/levemente amarelado
- [ ] 🔴 **Scan OBD na bateria HV**: verificar ausência de P0A80 (células degradadas) e P3xxx (falha HV geral)
- [ ] **Block voltages**: se com Dr. Prius, verificar uniformidade das tensões entre blocos (variação > 0,5V = alerta)
- [ ] **Fan da bateria HV**: ouvir se ventilador da bateria (traseiro) funciona — liga ao aquecer em uso
- [ ] **Temperatura da bateria**: não deve estar excessivamente quente mesmo após uso prolongado

### B) Motor a Combustão (2ZR-FXE)

- [ ] 🔴 **Óleo**: verificar cor (deve ser âmbar/marrom) e nível — óleo branco cremoso = água no sistema = catastrófico
- [ ] **Consumo de óleo**: perguntar histórico de reposição entre trocas — o 2ZR-FXE tem alguns relatos de consumo
- [ ] **Tampa do óleo**: verificar por dentro se há emulsificação (pasta branca = água)
- [ ] **EGR**: verificar fumaça escura/branca excessiva no arranque a frio
- [ ] **Aquecimento**: motor deve atingir temperatura normal rapidamente e se manter estável
- [ ] **Ruídos anormais**: sem batidas, chiados ou ruídos metálicos em qualquer faixa de RPM
- [ ] **Vela de ignição**: verificar histórico de troca (recomendado a cada 60.000 km)

### C) Freios

- [ ] **Pedal firme**: sem afundamento excessivo, sem pulsação
- [ ] **Frenagem responsiva**: frear em velocidade baixa — carro para progressiva e suavemente
- [ ] 🔴 **Brake actuator**: no Gen 3 era falha grave e cara. No Gen 4 foi melhorado, mas verificar se pedal tem comportamento estranho (esponjoso, inconsistente)
- [ ] **Pastilhas e discos**: verificar desgaste (pela regenerativa, tendem a durar mais, mas verificar)
- [ ] **Freio de estacionamento**: verificar funcionamento do freio elétrico (botão "P" no console)

### D) Transmissão / eCVT

- [ ] **Sem ruídos ao acelerar**: nenhum gemido, chiado ou vibração anormal
- [ ] **Sem ruídos ao desacelerar**: silêncio ou apenas som da regeneração
- [ ] **Vibração**: sem tremores em nenhuma velocidade (poderia indicar junta homocinética, pneu, ou problema no eCVT)
- [ ] **Marcha ré**: verificar câmera de ré, funcionamento suave, sem ruídos

### E) Bateria Auxiliar 12V

- [ ] 🔴 **Idade da bateria 12V**: perguntar data da última troca — recomendado substituir a cada 3–5 anos. Bateria morta = carro não liga em READY mode
- [ ] **Funcionamento elétrico geral**: vidros elétricos, retrovisores, travas, ar-condicionado
- [ ] **Iluminação**: faróis full-LED (Gen 4 tem LED de série na maioria das versões), DRLs, setas
- [ ] **Touch screen**: verificar responsividade e funcionamento do sistema Toyota Entune/áudio

### F) Exterior e Estrutura

- [ ] 🔴 **Catalisador**: o Prius Gen 4 é um dos veículos mais visados para furto de catalisador no Brasil e no exterior. Verificar por baixo do carro se o catalisador é original (não substituído por tubo reto ou catalisador aftermarket sem o sensor)
- [ ] **Assoalho por baixo**: buscar sinais de enchente (lama acumulada, oxidação excessiva, módulos elétricos afetados)
- [ ] **Longarinas e chassi**: verificar por torção ou solda de reparo (indício de colisão grave)
- [ ] **Pintura**: verificar uniformidade das cores nos painéis — diferenças indicam reparo pós-colisão
- [ ] **Vidros**: verificar trincas, desalinhamentos
- [ ] **Pneus**: verificar desgaste uniforme — desgaste irregular = problema de alinhamento, suspensão ou geometria
- [ ] **Suspensão**: empurrar cada canto do carro — deve absorver e não quicar (amortecedores ok)
- [ ] **Sensores de estacionamento**: verificar funcionamento (bip ao aproximar obstáculo)

### G) Recalls Obrigatórios

- [ ] 🔴 **Consultar recalls via RENAVAM** no site do SENATRAN/DENATRAN (gov.br)
- [ ] **Recall do airbag Takata**: afetou Prius 2016–2019 em muitos países — verificar se foi feito
- [ ] **Recall de software HV**: Toyota emitiu atualizações de software para o sistema híbrido — verificar se está atualizado
- [ ] **Outros recalls Toyota Brasil**: verificar site da Toyota Brasil (toyota.com.br → Serviços → Recall) com o chassi/VIN

> Para consultar recalls nos EUA (se for importado): **nhtsa.gov/recalls** com o VIN

### H) Documentação e Histórico

- [ ] 🔴 **Consulta DETRAN**: verificar débitos (IPVA, multas), restrições, comunicado de venda
- [ ] **Consulta sinistro**: verificar no DETRAN ou serviços como Consulta Leilão / FIPE se consta como sinistrado, leiloado, recuperado
- [ ] **Histórico de manutenção**: caderneta ou notas fiscais — troca de óleo, fluido do inversor (recomendado a cada 100.000 km ou 5 anos), 12V
- [ ] **Quilometragem coerente**: KM deve ser compatível com desgaste de interior, volante, pedais e histórico de manutenção
- [ ] **Proprietários anteriores**: mais proprietários = histórico mais incerto; verificar se consta no DUT

---

## 4. Prius Gen 3 × Gen 4 — O que melhorou

| Item | Gen 3 (ZVW30, 2009–2015) | Gen 4 (ZVW50, 2016–2022) |
|------|--------------------------|--------------------------|
| **Brake Actuator** | 🔴 Falha grave e cara — pedal duro, carro não para | ✅ Melhorado significativamente |
| **Consumo** | ~45–50 mpg (cidade) | ~52–56 mpg — mais eficiente |
| **Bateria HV** | NiMH — boa durabilidade | NiMH — mesmo tipo, melhor gerenciamento |
| **Design** | Convencional, aerodínâmico | Mais agressivo (frente Toyota "Keen Look") |
| **Direção** | Elétrica | Elétrica — feedback ligeiramente melhor |
| **Segurança** | Sem assistentes ativos | Toyota Safety Sense (colisão, faixa) em versões equipadas |
| **Tecnologia** | Sistema Toyota/Pioneer | Toyota Entune, conectividade melhorada |
| **Motor** | 1NZ-FXE (1.5L) | 2ZR-FXE (1.8L) — mais potente |

> **Conclusão**: O Gen 4 resolve o problema mais grave do Gen 3 (brake actuator) e oferece mais eficiência e tecnologia. A bateria ainda é NiMH e tem durabilidade similar.

---

## 5. Problemas Conhecidos do Gen 4 (ZVW50)

| Problema | Gravidade | O que verificar |
|----------|-----------|----------------|
| **Furto do catalisador** | 🔴 Alta | Verificar por baixo se catalisador é original |
| **Consumo de óleo (2ZR-FXE)** | Média | Histórico de reposição, nível na inspeção |
| **Bomba d'água elétrica (inversor)** | Média | Falha silenciosa — verificar temperatura do inversor, histórico |
| **EGR acúmulo de carbono** | Baixa-Média | Menos que Gen 3, mas verificar fumaça ao frio |
| **Desgaste dos pneus Ecopia EP422** | Baixa | Pneus originais gastam rápido — verificar se foram trocados por outros de qualidade similar |
| **Bateria 12V** | Média | Deve ser trocada a cada 3–5 anos; falha deixa carro parado |
| **Módulo TSS (Toyota Safety Sense)** | Baixa | Verificar se radar dianteiro não está desconfigurado ou com aviso |
| **Degradação da bateria HV** | Depende do uso | Verificar via Dr. Prius ou scanner Toyota específico |

---

## Resumo Executivo — Semáforo de Compra

| Situação | Decisão sugerida |
|----------|-----------------|
| SOH > 70%, sem DTCs HV, documentação ok | ✅ Compra com segurança |
| SOH 60–70%, sem DTCs, preço adequado | ⚠️ Negociar desconto para troca futura da bateria |
| DTC P0A80 ativo | 🔴 Apenas com preço muito abaixo + orçamento de substituição em mãos |
| Ícone "!" laranja no painel | 🔴 Não comprar sem diagnóstico completo e preço correspondente |
| Catalisador furtado | 🔴 Custo de reposição R$ 2.000–5.000 — descontar do preço |
| Sinistro grave / enchente | 🔴 Evitar — módulos elétricos comprometidos são imprevisíveis |

---

*Guia elaborado com base em: priusapp.com, Toyota Technical Information System, fóruns PriusChat, experiência de mecânicos especializados em híbridos.*
