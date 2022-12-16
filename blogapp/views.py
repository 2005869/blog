from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail
from django.views.generic import ListView
from . import forms
from . import models


# Create your views here.
'''
def post_list(request):
    object_list = models.Post.published.all()
    paginator = Paginator(object_list, 3)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request, 'blogapp/post/list.html', {'posts': posts, 'page': page})
'''


def post_detail(request, year, month, day, post):
    post = get_object_or_404(models.Post,
                             slug=post,
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    return render(request, 'blogapp/post/detail.html', {'post': post})


class PostListView(ListView):
    queryset = models.Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blogapp/post/list.html'


def post_share(request, post_id):
    post = get_object_or_404(models.Post, id=post_id, status='published')
    sent = False

    if request.method == 'POST':
        form = forms.EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f'{cd["name"]} recommends you read {post.title}'
            message = f'Read {post.title} at {post_url}\n\n{cd["name"]}\'s comments: {cd["comments"]}'
            send_mail(subject, message, 'no-reply@blog.com', [cd['to']])
            sent = True
    else:
        form = forms.EmailPostForm()
    return render(request, 'blogapp/post/share.html', {'post': post, 'form': form, 'sent': sent})