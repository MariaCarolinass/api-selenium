from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from .utils import is_from_previous_month
import time

class DomScraper:

    def __init__(self, driver):
        self.driver = driver

    def access_dom_site(self):
        try:
            self.driver.get("https://www.natal.rn.gov.br/dom")
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            print("Site carregado com sucesso!")
            time.sleep(2)
            return True
        except TimeoutException:
            print("Erro: Timeout ao carregar o site")
            return False
        except Exception as e:
            print(f"Erro ao acessar o site: {e}")
            return False

    def select_month_year(self, month_info):
        try:
            Select(self.driver.find_element(By.NAME, "mes")).select_by_value(f"{month_info['month']:02d}")
            Select(self.driver.find_element(By.NAME, "ano")).select_by_value(str(month_info['year']))
            search_button = self.driver.find_element(
                By.CSS_SELECTOR, "button.btn.btn-primary.m-2[data-attach-loading]"
            )
            search_button.click()
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".lista-documento li"))
            )
            time.sleep(2)
            print(f"Selecionado {month_info['month_pt']} / {month_info['year']}")
        except Exception as e:
            print(f"Não foi possível alterar mês/ano: {e}")

    def select_records_length(self, length):
        try:
            Select(self.driver.find_element(By.NAME, "example_length")).select_by_visible_text(str(length))
            time.sleep(2)
            print(f"Selecionado {length} registros por página")
        except Exception as e:
            print(f"Não foi possível alterar a quantidade de registros: {e}")

    def collect_pdfs(self, month_info):
        pdf_links = []
        visited_links = set()

        for element in self.driver.find_elements(By.XPATH, "//a[contains(translate(@href,'PDF','pdf'), '.pdf')]"):
            href = element.get_attribute("href")
            if href and href not in visited_links and is_from_previous_month(element.text, month_info):
                visited_links.add(href)
                pdf_links.append({
                    'url': href,
                    'title': element.text.strip() or f"Documento_{len(pdf_links)+1}",
                    'element': element
                })
                
        print(f"Coletados {len(pdf_links)} PDFs do DOM")
        return pdf_links
