import zipfile
import os

def criar_pacote_zip():
    arquivos_para_incluir = [
        "main.py",
        "requirements.txt",
        "README.md",
        "iniciar_calculadora.bat"
    ]
    
    zip_nome = "calculadora_bhaskara.zip"
    diretorio_atual = os.path.dirname(os.path.abspath(__file__))
    caminho_zip = os.path.join(diretorio_atual, zip_nome)
    
    with zipfile.ZipFile(caminho_zip, "w", zipfile.ZIP_DEFLATED) as zipf:
        for arq in arquivos_para_incluir:
            caminho_arq = os.path.join(diretorio_atual, arq)
            if os.path.exists(caminho_arq):
                zipf.write(caminho_arq, arcname=arq)
                print(f"Adicionado ao zip: {arq}")
            else:
                print(f"Aviso: {arq} não encontrado.")
                
    print(f"\nArquivo '{zip_nome}' gerado com sucesso em: {caminho_zip}")

if __name__ == "__main__":
    criar_pacote_zip()