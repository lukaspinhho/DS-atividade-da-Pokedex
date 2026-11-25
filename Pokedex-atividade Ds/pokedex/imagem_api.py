import urllib.request
import urllib.error
from .interfaces import IImagemServico

URL_SPRITE = "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{numero}.png"


class ImagemServicoPokeAPI(IImagemServico):

    def __init__(self,  timeout=8):
        self.timeout=timeout

    def baixar(self,numero):
        url = URL_SPRITE.format(numero=numero)

        req = urllib.request.Request(
            url,
            headers={"User-Agent": "pokedex-escolar/1.0"}
        )

        try:
            with urllib.request.urlopen(req,timeout=self.timeout) as resp:
                return resp.read()

        except urllib.error.HTTPError as e:
            if e.code == 404:
                raise ValueError(f"Não existe imagem nº{numero} na API.")

            raise ConnectionError(
                f"Erro ao acessar a API de imagens (HTTP {e.code}).")

        except urllib.error.URLError:
            raise ConnectionError("Sem conexão com a API de imagens.")