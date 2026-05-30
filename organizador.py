import os
import shutil
import logging
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from datetime import datetime

# Pastas que a gente não quer mexer pra não quebrar nada
pastas_ignoradas = [".git", "__pycache__", ".venv", "venv", "node_modules"]

def setup_log(pasta):
    # Cria um log com a data e hora atual
    nome_arquivo = f"organizador_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    log_file = os.path.join(pasta, nome_arquivo)
    
    # Limpa os logs antigos se tiver pra não duplicar no console
    logging.getLogger().handlers.clear()
    
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format="%(asctime)s - %(message)s"
    )
    return log_file

def pegar_nome_unico(destino):
    # Se o arquivo não existe, beleza, só retorna
    if not os.path.exists(destino):
        return destino
    
    # Se existe, bota um _1, _2 no final pra não sobrescrever
    base, ext = os.path.splitext(destino)
    contador = 1
    while True:
        novo_destino = f"{base}_{contador}{ext}"
        if not os.path.exists(novo_destino):
            return novo_destino
        contador += 1
        if contador > 1000: # Proteção basica pra não travar em loop infinito
            raise Exception("Muitos arquivos com o mesmo nome!")

def processar_arquivo(caminho_arquivo, pasta_base, simular, stats):
    nome_arquivo = os.path.basename(caminho_arquivo)
    
    # Ignora o próprio log do nosso programa
    if nome_arquivo.startswith("organizador_") and nome_arquivo.endswith(".log"):
        return
        
    # Pega a extensão pra saber onde jogar o arquivo
    if nome_arquivo.startswith('.'):
        pasta_destino = "Ocultos"
    else:
        _, ext = os.path.splitext(nome_arquivo)
        ext = ext.replace('.', '').upper()
        if not ext:
            pasta_destino = "Sem_Extensao"
        else:
            pasta_destino = ext
            
    dir_destino = os.path.join(pasta_base, pasta_destino)
    destino_final = os.path.join(dir_destino, nome_arquivo)
    
    # Se o arquivo já tá no lugar certo, ignora
    if os.path.abspath(caminho_arquivo) == os.path.abspath(destino_final):
        stats['ignorados'] += 1
        return
        
    try:
        destino_final = pegar_nome_unico(destino_final)
    except Exception as e:
        logging.error(f"Erro de nome em {nome_arquivo}: {e}")
        stats['erros'] += 1
        return
    
    # Se for só simulação, anota e sai fora
    if simular:
        logging.info(f"[SIMULACAO] Moveria: {nome_arquivo} -> {pasta_destino}")
        stats['simulados'] += 1
        return
        
    try:
        if not os.path.exists(dir_destino):
            os.makedirs(dir_destino)
        shutil.move(caminho_arquivo, destino_final)
        logging.info(f"Movido: {nome_arquivo} -> {pasta_destino}")
        stats['movidos'] += 1
    except Exception as e:
        logging.error(f"Deu erro ao mover {nome_arquivo}: {e}")
        stats['erros'] += 1

def organizar_arquivos(pasta_origem, simular, recursivo):
    stats = {'movidos': 0, 'simulados': 0, 'erros': 0, 'ignorados': 0}
    
    if recursivo:
        # os.walk é o clássico pra ler subpastas
        for root, dirs, files in os.walk(pasta_origem):
            # Tira as pastas ignoradas da lista pra ele nem entrar nelas
            dirs[:] = [d for d in dirs if d not in pastas_ignoradas]
            
            for file in files:
                caminho = os.path.join(root, file)
                processar_arquivo(caminho, pasta_origem, simular, stats)
    else:
        for item in os.listdir(pasta_origem):
            caminho_completo = os.path.join(pasta_origem, item)
            if os.path.isfile(caminho_completo):
                processar_arquivo(caminho_completo, pasta_origem, simular, stats)
                
    return stats

