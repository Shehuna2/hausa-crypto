from taggit.models import Tag
from django.db.models import Count, Q
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Post, Comment, Category
from .forms import CommentForm
from .utils import increase_post_views

from django.core.paginator import Paginator

def AboutPage(request):
    return render(request, 'about.html')

def PostList(request, tag_slug=None, category_slug=None):
    categories = Category.objects.annotate(post_count=Count('posts'))
    tag = None
    queryset = Post.objects.filter(status='published')

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        queryset = queryset.filter(tags__in=[tag])

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        queryset = queryset.filter(category=category)

    paginator = Paginator(queryset, 10)  # Number of posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    for post in page_obj:
        increase_post_views(post.id)

    popular_posts = Post.objects.order_by('-views')[:5]

    context = {
        'posts': page_obj,
        'tag': tag,
        'categories': categories,
        'popular_posts': popular_posts,
        'selected_category': category_slug,
    }
    return render(request, 'blog-grid.html', context)


def PostDetail(request, post):
    post = get_object_or_404(Post, slug=post, status='published')

    comments = post.comments.filter(active=True)
    new_comments = None
    comment_form = CommentForm(data=request.POST)

    query = request.GET.get('q')
    if query:
        posts = Post.objects.filter(
            Q(title__icontains=query) | Q(tag__icontains=query) | Q(category__icontains=query)
            ).distinct()

    if request.method == 'POST':
        if comment_form.is_valid():
            new_comments = comment_form.save(commit=False)
            new_comments.post = post
            new_comments.save()
            return redirect(post.get_absolute_url()+'#'+str(new_comments.id))
        else:
            comment_form = CommentForm()
    
    post_tags_ids = post.tag.values_list('id', flat=True)
    similar_posts = Post.objects.filter(status='published', tag__in=list(post_tags_ids)).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tag=Count('tag')).order_by('-same_tag', '-publish')[:6]
            
    context = {
        'post':post, 'comments':comments, 'comment_form':comment_form, 'similar_posts':similar_posts,
        }
    return render(request, 'post_details.html', context)

def ReplyComment(request):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            post_id = request.POST.get('post_id')
            parent_id = request.POST.get('parent_id')
            post_url = request.POST.get('post_url')

            reply = form.save(commit=False)
            reply.post = Post(id=post_id)
            reply.parent = Comment(id=parent_id)
            reply.save()

            return redirect(post_url+'#'+str(reply.id))
    return redirect("/")        




    # paginator = Paginator(posts, 2)
    # page = request.GET.get('page')
    # try:
    #     posts = paginator.page(page)
    # except PageNotAnInteger:
    #     posts = paginator.page(1)
    # except EmptyPage:
    #     posts = paginator.page(paginator.num_pages)














































