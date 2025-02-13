import os
import hashlib
import flet as ft
import pygame

# --- Funções de Áudio ---
# teste
def tocar_musica():
    """
    Inicializa o mixer do pygame e toca a música de fundo em loop.
    Caso o arquivo de áudio não seja encontrado, exibe uma mensagem de erro.
    """
    pygame.mixer.init()
    caminho_audio = "musica/WhatsApp Audio 2025-02-11 at 15.54.04.mpeg"

    if os.path.exists(caminho_audio):
        pygame.mixer.music.load(caminho_audio)
        pygame.mixer.music.play(loops=-1)
    else:
        print(f"Erro: Arquivo de áudio '{caminho_audio}' não encontrado.")

# --- Funções de Autenticação ---

def salvar_usuario(usuario: str, senha: str):
    """
    Criptografa a senha utilizando SHA-256 e salva o usuário com a senha (em hash)
    no arquivo 'usuarios.txt'.
    """
    senha_criptografada = hashlib.sha256(senha.encode()).hexdigest()

    with open("usuarios.txt", "a") as arquivo:
        arquivo.write(f"{usuario},{senha_criptografada}\n")


def verificar_login(usuario: str, senha: str) -> bool:
    """
    Verifica se o usuário e senha informados estão cadastrados.
    Retorna True se o login for válido; caso contrário, retorna False.
    """
    senha_hash = hashlib.sha256(senha.encode()).hexdigest()

    try:
        with open("usuarios.txt", "r") as arquivo:
            for linha in arquivo:
                usuario_cadastrado, senha_cadastrada = linha.strip().split(",")
                if usuario_cadastrado == usuario and senha_cadastrada == senha_hash:
                    return True  # Login válido
    except FileNotFoundError:
        pass

    return False  # Login inválido

# --- Telas e Lógica do Jogo ---

def tela_login(page: ft.Page):
    """
    Exibe a tela de login e cadastro, permitindo que o usuário efetue login
    ou se cadastre. Inicia a reprodução da música de fundo.
    """
    tocar_musica()
    page.clean()

    # Configurando o fundo da tela
    imagem_fundo = ft.Image(
        src="imagens_01/54cb77b0-c199-47e8-a24a-f1e2a073a8df.jpg",
        width=page.width,
        height=page.height,
        fit=ft.ImageFit.COVER
    )

    # Campos de entrada
    campo_usuario = ft.TextField(
        label="Digite seu login",
        width=300,
        border_radius=20,
        bgcolor=ft.colors.WHITE,
        text_style=ft.TextStyle(color=ft.colors.BLACK)
    )
    campo_senha = ft.TextField(
        label="Digite sua senha",
        password=True,
        width=300,
        border_radius=20,
        bgcolor=ft.colors.WHITE,
        text_style=ft.TextStyle(color=ft.colors.BLACK)
    )

    texto_feedback = ft.Text("", color=ft.colors.RED, size=16)

    # Ação para efetuar login
    def acao_login(e):
        login = campo_usuario.value.strip()
        senha = campo_senha.value.strip()

        if not login or not senha:
            texto_feedback.value = "Por favor, preencha todos os campos!"
        elif verificar_login(login, senha):
            tela_definir_palavra_secreta(page)
            return
        else:
            texto_feedback.value = "Login ou senha incorretos! Cadastre-se caso não tenha uma conta."

        page.update()

    # Ação para efetuar cadastro
    def acao_registro(e):
        login = campo_usuario.value.strip()
        senha = campo_senha.value.strip()

        if not login or not senha:
            texto_feedback.value = "Por favor, preencha todos os campos!"
        elif verificar_login(login, senha):
            texto_feedback.value = "Este usuário já está cadastrado!"
        else:
            salvar_usuario(login, senha)
            texto_feedback.value = "Cadastro realizado com sucesso! Agora faça login."
            texto_feedback.color = ft.colors.GREEN

        page.update()

    botao_entrar = ft.ElevatedButton("ENTRAR", on_click=acao_login)
    botao_registrar = ft.ElevatedButton("CADASTRAR", on_click=acao_registro)

    container_login = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text("BEM-VINDO!", size=24, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE),
                campo_usuario,
                campo_senha,
                texto_feedback,
                ft.Row([botao_entrar, botao_registrar], alignment=ft.MainAxisAlignment.CENTER)
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=15
        ),
        alignment=ft.alignment.center
    )

    pilha_componentes = ft.Stack(
        controls=[imagem_fundo, container_login],
        width=page.width,
        height=page.height
    )

    page.add(pilha_componentes)


