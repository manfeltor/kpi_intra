from django.shortcuts import render

def gerencia_main_WH(req):

    if req.user.groups.filter(name='management').exists():

        "1"

    
    else:
        
        return render(req, "landing.html")