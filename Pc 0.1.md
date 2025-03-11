## Procedimento de Compilação

<!-- Aqui fica o cabeçalho, onde teremos informações rápidas sobre as modificações do procedimento-->
<div align="center">
    <table border="1">
        <thead>
            <tr>
                <th><strong>CÓDIGO</strong></th>
                <th><strong>TÍTULO</strong></th>
                <th><strong>STATUS</strong></th>
                <th><strong>DATA DA REVISÃO</strong></th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>PC-2.0.3.-01</td>
                <td>Adicionar visual das condições</td>
                <td>Compilado</td>
                <td>05/02/2025</td>
            </tr>
        </tbody>
    </table>
</div>

### 1. Geral
Foi criado o arquivo **Db.py** sendo um script que reverencia ao SQLAlchemy
Foi criado o arquivo **models.py** sendo um script que guarda as classes do programa que serão usadas para a manipulação do banco de dados
Foi criado o **main.py** responsável pelas rotas, conexão com o banco de dados, etc
Foi criado o **homepage.html** sendo a pagina principal do programa quando o usuário acessar a aplicação variando se o usuário estiver ou não logado
Foi criado o **atualizar_usu.html** sendo responsável por atualizar informações do usuário no banco como troca de email, senha etc.
Foi criado o **login.html responsável** pelo login do usuário e acesso ao site
Foi criado o **register.html** responsável por registrar o usuário no banco de dados e consequentemente enviar o login para o banco.
No **main.py** foram criadas as rotas de login,registrar,homepage,logout e atualizar_usu respectivamente responsaveis por: login, registro, pagina inicial, logout e atualização das informações do usuario
Foram criados botões no html responsaveis por direcionar o usuario para um novo html
---

### 2. Programação

**Db.py**

Foi importado a biblioteca fask_sqlalchemy para a conexão do banco de dados, a variável db recebe o modelo do SQLAlchemy a fazendo ter todas as propriedades para manipulação de um banco:
```Python
from flask_sqlalchemy import SQLAlchemy 
db = SQLAlchemy()


```

**Objects > Players > obj_father_players > Step**

Foi adicionado no if da movimentação do jogador um && com a variável move_r == false, fazendo com que a variável knockback fique apenas para a função de sua condição, e esta nova (move_r) cuide dos demais casos referentes a outras condições no quesito de restringir a movimentação.

```GML
//Fazendo a movimentação do jogador
if(knockback == false && move_r == false){
	hor_speed = (walk_right - walk_left) * max_speed;
}
```

**Objects > Players > obj_father_players > Draw**

Foi adicionada uma nova region para a lógica das condições. A variavel total_conditions conta o numero de condições que estão ativas no jogador, o vetor v_conditions armazena todas as condições que o jogador pode ter, após isto é feito um loop para contar quantas condições estão ativas no jogador e aumentar em 1 o valor de total_conditions. A variavel total_width calcula a largura total ocupada pelos icones e a x_start calcula a posição inicial das condições para sua centralização,as variáveis x_condition e y_condition são iniciadas com o valor de x_start e y inicial do player para calcular as posições iniciais

Após isso, foram criados 7 ifs que verificam se a variável correspondente a uma condição do jogador é verdadeira. Caso seja, chama-se a função draw_sprite, que desenha:

O sprite da condição,

O frame do sprite,

A posição em x,

A posição em y - 100 (esse -100 faz com que o ícone fique acima da cabeça do player).

Após isso, adiciona-se +32 em x_condition, para que, caso o player sofra mais de uma condição, o próximo ícone seja desenhado a 32 pixels de distância do anterior.

