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
	 descricao VARCHAR(100),  
	 criador INTEGER NOT null,
	 foto_evento_url VARCHAR(100),
	 
	 CONSTRAINT fk_usuario
	 	FOREIGN KEY (criador)
	 	REFERENCES Usuarios(id)
	 	on delete CASCADE
); 

CREATE TABLE Inscricao 
( 
     id SERIAL PRIMARY key unique,
     usuario_id SERIAL NOT null,
     eventos_id SERIAL NOT null,
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
	tag_id SERIAL not null,
	eventos_id SERIAL not null,
	
	FOREIGN KEY(eventos_id) REFERENCES eventos(id) ON DELETE CASCADE,
    FOREIGN KEY(tag_id) REFERENCES tags(id) ON DELETE CASCADE
);