def tela_definir_palavra_secreta(page: ft.Page):
    """
    Exibe a tela para o usuário definir a palavra secreta que será utilizada no jogo da forca.
    """
    page.clean()

    imagem_fundo = ft.Image(
        src="imagens_01/3dcfe3a7-49cc-4480-a13d-67b5cbee4665.jpg",
        width=page.width,
        height=page.height,
        fit=ft.ImageFit.COVER
    )

    campo_palavra_secreta = ft.TextField(
        label="Defina a palavra secreta",
        width=300,
        bgcolor=ft.colors.BLACK54,
        text_style=ft.TextStyle(color=ft.colors.WHITE)
    )

    def acao_iniciar_jogo(e):
        if campo_palavra_secreta.value.strip():
            jogo_forca(page, campo_palavra_secreta.value.lower())
        else:
            campo_palavra_secreta.error_text = "Digite uma palavra válida!"
            page.update()

    botao_iniciar = ft.ElevatedButton("Iniciar Jogo", on_click=acao_iniciar_jogo)

    container_palavra = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text("Escolha a Palavra Secreta", size=24, weight=ft.FontWeight.BOLD, 
                        color=ft.colors.WHITE, bgcolor="BLACK54"),
                campo_palavra_secreta,
                botao_iniciar
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=15
        ),
        alignment=ft.alignment.center
    )

    pilha_componentes = ft.Stack(
        controls=[imagem_fundo, container_palavra],
        width=page.width,
        height=page.height
    )

    page.add(pilha_componentes)


