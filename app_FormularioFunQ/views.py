from django.shortcuts import render, redirect
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


def Respostas(request):

    id_aluno = request.session.get('id_aluno')

    aluno = Aluno.objects.get(id=id_aluno)

    nova_resposta = RespostaFormulario()
    nova_resposta.aluno = aluno

    for i in range(1, 19):
        setattr(nova_resposta, f'q{i}', request.POST.get(f'q{i}'))

    nova_resposta.save()

    request.session.pop('id_aluno', None)

    return redirect('PaginaAgradecimentos')