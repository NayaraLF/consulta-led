# 💡 Ferramenta de Consulta de Compatibilidade de Lâmpadas Automotivas

Sistema de consulta de compatibilidade de lâmpadas para veículos, com dados coletados de 3 fontes especializadas: **Liderauto**, **Rayx** e **Permak**.

## 📋 Conteúdo

- `scraping_lampadas.py` — Script que coleta dados das 3 fontes
- `consulta_lampadas.html` — Interface de busca (funciona offline com os dados coletados)
- `lampadas_data.json` — Base de dados gerada (criado após rodar o scraping)

---

## 🚀 Instalação Rápida

### 1. Preparar Python e dependências

```bash
pip install requests beautifulsoup4
```

### 2. Gerar os dados (uma única vez)

```bash
python scraping_lampadas.py
```

Isso criará o arquivo `lampadas_data.json` na mesma pasta.

**Resultado esperado:**
```
============================================================
SCRAPING DE LÂMPADAS AUTOMOTIVAS
============================================================

Scraping Liderauto...
  ✓ XXX registros extraídos
Scraping Rayx...
  ✓ XXX registros extraídos
Scraping Permak...
  ✓ XXX registros extraídos

✓ XXXX registros salvos em lampadas_data.json
============================================================
```

### 3. Abrir a interface de consulta

#### Opção A: Abrir localmente (recomendado)

```bash
python -m http.server 8000
```

Depois abra no navegador:
```
http://localhost:8000/consulta_lampadas.html
```

#### Opção B: Abrir diretamente (pode ter restrições)

Simplesmente abra o arquivo `consulta_lampadas.html` diretamente no navegador.
*Nota: Alguns navegadores podem bloquear o carregamento de `lampadas_data.json` por política de segurança CORS. Use a Opção A neste caso.*

---

## 📖 Como Usar

### Busca

1. **Digite na caixa "Busca Rápida":**
   - Nome da marca: `Ford`, `Chevrolet`, `Hyundai`
   - Modelo: `Fiesta`, `Civic`, `Onix`
   - Ano: `2010`, `2012/2019`
   - Tipo de lâmpada: `H4`, `HB3`, `H27`

   A busca funciona **em tempo real** — não precisa apertar Enter.

2. **Ou use o filtro "Filtrar por Montadora":**
   - Selecione uma marca específica para ver apenas aquele fabricante

3. **Interprete os resultados:**
   - **✓ OK** (verde) = Todos as fontes concordam
   - **⚠️ Divergências** (amarelo) = Fontes indicam valores diferentes
   - Se houver divergência, cada célula destaca as diferenças

---

## 🔍 Exemplos de Busca

| Busca | Resultado |
|-------|-----------|
| `Fiesta` | Todos os anos e versões do Ford Fiesta |
| `2020` | Todos os carros de 2020 |
| `H4` | Todos os carros que usam lâmpada H4 |
| `Civic 2015` | Honda Civic de 2015 especificamente |
| `HB3` | Todos os carros com farol HB3 |

---

## 📊 Estrutura dos Dados

Cada registro em `lampadas_data.json` contém:

```json
{
  "marca": "Ford",
  "modelo": "Fiesta",
  "ano_texto": "2012/2019",
  "farol_alto": "H4",
  "farol_baixo": "H4",
  "farol_milha": "H27",
  "fonte": "Liderauto",
  "notas": ""
}
```

### Campos:
- **marca**: Fabricante do veículo (ex: Ford, Chevrolet)
- **modelo**: Modelo específico (ex: Fiesta, Onix)
- **ano_texto**: Ano ou intervalo (ex: "2020", "2015/2019", "Todos")
- **farol_alto**: Código da lâmpada de farol alto (ex: H4, HB3)
- **farol_baixo**: Código da lâmpada de farol baixo (ex: H4, HB4)
- **farol_milha**: Código da lâmpada de milha (ex: H27, H11)
- **fonte**: De qual site foi coletado (Liderauto, Rayx ou Permak)
- **notas**: Observações adicionais (raramente preenchido)

---

## 🔄 Divergências Entre Fontes

Quando diferentes fontes indicam lâmpadas diferentes para o mesmo carro e ano:

1. A célula fica **destacada em amarelo** com aviso ⚠️
2. Todas as indicações aparecem agrupadas
3. A label de fonte aparece para cada uma

**Exemplo de divergência:**
```
Ford | Fiesta | 2012/2019
├─ Farol Alto
│  ├─ Liderauto: H4
│  └─ Rayx: HB3
├─ Farol Baixo
│  └─ (todas: H4)
└─ Farol Milha
   └─ (todas: H27)
```

**Dica:** Verifique o manual do seu veículo ou entre em contato com uma oficina se as fontes divergirem.

---

## 🛠️ Manutenção

### Atualizar dados

Para recolher dados mais recentes das 3 fontes, simplesmente execute novamente:

```bash
python scraping_lampadas.py
```

Isso sobrescreverá `lampadas_data.json` com os dados mais atualizados.

### Adicionar novas fontes

Para adicionar mais um site, estenda a classe `LampadasScraper` em `scraping_lampadas.py`:

1. Adicione um método `scrape_novosite(self)`
2. Coloque ele similar aos métodos existentes (Liderauto, Rayx, Permak)
3. Chame `self.scrape_novosite()` dentro de `run()`

---

## 🐛 Troubleshooting

### "Erro ao carregar dados" na interface

**Causa:** O arquivo `lampadas_data.json` não foi encontrado.

**Solução:**
1. Certifique-se de que rodou `python scraping_lampadas.py`
2. Verifique que os 3 arquivos estão na mesma pasta:
   - `scraping_lampadas.py`
   - `consulta_lampadas.html`
   - `lampadas_data.json` (criado após scraping)

### A busca não funciona offline

**Causa:** Política CORS do navegador.

**Solução:**
```bash
python -m http.server 8000
```
Depois acesse: `http://localhost:8000/consulta_lampadas.html`

### Dados incompletos ou desatualizados

**Solução:**
- Rode novamente: `python scraping_lampadas.py`
- Verifique se os sites de origem estão no ar
- Se um site mudou sua estrutura, a função de scraping correspondente precisará ser ajustada

---

## 📝 Notas Técnicas

### Normalização de dados

O script normaliza automaticamente:

- **Marcas:** Convertidas para Title Case (FORD → Ford)
- **Lâmpadas:** Reduzidas a forma canônica (HB3/9005 → HB3)
- **Células vazias:** Representadas como string vazia `""`
- **Variações:** Mantidas quando há ambiguidade (ex: "H1 ou H4")

### Fontes de dados

| Fonte | Estrutura | Atualização |
|-------|-----------|------------|
| **Liderauto** | HTML estático com listas | ~Mensal |
| **Rayx** | Tabela HTML única | ~Bimestral |
| **Permak** | Múltiplas tabelas por marca | ~Trimestral |

---

## 📄 Licença

Dados compilados de fontes públicas. Use conforme necessário.

---

## 💡 Dicas de Uso

1. **Sempre confirmar com manual do veículo** — as fontes são referências, não verdade absoluta
2. **Se houver divergências** — consulte a oficina ou o manual original
3. **Guardar a URL** — você pode bookmarcar `http://localhost:8000/consulta_lampadas.html` para acesso rápido
4. **Atualizar periodicamente** — rode o scraping a cada mês para ter dados frescos

---

**Desenvolvido com ❤️ para consultas rápidas e confiáveis de compatibilidade de lâmpadas automotivas.**
