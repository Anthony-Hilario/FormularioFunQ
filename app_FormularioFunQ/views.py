from django.shortcuts import render, redirect, get_object_or_404
from .models import Aluno, RespostaFormulario

# Create your views here.
def PaginaFormulario(request):
    return render(request,'PagFormulario/formulario.html')

def PaginaLogin(request):
    return render(request, 'PagLogin/login.html')

def PaginaAgradecimentos(request):
    return render(request, 'PagAgradecimentos/agradecimentos.html')



def Alunos(request):
    #salvar os dados do aluno para o banco de dados
    novo_aluno = Aluno()
    novo_aluno.nome = request.POST.get('name')
    novo_aluno.idade = request.POST.get('age')
    novo_aluno.save()

    request.session['id_aluno'] = novo_aluno.id

    return redirect('PaginaFormulario')



QUESTOES_REVERSAS = {4, 5, 16, 17, 18}
ESCALA_MIN = 1
ESCALA_MAX = 5

def Respostas(request):
    if request.method == 'POST':
        id_aluno = request.session.get('id_aluno')
        if not id_aluno:
            return redirect('PaginaLogin')  # Redireciona se a sessão expirar

        aluno = get_object_or_404(Aluno, id=id_aluno)

        nova_resposta = RespostaFormulario()
        nova_resposta.aluno = aluno

        for i in range(1, 19):
            valor_str = request.POST.get(f'q{i}')

            if valor_str is not None and valor_str.isdigit():
                valor = int(valor_str)

                # Se a pergunta for invertida, aplica a fórmula de inversão
                if i in QUESTOES_REVERSAS:
                    valor = (ESCALA_MAX + ESCALA_MIN) - valor

                setattr(nova_resposta, f'q{i}', valor)
            else:
                setattr(nova_resposta, f'q{i}', None)

        nova_resposta.save()

        # Limpa a sessão após salvar com sucesso
        request.session.pop('id_aluno', None)

        return redirect('PaginaAgradecimentos')