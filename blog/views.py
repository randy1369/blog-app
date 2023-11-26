from django.shortcuts import render, get_object_or_404, redirect
from .models import BlogPost, Categories, Subcategories, Tag
from .forms import BlogPostForm, SignUpForm
from django.db.models import Q
# for user authentication
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User 
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage



#===========================================================================================

# Auth

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('blog:login')
    else:
        form = SignUpForm()
    return render(request, 'blog/signup.html', {'form':form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('blog:blog_list')
        else:
            error_message = 'Invalid username or password.'
            return render(request, 'blog/login.html', {'error_message':error_message})
    else:
        return render(request, 'blog/login.html')


@login_required
def logout_view(request):
    logout(request)
    return redirect('blog:blog_list')


@login_required(login_url='blog:login')
def profile(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.user != user:
        return redirect('blog:profile',pk=request.user.pk)
    user_posts = BlogPost.objects.filter(author=user)
    favorites = user.favorite_posts.all()
    context = {
        'user': user,
        'user_posts': user_posts,
        'favorites': favorites,
    }
    return render(request, 'blog/profile.html', context)



#===========================================================================================================

# Posts by tags, and category, Search functionality
def posts_by_tag(request, tag_id):
    tag = get_object_or_404(Tag, pk=tag_id)
    posts = BlogPost.objects.filter(tags=tag)
    categories = Categories.objects.prefetch_related('subcategories')

    for post in posts:
        post.first_three_lines = post.content.split('\n')[3:11]

    # Number of posts to show per page
    posts_per_page = 3  # You can adjust this value

    paginator = Paginator(posts, posts_per_page)
    page = request.GET.get('page')

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    context = {'tag': tag, 'posts': posts, 'categories':categories}
    return render(request, 'blog/posts_by_tag.html', context)



def posts_for_subcategory(request, subcategory_id):
    subcategory = get_object_or_404(Subcategories, pk=subcategory_id)
    posts = BlogPost.objects.filter(subcategory=subcategory)
    categories = Categories.objects.prefetch_related('subcategories')

    for post in posts:
        post.first_three_lines = post.content.split('\n')[3:11]

    # Number of posts to show per page
    posts_per_page = 3  # You can adjust this value

    paginator = Paginator(posts, posts_per_page)
    page = request.GET.get('page')

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    context = {
        'subcategory':subcategory,
        'posts':posts,
        'categories': categories,

    }

    return render(request, 'blog/post_cat.html', context)


def search(request):
    query = request.GET.get('q', '').strip()  # Get the search query from the request
    categories = Categories.objects.prefetch_related('subcategories')

    if not query:
        results = BlogPost.objects.none()
    else:
        words = query.split()  # Split the query into individual words

        # Create a Q object for each word in the title field
        title_queries = Q()
        for word in words:
            title_queries |= Q(title__icontains=word)

        # Combine the title queries using the OR operator
        results = BlogPost.objects.filter(title_queries)

        for post in results:
            post.first_three_lines = post.content.split('\n')[3:11]

    # Number of results to show per page
    results_per_page = 3  
    paginator = Paginator(results, results_per_page)
    page = request.GET.get('page')

    try:
        results = paginator.page(page)
    except PageNotAnInteger:
        results = paginator.page(1)
    except EmptyPage:
        results = paginator.page(paginator.num_pages)

    context = {
        'query': query,
        'results': results,
        'categories': categories,
    }
    return render(request, 'blog/search_results.html', context)


#==========================================================================================================
# Display blog posts, categories tags, post in detail


def blog_cattags(request):
    categories = Categories.objects.prefetch_related('subcategories')
    tags = Tag.objects.all()
    context = {
        'categories': categories,
        'tags' : tags,

    }
    return render(request, 'blog/cattags.html', context)


def blog_list(request):
    posts = BlogPost.objects.all()
    categories = Categories.objects.prefetch_related('subcategories')

    for post in posts:
        post.first_three_lines = post.content.split('\n')[3:11]

    # Number of posts to show per page
    posts_per_page = 3  # You can adjust this value

    paginator = Paginator(posts, posts_per_page)
    page = request.GET.get('page')

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request, 'blog/blog_list.html', {'posts': posts, 'categories': categories})


def blog_detail(request, slug):
    print("View is called")
    post = get_object_or_404(BlogPost, slug=slug)
    categories = Categories.objects.prefetch_related('subcategories')
    tl = post.total_likes()
    print(f"Post title: {post.title}") 
    return render(request, 'blog/blog_detail.html', {'post': post, 'tl':tl, 'categories':categories})


#====================================================================================================================

# CRUD, LIKES, FAV

@login_required(login_url='blog:login')
def blog_create(request):

    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            blog_post = form.save(commit=False)
            blog_post.author = request.user
            blog_post.save()
            form.save_m2m()  # Save the many-to-many relationships (categories and tags)
            return redirect('blog:blog_detail', slug=blog_post.slug)
    else:
        form = BlogPostForm()
    return render(request, 'blog/blog_create.html', {'form': form})


@login_required(login_url='blog:login')
def blog_update(request, slug):
    post = get_object_or_404(BlogPost, slug=slug)
    if request.user != post.author:
        return redirect('blog:blog_detail', slug=slug)
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES,instance=post)
        if form.is_valid():
            form.save()
            return redirect('blog:blog_detail', slug=post.slug)

    else:
        form = BlogPostForm(instance=post)
    
    return render(request, 'blog/blog_update.html', {'form':form, 'post':post})


@login_required(login_url='blog:login')
def blog_delete(request, slug):
    post = get_object_or_404(BlogPost, slug=slug)
    if request.method == 'POST' and request.user == post.author:
        post.delete()
        return redirect('blog:blog_list')
    return render(request, 'blog/blog_delete.html', {'post': post})

def cattags(request):
    return render(request, 'blog/cat_tag.html')

def contact(request):
    return render(request, "blog/contact.html")


@login_required(login_url='blog:login')
def like_post(request, slug):
    post = get_object_or_404(BlogPost, slug=slug)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
        
    return redirect('blog:blog_detail', slug=slug) 

@login_required(login_url='blog:login')
def add_to_favorites(request, slug):
    post = get_object_or_404(BlogPost, slug=slug)
    if request.user in post.favorites.all():
        post.favorites.remove(request.user)
    else:
        post.favorites.add(request.user)
    return redirect('blog:blog_detail', slug=slug)

