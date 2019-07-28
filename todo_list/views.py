from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.core.paginator import Paginator
from .models import List, Blog
from .forms import ListForm
from django.contrib import messages

def home(request):
    blogs = Blog.objects
    blog_list = Blog.objects.all()          #블로그 모든 글들을 대상으로
    paginator = Paginator(blog_list,4)     #블로그 객체 세 개를 한 페이지로 자르기
    page = request.GET.get('page')          #request된 페이지가 뭔지를 알아내고 (변수에 담아내고)
    posts = paginator.get_page(page)        #request된 페이지를 얻어온 뒤 return 해준다
    return render(request, 'home.html', { 'blogs' : blogs, 'posts' : posts })
  
def detail(request, blog_id):
    post = get_object_or_404(Blog, pk = blog_id)
    return render(request, 'detail.html' , {"post": post})

def todo(request):
    if request.method == 'POST':
        form = ListForm(request.POST or None)

        if form.is_valid():
            form.save()
            all_items = List.objects.all
            messages.success(request, ('Item Has Been Added to List!'))
            return render(request, 'todo.html', {'all_items':all_items})

    else:
        all_items = List.objects.all
        return render(request, 'todo.html', {'all_items':all_items})

def delete(request, list_id):
    item = List.objects.get(pk=list_id)
    item.delete()
    messages.success(request, ('Item Has Been Deleted!'))
    return redirect('todo')

def cross_off(request, list_id):
    item = List.objects.get(pk=list_id)
    item.completed = True
    item.save()
    return redirect('todo')

def uncross(request, list_id):
    item = List.objects.get(pk=list_id)
    item.completed = False
    item.save()
    return redirect('todo')

def edit(request, list_id):
    if request.method == 'POST':
        item = List.objects.get(pk=list_id)

        form = ListForm(request.POST or None, instance=item)

        if form.is_valid():
            form.save()
            messages.success(request, ('Item Has Been Edited!'))
            return redirect('todo')
    
    else:
        item = List.objects.get(pk=list_id)
        return render(request, 'edit.html', {'item':item})

def new(request):
    return render(request, 'new.html')

def create(request):
    blog = Blog()
    blog.title = request.GET['title']
    blog.body = request.GET['body']
    blog.pub_date = timezone.datetime.now()
    blog.save()
    return redirect('/'+str(blog.id))