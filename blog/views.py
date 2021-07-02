from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Post
from django.views.generic import ListView, DetailView
from django.views import View
from .forms import CommentsForm

class StartingPage(ListView):
      template_name = 'blog/index.html'
      model = Post
      ordering = ['-date']
      context_object_name = 'posts'

      def get_queryset(self):
            query = super().get_queryset()
            data=query[:3]
            return data
      
# fucntion way of doing abov codes
# def starting_page(request):
#     latest_posts = Post.objects.all().order_by('-date')[:3]
#     return render(request, "blog/index.html", {
#       "posts": latest_posts
#     })


class Posts(ListView):
      template_name = 'blog/all-posts.html'
      model = Post
      ordering = ['-date']
      context_object_name='all_posts'

# def posts(request):
#     all_posts = Post.objects.all().order_by('-date')
#     return render(request, "blog/all-posts.html", {
#       "all_posts": all_posts
#     })


class PostDetail(View):
      def get(self, request, slug):
            stored_posts=request.session.get('stored_posts')
            if stored_posts is not None:
                  saved_for_later=Post.objects.get(slug=slug).id in stored_posts
            else:
                  saved_for_later=False
            return render(request, 'blog/post-detail.html',{
                  'post':Post.objects.get(slug=slug),
                  'comments_form': CommentsForm(),
                  'tags': Post.objects.get(slug=slug).tags.all(),
                  'comments': Post.objects.get(slug=slug).comments.all().order_by('-id'),
                  'saved_for_later':saved_for_later,
            })
      
      def post(self, request, slug):
            post=Post.objects.get(slug=slug)
            comments_form = CommentsForm(request.POST)

            if comments_form.is_valid():
                  comment=comments_form.save(commit=False)
                  comment.post = post
                  comment.save()
                  return HttpResponseRedirect(reverse('post-detail-page', args=[slug]))

            stored_posts=request.session.get('stored_posts')
            if stored_posts is not None:
                  saved_for_later=Post.objects.get(slug=slug).id in stored_posts
            else:
                  saved_for_later=False

            return render(request, 'blog/post-detail.html',{
                  'post': post,
                  'comments_form': comments_form,
                  'tags': post.tags.all(),
                  'comments': post.comments.all().order_by('-id'),
                  'saved_for_later':saved_for_later,
            })



# def post_detail(request, slug):
#     post = get_object_or_404(Post, slug=slug)
#     return render(request, "blog/post-detail.html", {
#       "post": post,
#       'tags':post.tags.all(),
#     })

class ReadLaterView(View):
      def post(self, request):
            stored_posts=request.session.get('stored_posts')
            if stored_posts is None:
                  stored_posts=[]

            id=int(request.POST['post_id'])

            if id not in stored_posts:
                  stored_posts.append(id)
            else:
                  stored_posts.remove(id)
            request.session['stored_posts'] = stored_posts

            return HttpResponseRedirect('/')

      def get(self, request):
            stored_posts=request.session.get('stored_posts')

            context={}
            if stored_posts is None or len(stored_posts)==0:
                  context['posts']=[]
                  context['has_posts']=False
            else:
                  posts=Post.objects.filter(id__in=stored_posts)
                  context['posts']=posts
                  context['has_posts']=True

            return render(request, 'blog/read-later.html', context)
            