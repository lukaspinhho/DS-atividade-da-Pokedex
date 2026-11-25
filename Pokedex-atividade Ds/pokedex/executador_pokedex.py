from .interfaces import IImagemServico, IPokemonRepositorio
from .modelo import Pokemon
class Executadores:
    def __init__(self, repositorio: IPokemonRepositorio,imagens:IImagemServico):
        self._repo =repositorio
        self._imagens =imagens


    def cadastrar(self, pokemon: Pokemon):
        pokemon.validar()
        aviso = self._tentar_baixar_imagem(pokemon)
        return self._repo.inserir(pokemon), aviso

    def alterar(self, pokemon: Pokemon):
        pokemon.validar()

        atual = self._repo.buscar_por_id(pokemon.id)

        if atual is None:
            raise ValueError("Pokemon não encontrado.")

        aviso=None

        if atual.numero !=pokemon.numero or atual.imagem is None:
            aviso=self._tentar_baixar_imagem(pokemon)
        else:
            pokemon.imagem=atual.imagem

        self._repo.atualizar(pokemon)
        return aviso

    def excluir(self,id_pokemon):
        self._repo.excluir(id_pokemon)

    def obter(self,id_pokemon):
        return self._repo.buscar_por_id(id_pokemon)

    def listar(self):
        return self._repo.listar()

    def consultar(self,campo,termo):
        termo = termo.strip()

        if not termo:
            return self._repo.listar()

        if campo == "numero" and not termo.isdigit():
            raise ValueError(
                "Para consultar por número, digite apenas dígitos."
            )

        return self._repo.consultar(campo, termo)

    def _tentar_baixar_imagem(self, pokemon):
        try:
            pokemon.imagem = self._imagens.baixar(pokemon.numero)
            return None

        except (ValueError, ConnectionError) as erro:
            pokemon.imagem = None
            return str(erro)