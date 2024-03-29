from .models import Book
from django.urls import reverse_lazy
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.views.generic.edit import CreateView, DeleteView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.base import TemplateView
from django.views.generic import  View
from .forms import UserForm
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.http import HttpResponse, HttpResponseNotFound
from django.http import FileResponse, Http404

class first_page(TemplateView):
    template_name = "books/first_page.html"


class IndexView(ListView):
    queryset = Book.objects.all()
    context_object_name = 'books'
    template_name = 'books/index.html'
   # paginate_by = 2

class DetailView(DetailView):
    model = Book
    template_name = 'books/details.html'

class BookCreate(CreateView):
    model = Book
    fields = ['name', 'author', 'price', 'type', 'image', 'pdf']
    template_name = 'books/book_creation_form_s.html'

class BookDelete(DeleteView):
    model = Book
    success_url = reverse_lazy('books:index')

class UserFormView(View):
    form_class = UserForm
    template_name = 'books/signup_form.html'

    # display blank form
    def get(self, request):
        form = self.form_class(None)  # here form is object
        return render(request, self.template_name, {'form': form})

    # process data after we hit submit button
    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save(commit=False)     # user is object,we have not saved data

            # cleaned data
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()  # it makes the user to be registered in database of admin but still they are not logined

            # return user object if details are correct
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('books:index')


        return render(request, self.template_name, {'form': form})

class login_user(View):
    form_class = UserForm
    template_name = 'books/login_form.html'
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

class checklogin(View):
    form_class = UserForm
    def post(self, request):
        form = self.form_class(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('books:index')
        else:
            return HttpResponse("<h1>OOPS!<br>You entered wrong details. Please go back and login again.")

class log_out(View):
    def get(self, request):
        logout(request)
        return redirect('books:first_page')

