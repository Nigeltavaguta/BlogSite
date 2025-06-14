from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from django.core.paginator import Paginator
from django.db import models

def index(request):
    categories = Category.objects.annotate(
        post_count=models.Count('category', filter=models.Q(category__status='1'))
    )
    
    post = Blog.objects.order_by('-id')
    main_post = Blog.objects.filter(Main_post=True, status='1').order_by('-id')[:1]
    recent = Blog.objects.filter(section='Recent', status='1').order_by('-id')[:5]
    popular = Blog.objects.filter(section='Popular', status='1').order_by('-id')[:5]
    trending = Blog.objects.filter(section='Trending', status='1').order_by('-id')[2:5]
    trending_large = Blog.objects.filter(section='Trending', status='1').order_by('-id')[:2]
    
    editors_pick = Blog.objects.filter(section='EditorsPick', status='1').order_by('-id')
    editors_pick_large = editors_pick[:1]
    editors_pick_small = editors_pick[1:5]

    inspiration_posts = Blog.objects.filter(section='Inspiration', status='1').select_related('author').order_by('-id')[:3]
    celebration_posts = Blog.objects.filter(section='Celebration', status='1').select_related('author').order_by('-id')[:3]

    latest_posts_list = Blog.objects.filter(status='1').select_related('author').order_by('-date')
    paginator = Paginator(latest_posts_list, 4)
    page_number = request.GET.get('page')
    latest_posts = paginator.get_page(page_number)
    
    context = {
        'post': post,
        'main_post': main_post,
        'recent': recent,
        'categories': categories,
        'popular': popular,
        'trending': trending,
        'trending_large': trending_large,
        'latest_posts': latest_posts,
        'editors_pick_large': editors_pick_large,
        'editors_pick_small': editors_pick_small,
        'inspiration_posts': inspiration_posts,
        'celebration_posts': celebration_posts,
    }
    return render(request, 'index.html', context)

def blog_detail(request, slug):
    category = Category.objects.all()
    post = get_object_or_404(Blog, blog_slug=slug)
    comments = Comment.objects.filter(blog_id=post.id).order_by('-date')

    context = {
        'category': category,
        'post': post,
        'comments': comments
    }
    return render(request, "blog_detail.html", context)

def category(request, slug):
    category_obj = get_object_or_404(Category, slug=slug)
    posts = Blog.objects.filter(category=category_obj, status='1').order_by('-date')
    categories = Category.objects.annotate(
        post_count=models.Count('category', filter=models.Q(category__status='1'))
    )
    
    context = {
        'category': category_obj,
        'posts': posts,
        'categories': categories,
        'active_category': slug
    }
    return render(request, 'category.html', context)

def add_comment(request, slug):
    if request.method == 'POST':
        post = get_object_or_404(Blog, blog_slug=slug)
        email = request.POST.get("InputEmail")
        website = request.POST.get("InputWeb")
        name = request.POST.get("InputName")
        comment_text = request.POST.get("InputComment")
        parent_id = request.POST.get("parent_id")
        parent_comment = None

        if parent_id:
            parent_comment = get_object_or_404(Comment, id=parent_id)

        Comment.objects.create(
            post=post,
            name=name,
            email=email,
            website=website,
            comment=comment_text,
            parent=parent_comment
        )
        return redirect('blog_detail', slug=post.blog_slug)
    return redirect('blog_detail')