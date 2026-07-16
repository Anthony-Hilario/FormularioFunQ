from django.shortcuts import render

# Create your views here.
def PaginaFormulario(request):
    return render(request,'PagFormulario/formulario.html')