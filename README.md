Organizador de Arquivos

Um aplicativo simples para organizar automaticamente os arquivos de uma pasta. Ele lê os arquivos soltos e os separa em subpastas com base em suas extensões (ex: arquivos .pdf vão para a pasta PDF, .jpg vão para JPG, etc).

Funcionalidades:

    Interface Gráfica Simples: Fácil de usar, sem precisar digitar comandos no terminal.

    Organização Automática: Identifica a extensão e cria a pasta correspondente automaticamente.

    Modo Recursivo: Opção de varrer subpastas e trazer todos os arquivos organizados para a raiz da pasta selecionada.

    Modo Simulação (Dry-Run): Permite testar a ferramenta e gerar um log do que aconteceria, sem mover os arquivos de verdade.

    Geração de Logs: Cria um arquivo de texto detalhando tudo o que foi movido, ignorado ou se houve algum erro.

    Proteção contra Sobrescrita: Se já existir um arquivo com o mesmo nome no destino, ele renomeia o novo arquivo automaticamente (ex: documento_1.txt) para evitar perda de dados.

Como Usar:

Opção 1: Usando o Executável (Windows)

    Vá na aba Releases na barra lateral direita do GitHub.

    Baixe o arquivo organizador.exe.

    Dê dois cliques no arquivo baixado, selecione a pasta desejada e clique em "OK (Organizar)".

Opção 2: Rodando o Código-Fonte (Desenvolvedores)

    Clone este repositório no seu computador.

    Abra o terminal na pasta do projeto.

    Execute o script usando o comando: python organizador.py
    (Nota: O projeto não exige a instalação de bibliotecas externas pelo pip, ele utiliza apenas bibliotecas nativas do Python).

Ferramentas Utilizadas:

    Python 3

    Tkinter (ttk)

    PyInstaller