def jogo_forca(page: ft.Page, palavra: str):
    """
    Implementa a lógica do jogo da forca.
    Permite que o usuário adivinhe letras da palavra secreta,
    atualizando a interface conforme o progresso.
    """
    page.clean()

    imagem_fundo = ft.Image(
        src="imagens_01/eb5a69d6-bdb4-47d5-954e-56b7934076b6.jpg",
        width=page.width,
        height=page.height,
        fit=ft.ImageFit.COVER
    )

    letras_incorretas = []
    letras_certas = []
    tentativas_restantes = 7

    texto_palavra = ft.Text(
        value="Palavra: " + "- " * len(palavra),
        size=28,
        bgcolor="BLACK54",
        color=ft.colors.WHITE
    )

    texto_tentativas = ft.Text(
        value=f"Tentativas restantes: {tentativas_restantes}",
        size=30,
        bgcolor="BLACK54",
        color=ft.colors.WHITE
    )

    texto_letras_erradas = ft.Text(
        value="Letras erradas: ",
        size=30,
        bgcolor="BLACK54",
        color=ft.colors.WHITE
    )

    campo_letra = ft.TextField(
        label="Digite uma letra",
        width=250,
        bgcolor=ft.colors.WHITE,
        text_style=ft.TextStyle(color=ft.colors.BLACK)
    )

    def acao_adivinhar_letra(e):
        nonlocal tentativas_restantes

        letra = campo_letra.value.lower()
        campo_letra.value = ""

        # Ignora se a letra já foi digitada ou se não é uma única letra
        if letra in letras_certas or letra in letras_incorretas or len(letra) != 1:
            return

        if letra in palavra:
            letras_certas.append(letra)
        else:
            letras_incorretas.append(letra)
            tentativas_restantes = max(0, tentativas_restantes - 1)

        palavra_atual = "".join([l if l in letras_certas else "- " for l in palavra])

        texto_palavra.value = f"Palavra: {palavra_atual}"
        texto_tentativas.value = f"Tentativas restantes: {tentativas_restantes}"
        texto_letras_erradas.value = f"Letras erradas: {', '.join(letras_incorretas)}"

        # Se o jogador acertou todas as letras, exibe a tela de vitória
        if "_" not in palavra_atual:
            tela_vitoria(page, palavra)
            return

        # Se as tentativas se esgotaram, exibe a tela de derrota
        if tentativas_restantes <= 0:
            tela_derrota(page)
            return

        page.update()

    def acao_reiniciar_jogo(e):
        tela_definir_palavra_secreta(page)

    botao_reiniciar = ft.ElevatedButton("Reiniciar Jogo", on_click=acao_reiniciar_jogo, visible=False)
    botao_adivinhar = ft.ElevatedButton("Adivinhar Letra", on_click=acao_adivinhar_letra)

    container_jogo = ft.Container(
        content=ft.Column(
            controls=[
                texto_palavra,
                texto_tentativas,
                texto_letras_erradas,
                campo_letra,
                botao_adivinhar,
                botao_reiniciar
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10
        ),
        alignment=ft.alignment.center
    )

    pilha_componentes = ft.Stack(
        controls=[imagem_fundo, container_jogo],
        width=page.width,
        height=page.height
    )

    page.add(pilha_componentes)


def tela_derrota(page: ft.Page):
    """
    Exibe uma tela com uma imagem e mensagem indicando que o jogador perdeu.
    """
    page.clean()
    
    # def acao_reiniciar_jogo(e):
    #     tela_definir_palavra_secreta(page)

    # botao_reiniciar = ft.ElevatedButton("Reiniciar Jogo", on_click=acao_reiniciar_jogo)

    imagem_derrota = ft.Image(
        src="imagens_01/cf51c638-624e-47ae-b7ee-2d2bfd143011.jpg",
        width=page.width,
        height=page.height,
        fit=ft.ImageFit.COVER
    )

    texto_derrota = ft.Text(
        "VOCÊ PERDEU !!! TENTE NOVAMENTE ANTES QUE EU SURTE!",
        size=28,
        bgcolor="BLACK54",
        color=ft.colors.WHITE,
        weight=ft.FontWeight.BOLD
    )

    container_derrota = ft.Container(
        content=ft.Column(
            controls=[texto_derrota, ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        ),
        alignment=ft.alignment.center
    )

    pilha_componentes = ft.Stack(
        controls=[imagem_derrota, container_derrota],
        width=page.width,
        height=page.height
    )

    page.add(pilha_componentes)


def tela_vitoria(page: ft.Page, palavra: str):
    """
    Exibe uma tela com uma imagem e mensagem indicando que o jogador venceu.
    """
    page.clean()
    
    # def acao_reiniciar_jogo(e):
    #     tela_definir_palavra_secreta(page)

    # botao_reiniciar = ft.ElevatedButton("Reiniciar Jogo", on_click=acao_reiniciar_jogo)

    imagem_vitoria = ft.Image(
        src="imagens_01/eb5a69d6-bdb4-47d5-954e-56b7934076b6.jpg",
        width=page.width,
        height=page.height,
        fit=ft.ImageFit.COVER
    )

    texto_vitoria = ft.Text(
        f"PARABÉNS! VOCÊ VENCEU! A palavra era: {palavra}",
        size=28,
        bgcolor="BLACK54",
        color=ft.colors.WHITE,
        weight=ft.FontWeight.BOLD
    )

    container_vitoria = ft.Container(
        content=ft.Column(
            controls=[texto_vitoria, ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        ),
        alignment=ft.alignment.center
    )

    pilha_componentes = ft.Stack(
        controls=[imagem_vitoria, container_vitoria],
        width=page.width,
        height=page.height
    )

    page.add(pilha_componentes)


# --- Função Principal ---

def main(page: ft.Page):
    page.title = "Jogo da Forca"
    page.bgcolor = ft.colors.BLACK
    tela_login(page)


ft.app(target=main)
