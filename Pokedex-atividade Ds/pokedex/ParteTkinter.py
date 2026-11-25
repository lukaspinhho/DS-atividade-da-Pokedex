import tkinter as tk                 #importa o mínimo possível
from tkinter import messagebox       #por isso precisa colocar um "complemento" ou algo do tipo.
from PIL import Image
import io
import customtkinter as ctk  #para personalizar o Tkinter

from .modelo import Pokemon
from .executador_pokedex import Executadores
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")
class Pokedex_tkinter(ctk.CTk):  # Maior parte será relacionada a gráfica
    def __init__(self, servico):
        super().__init__()
        messagebox.showinfo('Pokedex','Sua Pokedex abriu')#mensagem
        self.title("Pokedex") 
        self.geometry("850x600") #tamanho da janela
        self.configure(fg_color="#04FAEE") #parte funco
        self.servico=servico
        self.id=None
        self.foto=None
        self.campos={}
        quadro=ctk.CTkFrame(self,fg_color="#1C5C39")
        quadro.pack(side="right") #ladOs

        for campo in ["numero", "nome", "tipo", "nivel", #para os campos 
                      "hp", "ataque", "defesa"]:
            entrada =ctk.CTkEntry(
                quadro,placeholder_text=campo.capitalize(),
                width=325)
             #pady tem relação com a área de certos elementos como as caixas, a parte da imagem e etc....
            entrada.pack(pady=6) 
            self.campos[campo]=entrada
        self.descricao=ctk.CTkTextbox(quadro, width=320, height=67)
        self.descricao.pack(pady=6)
        self.imagem =ctk.CTkLabel(quadro, text="-=-=-=Imagem do pokémon-=-=-=-=")
        self.imagem.pack(pady=11)
        for texto, funcao in [
            (":Cadastrar:",  self.cadastrar),(":Alterar:", self.alterar),(":Excluir:",self.excluir),(":Limpar: ",self.limpar)]:
            ctk.CTkButton(
             quadro, text=texto,
             fg_color="#2BAD2B",
             command=funcao
            ).pack(pady=7.5)
        painel = ctk.CTkFrame(self, fg_color="#277E4E")
        painel.pack(side="right", padx=15, pady=12, fill="both", expand=True) 
        self.lista = ctk.CTkTextbox(painel, width=350)
        self.lista.pack(padx=10, pady=10, fill="both", expand=True)
        self.lista.bind("<ButtonRelease-1>", self.selecionar)

        ctk.CTkButton(
            painel, text="Atualize a lista",
            command=self.listar
        ).pack(pady=5)
        self.listar()

    def ler(self): #criação da função da parte de pegar 
        return Pokemon(
            numero=  int(self.campos["numero"].get()), 
            nome=  self.campos["nome"].get(),
            tipo=  self.campos["tipo"].get(),
            nivel=  int(self.campos["nivel"].get()),
            hp=   int(self.campos["hp"].get()),
            ataque=  int(self.campos["ataque"].get()),
            defesa=  int(self.campos["defesa"].get()),
            descricao=  self.descricao.get("1.0", "end").strip())
    def cadastrar(self): #funçao para parte do cadastro, principalmente o botão
        try:
            self.servico.cadastrar(self.ler())
            self.listar()
            self.limpar() 
        except Exception as erro:
            messagebox.showerror("erro", str(erro))#erro mensagem
    def listar(self):
        self.lista.delete("1.0", "end")
        for p in self.servico.listar():
            self.lista.insert(
                "end",
                f"ID:{p.id} | Nº: {p.numero}\n"
                f"Nome:{p.nome} | Tipo: {p.tipo}\n"
                f"Nível:{p.nivel}\n"
                "\033[33m-==-=-=-=-=-=-=-=-=-=-===-=-=-=-=-=-\033[m\n")
    def selecionar(self,  evento):
        linha = self.lista.index(f"@{evento.x},{evento.y}").split(".")[0]
        conteudo = self.lista.get(f"{linha}.0", f"{linha}.end")

        if conteudo.startswith("ID:"):
            try:
                id_pokemon=int(conteudo.split("|")[0].replace("ID:", "").strip())
                p = self.servico.obter(id_pokemon)

                if p:
                    self.id =p.id

                    for campo in self.campos:
                        self.campos[campo].delete(0, "end")
                        self.campos[campo].insert(0, str(getattr(p, campo)))

                    self.descricao.delete("1.0", "end")
                    self.descricao.insert("1.0", p.descricao)

                    self.mostrar_imagem(p.imagem)

            except Exception as erro:
                messagebox.showerror("errro!", str(erro))

    def mostrar_imagem(self, dados):
        if not dados:
            self.foto =None
            self.imagem.configure(image=None, text="Sem imagem disponível")
            return

        try:
            foto = Image.open(io.BytesIO(dados))
            self.foto = ctk.CTkImage(
                light_image=foto,
                dark_image=foto,
                size=(130, 130)
            )
            self.imagem.configure(image=self.foto, text="")

        except Exception:
            self.imagem.configure(image=None, text="a imagem não está disponível")

    def alterar(self):
        if self.id is None:
            messagebox.showwarning("atenção", "Selecione um Pokémon.")
            return

        try:
            p = self.ler()
            p.id = self.id
            self.servico.alterar(p)
            self.limpar()
            self.listar()
        except Exception as erro:
            messagebox.showerror("Erro", str(erro))

    def excluir(self): #excluir
        if self.id is None:
            messagebox.showwarning("Atenção", "Selecione um Pokémon.")
            return

        if messagebox.askyesno("Excluir", "Deseja excluir?"):
            self.servico.excluir(self.id)
            self.limpar()
            self.listar()

    def limpar(self): #função para limpar valores da barra
        self.id = None

        for campo in self.campos.values():
            campo.delete(0,"end")

        self.descricao.delete("1.0", "end")
        self.foto = None
        self.imagem.configure(image=None,text="Imagem do Pokémon")