from django.contrib import admin
from .models import Aluno, RespostaFormulario


@admin.register(Aluno)
class AlunoAdmin(admin.ModelAdmin):
    # Exibe o ID único e a idade na listagem
    list_display = ('id', 'idade')
    
    # Substituído 'nome' por busca por 'id' e 'idade'
    search_fields = ('id', 'idade')
    
    # Permite filtrar alunos por faixa etária na lateral
    list_filter = ('idade',)


@admin.register(RespostaFormulario)
class RespostaFormularioAdmin(admin.ModelAdmin):
    # Colunas que aparecerão na tabela de listagem do Admin
    list_display = ('id', 'aluno', 'grupo', 'pesquisador')

    # Aponta para o template customizado com o botão de download
    change_list_template = "admin/respostaformulario_change_list.html"

    # Filtros laterais para facilitar a análise dos dados no TCC
    list_filter = ('grupo', 'pesquisador', 'aluno__idade')

    # Busca por ID do aluno, idade, grupo ou pesquisador
    search_fields = ('aluno__id', 'aluno__idade', 'grupo', 'pesquisador')

    # Organização visual dos campos na tela de edição do registro
    fieldsets = (
        ('Informações da Pesquisa', {
            'fields': ('aluno', 'grupo', 'pesquisador')
        }),
        ('Questões Fechadas (Escala Likert q1 a q18)', {
            'classes': ('collapse',),  # Encolhido por padrão para não poluir a tela
            'fields': tuple(f'q{i}' for i in range(1, 19))
        }),
        ('Questões Abertas (q19 a q24)', {
            'fields': (
                'q19_opiniao_atividade',
                'q20_sentimento_jogo',
                'q21_compreensao_conceitos',
                'q22_fator_interesse',
                'q23_pontos_negativos',
                'q24_sugestoes_mudanca',
            )
        }),
    )