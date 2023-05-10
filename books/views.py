from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView

from books.models import Book, BookAuthor, Author, BookReview
from books.forms import BookReviewForm

# class BooksListView(ListView):
#     template_name = "books/list.html"
#     queryset = Book.objects.all()
#     context_object_name = "books"
#     paginate_by = 2

class BooksListView(View):
    def get(self, request):
        books = Book.objects.all().order_by('id')
        search_query = request.GET.get("q", '')
        if search_query:
            books = books.filter(title__icontains=search_query)
        paginator = Paginator(books, 4)

        page_num = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_num)
        return render(
            request,
            "books/list.html",
            {
                "page_obj": page_obj,
                "search_query": search_query,
            }
        )


# class BookDetailView(DetailView):
#     template_name = "books/detail.html"
#     pk_url_kwarg = "id"
#     model = Book


class BookDetailView(View):
    def get(self, request, id):
        book = Book.objects.get(id=id)
        review_form = BookReviewForm()
        return render(
            request,
            "books/detail.html",
            {
                "book": book,
                "review_form": review_form,
            }
        )


class AddReviewView(LoginRequiredMixin ,View):
    def post(self, request, id):
        book = Book.objects.get(id=id)
        review_form = BookReviewForm(data=request.POST)

        if review_form.is_valid():
            BookReview.objects.create(
                book=book,
                user=request.user,
                starts_given=review_form.cleaned_data['starts_given'],
                comment=review_form.cleaned_data['comment'],
            )

            return redirect(reverse("books:detail", kwargs={"id":book.id}))
        return render(request, "books/detail.html",   {"review_form": review_form, })


class EditReviewView(LoginRequiredMixin, View):
    def get(self, request, book_id, review_id):
        book = Book.objects.get(id=book_id)
        review = book.bookreview_set.get(id=review_id)
        review_form = BookReviewForm(instance=review)
        context = {
            "book": book,
            "review": review,
            "review_form": review_form
        }
        return render(request, "books/edit_review.html", context)

    def post(self, request, book_id, review_id):
        book = Book.objects.get(id=book_id)
        review = book.bookreview_set.get(id=review_id)
        review_form = BookReviewForm(instance=review, data=request.POST)

        if review_form.is_valid():
            review_form.save()
            return redirect(reverse("books:detail", kwargs={"id":book.id}))

        return render(request, "books/edit_review.html")


class ConfirmDeleteReviewView(LoginRequiredMixin, View):
    def get(self, request, book_id, review_id):
        book = Book.objects.get(id=book_id)
        review = book.bookreview_set.get(id=review_id)
        context = {
            "book": book,
            "review": review,
        }
        return render(request, "books/confirm_delete_review.html", context)


class DeleteReviewView(LoginRequiredMixin, View):
    def get(self, request, book_id, review_id):
        book = Book.objects.get(id=book_id)
        review = book.bookreview_set.get(id=review_id)

        review.delete()
        messages.success(request, "Successfully deleted Review!")

        return redirect(reverse("books:detail", kwargs={"id": book.id}))

