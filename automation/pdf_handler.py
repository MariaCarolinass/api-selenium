import time, os
import requests
from .utils import generate_filename

class PDFHandler:
    
    def __init__(self, driver, download_dir):
        self.driver = driver
        self.download_dir = download_dir

    def download_pdf(self, pdf_info, index):
        try:
            print(f"Baixando ({index + 1}): {pdf_info['title']}")

            old_files = list(self.download_dir.glob("dom_*.pdf"))

            if 'element' in pdf_info:
                self.driver.execute_script("arguments[0].click();", pdf_info['element'])
                
                max_wait = 15
                waited = 0
                
                while waited < max_wait:
                    time.sleep(1)
                    waited += 1
                    
                    new_files = list(self.download_dir.glob("*.pdf"))
                    downloaded = [f for f in new_files if f not in old_files]
                    
                    if downloaded:
                        latest_file = max(downloaded, key=os.path.getctime)
                        part_files = list(self.download_dir.glob("*.part"))

                        if not part_files and latest_file.stat().st_size > 0:
                            new_name = generate_filename(pdf_info['title'], index)
                            new_path = self.download_dir / new_name
                            
                            if latest_file != new_path:
                                latest_file.rename(new_path)
                            
                            print(f"Download concluído: {new_path.name}")
                            return str(new_path)
            else:
                response = requests.get(pdf_info['url'], stream=True, timeout=30)
                if response.status_code == 200:
                    filename = generate_filename(pdf_info['title'], index)
                    filepath = self.download_dir / filename
                    
                    with open(filepath, 'wb') as f:
                        for chunk in response.iter_content(chunk_size=8192):
                            f.write(chunk)
                    
                    print(f"Download direto concluído: {filename}")
                    return str(filepath)
        except Exception as e:
            print(f"Erro ao baixar {pdf_info['title']}: {e}")
        return None

    def upload_pdf(self, file_path):
        try:
            print(f"Fazendo upload: {os.path.basename(file_path)}")

            if not os.path.exists(file_path):
                print(f"Arquivo não encontrado: {file_path}")
                return None
            
            file_size = os.path.getsize(file_path)
            if file_size == 0:
                print(f"Arquivo vazio: {file_path}")
                return None
            
            print(f"Tamanho do arquivo: {file_size / 1024 / 1024:.2f} MB")

            upload_services = [
                {
                    'name': 'tmpfiles.org',
                    'url': 'https://tmpfiles.org/api/v1/upload',
                    'field': 'file'
                },
                {
                    'name': '0x0.st',
                    'url': 'https://0x0.st',
                    'field': 'file'
                }, 
                {
                    'name': 'file.io',
                    'url': 'https://file.io/?expires=1w',
                    'field': 'file'
                }
            ]
            
            for service in upload_services:
                try:
                    print(f"Tentando upload via {service['name']}...")

                    headers_list = [
                        {
                            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
                        },
                        {} # Sem headers
                    ]
                    
                    for i, headers in enumerate(headers_list):
                        try:
                            time.sleep(2)
                            
                            with open(file_path, 'rb') as f:
                                files = {service['field']: (os.path.basename(file_path), f, 'application/pdf')}
                                
                                response = requests.post(
                                    service['url'],
                                    files=files,
                                    headers=headers,
                                    timeout=120,
                                    allow_redirects=True
                                )
                            
                            print(f"{service['name']} resposta: {response.status_code}")

                            if response.status_code == 200:
                                response_text = response.text.strip()

                                if service['name'] == 'tmpfiles.org':
                                    try:
                                        import json
                                        data = json.loads(response_text)
                                        if data.get('status') == 'success' and data.get('data', {}).get('url'):
                                            url = data['data']['url']
                                            print(f"Upload {service['name']} realizado: {url}")
                                            return url
                                    except:
                                        pass
                                elif service['name'] == '0x0.st':
                                    if response_text.startswith('http'):
                                        url = response_text.split()[0]
                                        print(f"Upload {service['name']} realizado: {url}")
                                        return url
                                elif service['name'] == 'file.io':
                                    try:
                                        import json
                                        data = json.loads(response_text)
                                        if data.get('success') and data.get('link'):
                                            url = data['link']
                                            print(f"Upload {service['name']} realizado: {url}")
                                            return url
                                    except:
                                        pass

                                if len(response_text) < 200:
                                    print(f"{service['name']} resposta: {response_text}")

                            elif response.status_code == 413:
                                print(f"{service['name']}: Arquivo muito grande")
                                break
                            elif response.status_code == 403:
                                print(f"{service['name']}: 403 (tentativa {i+1}/3)")
                                continue
                            else:
                                print(f"{service['name']}: Status {response.status_code}")

                        except requests.exceptions.RequestException as e:
                            print(f"{service['name']} erro de rede (tentativa {i+1}): {e}")
                            continue
                    
                except Exception as e:
                    print(f"Erro com {service['name']}: {e}")
                    continue
            
            print(f"Falha no upload de {file_path} em todos os serviços.")
            return None
        
        except Exception as e:
            print(f"Erro ao fazer upload de {file_path}: {e}")
            return None