from abc import ABC, abstractmethod
class IPokemonRepositorio(ABC):
    @abstractmethod
    def inserir(self, pokemon):
        """"""
    @abstractmethod
    def atualizar(self, pokemon):
        """"""
    @abstractmethod
    def excluir(self, id_pokemon):
        """"""
    @abstractmethod
    def buscar_por_id(self, id_pokemon):
        """"""
    @abstractmethod
    def listar(self):
        """"""
    @abstractmethod
    def consultar(self, campo, termo):
        """"""
class IImagemServico(ABC):
    """"""

    @abstractmethod
    def baixar(self, numero):
        """"""