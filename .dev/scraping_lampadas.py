"""
Scraping de tabelas de compatibilidade de lâmpadas automotivas
Fontes: Liderauto, Rayx, Permak
Output: lampadas_data.json
"""

import requests
from bs4 import BeautifulSoup
import json
import re
from typing import List, Dict
import time

class LampadasScraper:
    def __init__(self):
        self.dados = []
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

    def normalizar_marca(self, marca: str) -> str:
        """Converte marca para Title Case e remove prefixos"""
        marca = marca.strip()

        # Remover prefixo comum "Tabela De Lâmpadas Automotivas"
        if marca.lower().startswith('tabela de lâmpadas automotivas'):
            marca = marca[len('tabela de lâmpadas automotivas'):].strip()

        return marca.title()

    def normalizar_ano(self, ano: str) -> str:
        """Normaliza anos: 2016/.. vira 2016/2026 (ano atual)"""
        import datetime
        import re
        ano = ano.strip()
        ano_atual = datetime.datetime.now().year

        # Se é "TODOS", manter como está
        if ano.upper() == 'TODOS':
            return 'Todos'

        # Remove pontos excessivos e limpa a string
        ano = re.sub(r'\.{2,}', '..', ano)  # Normaliza ... para ..

        # Se termina com "/.." ou "...", substitui pelo ano atual
        if ano.endswith('/..') or ano.endswith('...') or ano.endswith('/'):
            # Extrai apenas números da parte inicial
            match = re.search(r'(\d{4})', ano)
            if match:
                inicio = match.group(1)
                return f"{inicio}/{ano_atual}"

        # Se começa com pontos (dados ruins), tenta extrair ano no fim
        if ano.startswith('.'):
            match = re.search(r'(\d{4})', ano)
            if match:
                return match.group(1)

        # Se é apenas números/barra, valida formato
        if re.match(r'^\d{4}/\d{4}$', ano):
            return ano

        # Se tem intervalo válido, manter
        if '/' in ano:
            partes = ano.split('/')
            if len(partes) == 2 and partes[0].isdigit() and partes[1].isdigit():
                return ano

        # Extrai primeiro número encontrado se houver
        match = re.search(r'(\d{4})', ano)
        if match:
            return match.group(1)

        # Se nada funcionou, retorna vazio
        return ''

    def normalizar_lampada(self, lampada: str) -> str:
        """Normaliza notações de lâmpada"""
        if not lampada or lampada.strip() in ['-', '—', '...', '']:
            return ""

        lampada = lampada.strip()

        # Normalizar variantes comuns
        normalizacoes = {
            r'HB3[/\s]*9005': 'HB3',
            r'HB4[/\s]*9006': 'HB4',
            r'H11[/\s]*H8[/\s]*H16': 'H11',
        }

        for padrao, substitui in normalizacoes.items():
            lampada = re.sub(padrao, substitui, lampada, flags=re.IGNORECASE)

        return lampada

    def scrape_liderauto(self) -> int:
        """Scraping do site Liderauto"""
        url = "https://www.liderautoparts.com.br/aplicacao-lampadas-automotivas"

        try:
            print(f"Scraping Liderauto...")
            response = requests.get(url, headers=self.headers, timeout=10)
            response.encoding = 'utf-8'
            soup = BeautifulSoup(response.content, 'html.parser')

            count = 0
            marca_atual = ""

            # Procurar por estruturas de texto com marcas em negrito
            for elem in soup.find_all(['b', 'strong']):
                texto = elem.get_text().strip()

                # Verificar se é uma marca (palavras simples, não contém números)
                if texto and not any(char.isdigit() for char in texto) and len(texto) < 30:
                    # Pode ser uma marca
                    parent = elem.find_parent('div', class_=re.compile('content|description'))
                    if parent:
                        marca_atual = self.normalizar_marca(texto)

                        # Procurar linhas seguintes
                        for linha in parent.find_all('p'):
                            texto_linha = linha.get_text().strip()
                            if '|' in texto_linha:
                                partes = [p.strip() for p in texto_linha.split('|')]
                                if len(partes) >= 5:
                                    record = {
                                        "marca": marca_atual,
                                        "modelo": partes[0],
                                        "ano_texto": self.normalizar_ano(partes[1]),
                                        "farol_alto": self.normalizar_lampada(partes[2]),
                                        "farol_baixo": self.normalizar_lampada(partes[3]),
                                        "farol_milha": self.normalizar_lampada(partes[4]),
                                        "fonte": "Liderauto",
                                        "notas": ""
                                    }
                                    self.dados.append(record)
                                    count += 1

            print(f"  [OK] {count} registros extraidos")
            return count

        except Exception as e:
            print(f"  [ERRO] {e}")
            return 0

    def scrape_rayx(self) -> int:
        """Scraping do site Rayx"""
        url = "https://www.rayx.com.br/aplicacao.html"

        try:
            print(f"Scraping Rayx...")
            response = requests.get(url, headers=self.headers, timeout=10)
            response.encoding = 'utf-8'
            soup = BeautifulSoup(response.content, 'html.parser')

            count = 0

            # Procurar tabelas
            table = soup.find('table')
            if table:
                rows = table.find_all('tr')[1:]  # Pular cabeçalho

                for row in rows:
                    cells = row.find_all('td')
                    if len(cells) >= 5:
                        veiculo = cells[0].get_text().strip()

                        # Separar marca e modelo
                        if ' - ' in veiculo:
                            marca, modelo = veiculo.split(' - ', 1)
                            marca = self.normalizar_marca(marca)
                            modelo = modelo.strip()
                        else:
                            marca = self.normalizar_marca(veiculo)
                            modelo = ""

                        record = {
                            "marca": marca,
                            "modelo": modelo,
                            "ano_texto": self.normalizar_ano(cells[1].get_text().strip()),
                            "farol_alto": self.normalizar_lampada(cells[2].get_text()),
                            "farol_baixo": self.normalizar_lampada(cells[3].get_text()),
                            "farol_milha": self.normalizar_lampada(cells[4].get_text()),
                            "fonte": "Rayx",
                            "notas": ""
                        }
                        self.dados.append(record)
                        count += 1

            print(f"  [OK] {count} registros extraidos")
            return count

        except Exception as e:
            print(f"  [ERRO] {e}")
            return 0

    def scrape_permak(self) -> int:
        """Scraping do site Permak"""
        url = "https://www.permak.com.br/tabela-de-aplicacao-de-lampadas-automotivas/"

        try:
            print(f"Scraping Permak...")
            response = requests.get(url, headers=self.headers, timeout=10)
            response.encoding = 'utf-8'
            soup = BeautifulSoup(response.content, 'html.parser')

            count = 0
            marca_atual = ""

            # Procurar por h2 (marca) seguido de tabela
            for h2 in soup.find_all('h2'):
                marca_texto = h2.get_text().strip()
                if marca_texto and not any(char.isdigit() for char in marca_texto):
                    marca_atual = self.normalizar_marca(marca_texto)

                    # Procurar tabela seguinte
                    table = h2.find_next('table')
                    if table:
                        rows = table.find_all('tr')[1:]  # Pular cabeçalho

                        for row in rows:
                            cells = row.find_all('td')
                            if len(cells) >= 5:
                                # ATENÇÃO: Permak tem ordem inversa (Baixo, Alto)
                                record = {
                                    "marca": marca_atual,
                                    "modelo": cells[0].get_text().strip(),
                                    "ano_texto": self.normalizar_ano(cells[1].get_text().strip()),
                                    "farol_alto": self.normalizar_lampada(cells[3].get_text()),  # Invertido
                                    "farol_baixo": self.normalizar_lampada(cells[2].get_text()),  # Invertido
                                    "farol_milha": self.normalizar_lampada(cells[4].get_text()),
                                    "fonte": "Permak",
                                    "notas": ""
                                }
                                self.dados.append(record)
                                count += 1

            print(f"  [OK] {count} registros extraidos")
            return count

        except Exception as e:
            print(f"  [ERRO] {e}")
            return 0

    def salvar_json(self, filename: str = "lampadas_data.json"):
        """Salva dados em JSON"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.dados, f, ensure_ascii=False, indent=2)
        print(f"\n[OK] {len(self.dados)} registros salvos em {filename}")

    def run(self):
        """Executa todos os scrapers"""
        print("=" * 60)
        print("SCRAPING DE LÂMPADAS AUTOMOTIVAS")
        print("=" * 60 + "\n")

        total = 0
        total += self.scrape_liderauto()
        time.sleep(1)  # Respeito aos servidores
        total += self.scrape_rayx()
        time.sleep(1)
        total += self.scrape_permak()

        self.salvar_json()
        print("=" * 60)


if __name__ == "__main__":
    scraper = LampadasScraper()
    scraper.run()
