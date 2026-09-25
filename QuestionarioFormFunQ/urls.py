from django.urls import path
from django.contrib import admin
from app_FormularioFunQ import views

urlpatterns = [
    path('home/', views.PaginaFormulario, name='PaginaFormulario'),
    path('', views.PaginaInicial, name='PaginaInicial'),
    path('login/', views.PaginaLogin, name='PaginaLogin'),
    path('agradecimentos/', views.PaginaAgradecimentos, name='PaginaAgradecimentos'),
    path('respostas/', views.Respostas, name='listagem_respostas'),
    path('alunos/', views.Alunos, name='listagem_alunos'),
    path('sobre/', views.PaginaSobre, name='PaginaSobre'),
    path('equipe/', views.PaginaEquipe, name='PaginaEquipe'),
    path('ifrn/', views.PaginaIFRN, name='PaginaIFRN'),
    path('admin/', admin.site.urls),
    path('admin-painel/exportar-pdf/', views.gerar_pdf_questionario, name='gerar_pdf_questionario'),
    path('admin-painel/exportar-csv/', views.exportar_csv_respostas, name='exportar_csv_respostas'),
]
