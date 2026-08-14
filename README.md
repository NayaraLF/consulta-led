# 💡 Ferramenta de Consulta de Compatibilidade de Lâmpadas Automotivas

Sistema online para consultar compatibilidade de lâmpadas automotivas. Dados agregados de múltiplas fontes especializadas.

**🌐 [Acessar a ferramenta](https://consulta-led-git-main-nayara-louback-francos-projects.vercel.app)**

## 🚀 Recursos

- ✅ **Busca em tempo real** — procure por marca, modelo, ano ou código de lâmpada
- ✅ **Filtro por montadora** — refine resultados por fabricante
- ✅ **Dados de múltiplas fontes** — Rayx, Permak (1.000+ registros)
- ✅ **Interface offline** — funciona completamente no navegador
- ✅ **Sem servidor** — site estático, rápido e seguro

## 📁 Estrutura

```
consulta-led/
├── public/
│   └── consulta_lampadas.html    # Interface web completa
├── data/
│   └── lampadas_data.json        # Base de dados (1.000+ registros)
├── vercel.json                   # Deploy config
└── README.md
```

## 🎯 Como Usar

1. Acesse o site
2. **Busca Rápida:** Digite marca, modelo, ano ou código (H4, HB3, etc)
3. **Filtro:** Selecione uma montadora específica
4. Visualize as especificações e fonte dos dados

### Exemplos de Busca

| Busca | Resultado |
|-------|-----------|
| `Civic` | Todos os Civic (marca Honda) |
| `2020` | Todos os carros de 2020 |
| `H4` | Todos os carros com lâmpada H4 |
| `Honda` | Todos os Honda |

## 🔄 Atualizar Dados

Os dados são atualizados manualmente via scraping local. Se quiser coletar dados novos:

1. Execute o script de coleta (não incluído no repositório)
2. O arquivo `data/lampadas_data.json` será atualizado
3. Faça push para o repositório

## 📊 Estrutura dos Dados

Cada registro em `lampadas_data.json`:

```json
{
  "marca": "Honda",
  "modelo": "Civic",
  "ano_texto": "2015/2020",
  "farol_alto": "H1",
  "farol_baixo": "HB3",
  "farol_milha": "H27",
  "fonte": "Rayx",
  "notas": ""
}
```

### Campos

- **marca** — Fabricante do veículo
- **modelo** — Modelo específico
- **ano_texto** — Ano ou intervalo (ex: "2020", "2015/2019")
- **farol_alto** — Código da lâmpada de farol alto
- **farol_baixo** — Código da lâmpada de farol baixo
- **farol_milha** — Código da lâmpada de milha
- **fonte** — Origem dos dados (Rayx, Permak)
- **notas** — Observações adicionais

## ⚙️ Deploy

Hospedado no Vercel. Qualquer push para `main` dispara um redeploy automático.

```bash
git push origin main
```

## 📝 Licença

Dados compilados de fontes públicas. Uso livre.

---

**Desenvolvido com ❤️**
