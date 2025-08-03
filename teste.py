import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scrape_with_selenium(url, target_class):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Executar sem abrir o navegador
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(options=options)
    texts = []

    try:
        driver.get(url)
        
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, target_class))
        )
        
        elements = driver.find_elements(By.CLASS_NAME, target_class)

        for el in elements:
            text = el.text.strip()
            if text:
                texts.append(text)

        print(f" Página {url} -> {len(elements)} elementos encontrados.")

    finally:
        driver.quit()

    return texts


if __name__ == '__main__':
    base_url = 'https://www.paodeacucar.com/categoria/alimentos?s=relevance&p={}'
    target_class = 'Link-sc-j02w35-0'

    all_texts = []

    for page in range(1, 8):  # Exemplo: páginas 1 a 7
        url = base_url.format(page)
        print(f"\n=== Raspando página {page} ===")
        texts = scrape_with_selenium(url, target_class)
        all_texts.extend(texts)

    # Salvar resultados finais
    with open('paodeacucar.json', 'w', encoding='utf-8') as f:
        json.dump(all_texts, f, ensure_ascii=False, indent=4)

    print(f"\n Total de itens coletados: {len(all_texts)}")
    print(" Dados salvos em 'paodeacucar.json'.")
