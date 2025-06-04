function ExibeSenha() {
    var senhaInput = document.getElementById('senhaForm');
    var btnToggle = document.getElementById('toggleSenha');

    // Verificações para depuração (verifique o console do navegador)
    if (!senhaInput) {
        console.error("Erro: Campo de senha com ID 'senhaForm' não foi encontrado!");
        return; // Para a execução se o campo não for achado
    }
    if (!btnToggle) {
        console.error("Erro: Botão com ID 'toggleSenha' não foi encontrado!");
        return; // Para a execução se o botão não for achado
    }

    var olhoAberto = btnToggle.querySelector('.bi-eye-fill');
    var olhoFechado = btnToggle.querySelector('.bi-eye-slash-fill');

    if (!olhoAberto) {
        console.warn("Aviso: Ícone 'olhoAberto' (classe '.bi-eye-fill') não encontrado dentro do botão.");
    }
    if (!olhoFechado) {
        console.warn("Aviso: Ícone 'olhoFechado' (classe '.bi-eye-slash-fill') não encontrado dentro do botão.");
    }

    // Lógica principal
    if (senhaInput.type === 'password') {
        senhaInput.type = 'text';
        if (olhoAberto) olhoAberto.style.display = 'none';
        if (olhoFechado) olhoFechado.style.display = 'inline-block';
    } else {
        senhaInput.type = 'password';
        if (olhoAberto) olhoAberto.style.display = 'inline-block';
        if (olhoFechado) olhoFechado.style.display = 'none';
    }
}


function ExibeSenhaRegistro() {
    var senhaInput = document.getElementById('senhaFormRegistro');
    var btnToggle = document.getElementById('toggleSenhaRegistro');
    var olhoAberto = btnToggle.querySelector('.bi-eye-fill');
    var olhoFechado = btnToggle.querySelector('.bi-eye-slash-fill');

    if (!senhaInput || !btnToggle || !olhoAberto || !olhoFechado) return;

    if (senhaInput.type === 'password') {
        senhaInput.type = 'text';
        olhoAberto.style.display = 'none';
        olhoFechado.style.display = 'inline-block';
    } else {
        senhaInput.type = 'password';
        olhoAberto.style.display = 'inline-block';
        olhoFechado.style.display = 'none';
    }
}

function ExibeConfirmarSenha() {
    var senhaInput = document.getElementById('confirmarSenhaForm');
    var btnToggle = document.getElementById('toggleConfirmarSenha');
    var olhoAberto = btnToggle.querySelector('.bi-eye-fill');
    var olhoFechado = btnToggle.querySelector('.bi-eye-slash-fill');

    if (!senhaInput || !btnToggle || !olhoAberto || !olhoFechado) return;

    if (senhaInput.type === 'password') {
        senhaInput.type = 'text';
        olhoAberto.style.display = 'none';
        olhoFechado.style.display = 'inline-block';
    } else {
        senhaInput.type = 'password';
        olhoAberto.style.display = 'inline-block';
        olhoFechado.style.display = 'none';
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

function toggleLocalizacaoEvento() {
    const tipoForm = document.getElementById("tipoForm");
    const localizacaoContainer = document.getElementById("localizacaoContainer");
    const linkForm = document.getElementById("linkContainer")

    function toggle() {
        if (tipoForm.value === "Presencial") {
            localizacaoContainer.style.display = "block";
            linkForm.style.display = "none"
        } 
        else if (tipoForm.value === "Online"){
            localizacaoContainer.style.display = "none";
            linkForm.style.display = "block"
            document.getElementById("localizacaoForm").value = "";
        }
    }

    toggle(); // executa ao carregar
    tipoForm.addEventListener("change", toggle); // executa ao mudar
}

// Script para controlar o scroll do carrossel horizontal
document.addEventListener('DOMContentLoaded', () => {
    const carousel = document.getElementById('carouselFavoritos');
    const prevBtn = document.getElementById('prevBtn');
    const nextBtn = document.getElementById('nextBtn');

    const scrollAmount = 280; 

    if (carousel && prevBtn && nextBtn) {
        prevBtn.addEventListener('click', () => {
            carousel.scrollBy({ left: -scrollAmount, behavior: 'smooth' });
        });

        nextBtn.addEventListener('click', () => {
            carousel.scrollBy({ left: scrollAmount, behavior: 'smooth' });
        });
    }
});