function ExibeSenha() {
    var x = document.getElementById("senha");
    if (x.type === "password") {
      x.type = "text";
    } else {
      x.type = "password";
    }
  }

  function mostrarImagem(event) {
    const preview = document.getElementById('preview');
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            preview.src = e.target.result;
            preview.style.display = "block";
        };
        reader.readAsDataURL(file);
    }
}


  function mostrarEvento(id) {
    const eventos = document.querySelectorAll('.evento-card');
    eventos.forEach(evento => {
      if (evento.id !== 'evento-' + id) {
        evento.style.display = 'none';
      } else {
        evento.classList.add('evento-detalhado');
        const detalhes = evento.querySelector('.card-footer');
        if (detalhes) detalhes.classList.add('show');
      }
    });
  }

  function voltarLista() {
    const eventos = document.querySelectorAll('.evento-card');
    eventos.forEach(evento => {
      evento.style.display = 'block';
      evento.classList.remove('evento-detalhado');
      const detalhes = evento.querySelector('.card-footer');
      if (detalhes) detalhes.classList.remove('show');
    });
  }


document.getElementById('formEvento').addEventListener('submit', function(event) {
  event.preventDefault(); // Evita o envio padrão do formulário
  enviarConteudo(); // Chama a função desejada
});

function validarEnvio() {
  let inputFile = document.getElementById("fileInput");
  let aviso = document.getElementById("aviso");

  if (inputFile.files.length === 0) {
      aviso.innerText = "Por favor, selecione uma imagem antes de enviar!";
      aviso.style.color = "red";
      return false;
  } else {
      aviso.innerText = "";
      return true;
  }
}

function toggleDetalhes(card) {
    const detalhes = card.querySelector('.detalhes');
    detalhes.classList.toggle('mostrar');
    detalhes.classList.toggle('oculto');
}