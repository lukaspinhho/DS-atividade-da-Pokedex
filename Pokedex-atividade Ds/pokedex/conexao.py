import os
import mysql.connector
class Conexao:
    def __init__(self, host=None, usuario=None, senha=None, banco=None):
        self.config = {
            "host":host or os.getenv("POKEDEX_DB_HOST", "localhost"),
            "user":usuario or os.getenv("POKEDEX_DB_USER", "root"),
            "password":senha if senha is not None else os.getenv("POKEDEX_DB_PASSWORD", "P@r@d0x0"),
            "database":banco or os.getenv("POKEDEX_DB_NAME", "pokedex"),}
    def obter(self):
        return mysql.connector.connect(**self.config)