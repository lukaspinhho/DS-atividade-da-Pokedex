class Pokemon:
    def __init__(self, numero, nome, tipo, nivel=1, hp=0, ataque=0,
                 defesa=0, descricao=" ", imagem=None,id=None):
        self.id = id
        self.numero =numero
        self.nome =nome
        self.tipo =tipo
        self.nivel =nivel
        self.hp =hp
        self.ataque =ataque
        self.defesa =defesa
        self.descricao =descricao
        self.imagem =imagem 

    def validar(self):
        if not str(self.nome).strip():
            raise ValueError("Coloque o nomu.")
        if not str(self.tipo).strip():
            raise ValueError("Coloque o tipo")
        for campo in ("numero", "nivel", "hp", "ataque", "defesa"):
            valor = getattr(self, campo)
            if not isinstance(valor, int) or valor < 0:
                raise ValueError(f"'{campo}'Deve ser um número inteiro ou zero.")
        if self.numero < 1:
            raise ValueError("O número da Pokedex deve ser um número maior que zero.")

    def __str__(self):
        return f"#{self.numero} {self.nome} ({self.tipo})"