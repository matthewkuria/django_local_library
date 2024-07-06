from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic
from .models import Book, Author, BookInstance, Genre
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin

# Create a generic class based view
class BookListView(generic.ListView):
    model = Book
    paginate_by= 3
    context_object_name = 'book_list'   # your own name for the list as a template variable
    # queryset = Book.objects.filter(title__icontains='')[:5] # Get 5 books containing the title war
    template_name = 'books/my_arbitrary_template_name_list.html'  # Specify your own template name/location

class BookDetailView(generic.DetailView):
    model = Book


class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return (
            BookInstance.objects.filter(borrower=self.request.user)
            .filter(status__exact='o')
            .order_by('due_back')
        )
# Create a  generic class based view to show librarians the books borrowed
class BooksBorrowedListView(PermissionRequiredMixin,generic.ListView):
    permission_required = 'catalog.can_mark_returned'
    model = BookInstance
    paginate_by = 5
    context_object_name = 'borrowed_books'
    template_name = 'catalog/bookinstance_borrowed_books.html'


    def get_queryset(self):
        return(
            BookInstance.objects.all()
            .filter(status__exact='o')
            .order_by('due_back')

        )
# Create a generic class based view for the authors
class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 3
    context_object_name = 'author_list'
    queryset = Author.objects.filter(first_name__contains='')[:5]
    template_name='authors/my_arbitrary_template_name_list.html'

class AuthorDetailView(generic.DetailView):
    model = Author
    
def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_react_books = Book.objects.filter(title__exact='React JS').count()
    num_instances = BookInstance.objects.all().count()

    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    # The 'all()' is implied by default.
    num_authors = Author.objects.count()
    # Generate the number of genres
    num_genre = Genre.objects.all().count()
    num_genre_instances = Genre.objects.filter(name__exact='Fantasy').count()
    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_books': num_books,
        'num_react_books':num_react_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_genre': num_genre,
        'num_genre_instances': num_genre_instances,
        'num_visits':num_visits,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)

