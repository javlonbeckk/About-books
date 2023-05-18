from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth import logout
from django.views.generic import ListView, DeleteView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView

#local imports
from .forms import AddPostForm, RegisterUserForm, LoginUserForm
from .models import Books, Category
from .utils import DataMixin, menu


class BooksHome(DataMixin, ListView):
    model = Books
    template_name = "books/index.html"
    context_object_name = "posts"
    
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Main Page')
        return dict(list(context.items()) + list(c_def.items())) 

    def get_queryset(self):
        return Books.objects.filter(is_published=True)

# def index(request):
#     posts = Books.objects.all()

#     context = {
#         'posts': posts,
#         'menu': menu, 
#         'title': 'Main Page',
#         'cat_selected': 0,
#     }
    
#     return render(request, 'books/index.html', context=context)

def about(request):
    return render(request, 'books/about.html', {'menu': menu, 'title': 'About'})

class AddPage(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'books/addpage.html'
    success_url = reverse_lazy('home')
    login_url = reverse_lazy('home')
    
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Add book")
        return dict(list(context.items()) + list(c_def.items())) 
    

# def addpage(request):
#     if request.method == 'POST':
#         form = AddPostForm(request.POST, request.FILES)
#         if form.is_valid():
#             #print(form.cleaned_data)
#             form.save()
#             return redirect('home')
#     else:
#         form = AddPostForm()

#     return render(request, 'books/addpage.html', {'form': form, 'menu': menu, 'title': 'Добавление статьи'})

def contact(request):
    return HttpResponse('Contact')

def login(request):
    return HttpResponse('Login')

def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Page not found</h1>')

class ShowPost(DataMixin, DeleteView):
    model = Books
    template_name = 'books/post.html'
    slug_url_kwarg = 'post_slug'
    #pk_url_kwarg = 'post_pk'
    context_object_name = 'book' #html file da post degan variable ga boradi shu narsa
    
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['book'])
        return dict(list(context.items()) + list(c_def.items())) 


# def show_post(request, post_slug):
#     post = get_object_or_404(Books, slug=post_slug)
    
#     context = {
#         'post': post,
#         'menu': menu,
#         'title': post.title,
#         'cat_selected': post.cat_id,
#     }
    
#     return render(request, 'books/post.html', context=context)

class BooksCategory(DataMixin, ListView):
    model = Books
    template_name = 'books/index.html'
    context_object_name = 'posts'
    allow_empty = False #agar boshqa slug kiritilgan bosa index error mas 404 chiqaradi

    def get_queryset(self):
        return Books.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True)
    
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(
            title = str(context['posts'][0].cat),
            cat_selected = context['posts'][0].cat_id
        )
        return dict(list(context.items()) + list(c_def.items())) 
# def show_category(request, cat_slug):
#     cat_id = Category.objects.filter(slug=cat_slug)[0].pk
#     posts = Books.objects.filter(cat_id=cat_id)
    
#     print(len(posts)) 
#     if len(posts) == 0:
#         raise Http404()

#     context = {
#         'posts': posts,
#         'menu': menu,
#         'title': 'Отображение по рубрикам',
#         'cat_selected': cat_id,
#     }

#     return render(request, 'books/index.html', context=context)

class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'books/register.html'
    success_url = reverse_lazy('login')
    
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Registration")
        return dict(list(context.items()) + list(c_def.items()))
    
    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')
    
    
class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'books/login.html'
    
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Login')
        return dict(list(context.items()) + list(c_def.items()))
    
    def get_success_url(self):
        return reverse_lazy('home')

def logout_user(request):
    logout(request)
    return redirect('login')