```GML
#region // Desenhando as Condições
if(global.gamemode = "1x1"){
	if(obj_gameplay.game_state == "Playing"){
		draw_condition = true;
	} else {
		draw_condition = false;
	}
} else if(global.gamemode = "Headball"){
	if(obj_gameplay_hball.game_state == "Playing"){
		draw_condition = true;
	} else {
		draw_condition = false;
	}
}

// Limitando o motivo de desenhar as condições
if(draw_condition){
	// Conta o total de condições 
	var total_conditions = 0;

	// Vetor com todas as condições
	var v_conditions = [player_obj.knockback, player_obj.stunned, player_obj.slow, player_obj.invincibility, player_obj.fast, player_obj.high_jump, player_obj.transformed];

	// Loop for para contar o total de condições ativas no jogador
	for (var i = 0; i < array_length(v_conditions); i++) {
		if(v_conditions[i]){
			total_conditions +=1;
		}
	}
	
	// Largura ocupada pelos sprites
	var total_width = total_conditions * 32;
	// Calcula o inicio ajustando a posição para centralizar
	var start_x = x - (total_width / 2) + 16;

	var x_condition = start_x; // Posição X inicial
	var y_condition = y; // Posição Y inicial

	// Desenhando o icone de stunado
	if(player_obj.knockback == true){
	    draw_sprite(spr_random_portrait, 0,x_condition, y_condition-100);
	    x_condition += 32; // Move a posição X para a próxima condição

	}
	if(player_obj.stunned == true){
		draw_sprite(spr_random_portrait, 0,x_condition, y_condition-100);
	    x_condition += 32; // Move a posição X para a próxima condição
	}

	if(player_obj.slow == true){
		draw_sprite(spr_condition_slow, 0,x_condition, y_condition-100);
	    x_condition += 32; // Move a posição X para a próxima condição
	}

	if(player_obj.invincibility == true){
		draw_sprite(spr_condition_invincibility, 0,x_condition, y_condition-100);
	    x_condition += 32; // Move a posição X para a próxima condição
	}

	if(player_obj.fast == true){
		draw_sprite(spr_condition_fast, 0,x_condition, y_condition-100);
	    x_condition += 32; // Move a posição X para a próxima condição
	}

	if(player_obj.high_jump == true){
		draw_sprite(spr_condition_high_jump, 0,x_condition, y_condition-100);
	    x_condition += 32; // Move a posição X para a próxima condição
	}

	if(player_obj.transformed == true){
		draw_sprite(spr_condition_transformed, 0,x_condition, y_condition-100);
	    x_condition += 32; // Move a posição X para a próxima condição
	}
}
#endregion
```

**Objects > Gameplay > Headball > obj_gameplay_hball > Create**

Para evitar que seja desenhado as condições quando tiver dentro de uma partida, foi preciso editar o código dos objetos de gameplay que tem em cada modo de jogo.

```GML
// Para ver o estado do jogo
game_state = "Playing";
```

**Objects > Gameplay > Headball > obj_gameplay_hball > Step**

Foi modificado para ver qual o estado que está o jogo, se está sendo jogado ou se está na tela de carregamento.

```GML
#region //Condições que ativam o jogador ganhar (preencher depois)
#endregion
#region //Controle de tempo da partida
if(time_left > 0){
	time_left--;
	
	game_state = "Playing";
}

#region //Programação para o final da partida
if(game_over){
	game_state = "Encerring";
	
	//Verifica se o placar dos player é igual e se a prorrogação ainda não foi ativada
	if(players_score[0] == players_score[1] && extension == false){
		if(final_countdown == false){
			//Inicia a prorrogação
			game_over = false;
			extension = true;
			time_left = 60 * 180;
		}
	}
		
	timer++;
		
	if(timer >= 60 * 5){ //Fazendo com qe depois de 5 segundos ele volte para a room selection;
		room_goto(rm_selection);
		obj_selection.confirmed1 = false;
		obj_selection.confirmed2 = false;	
	}
}
#endregion
#endregion
```

**Objects > Gameplay > 1x1 > obj_gameplay > Create**

Para evitar que seja desenhado as condições quando tiver dentro de uma partida, foi preciso editar o código dos objetos de gameplay que tem em cada modo de jogo.

```GML
// Para ver o estado do jogo
game_state = "Playing";
```

**Objects > Gameplay > 1x1 > obj_gameplay > Step**

