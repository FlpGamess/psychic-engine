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