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

    return redirect('PaginaFormulario')

def Respostas(request):
    nova_resposta = RespostaFormulario()

    for i in range(1, 19):
        setattr(nova_resposta, f'q{i}', request.POST.get(f'q{i}'))

    nova_resposta.save()

    return redirect('PaginaAgradecimentos')