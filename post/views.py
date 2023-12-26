from django.shortcuts import get_object_or_404, render, redirect
from .forms import PostForm
from .models import Post
from django.urls import reverse

# Create your views here.

def post_list(request):
    post_list = Post.objects.all()
    context = {
        'post_list': post_list,
    }
    return render(request, 'post/index.html', context)


def post_detail(request, post_id):
    post = Post.objects.get(id=post_id)
    context = {
        'post':post,
    }
    return render(request, 'post/post_detail.html', context)

def post_new(request):
    if request.method == 'GET':
        form = PostForm()
        
    elif request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save()
            post_detail_url = reverse('post:post_detail', kwargs={'post_id': post.id})
            return redirect(post_detail_url)
        
    return render(request, 'post/post_new.html', {
        'form' : form,
    })
    
def post_edit(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    if request.method == 'GET':
        form = PostForm(instance=post)
        
    elif request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save()
            post_detail_url = reverse('post:post_detail', kwargs={'post_id': post.id})
            return redirect(post_detail_url)
        
    return render(request, 'post/post_edit.html', {
        'form':form,
    })