```GML
//Desenhando o vencendor do jogo
draw_set_font(fnt_pixel);
draw_set_halign(fa_center);
draw_set_valign(fa_middle);
draw_self();

//Desenhando o tempo
draw_text_ext_transformed(room_width/2, y, round(time_left/60), 5, 500, 4, 4, 0);


#region // Desenhando 
if(time_left <= 0 || obj_player1.life <= 0 || obj_player2.life <= 0){
	game_state = "Encerring";
	
	// Ativando as invecibilidade
	obj_player1.invincibility = true;
	obj_player2.invincibility = true;
	
	// Verifica as condições de vitória ou empate
	if(obj_player1.life > obj_player2.life){
		draw_text_ext_transformed(room_width/2, room_height/2, "JOGADOR 1 VENCEU!", 5, 500, 4, 4, 0);
	} else if(obj_player2.life > obj_player1.life){
		draw_text_ext_transformed(room_width/2, room_height/2, "JOGADOR 2 VENCEU!", 5, 500, 4, 4, 0);
	} else {
		draw_text_ext_transformed(room_width/2, room_height/2, "EMPATE", 5, 100, 4, 4, 0);
	}
	
	timer_red++;
	
	if(timer_red > (60 * 5)){
		game_over = true;
	}
}

if(game_over){
	// Pegando o tamanho da tela
	var _x1 = camera_get_view_x(view_camera[0]);
	var _width = camera_get_view_width(view_camera[0]);
	var _x2 = _x1 + _width;
	var _middle_w = _x1 + (_width/2);
	
	var _y1 = camera_get_view_y(view_camera[0]);
	var _height = camera_get_view_height(view_camera[0]);
	var _y2 = _y1 + _height;
	var _middle_h = _y1 + (_height/2);
	
	var _red = #9E0B0F;
	
	var _time = clamp(curr_time/60, 0, 1);
	
	value = ease_out(0, _width, _time);
	draw_rectangle_color(_x1, _y1, _x1 + value, _height, _red, _red, _red, _red, 0);
	
	if(_time < 1){
		curr_time += 1;
	}
	
	if(alarm[1] = -1){
		alarm[1] = 60 * 5;
	}
	
	
	draw_text_ext_transformed(room_width/2, room_height/2, "Redicionando para o menu inicial em " + string(round(alarm[1]/60)) + "s", 10, 250, 3, 3, 0);
		
}
#endregion

draw_set_halign(-1);
draw_set_valign(-1);
```

**Scripts > scr_skills_attack**

**scr_lucas_player_attack()**
Todas as linhas referentes à variável knockback foram alteradas para move_r, já que agora a variável move_r é responsável por restringir o movimento geral. Além disso, foi adicionada a referência à variável fast do player (_player.fast), fazendo com que o Lucas ganhe a condição veloz em sua habilidade.

**scr_naja_player_attack()**
Todas as linhas que tinham referência à variável knockback no state "Stunned" foram alteradas para move_r, já que agora a variável move_r é responsável por restringir o movimento geral. Essas mudanças fazem com que a Naja aplique a condição stunado no inimigo.
 
