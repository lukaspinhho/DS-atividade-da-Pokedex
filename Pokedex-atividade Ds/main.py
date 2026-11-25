from pokedex.conexao import Conexao
from pokedex.imagem_api import ImagemServicoPokeAPI
from pokedex.repositorio_mysql import PokemonRepositorioMySQL
from pokedex.executador_pokedex import Executadores
from pokedex.ParteTkinter import Pokedex_tkinter
def main():
    repositorio = PokemonRepositorioMySQL(Conexao())
    servico = Executadores(repositorio, ImagemServicoPokeAPI())
    Pokedex_tkinter(servico).mainloop()
if __name__ == "__main__":
    main()