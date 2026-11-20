
let token = null;
let pacientes = [];
let medicos = [];
let consultas = [];
let especialidades = [];

const $ = id => document.getElementById(id);

function mostrarAlerta(mensagem, tipo = "success") {
    const alerta = $("alerta");
    alerta.textContent = mensagem;
    alerta.className = `alert alert-${tipo}`;
}

async function api(url, options = {}) {
    const headers = {
        ...options.headers
    };

    if (token) {
        headers.Authorization = `Bearer ${token}`;
    }

    if (options.body && !(options.body instanceof FormData)) {
        headers["Content-Type"] = "application/json";
    }

    const resposta = await fetch(url, {
        ...options,
        headers
    });

    if (resposta.status === 401) {
        logout();
        throw new Error("Sessão expirada. Faça login novamente.");
    }

    const dados = await resposta.json();

    if (!resposta.ok) {
        throw new Error(
            typeof dados.detail === "string"
                ? dados.detail
                : "Erro ao realizar operação."
        );
    }

    return dados;
}

$("loginForm").addEventListener("submit", async event => {
    event.preventDefault();

    const form = new URLSearchParams();
    form.append("username", $("email").value);
    form.append("password", $("senha").value);

    try {
        $("loginError").textContent = "";

        const resposta = await fetch("/auth/login", {
            method: "POST",
            body: form
        });

        const dados = await resposta.json();

        if (!resposta.ok) {
            throw new Error("E-mail ou senha inválidos.");
        }

        token = dados.access_token;

        const usuario = await api("/auth/me");

        $("usuarioNome").textContent = usuario.nome;
        $("loginScreen").classList.add("d-none");
        $("appScreen").classList.remove("d-none");

        await carregarDados();
    } catch (erro) {
        $("loginError").textContent = erro.message;
    }
});

function logout() {
    token = null;
    $("appScreen").classList.add("d-none");
    $("loginScreen").classList.remove("d-none");
    $("senha").value = "";
}

function mostrarSecao(secao) {
    document.querySelectorAll(".page-section").forEach(elemento => {
        elemento.classList.add("d-none");
    });

    $(secao).classList.remove("d-none");

    $("pageTitle").textContent =
        secao.charAt(0).toUpperCase() + secao.slice(1);
}

async function carregarDados() {
    try {
        [pacientes, medicos, consultas, especialidades] =
            await Promise.all([
                api("/pacientes/"),
                api("/medicos/"),
                api("/consultas/"),
                api("/medicos/especialidades")
            ]);

        $("totalPacientes").textContent = pacientes.length;
        $("totalMedicos").textContent = medicos.length;
        $("totalConsultas").textContent =
            consultas.filter(c => c.status === "agendada").length;

        renderizarPacientes();
        renderizarMedicos();
        renderizarConsultas();
        carregarSeletores();
    } catch (erro) {
        mostrarAlerta(erro.message, "danger");
    }
}

function criarCelula(linha, valor) {
    const td = document.createElement("td");
    td.textContent = valor ?? "-";
    linha.appendChild(td);
}

function renderizarPacientes() {
    const tabela = $("tabelaPacientes");
    tabela.replaceChildren();

    pacientes.forEach(p => {
        const linha = document.createElement("tr");
        [p.id, p.nome, p.cpf, p.telefone].forEach(
            valor => criarCelula(linha, valor)
        );
        tabela.appendChild(linha);
    });
}

function renderizarMedicos() {
    const tabela = $("tabelaMedicos");
    tabela.replaceChildren();

    medicos.forEach(m => {
        const especialidade = especialidades.find(
            e => e.id === m.especialidade_id
        );

        const linha = document.createElement("tr");

        [
            m.id,
            m.nome,
            m.crm,
            especialidade?.nome ?? "Não informada"
        ].forEach(valor => criarCelula(linha, valor));

        tabela.appendChild(linha);
    });
}

function renderizarConsultas() {
    const tabela = $("tabelaConsultas");
    tabela.replaceChildren();

    consultas.forEach(c => {
        const paciente = pacientes.find(p => p.id === c.paciente_id);
        const medico = medicos.find(m => m.id === c.medico_id);

        const linha = document.createElement("tr");

        [
            c.id,
            paciente?.nome ?? "Paciente não encontrado",
            medico?.nome ?? "Médico não encontrado",
            new Date(c.data_hora).toLocaleString("pt-BR"),
            c.status
        ].forEach(valor => criarCelula(linha, valor));

        tabela.appendChild(linha);
    });
}

function preencherSelect(id, itens) {
    const select = $(id);
    select.replaceChildren();

    itens.forEach(item => {
        const option = document.createElement("option");
        option.value = item.id;
        option.textContent = item.nome;
        select.appendChild(option);
    });
}

function carregarSeletores() {
    preencherSelect("consultaPaciente", pacientes);
    preencherSelect("consultaMedico", medicos);
}

$("formPaciente").addEventListener("submit", async event => {
    event.preventDefault();

    const dados = {
        nome: $("pacienteNome").value,
        cpf: $("pacienteCpf").value,
        data_nascimento: $("pacienteNascimento").value,
        telefone: $("pacienteTelefone").value || null,
        email: $("pacienteEmail").value || null,
        alergias: $("pacienteAlergias").value || null
    };

    try {
        await api("/pacientes/", {
            method: "POST",
            body: JSON.stringify(dados)
        });

        bootstrap.Modal.getInstance($("modalPaciente")).hide();
        $("formPaciente").reset();

        await carregarDados();
        mostrarAlerta("Paciente cadastrado com sucesso.");
    } catch (erro) {
        mostrarAlerta(erro.message, "danger");
        alert(erro.message);
    }
});

$("formConsulta").addEventListener("submit", async event => {
    event.preventDefault();

    const dados = {
        paciente_id: Number($("consultaPaciente").value),
        medico_id: Number($("consultaMedico").value),
        data_hora: $("consultaData").value,
        observacoes: $("consultaObservacoes").value || null
    };

    try {
        await api("/consultas/", {
            method: "POST",
            body: JSON.stringify(dados)
        });

        bootstrap.Modal.getInstance($("modalConsulta")).hide();
        $("formConsulta").reset();

        await carregarDados();
        mostrarAlerta("Consulta agendada com sucesso.");
    } catch (erro) {
        mostrarAlerta(erro.message, "danger");
        alert(erro.message);
    }
});
