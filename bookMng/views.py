from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required

from .models import MainMenu, Book, Comment, AdditionalComments  # Added AdditionalComment import
from .forms import BookForm, CommentForm, AdditionalCommentForm  # Added AdditionalCommentForm import

def index(request):
    return render(request, 'bookMng/index.html', {'item_list': MainMenu.objects.all()})

@login_required(login_url=reverse_lazy('login'))
def postbook(request):
    book_form = BookForm()
    comment_form = CommentForm()

    if request.method == 'POST':
        book_form = BookForm(request.POST, request.FILES)
        comment_form = CommentForm(request.POST)
        if book_form.is_valid() and comment_form.is_valid():
            book = book_form.save(commit=False)
            book.username = request.user
            book.save()
            comment = comment_form.save(commit=False)
            comment.book = book
            comment.user = request.user
            comment.save()
            return redirect('displaybooks')
    context = {'book_form': book_form, 'comment_form': comment_form}
    return render(request, 'bookMng/postbook.html', context)

@login_required(login_url=reverse_lazy('login'))
def displaybooks(request):
    books = Book.objects.all()
    for b in books:
        b.pic_path = b.picture.url[14:]
        b.comments = Comment.objects.filter(book=b)
    return render(request, 'bookMng/displaybooks.html', {'item_list': MainMenu.objects.all(), 'books': books})

class Register(CreateView):
    template_name = 'registration/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('register-success')

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(self.success_url)

@login_required(login_url=reverse_lazy('login'))
def book_detail(request, book_id):
    book = Book.objects.get(id=book_id)
    book.pic_path = book.picture.url[14:]
    comments = Comment.objects.filter(book=book)
    additional_comments = AdditionalComments.objects.filter(book=book)  # Fetch additional comments

    if request.method == 'POST':
        additional_comment_form = AdditionalCommentForm(request.POST)
        if additional_comment_form.is_valid():
            additional_comment = additional_comment_form.save(commit=False)
            additional_comment.book = book
            additional_comment.user = request.user
            additional_comment.save()
            return redirect('book_detail', book_id=book_id)

    else:
        additional_comment_form = AdditionalCommentForm()

    return render(request, 'bookMng/book_detail.html', {'item_list': MainMenu.objects.all(), 'book': book, 'comments': comments, 'additional_comments': additional_comments, 'comment_form': CommentForm(), 'additional_comment_form': additional_comment_form})

@login_required(login_url=reverse_lazy('login'))
def mybooks(request):
    books = Book.objects.filter(username=request.user)
    for b in books:
        b.pic_path = b.picture.url[14:]
    return render(request, 'bookMng/mybooks.html', {'item_list': MainMenu.objects.all(), 'books': books})

@login_required(login_url=reverse_lazy('login'))
def book_delete(request, book_id):
    book = Book.objects.get(id=book_id)
    book.delete()
    return render(request, 'bookMng/book_delete.html', {'item_list': MainMenu.objects.all(), 'book': book})