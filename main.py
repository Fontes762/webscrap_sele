import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scrape_with_selenium(url):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Executar sem abrir o navegador
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(options=options)

    try:
        driver.get(url)
        
        # Esperar até que algum parágrafo <p> esteja presente
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'p'))
        )
        
        # Coletar todos os elementos <p> visíveis
        paragraphs = driver.find_elements(By.CSS_SELECTOR, 'p')

        texts = []
        for p in paragraphs:
            text = p.text.strip()
            if text:
                texts.append(text)

        print(f"\n🔍 Foram encontrados {len(texts)} parágrafos com texto.\n")

        # Salvar os resultados em um arquivo JSON
        with open('resultados.json', 'w', encoding='utf-8') as f:
            json.dump({"paragrafos": texts}, f, ensure_ascii=False, indent=4)

        print("✅ Dados salvos em 'resultados.json'.")

    finally:
        driver.quit()

if __name__ == '__main__':
    target_url = 'https://www.supermarketdelivery.com.br/store/8__3285/large' 
    scrape_with_selenium(target_url)
