from automation.driver_manager import DriverManager
from automation.dom_scraper import DomScraper
from automation.pdf_handler import PDFHandler
from api.database import SessionLocal, engine
from api import crud
from automation.utils import get_previous_month_info

def run():
    try:
        print("Iniciando automação do Diário Oficial de Natal")
        print("=" * 50)
        
        manager = DriverManager()
        driver = manager.setup_driver()
        scraper = DomScraper(driver)
        handler = PDFHandler(driver, manager.download_dir)

        scraper.access_dom_site()
        month_info = get_previous_month_info()
        scraper.select_month_year(month_info)
        scraper.select_records_length(100)
        pdfs = scraper.collect_pdfs(month_info)

        downloaded_files = []
        for i, pdf in enumerate(pdfs):
            path = handler.download_pdf(pdf, i)
            if path:
                downloaded_files.append({'path': path, 'title': pdf['title']})

        print(f"Total de arquivos baixados: {len(downloaded_files)}\n")

        db = SessionLocal()
        uploaded_urls = []
        for pdf in downloaded_files:
            url = handler.upload_pdf(pdf['path'])
            if url:
                crud.create_dom_file(db, title=pdf['title'], url=url,
                                    month=month_info['month'], year=month_info['year'])
                uploaded_urls.append(url)

        db.close()
        driver.quit()
        
        print("\n" + "=" * 50)
        print("Automação concluída com sucesso!")
        print("=" * 50)
        print(f"Arquivos baixados: {len(downloaded_files)}")
        print(f"Uploads realizados: {len(uploaded_urls)}")
            
        if uploaded_urls:
            print("\nURLs DOS UPLOADS:")
            for i, url in enumerate(uploaded_urls, 1):
                print(f"{i:2d}. {url}")

    except Exception as e:
        print(f"Erro na automação: {e}")

from sqlalchemy import text

def main():
    run()

if __name__ == "__main__":
    main()