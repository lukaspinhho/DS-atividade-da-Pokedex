from .interfaces import IPokemonRepositorio
from .modelo import Pokemon
_COLUNAS_SEM_IMAGEM="id, numero, nome, tipo, nivel, hp, ataque, defesa, descricao"


def _linha_para_pokemon(linha, com_imagem=False):
    return Pokemon(
        id=linha[0], numero=linha[1], nome=linha[2], tipo=linha[3],
        nivel=linha[4], hp=linha[5], ataque=linha[6], defesa=linha[7],
        descricao=linha[8] or "",
        imagem=bytes(linha[9]) if com_imagem and linha[9] is not None else None,)
class PokemonRepositorioMySQL(IPokemonRepositorio):
    def __init__(self, conexao):
        self._conexao =conexao

    def _executar(self,  sql,params= (),fetch=False):
        con = self._conexao.obter()
        try:
            cur = con.cursor()
            cur.execute(sql,params)
            if fetch:
                return cur.fetchall()
            con.commit()
            return cur.lastrowid
        finally:
            con.close()
    def inserir(self,p):
        sql = ("INSERT INTO pokemon (numero, nome, tipo, nivel, hp, ataque, defesa, descricao, imagem) " #ligado ao codigo de inserir no SQL
               "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)")
        return self._executar(sql, (p.numero,p.nome,p.tipo,p.nivel,p.hp,
                                    p.ataque,p.defesa,p.descricao,p.imagem))

    def atualizar(self,p):
        sql = ("UPDATE pokemon SET numero=%s, nome=%s, tipo=%s, nivel=%s, hp=%s, "
               "ataque=%s, defesa=%s, descricao=%s, imagem=%s WHERE id=%s")
        self._executar(sql, (p.numero,p.nome,p.tipo, p.nivel,p.hp,p.ataque,
                             p.defesa,p.descricao,p.imagem,p.id))

    def excluir(self,id_pokemon):
        self._executar("DELETE FROM pokemon WHERE id=%s", (id_pokemon,))

    def buscar_por_id(self,id_pokemon):
        linhas = self._executar(
            f"SELECT {_COLUNAS_SEM_IMAGEM}, imagem FROM pokemon WHERE id=%s",
            (id_pokemon,), fetch=True)
        return _linha_para_pokemon(linhas[0],com_imagem=True) if linhas else None

    def listar( self):
        linhas = self._executar(
            f"SELECT {_COLUNAS_SEM_IMAGEM} FROM pokemon ORDER BY numero, nome",fetch=True)
        return [_linha_para_pokemon(l) for l in linhas]

    def consultar(self, campo, termo):
        if campo=="numero":
            sql = f"SELECT {_COLUNAS_SEM_IMAGEM} FROM pokemon WHERE numero=%s ORDER BY nome"
            params = (int(termo),)
        elif campo in ("nome", "tipo"):  
            sql = f"SELECT {_COLUNAS_SEM_IMAGEM} FROM pokemon WHERE {campo} LIKE %s ORDER BY nome"
            params =(f"%{termo}%",)
        else:
            raise ValueError("Campo de consulta inválido.")
        return [_linha_para_pokemon(l) for l in self._executar(sql, params, fetch=True)]