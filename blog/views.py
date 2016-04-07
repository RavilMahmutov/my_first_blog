from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone
from .models import Post, Comment
from .forms import PostForm, CommentForm



def post_list(request):
	posts = Post.objects.filter(published_date__lte = timezone.now()).order_by('-published_date')
	paginator = Paginator(posts, 5)
	page = request.GET.get('page')
	try:
		posts_page = paginator.page(page)   #Создал переменную posts_page, чтобы не запутаться с основным список постов
	except PageNotAnInteger:
		posts_page = paginator.page(1)  #если номер страницы не число - вернуть первую страницу
	except EmptyPage:
		posts_page = paginator.page(paginator.num_pages)  #если страница вне диапазона, например 9999, то вернет последнюю страницу   

	return render(request, 'blog/post_list.html', {'posts_page':posts_page})



def post_detail(request, pk):
	post = get_object_or_404(Post, pk=pk)
	return render(request, 'blog/post_detail.html', {'post': post})



@login_required
def post_new(request):
	if request.method == 'POST':
		form = PostForm(request.POST)
		if form.is_valid():
			post = form.save(commit=False)
			post.author = request.user
			post.save()
			return redirect('blog.views.post_detail', pk=post.pk)
	else:
		form = PostForm()
	return render(request, 'blog/post_edit.html', {'form': form})



@login_required
def post_edit(request, pk):
	post = get_object_or_404(Post, pk=pk)
	if request.method == 'POST':
		form = PostForm(request.POST, instance=post)
		if form.is_valid():
			post = form.save(commit=False)
			post.author = request.user
			post.published_date = timezone.now()
			post.save()
			return redirect('blog.views.post_detail', pk=post.pk)
	else:
		form = PostForm(instance=post)
	return render(request, 'blog/post_edit.html', {'form': form})



@login_required
def post_draft_list(request):
	posts = Post.objects.filter(published_date__isnull=True).order_by('create_date').reverse()
	return render(request, 'blog/post_draft_list.html', {'posts': posts})



@login_required
def post_publish(request, pk):
	post = get_object_or_404(Post, pk=pk)
	post.publish()
	return redirect('blog.views.post_detail', pk=pk)




@login_required
def post_remove(request, pk):
	post = get_object_or_404(Post, pk=pk)
	post.delete()
	return redirect('blog.views.post_list')



@login_required
def add_comment_to_post(request, pk):
	post = get_object_or_404(Post, pk=pk)
	if request.method == "POST":
		form = CommentForm(request.POST)
		if form.is_valid():
			comment = form.save(commit=False)
			comment.post = post
			comment.author = request.user
			comment.save()
			return redirect('blog.views.post_detail', pk = post.pk)
	else:
		form = CommentForm()
		return render(request, 'blog/add_comment_to_post.html', {'form': form})


