from django.shortcuts import render
from django.conf import settings
from pathlib import Path
from django.core.paginator import Paginator, EmptyPage

def index(request, subpath=""):
    base_path = Path(settings.MUSIC_ROOT)
    current_path = (base_path / subpath).resolve()

    if not str(current_path).startswith(str(Path(settings.MUSIC_ROOT))):
        return render(request, 'explorer/index.html', {"erro": "Acesso negado."})
    
    pastas = []
    musicas = []

    for item in sorted(current_path.iterdir()):
        if item.is_dir():
            pastas.append({
                'nome': item.name,
                'caminho': str(Path(subpath)/item.name).replace("\\", "/")
            })
        elif item.suffix.lower() == ".mp3":
            musicas.append({
                "nome": item.name,
                "caminho": str(Path(subpath) / item.name).replace("\\", "/")
            })

    #paginação
    page_f = request.GET.get("page_pasta", 1)
    paginator_f = Paginator(pastas, 10)

    try:
        pastas_page = paginator_f.page(page_f)
    except EmptyPage:
        pastas_page = paginator_f.page(paginator_f.num_pages)

    #Paginação de musicas
    page_m = request.GET.get("page_musica", 1)
    paginator_m = Paginator(musicas, 10)
    try:
        musicas_page = paginator_m.page(page_m)
    except EmptyPage:
        musicas_page = paginator_m.page(paginator_m.num_pages)

    pai = str(Path(subpath).parent) if subpath else None
    contexto = {
        "pastas": pastas_page,
        "musicas": musicas_page,
        "subpath": subpath,
        "voltar": pai if pai != subpath else None,
        "p_f": pastas_page,
        "p_m": musicas_page,
    }

    return render(request, 'explorer/index.html', contexto)