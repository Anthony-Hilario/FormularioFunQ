from django.shortcuts import render, redirect, get_object_or_404
from .models import Aluno, RespostaFormulario

import io
import csv
from django.http import FileResponse, HttpResponse
from django.contrib.admin.views.decorators import staff_member_required
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

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
def gerar_pdf_questionario(request):
    buffer = io.BytesIO()
    
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )
    
    story = []
    styles = getSampleStyleSheet()

    # Estilos
    titulo_style = ParagraphStyle(
        'TituloPDF',
        parent=styles['Heading1'],
        fontSize=15,
        leading=18,
        alignment=1,
        textColor=colors.HexColor('#10b981'),
        spaceAfter=8
    )
    
    subtitulo_style = ParagraphStyle(
        'SubtituloPDF',
        parent=styles['Normal'],
        fontSize=9,
        leading=12,
        alignment=1,
        textColor=colors.HexColor('#64748b'),
        spaceAfter=15
    )

    pergunta_style = ParagraphStyle(
        'TextoPergunta',
        parent=styles['Normal'],
        fontSize=9.5,
        leading=13,
        textColor=colors.HexColor('#1e293b')
    )

    # 1. Cabeçalho
    story.append(Paragraph("<b>Questionário de Avaliação FunQ</b>", titulo_style))
    story.append(Paragraph("Responda às questões de 1 a 18 marcando uma nota de 1 a 5, e responda as questões abertas nas linhas indicadas.", subtitulo_style))
    story.append(Spacer(1, 5))

    # 2. Dados de Identificação do Aluno / Pesquisa
    dados_identificacao = [
        [Paragraph("<b>Nome do Aluno:</b> __________________________________________________", styles['Normal'])],
        [Paragraph("<b>Turma/Série:</b> __________________ &nbsp;&nbsp; <b>Grupo:</b> __________________", styles['Normal'])],
        [Paragraph("<b>Pesquisador:</b> ___________________ &nbsp;&nbsp; <b>Data:</b> ____/____/________", styles['Normal'])]
    ]
    tabela_id = Table(dados_identificacao, colWidths=[520])
    tabela_id.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(tabela_id)
    story.append(Spacer(1, 10))

    # 3. Lista de perguntas objetivas (q1 a q18) — Idênticas ao HTML
    perguntas_objetivas = [
        "Eu pude opinar sobre o que fazer.",                       # q1
        "Eu pude decidir como fazer as coisas.",                  # q2
        "Senti-me livre para fazer as coisas do meu jeito.",       # q3
        "A atividade foi fácil demais para mim.",                  # q4
        "A atividade foi difícil demais para mim.",                 # q5
        "Senti que os desafios eram adequados para mim.",         # q6
        "Eu me diverti.",                                         # q7
        "Eu gostei da atividade.",                                # q8
        "Eu gostaria de fazer essa atividade novamente.",          # q9
        "Esqueci de tudo ao meu redor.",                          # q10
        "Perdi a noção do tempo.",                                # q11
        "Eu estava totalmente focado na atividade.",              # q12
        "Senti-me parte do grupo.",                               # q13
        "Senti-me confortável com os outros.",                    # q14
        "Senti que podia ser eu mesmo.",                          # q15
        "Senti-me estressado(a).",                                # q16
        "Senti-me frustrado(a).",                                 # q17
        "Senti-me entediado(a)."                                  # q18
    ]

    # Renderiza tabela para as questões 1 a 18
    for idx, texto_pergunta in enumerate(perguntas_objetivas, 1):
        texto_p = f"<b>{idx}.</b> {texto_pergunta}"
        linha = [
            Paragraph(texto_p, pergunta_style),
            Paragraph("( ) 1 &nbsp; ( ) 2 &nbsp; ( ) 3 &nbsp; ( ) 4 &nbsp; ( ) 5", styles['Normal'])
        ]
        t = Table([linha], colWidths=[360, 160])
        t.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LINEBELOW', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
            ('TOPPADDING', (0, 0), (-1, -1), 3),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ]))
        story.append(t)

    story.append(Spacer(1, 10))

    # 4. Lista de perguntas abertas / discursivas (q19 a q24) — Idênticas ao HTML
    perguntas_discursivas = [
        "19. O que você achou da atividade realizada?",
        "20. Como você se sentiu durante a realização do jogo?",
        "21. Você acredita que o jogo ajudou na compreensão dos conceitos trabalhados?",
        "22. O que fez você permanecer interessado na atividade?",
        "23. O que você menos gostou na atividade?",
        "24. O que você mudaria no jogo?"
    ]

    for q_texto in perguntas_discursivas:
        story.append(Paragraph(f"<b>{q_texto}</b>", pergunta_style))
        story.append(Spacer(1, 3))
        # Linhas pontilhadas para o aluno responder a lápis/caneta no PDF
        linhas_resposta = [
            [Paragraph("__________________________________________________________________________________", styles['Normal'])],
            [Paragraph("__________________________________________________________________________________", styles['Normal'])]
        ]
        t_linhas = Table(linhas_resposta, colWidths=[520])
        t_linhas.setStyle(TableStyle([
            ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
        ]))
        story.append(t_linhas)
        story.append(Spacer(1, 6))

    doc.build(story)
    buffer.seek(0)
    
    return FileResponse(buffer, as_attachment=True, filename='Questionario_FunQ_Fisico.pdf')


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