```GML
#region //Ataque do Lucas
function scr_lucas_player_attack(_my_enemy, _player){
	/* A ideia é que o Lucas consiga dar um dash na horizontal e conseguir dar dano
	no inimigo durante todo o trajeto. */
	
	if(is_created == true){
		//Pegando a máscara de colisão do jogador
		sprite_index = spr_player1;
		image_alpha = 0;
		
		_player.move_r = true;
		_player.fast = true;
		
		timer = 0;
		
		is_created = false;
	}
	
	timer++;
	
	x = _player.x;
	y = _player.y;
	
	//Para faazer o efeito de Ghost
	with(instance_create_layer(_player.x, _player.y, "Skills", obj_ghost)){
		var _ghost = obj_ghost;
		_ghost.sprite_index = _player.sprite_index;
		_ghost.image_xscale = _player.image_xscale;
		_ghost.image_yscale = _player.image_yscale;
		_ghost.image_blend = c_yellow;
		_ghost.image_alpha = 0.3;
		_ghost.image_speed = 0;
	}
	
	if(_player.player_direction > 0){
		_player.hor_speed = 15;

	} else if(_player.player_direction < 0){
		_player.hor_speed = -15;
	}
	
	_player.ver_speed = 0;
	
	if(place_meeting(_player.x, _player.y, _my_enemy)){
		scr_damage_base(_my_enemy);
	}

	//se o timmer for maior/igual a 10 ou encostar com uma parede em x destroi
	if(timer >= 10 || place_meeting(x + _player.hor_speed, y, colision_array)){
		_player.move_r = false;
		_player.fast = false;
		instance_destroy();
	}
}
#endregion

#region //Ataque da Naja
function scr_naja_player_attack(_my_enemy, _player){
	/* A ideia do ataque da Naja é lançar um projétil para frente, semelhante a flecha do Acir
	capaz de  pedrificar o jogador inimigo quando encostado */
	
	if(is_created == true){
		sprite_index = spr_naja_attack1
		my_direction =	_player.player_direction;
		
		if(my_direction < 0){
			image_xscale = -(image_xscale)
		}
		
		timer = 0
		max_speed = 4;
		
		state = "Beam";
		
		//Lockando o "evento de Created"
		is_created = false
	}
	
	//Velocidade do projetil enquanto não acerta o inimigo
	if(state == "Beam"){
		hor_speed = my_direction * max_speed
	
		//Colisão com o eixo x
		if(place_meeting(x + hor_speed, y, colision_array)){
			while(!place_meeting(x + sign(hor_speed), y, colision_array)){ //Se ele estiver muito próximo (igual a velocidade horizontal) ele vai reduzindo por pixel andado.
				x = x + sign(hor_speed);
			}
		
			hor_speed = 0;
			instance_destroy();
		}
			x = x + hor_speed;
			
			if(place_meeting(x, y, _my_enemy)){
				state = "Stunned";
			}
	}
	
	//Contato com o inimigo
	if(state == "Stunned"){	
	
	
		//Grudando o ataque no inimigo para aplicar o efeito
		x = _my_enemy.x;
		y = _my_enemy.y - 50;
		
		
		//Deixando o projétil grudado invisivel
		image_alpha = 0;
		
		//Fazendo o inimigo ficar cinza quando tiver petrificado
		_my_enemy.image_blend = c_gray;
		
		//Fazendo o player ficar no ultimo sprite
		_my_enemy.image_index = _my_enemy.image_number-1;
		
		//Fazendo o player parar na hora e ficar stunnado
		_my_enemy.move_r = true;
		_my_enemy.stunned = true;
		_my_enemy.hor_speed = 0;
		timer++;
		
		//Timer do stun
		if(timer >= 60 * 1.5){
			_my_enemy.stunned = false;
			_my_enemy.state = "Idle"; //Resetando ele para as animações normais
			_my_enemy.move_r = false;
			
			//Voltando a cor do sprite 
			_my_enemy.image_blend = c_white;
			
			//Destruindo o obj de efeito e o ataque
			instance_destroy();
		}
	}
}
#endregion
```

Neste script, foram feitas alterações em todas as defesas dos personagens, exceto na da Bruna. Em todas as linhas que tinham referência à variável knockback, foram alteradas para a variável move_r, fazendo com que knockback seja usada apenas para sua condição, que é aplicada apenas na defesa da Bruna (até o momento).

Abaixo, envio todo o script e explico as mudanças nas devidas funções:

**scr_esqueleto_player_defense()**
Foi feita apenas a mudança da variável knockback para move_r.

**scr_erick_player_defense()**
Foi feita apenas a mudança da variável knockback para move_r.

**scr_acir_player_defense()**
Foram adicionadas variáveis das respectivas condições aplicadas pelos states da habilidade:

**spr_acir_defense1 (arara azul):**
Adicionada a linha do _player.high_jump, permitindo que o Acir tenha a condição de pulo alto.

