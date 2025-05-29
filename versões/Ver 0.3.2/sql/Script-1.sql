CREATE TABLE Usuarios 
( 
	 id SERIAL PRIMARY KEY ,  
	 nome VARCHAR(100) NOT NULL,  
	 email VARCHAR(100) NOT null UNIQUE,  
	 senha VARCHAR(100) NOT null,
	 foto_perfil_url VARCHAR(100)
); 

CREATE TABLE Eventos 
( 
	 id SERIAL PRIMARY KEY ,  
	 titulo VARCHAR(100) NOT NULL,  
	 data_inscricao TIMESTAMP NOT NULL,
	 data_prazo TIMESTAMP NOT NULL,  
	 data_execucao TIMESTAMP NOT NULL,  
	 localizacao VARCHAR(100),  
	 descricao VARCHAR(10000),  
	 criador INTEGER NOT null,
	 foto_evento_url VARCHAR(100),
	 limite Integer,
	 
	 CONSTRAINT fk_usuario
	 	FOREIGN KEY (criador)
	 	REFERENCES Usuarios(id)
	 	on delete CASCADE
);

ALTER TABLE Eventos
ALTER COLUMN descricao TYPE VARCHAR(10000);

CREATE TABLE Inscricao 
( 
     id SERIAL PRIMARY key unique,
     usuario_id INTEGER NOT null,
     eventos_id INTEGER NOT null,
     compareceu BOOLEAN DEFAULT FALSE,
     data_inscricao DATE NOT NULL DEFAULT CURRENT_DATE,
     status VARCHAR(10) CHECK (status IN ('confirmado', 'cancelado')),

        CONSTRAINT fk_evento
            FOREIGN KEY (eventos_id)
            REFERENCES Eventos(id)
            ON DELETE CASCADE,

        CONSTRAINT fk_usuario
            FOREIGN KEY (usuario_id)
            REFERENCES Usuarios(id)
            ON DELETE CASCADE
);

create table Tags
(
	id SERIAL primary key unique,
	nome VARCHAR(100) NOT NULL
);

create table evento_tags
(
	tag_id INTEGER not null,
	eventos_id INTEGER not null,
	
	FOREIGN KEY(eventos_id) REFERENCES eventos(id) ON DELETE CASCADE,
    FOREIGN KEY(tag_id) REFERENCES tags(id) ON DELETE CASCADE
);


drop table Eventos cascade;
drop table evento_tags cascade;
drop table inscricao;

select * from usuarios u;

select * from evento_tags;

select * from tags;

select * from Inscricao;

select * from eventos;
