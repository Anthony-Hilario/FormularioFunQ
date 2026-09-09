from django.db import models

# Create your models here.
class Aluno(models.Model):
    nome = models.CharField(max_length=255)
    idade = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.nome} ({self.idade} anos)"


class RespostaFormulario(models.Model):
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)

    grupo = models.CharField(max_length=100, blank=True, null=True, verbose_name="Grupo de Teste")
    pesquisador = models.CharField(max_length=100, blank=True, null=True, verbose_name="Pesquisador")

    q1 = models.PositiveSmallIntegerField()
    q2 = models.PositiveSmallIntegerField()
    q3 = models.PositiveSmallIntegerField()
    q4 = models.PositiveSmallIntegerField()
    q5 = models.PositiveSmallIntegerField()
    q6 = models.PositiveSmallIntegerField()
    q7 = models.PositiveSmallIntegerField()
    q8 = models.PositiveSmallIntegerField()
    q9 = models.PositiveSmallIntegerField()
    q10 = models.PositiveSmallIntegerField()
    q11 = models.PositiveSmallIntegerField()
    q12 = models.PositiveSmallIntegerField()
    q13 = models.PositiveSmallIntegerField()
    q14 = models.PositiveSmallIntegerField()
    q15 = models.PositiveSmallIntegerField()
    q16 = models.PositiveSmallIntegerField()
    q17 = models.PositiveSmallIntegerField()
    q18 = models.PositiveSmallIntegerField()

    q19_opiniao_atividade = models.TextField(blank=True, null=True)
    q20_sentimento_jogo = models.TextField(blank=True, null=True)
    q21_compreensao_conceitos = models.TextField(blank=True, null=True)
    q22_fator_interesse = models.TextField(blank=True, null=True)
    q23_pontos_negativos = models.TextField(blank=True, null=True)
    q24_sugestoes_mudanca = models.TextField(blank=True, null=True)