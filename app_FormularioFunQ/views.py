from django.shortcuts import render, redirect, get_object_or_404
from .models import Aluno, RespostaFormulario

import os
import csv
from django.http import FileResponse, HttpResponse
from django.contrib.admin.views.decorators import staff_member_required
from django.conf import settings


# Create your views here.
def PaginaFormulario(request):
    return render(request,'PagFormulario/formulario.html')

def PaginaLogin(request):
    return render(request, 'PagLogin/login.html')

def PaginaAgradecimentos(request):
    return render(request, 'PagAgradecimentos/agradecimentos.html')

def PaginaInicial(request):
    return render(request, 'PagInicial/inicio.html')

def PaginaSobre(request):
    return render(request, 'PagInicial/sobre.html')

def PaginaEquipe(request):
    return render(request, 'PagInicial/equipe.html')

def PaginaIFRN(request):
    return render(request, 'PagInicial/ifrn.html')



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

        nova_resposta.q19_opiniao_atividade = request.POST.get('q19_opiniao_atividade')
        nova_resposta.q20_sentimento_jogo = request.POST.get('q20_sentimento_jogo')
        nova_resposta.q21_compreensao_conceitos = request.POST.get('q21_compreensao_conceitos')
        nova_resposta.q22_fator_interesse = request.POST.get('q22_fator_interesse')
        nova_resposta.q23_pontos_negativos = request.POST.get('q23_pontos_negativos')
        nova_resposta.q24_sugestoes_mudanca = request.POST.get('q24_sugestoes_mudanca')

        nova_resposta.save()

        # Limpa a sessão após salvar com sucesso
        request.session.pop('id_aluno', None)

        return redirect('PaginaAgradecimentos')



@staff_member_required
def exportar_csv_respostas(request):
    response = HttpResponse(content_type='text/csv; charset=utf-8-sig')
    response['Content-Disposition'] = 'attachment; filename="Respostas_FunQ_Alunos.csv"'

    writer = csv.writer(response, delimiter=';')

    # Cabeçalho do CSV
    cabecalho = [
        'ID',
        'Nome do Aluno',
        'Grupo de Teste',
        'Pesquisador',
        # Questões objetivas (q1 a q18)
        'q1', 'q2', 'q3', 'q4', 'q5', 'q6', 'q7', 'q8', 'q9',
        'q10', 'q11', 'q12', 'q13', 'q14', 'q15', 'q16', 'q17', 'q18',
        # Questões abertas (q19 a q24)
        'q19_opiniao_atividade',
        'q20_sentimento_jogo',
        'q21_compreensao_conceitos',
        'q22_fator_interesse',
        'q23_pontos_negativos',
        'q24_sugestoes_mudanca'
    ]
    writer.writerow(cabecalho)

    respostas = RespostaFormulario.objects.select_related('aluno').all().order_by('id')

    for r in respostas:
        # Pega o nome do aluno ou salva como N/A se não houver aluno associado
        nome_aluno = r.aluno.nome if (r.aluno and hasattr(r.aluno, 'nome')) else str(r.aluno) if r.aluno else 'N/A'

        linha = [
            r.id,
            nome_aluno,
            r.grupo or '',
            r.pesquisador or '',
            # Valores de q1 a q18
            r.q1, r.q2, r.q3, r.q4, r.q5, r.q6, r.q7, r.q8, r.q9,
            r.q10, r.q11, r.q12, r.q13, r.q14, r.q15, r.q16, r.q17, r.q18,
            # Respostas das questões abertas
            r.q19_opiniao_atividade or '',
            r.q20_sentimento_jogo or '',
            r.q21_compreensao_conceitos or '',
            r.q22_fator_interesse or '',
            r.q23_pontos_negativos or '',
            r.q24_sugestoes_mudanca or ''
        ]
        writer.writerow(linha)

    return response


@staff_member_required
def exportar_pdf_formulario(request):
    # Caminho exato onde o PDF estático está salvo
    caminho_pdf = os.path.join(settings.BASE_DIR, 'app_FormularioFunQ', 'static', 'pdf', 'Questionario_FunQ_Fisico.pdf')
    
    if os.path.exists(caminho_pdf):
        # O FileResponse entrega o arquivo com baixo consumo de memória
        return FileResponse(open(caminho_pdf, 'rb'), as_attachment=True, filename='Formulario_FunQ.pdf')
    
    raise Http404("Arquivo PDF não encontrado no servidor.")