**spr_acir_defense2 (onça):**
Adicionada a linha do _player.fast, permitindo que o Acir tenha a condição de veloz.

**spr_acir_defense3 (tatu):**
Adicionada a linha do _player.slow, permitindo que o Acir tenha a condição de lento, além da de invencibilidade.

**scr_lucas_player_defense()**
Foi feita apenas a mudança da variável knockback para move_r, além de adicionar a linha do _player.fast, permitindo que o Lucas tenha a condição veloz, além de invencibilidade durante a habilidade.

**scr_naja_player_defense()**
Foi feita apenas a mudança da variável knockback para move_r, além de adicionar a linha do _player.fast, permitindo que a Naja tenha a condição veloz, além de transformada durante a habilidade.

```GML
#region //Defesa do Esqueleto
function scr_esqueleto_player_defense(_my_enemy, _player){
	if(is_created == true){
		is_created = false;
		
		_player.stunned = true;
		_player.move_r = true;
		_player.hor_speed = 0;
	}
	
	timer++;
	
	//Mudando para o estado caindo para que ele ainda seja capaz de causar dano
	_player.state = "Fall";
	
	//Deixando o player imortal
	_player.invincibility = true;
	_player.sprite_index = spr_esqueleto_defense;
	
	//Lockando o sprite da animação em 1 frame
	if(_player.image_index >= _player.image_number-1){
		_player.image_index = _player.image_number-1;
		
		_player.move_r = true;
		_player.hor_max = 0;
	}
	
	//tempo de duração da habilidade	
	if(timer >= 120 && _player.alarm[1] = -1){
		_player.stunned = false;
		_player.move_r = false;
		_player.alarm[1] = 60;
	}
	
	if(timer >= 180){
		_player.invincibility = false;
		instance_destroy();
	}	
		

}
#endregion

#region //Defesa da Bruna
function scr_bruna_player_defense(_my_enemy, _player){
	/*
	A ideia é que a Bruna crie uma chama que fique grande quando colida com o chão que destrua ataques 
	inimigos e caso um inimigo colida com esta chama ele deve ser empurrado
	*/
	
    if(is_created == true){ //Verificando se ele foi criado para pegar os valores apenas uma vez.
		sprite_index = spr_bruna_defense1;
		
        //Lockando a variavel
         is_created = false;
		 
		//Estado inicial da chama
         state = "lfire"
	}
	
	//Chama enquanto não colidir com o eixo x (queda livre)
    if(state == "lfire"){
		ver_speed = ver_speed + 0.15
	
	//Colisão com eixo y
		if(place_meeting(x, y + ver_speed, colision_array)){
			while(!place_meeting(x, y + sign(ver_speed), colision_array)){
				y += sign(ver_speed);
			}
    
			ver_speed = 0;
	
			//Muda para o estado de chama alta
			state = "hfire";
		}
	
	
		y += ver_speed;
    }
	
	//Estado chama alta
    if(state == "hfire"){
        sprite_index= spr_bruna_defense2
		
		//Colisão com o inimigo
        if(place_meeting(x, y, _my_enemy)){
			//Pegando a direção da repulsão
			var _dir = point_direction(player_def.x, player_def.y, _my_enemy.x, _my_enemy.y)
			_my_enemy.knockback = true;
			
			if(_my_enemy.knockback == true){
				//Timer da duração da repulsão
				_my_enemy.alarm[2] = 20 
				//R para os 2 eixos
				_my_enemy.hor_speed = lengthdir_x(6, _dir)
				_my_enemy.ver_speed = lengthdir_y(6, _dir)
			}
        }
		
		//Colidindo e destruindo ataques inimigos
        if(place_meeting(x, y, enemy_atk)){
            instance_destroy(enemy_atk)
        }
		
        timer++
		
		if(image_index > image_number-1){
			image_index = image_number-2;
		}
		
		//Tempo da habilidade
		if(timer == 80){
			instance_destroy();
		}
    }
}

#endregion

#region //Defesa do Erick
function scr_erick_player_defense(_my_enemy, _player){
	/*A ideia é ele cria um escudo que mude de direção conforme ele muda, bloqueie projeteis
	e se encostar no inimigo stune*/
	if(is_created == true){
		sprite_index = spr_erick_defense;
		is_created = false;
		
		//estado inicial como escudo
		state = "shield";
		timer = 0;
	}
	
	my_direction =	_player.player_direction;	
	
	//Estado escudo
	if(state == "shield"){
		timer++;
		
		//Timer de existencia do escudo neste modo
		if(timer >= 80){
			instance_destroy();	
		}
		
		//Ajustando para que o escudo fique na frente do erick 
		if(my_direction > 0){
			if(image_xscale < 0){
				image_xscale = abs(image_xscale);
			}
			
			x = _player.x + 50
			y = _player.y - 40 
		}
		//Ajustando para que o escudo fique na frente do erick 
		if(my_direction < 0){
			
			if(image_xscale > 0){
				image_xscale = -image_xscale;
			}
			
			x = _player.x - 50
			y = _player.y - 40
		}
		//Destroi ataques do inimigos e relar e se destroi
		if(place_meeting(x, y, enemy_atk)){
			instance_destroy(enemy_atk)
			instance_destroy();
		}
		
		//Se encostar no inimigo muda para o estado stun e reseta o timer de duração
		if(place_meeting(x,y, _my_enemy)){
			timer = 0;
			state = "stun";
		}
	}
	
	//Estado de stun
	if(state == "stun"){
		timer++;
		
		//Escondendo o sprite
		image_alpha = 0;
		
		//Fazendo o sprite se manter dentro do inimigo
		x = _my_enemy.x;
		y = _my_enemy.y - 40;
		
		//Variaveis para o stun
		_my_enemy.stunned = true;
		_my_enemy.move_r = true;
		_my_enemy.hor_speed = 0;
		
		//timer do stun
		if(timer >= 40){
			_my_enemy.stunned = false;
			_my_enemy.move_r = false;
			instance_destroy();
		}
	}
}
#endregion

#region //Defesa do Acir
#region // Escolha do Totem do Acir
function scr_acir_defense_choice(_player){
	if(is_created == true){	
		toten = choose(spr_acir_defense1, spr_acir_defense2, spr_acir_defense3);
		sprite_index = toten;
		_player.toten = toten;
		is_created = false;
	}
	
	x = _player.x;
	y = _player.y - 100;
}
#endregion


function scr_acir_player_defense(_my_enemy, _player, _toten){
	if(is_created == true){
		//Escolhe o totem;
		sprite_index = _toten;
		
		//Pegando  direção do totem
		my_direction = _player.player_direction;
		
		//Escolhe a quantidade de vida
		life = 1;
		
		//Diminuindo o damanho do toten
		image_xscale = 2.5;
		image_yscale = 2.5;
		
		//Não deixando ele loopar esse evento
		is_created = false;
	}

	if(place_meeting(x, y + ver_speed, colision_array)){
		while(!place_meeting(x, y + sign(ver_speed), colision_array)){
			y += sign(ver_speed);
		}
			ver_speed = 0;
	}
	
	y += ver_speed;

	//Para o inimigo pular na cabeça do totem
	var _broken_toten = instance_place(x ,y + 14 , _my_enemy);

	if(_broken_toten && _my_enemy.state == "Fall" && life = 1){
		_my_enemy.state = "Jump";
		_my_enemy.ver_speed = -7;
		life = 0;
	}
	
	//Para o jogador pular na cabeça do totem
	var _jump_toten = instance_place(x ,y + 14 , _player);

	if(_jump_toten && _player.state == "Fall" && life = 1){
		_player.state = "Jump";
		_player.ver_speed = -7;
	}

	//Script do funcionamento das skills
	if (timer < 300){
		timer++;
	
		switch(toten){
			case spr_acir_defense1:
			_player.high_jump = true;
				if(_player.jump && can_jump == 0){
					_player.ver_speed = -8.5;
					can_jump = 1;
				}
					
				if(place_meeting(_player.x, _player.y + 1, colision_array)){
					can_jump = 0;
				}
			break;
			
			case spr_acir_defense2:
				_player.max_speed = 6.5;
				_player.fast = true
				
			break;
			
			case spr_acir_defense3:
				_player.invincibility = true;
				_player.slow = true
				
				if(_player.alarm[1] = -1){
					alarm[1] = 300;
				}
				
				
				if(_player.jump && can_jump == 0){
					_player.ver_speed = -6.5;
					can_jump = 1;
				}
					
				if(place_meeting(_player.x, _player.y + 1, colision_array)){
					can_jump = 0;
				}
				
				_player.max_speed = 4.2;
			break;
		}
	} else { //Caso tempo encerre 
		life = 0;
	}
	
	if(life == 0){
		//Animação de morte do totem;
		switch(toten){
			case spr_acir_defense1:
				sprite_index = spr_acir_defense1_1
			break;
			
			case spr_acir_defense2:
				sprite_index = spr_acir_defense2_2
			break;
			
			case spr_acir_defense3:
				sprite_index = spr_acir_defense3_3
				
			break;
		}
	
		if(image_index >= image_number-1){
			instance_destroy()
		}
	
		//Retorna as variaveis base;
		_player.invincibility = false;
		_player.slow = false;
		_player.fast = false;
		_player.high_jump = false;
		
		if(_player.jump && place_meeting(_player.x, _player.y, colision_array)){
			_player.ver_speed = -7;
			
		}
	
		_player.max_speed = 5;
	}
}
#endregion

#region //Defesa do Lucas
function scr_lucas_player_defense(_my_enemy, _player){
	/* A ideia da defesa é um dash que é capaz de ficar invencível durante o tempo desse dash
	, fazendo com que ele tenha bastante mobilidade e que consigar criar jogadas com isso. */
	if(is_created == true){
		_player.move_r = true;
		_player.invincibility = true;
		_player.fast = true;
		_player.alarm[1] = 60;
		//Tempo do dash
		timer = 0;
		is_created = false;
	}
	
	timer++;
	
	with(instance_create_layer(_player.x, _player.y, "Skills", obj_ghost)){
		var _ghost = obj_ghost;
		_ghost.sprite_index = _player.sprite_index;
		_ghost.image_xscale = _player.image_xscale;
		_ghost.image_yscale = _player.image_yscale;
		_ghost.image_blend = c_blue;
		_ghost.image_alpha = 0.3;
		_ghost.image_speed = 0;
	}
	
	//ganha velocidade dependendo da direção
	if(_player.player_direction > 0){
		_player.hor_speed = 15;
	} else if(_player.player_direction < 0){
		_player.hor_speed = -15;
	}
	
	_player.ver_speed = 0;
	
	//Se o timer for maior/igual a 10 ou encostar com uma parede em x destroi
	if(timer >= 10 || place_meeting(x + _player.hor_speed, y, obj_colision)){
		_player.move_r = false;
		_player.fast = false;
		_player.invincibility = false;
		instance_destroy();
	}
}
#endregion 

#region //Defesa da Naja
function scr_naja_player_defense(_my_enemy, _player){
    /* A ideia da defesa da */
    if(is_created == true){
        timer = 0;
        _player.max_speed = 12;
        _player.transformed = true;
		_player.fast = true;
		
        //Lockando o evento "Create"
        is_created = false;
    }

    timer++;

    _player.sprite_index = spr_naja_defense1;

    if(_player.image_index >= _player.image_number-1){
        _player.image_index = _player.image_number-1;
    }

    if(timer >= 60){
        _player.sprite_index = spr_naja_defense2;

        if(_player.image_index >= _player.image_number-1){
            _player.max_speed = 5;
            _player.transformed = false;
			_player.fast= false;
            instance_destroy();
        }
    }
}
#endregion
```

### 3. Autores
Felipe Pereira da Silva

Vulgo FlpGamess.
