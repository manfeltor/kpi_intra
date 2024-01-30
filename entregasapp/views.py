from django.shortcuts import render

# Create your views here.

def render_main(req):

    return render(req, "entregasmain.html")