# --- TELA ---
def iniciar_gui():
    root = tk.Tk()
    root.title("Organizador de Arquivos V1.0")
    root.geometry("600x380")
    
    # Tenta usar um tema mais bonitinho se tiver no PC
    style = ttk.Style()
    if 'vista' in style.theme_names():
        style.theme_use('vista')
    elif 'clam' in style.theme_names():
        style.theme_use('clam')
    
    # Variáveis da tela
    pasta_var = tk.StringVar()
    recursivo_var = tk.BooleanVar()
    simular_var = tk.BooleanVar()
    
    def escolher_pasta():
        pasta = filedialog.askdirectory(title="Selecione a pasta Source")
        if pasta:
            pasta_var.set(pasta)
            
    def rodar():
        pasta = pasta_var.get()
        if not pasta:
            messagebox.showwarning("Aviso", "Selecione uma pasta (Source) primeiro!")
            return
            
        log_gerado = setup_log(pasta)
        root.config(cursor="wait")
        root.update()
        
        try:
            resultados = organizar_arquivos(pasta, simular_var.get(), recursivo_var.get())
            
            msg = (
                f"Feito!\n\n"
                f"Movidos: {resultados['movidos']}\n"
                f"Simulados: {resultados['simulados']}\n"
                f"Ignorados: {resultados['ignorados']}\n"
                f"Erros: {resultados['erros']}\n\n"
                f"Log salvo em: {os.path.basename(log_gerado)}"
            )
            messagebox.showinfo("Sucesso", msg)
        except Exception as e:
            messagebox.showerror("Erro", f"Deu erro na execução:\n{e}")
        finally:
            root.config(cursor="")

    # Montando o layout
    frame_top = ttk.Frame(root, padding=15)
    frame_top.pack(fill='both', expand=True)
    
    texto = (
        "Este aplicativo organiza automaticamente os arquivos de uma pasta selecionada.\n"
        "Ele criará subpastas baseadas nas extensões dos arquivos (ex: PDF, JPG, TXT)\n"
        "e moverá os arquivos para dentro de suas respectivas pastas."
    )
    ttk.Label(frame_top, text=texto, justify='center').pack(pady=(0, 20))
    
    # Box do Source
    frame_source = ttk.LabelFrame(frame_top, text="Selecione a Pasta de Origem", padding=10)
    frame_source.pack(fill='x', pady=10)
    
    ttk.Label(frame_source, text="Source:").grid(row=0, column=0, padx=5)
    ttk.Entry(frame_source, textvariable=pasta_var, state='readonly', width=50).grid(row=0, column=1, sticky='ew')
    ttk.Button(frame_source, text="📂 Browse...", command=escolher_pasta).grid(row=0, column=2, padx=5)
    frame_source.columnconfigure(1, weight=1)
    
    # Box das Opções
    frame_opcoes = ttk.LabelFrame(frame_top, text="Opções", padding=10)
    frame_opcoes.pack(fill='x', pady=10)
    
    ttk.Checkbutton(frame_opcoes, text="Incluir subpastas (Recursivo) - Todos irão para a raiz", variable=recursivo_var).pack(anchor='w', pady=2)
    ttk.Checkbutton(frame_opcoes, text="Apenas Simular (Dry-Run) - Não move os arquivos de verdade", variable=simular_var).pack(anchor='w', pady=2)
    
    # Botões de baixo
    frame_botoes = ttk.Frame(frame_top)
    frame_botoes.pack(fill='x', pady=20)
    
    ttk.Button(frame_botoes, text="✔️ OK (Organizar)", command=rodar).pack(side='right', padx=5)
    ttk.Button(frame_botoes, text="Cancelar", command=root.quit).pack(side='right', padx=5)

    # Força janela pra frente
    root.attributes('-topmost', True)
    root.update()
    root.attributes('-topmost', False)
    
    root.mainloop()

if __name__ == "__main__":
    iniciar_gui()