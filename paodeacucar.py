import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scrape_with_selenium(url, target_class):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Executar sem abrir o navegador
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(options=options)

    try:
        driver.get(url)
        
        # Esperar até que pelo menos um elemento da classe target_class esteja presente
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, target_class))
        )
        
        # Buscar elementos pela classe
        elements = driver.find_elements(By.CLASS_NAME, target_class)

        texts = []
        for el in elements:
            text = el.text.strip()
            if text:
                texts.append(text)

        print(f"\n🔍 Foram encontrados {len(texts)} elementos com a classe '{target_class}'.\n")

        # Salvar os resultados em JSON
        with open('paodeacucar.json', 'w', encoding='utf-8') as f:
            json.dump({target_class: texts}, f, ensure_ascii=False, indent=4)

        print("✅ Dados salvos em 'resultados.json'.")

    finally:
        driver.quit()

if __name__ == '__main__':
    target_url = 'https://www.paodeacucar.com/categoria/alimentos?s=relevance&p=7'
    target_class = 'Link-sc-j02w35-0.bEJTOI.Title-sc-20azeh-10.gdVmss'  # Troque pela classe que quiser buscar
    scrape_with_selenium(target_url, target_class)
