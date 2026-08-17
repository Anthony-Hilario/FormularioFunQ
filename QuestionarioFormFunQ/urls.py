from django.urls import path
from app_FormularioFunQ import views

urlpatterns = [
    path('home/', views.PaginaFormulario, name='PaginaFormulario'),
    path('', views.PaginaInicial, name='PaginaInicial'),
    path('login/', views.PaginaLogin, name='PaginaLogin'),
    path('agradecimentos/', views.PaginaAgradecimentos, name='PaginaAgradecimentos'),
    path('respostas/', views.Respostas, name='listagem_respostas'),
    path('alunos/', views.Alunos, name='listagem_alunos'),
]
