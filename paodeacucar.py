import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
import time

def scrape_all_pages(base_url, xpath_nome, xpath_preco):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Executar sem abrir o navegador
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)
    all_produtos = []
    page_num = 1
    max_pages = 100 # Limite para evitar raspagem infinita, pode ser ajustado

    try:
        while page_num <= max_pages:
            url = f"{base_url}?s=relevance&p={page_num}"
            print(f"Acessando a página: {url}")
            driver.get(url)

            try:
                # Esperar até que pelo menos um elemento de nome de produto esteja visível
                WebDriverWait(driver, 15).until(
                    EC.visibility_of_element_located((By.XPATH, xpath_nome))
                )
                # Esperar até que pelo menos um elemento de preço de produto esteja visível
                WebDriverWait(driver, 15).until(
                    EC.visibility_of_element_located((By.XPATH, xpath_preco))
                )
            except Exception as e:
                print(f"Erro ao carregar elementos na página {page_num}: {e}")
                print(f"Nenhum produto encontrado na página {page_num}. Parando a raspagem.")
                break

            retries = 3
            for attempt in range(retries):
                try:
                    elements_nome = driver.find_elements(By.XPATH, xpath_nome)
                    nomes = [el.get_attribute("alt") for el in elements_nome if el.get_attribute("alt")]

                    elements_preco = driver.find_elements(By.XPATH, xpath_preco)
                    precos = [el.text for el in elements_preco if el.text]
                    break
                except StaleElementReferenceException:
                    print(f"StaleElementReferenceException no attempt {attempt + 1}. Retrying...")
                    time.sleep(1) # Pequena pausa antes de tentar novamente
            else:
                print(f"Falha ao encontrar elementos após {retries} tentativas na página {page_num}. Parando a raspagem.")
                break

            if not nomes or not precos:
                print(f"Nenhum nome ou preço encontrado na página {page_num}. Parando a raspagem.")
                break

            for i in range(min(len(nomes), len(precos))):
                all_produtos.append({
                    "nome": nomes[i],
                    "preco": precos[i],
                    "mercado": "Pão de Açucar"
                })
            
            print(f"Página {page_num} raspada. Total de produtos coletados: {len(all_produtos)}")
            page_num += 1
            time.sleep(3) # Aumentado o tempo de pausa

        with open("paodeacucar_all_pages.json", "w", encoding="utf-8") as f:
            json.dump(all_produtos, f, ensure_ascii=False, indent=4)

        print(f"✅ Dados de todas as páginas salvos em \"paodeacucar_all_pages.json\". Total de produtos: {len(all_produtos)}")

    finally:
        driver.quit()

if __name__ == "__main__":
    base_url = "https://www.paodeacucar.com/categoria/alimentos"
    xpath_nome = "//a[contains(@href, '/produto/' )]/img"
    xpath_preco = "//p[contains(@class, 'PriceValue-sc-20azeh-4')]"
    scrape_all_pages(base_url, xpath_nome, xpath_preco)
