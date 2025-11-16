from django.shortcuts import render
from django.http import HttpResponse
from .models import MainMenu
from .forms import BookForm
from django.http import HttpResponseRedirect
from .models import Book
from .forms import RatingForm
from .models import Rating

from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.db.models import Avg, Count
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect








# Create your views here.
def index(request):
    return render(request,
                  'bookMng/index.html',
                  {
                      'item_list': MainMenu.objects.all()
                  })


def postbook(request):
    submitted = False
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            #form.save()
            book = form.save(commit=False)
            try:
                book.username = request.user
            except Exception:
                pass
            book.save()
            return HttpResponseRedirect('/postbook?submitted=True')
    else:
        form = BookForm()
        if 'submitted' in request.GET:
            submitted = True
    return render(request,
                  'bookMng/postbook.html',
                  {
                      'form': form,
                      'item_list': MainMenu.objects.all(),
                      'submitted': submitted
                  })

def displaybooks(request):
    # annotate each Book with its average rating and rating count
    books = Book.objects.all().annotate(
        avg_rating=Avg('rating__value'),
        rating_count=Count('rating')
    )
    for b in books:
        b.pic_path = b.picture.url[14:]
    return render(request,
                  'bookMng/displaybooks.html',
                  {
                      'item_list': MainMenu.objects.all(),
                      'books': books
                  })


def search_books(request):
    """Search books by name (case-insensitive). If the query is empty or
    no matches are found, the page will render with no books shown.
    """
    q = request.GET.get('q', '')
    q = q.strip()
    if q:
        books = Book.objects.filter(name__icontains=q).annotate(
            avg_rating=Avg('rating__value'),
            rating_count=Count('rating')
        )
        for b in books:
            b.pic_path = b.picture.url[14:]
    else:
        # Empty query => show no results (user asked for nothing to appear)
        books = Book.objects.none()

    return render(request, 'bookMng/displaybooks.html', {
        'item_list': MainMenu.objects.all(),
        'books': books,
        'search_query': q,
    })


class Register(CreateView):
    template_name = 'registration/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('register-success')

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(self.success_url)

def book_detail(request, book_id):
        book = Book.objects.get(id=book_id)

        book.pic_path = book.picture.url[14:]
        return render(request,
                      'bookMng/book_detail.html',
                      {
                          'item_list': MainMenu.objects.all(),
                          'book': book
                      })

def mybooks(request):
    # If user is not authenticated, don't query or process books — template
    # will show a login prompt. This avoids errors when accessing file URLs.
    if not request.user.is_authenticated:
        return render(request,
                      'bookMng/mybooks.html',
                      {
                          'item_list': MainMenu.objects.all(),
                          'books': Book.objects.none()
                      })

    books = Book.objects.filter(username=request.user)
    for b in books:
        # defensive: some Book instances may not have an uploaded file
        try:
            b.pic_path = b.picture.url[14:]
        except Exception:
            b.pic_path = ''

    return render(request,
                  'bookMng/mybooks.html',
                  {
                      'item_list': MainMenu.objects.all(),
                      'books': books
                  })
def book_delete(request, book_id):
    book = Book.objects.get(id=book_id)
    book.delete()

    return render(request,
                  'bookMng/book_delete.html',
                  {
                      'item_list': MainMenu.objects.all(),
                  })


def about(request):
    """Simple About Us page."""
    return render(request, 'bookMng/about.html', {
        'item_list': MainMenu.objects.all()
    })


def person_profile(request, slug):
    """Render a simple person profile page based on slug.

    Currently this uses a small in-memory map for content. For a
    production app you would store people in the database.
    """
    people = {
        'hector-corona': {
            'name': 'Hector Corona',
            'title': 'Software Developer',
            'bio': 'Hector is a student and developer working on web applications. He enjoys building Django projects and learning UI/UX design.',
            'photo': 'uploads/hector.jpg'
        }
    }
    # Add more people by adding new slug keys here. Example:
    people['kevin-luo'] = {
        'name': 'Kevin Luo',
        'title': 'Data Scientist',
        'bio': 'Kevin works on data engineering and machine learning pipelines. He enjoys visualizing data and building analytics tools.',
        'photo': 'uploads/kevin.jpg'
    }
    people['esmeralda-amado'] = {
        'name': 'Esmeralda Amado',
        'title': 'Software Developer',
        'bio': 'Esmeralda is a student and developer working on web applications. She likes long walks on the beach with her computer to code.',
        'photo': 'uploads/esmeralda.jpg'
    }
    people['evelyn-muneton'] = {
        'name': 'Evelyn Muneton',
        'title': 'Software Developer',
        'bio': 'Evelyn likes to develop and code super hard.',
        'photo': 'uploads/evelyn.jpg'
    }
    people['raquel-alvarado'] = {
        'name': 'Raquel Alvarado',
        'title': 'Software Developer',
        'bio': 'Raquel has a passion for complex data structures.',
        'photo': 'uploads/raquel.jpg'
    }
    people['brian-gonzales'] = {
        'name': 'Brian Gonzales',
        'title': '???',
        'bio': '???',
        'photo': 'uploads/brian.jpg'
    }

    person = people.get(slug)
    if not person:
        # simple 404
        from django.http import Http404
        raise Http404('Person not found')

    return render(request, 'bookMng/person.html', {
        'item_list': MainMenu.objects.all(),
        'person': person
    })

@login_required
def book_rating(request, book_id):
    book = Book.objects.get(id=book_id)
    # Prevent users from rating their own book
    if book.username and book.username == request.user:
        messages.error(request, "You cannot rate your own book.")
        return redirect('displaybooks')
    submitted = False

    # Check if the user has rated this book before
    existing_rating = Rating.objects.filter(book=book, user=request.user).first()

    if request.method == 'POST':
        form = RatingForm(request.POST, instance=existing_rating)
        if form.is_valid():
            rating = form.save(commit=False)
            rating.book = book
            rating.user = request.user
            rating.save()
            # use messages and redirect back to the display page so users see the updated average
            messages.success(request, 'Your rating has been saved.')
            return redirect('displaybooks')
    else:
        form = RatingForm(instance=existing_rating)

    return render(request, 'bookMng/book_rating.html', {
        'book': book,
        'form': form,
        'submitted': submitted,
        'item_list': MainMenu.objects.all()
    })