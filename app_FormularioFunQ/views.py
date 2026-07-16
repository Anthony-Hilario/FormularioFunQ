from django.shortcuts import render

# Create your views here.
def PaginaFormulario(request):
    return render(request,'PagFormulario/formulario.html')

def PaginaLogin(request):
    return render(request, 'PagLogin/login.html')