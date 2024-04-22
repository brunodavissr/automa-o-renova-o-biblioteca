from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from datetime import date

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    data_hoje = date.today()
    
    page.goto('https://pergamum.pucgoias.edu.br/pergamum/biblioteca_s/meu_pergamum/index.php')
    
    page.locator("#id_login").fill("**************")
    page.locator('#id_senhaLogin').fill("****")
    page.locator('#button').click()

    page.wait_for_load_state('networkidle')

    page_content = page.content()

    soup = BeautifulSoup(page_content, 'html.parser')

    dados_livros = soup.find_all('td', class_='txt_cinza_10')
    
    for i in range(3, len(dados_livros), 3):
        data_limite = date(
            int(dados_livros[i].text.strip().split('/')[2]),
            int(dados_livros[i].text.strip().split('/')[1]),
            int(dados_livros[i].text.strip().split('/')[0])
        )
        quantidade_renovacoes_feitas = dados_livros[i+1].text.strip()[0]
        if(data_limite <= data_hoje):
            if(quantidade_renovacoes_feitas < 3):
                print(f"Tem que renovar o livro hoje! Está será a {quantidade_renovacoes_feitas} renovação.")
                page.locator('#botao_renovar' + str(int(i/3))).click()
            else:
                print("Quantidades de renovações feitas atingiu o limite e hoje é o prazo para devolver. Devolva o livro hoje!!!")
        else:
            print(f"Nao precisa renovar o livro hoje. Já foram feitas {quantidade_renovacoes_feitas} renovações até agora.")

    browser.close()