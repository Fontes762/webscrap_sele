import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scrape_all_pages(base_url, xpath_nome, xpath_preco):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)
    all_produtos = []
    page_num = 1
    max_pages = 3  # Aumente conforme necessário

    try:
        while page_num <= max_pages:
            url = f"{base_url}?page={page_num}"
            print(f"\n➡️ Acessando: {url}")
            driver.get(url)

            # Scroll for loading all products
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)

            try:
                # Aguardar o carregamento dos produtos
                WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, ".vtex-product-summary-2-x-productBrand"))
                )
                WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "[class*='containerCustomPrices']"))
                )
            except Exception as e:
                print(f"❌ Elementos não encontrados na página {page_num}: {e}")
                break

            # Buscar nomes dos produtos
            nomes_el = driver.find_elements(By.CSS_SELECTOR, ".vtex-product-summary-2-x-productBrand")
            
            # Buscar preços dos produtos
            precos_el = driver.find_elements(By.CSS_SELECTOR, "[class*='containerCustomPrices']")

            nomes = [el.get_attribute("textContent").strip() for el in nomes_el]
            
            # Extrair preços - pegar apenas o primeiro preço de cada elemento (preço de venda)
            precos = []
            for el in precos_el:
                preco_text = el.get_attribute("textContent").strip()
                # Extrair o primeiro preço que aparece (geralmente o preço de venda)
                if "R$" in preco_text:
                    # Dividir por R$ e pegar o primeiro preço válido
                    partes = preco_text.split("R$")
                    for parte in partes[1:]:  # Pular a primeira parte vazia
                        preco_limpo = "R$" + parte.split("R$")[0].strip()
                        if preco_limpo != "R$":
                            precos.append(preco_limpo)
                            break
                else:
                    precos.append(preco_text)

            print(f"📊 Página {page_num}: {len(nomes)} nomes, {len(precos)} preços encontrados")

            if not nomes:
                print("⚠️ Nenhum produto encontrado.")
                break

            # Garantir que temos o mesmo número de nomes e preços
            min_length = min(len(nomes), len(precos))
            
            for i in range(min_length):
                all_produtos.append({
                    "nome": nomes[i],
                    "preco": precos[i],
                    "mercado": "Zona Sul"
                })

            print(f"✅ Página {page_num} raspada. Produtos até agora: {len(all_produtos)}")
            page_num += 1
            time.sleep(2)

        with open("zonasul_all_pages.json", "w", encoding="utf-8") as f:
            json.dump(all_produtos, f, ensure_ascii=False, indent=4)
        print(f"\n📦 Raspagem concluída. Total: {len(all_produtos)} produtos salvos.")

    finally:
        driver.quit()

def scrape_all_pages_alternative(base_url):
    """
    Versão alternativa usando seletores CSS mais específicos
    """
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)
    all_produtos = []
    page_num = 1
    max_pages = 3

    try:
        while page_num <= max_pages:
            url = f"{base_url}?page={page_num}"
            print(f"\n➡️ Acessando: {url}")
            driver.get(url)

            # Scroll para carregar todos os produtos
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)

            try:
                # Aguardar carregamento dos cards de produtos
                WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, ".vtex-product-summary-2-x-container"))
                )
            except Exception as e:
                print(f"❌ Cards de produtos não encontrados na página {page_num}: {e}")
                break

            # Buscar todos os cards de produtos
            product_cards = driver.find_elements(By.CSS_SELECTOR, ".vtex-product-summary-2-x-container")
            
            print(f"📦 Encontrados {len(product_cards)} cards de produtos na página {page_num}")

            for card in product_cards:
                try:
                    # Extrair nome do produto
                    nome_el = card.find_element(By.CSS_SELECTOR, ".vtex-product-summary-2-x-productBrand")
                    nome = nome_el.get_attribute("textContent").strip()
                    
                    # Extrair preço do produto
                    preco_el = card.find_element(By.CSS_SELECTOR, "[class*='containerCustomPrices']")
                    preco_text = preco_el.get_attribute("textContent").strip()
                    
                    # Processar o preço para pegar apenas o primeiro valor
                    preco = "Não encontrado"
                    if "R$" in preco_text:
                        partes = preco_text.split("R$")
                        for parte in partes[1:]:
                            preco_limpo = "R$" + parte.split("R$")[0].strip()
                            if preco_limpo != "R$" and len(preco_limpo) > 3:
                                preco = preco_limpo
                                break
                    
                    all_produtos.append({
                        "nome": nome,
                        "preco": preco,
                        "mercado": "Zona Sul"
                    })
                    
                except Exception as e:
                    print(f"⚠️ Erro ao extrair dados de um card: {e}")
                    continue

            print(f"✅ Página {page_num} processada. Total de produtos: {len(all_produtos)}")
            
            # Verificar se há próxima página
            if len(product_cards) == 0:
                print("🔚 Nenhum produto encontrado, finalizando...")
                break
                
            page_num += 1
            time.sleep(2)

        # Salvar resultados
        with open("zonasul_all_pages.json", "w", encoding="utf-8") as f:
            json.dump(all_produtos, f, ensure_ascii=False, indent=4)
        print(f"\n📦 Raspagem concluída. Total: {len(all_produtos)} produtos salvos.")
        
        return all_produtos

    finally:
        driver.quit()

if __name__ == "__main__":
    base_url = "https://www.zonasul.com.br/hortifruti/d"
    
    print("🚀 Iniciando raspagem com método alternativo...")
    produtos = scrape_all_pages_alternative(base_url)
    
    print(f"\n📊 Resumo final:")
    print(f"Total de produtos coletados: {len(produtos)}")
    if produtos:
        print(f"Primeiro produto: {produtos[0]}")
        print(f"Último produto: {produtos[-1]}")
