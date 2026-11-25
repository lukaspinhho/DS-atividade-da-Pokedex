CREATE DATABASE pokedex; --Criar este banco

USE pokedex; -- igual clicar 2 vezes no negócio do schema, para definir este BD


CREATE TABLE If NOT Exists pokemon(
    id INT Auto_Increment Primary Key,
    numero Int NOT NULL,
    nome VARCHAR(100) NOT NULL,
    tipo VARCHAR(45) NOT NULL,
    nivel Int NOT NULL,
    hp Int NOT NULL,
    ataque Int NOT NULL,
    defesa Int NOT NULL,
    descricao varchar(345),
    imagem LONGBLOB

)