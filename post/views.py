from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment
from .forms import PostForm, CommentForm
from django.utils import timezone
from django.contrib.auth.decorators import login_required
 
def index(request):
    posts = Post.objects.all()
    search_key = request.GET.get("keyword", "")
    print(search_key)
    if search_key:
        print(search_key)
        posts = Post.objects.filter(title__icontains=search_key)
       
    return render(request, 'post/post_list.html', {'posts':posts, 'q':search_key})

    # posts = Post.objects.all()
    # return render(request, 'post/post_list.html', {'posts': posts})
 
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'post/post_detail.html', {'post': post})
 
@login_required
def post_new(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.created = timezone.now()
            post.save()
            return redirect('post:post_list')
    else:
        form = PostForm()
    return render(request, 'post/post_form.html', {'form': form})
 
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        post.delete()
        return redirect('post:post_list')
    return render(request, 'post/post_delete.html', {'post': post})
 
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
   
    if request.method == 'GET':
        form = PostForm(instance=post)
       
    elif request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save()
            return redirect('post:post_detail', pk=pk)
       
    return render(request, 'post/post_edit.html', {
        'form': form,
    })
    
# def list(request):
#     posts = Post.objects.all()
#     search_key = request.GET.get("keyword")
#     print(search_key)
#     if search_key:
#         print(search_key)
#         posts = Post.objects.filter(title__icontains=search_key)
       
#     return render(request, 'post/post_list.html', {'posts':posts, 'q':search_key})

def Comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = CommentForm(request.POST)
    if comments.is_valid():
        comments = comments.save(commit=False)
        comments.post = get_object_or_404(Post, pk=post.pk)
        comments.user = request.user
        comments.save()
    return redirect('post:post_detail', pk=post.pk)

