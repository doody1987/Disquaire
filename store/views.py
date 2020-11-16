from django.shortcuts import render, get_object_or_404
from django import forms
from .models import Album, Artist, Contact, Booking
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def index(request):
    albums = Album.objects.filter(available = True).order_by('-created_at')[:12]
    context = {'albums': albums}
    return render(request, 'store/index.html', context)


def listing(request):
    album_list = Album.objects.filter(available=True)
    paginator = Paginator(album_list, 3)
    page = request.GET.get('page')
    try:
        albums = paginator.page(page)
    except PageNotAnInteger:
        albums = paginator.page(1)
    except EmptyPage:
        albums = paginator.page(paginator.num_pages)
    context = {
        'albums': albums,
        'paginate': True
    }
    return render(request, 'store/listing.html', context)

def detail(request, album_id):
    album = get_object_or_404(Album, pk= album_id)
    artists_name = " ".join([artist.name for artist in album.artists.all()])
    context = {
        'album_title': album.title,
        'artists_name': artists_name,
        'album_id': album.id,
        'thumbnail': album.photo.url,
    }
    return render(request, 'store/detail.html', context)




def search(request):
    query = request.GET.get('query')
    if not query:
        albums = Album.objects.all()
    else:
        albums = Album.objects.filter(title__icontains=query)

        if not albums.exists():
            albums = Album.objects.filter(artists__name__icontains=query)

    title = "Résultats pour la requete %s"%query
    context = {
        'albums': albums,
        'title': title,
    }
    return render(request, 'store/search.html', context)





class NouvAlb(forms.Form):
    title = forms.CharField()
    photo = forms.FileField()
    reference = forms.IntegerField()
    created_at = forms.DateTimeField()
    available = forms.BooleanField()

def nouv_alb(request):
    sauvegarde = False
    form = NouvAlb(request.POST or None, request.FILES)
    if form.is_valid():
        album = Album()
        album.title = form.cleaned_data["title"]
        album.photo = form.cleaned_data["photo"]
        album.reference = form.cleaned_data["reference"]
        album.created_at = form.cleaned_data["created_at"]
        album.available = form.cleaned_data["available"]
        album.save()
        sauvegarde = True

    return render(request, 'alb_form.html', {
        'form': form,
        'sauvegarde': sauvegarde
    })


def voir_albums(request):
    return render(
        request,
        'voir_album.html',
        {'albums': Album.objects.all()}
    )




