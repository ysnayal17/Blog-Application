from django.views import generic
from .models import Post, Comment
from .forms import CommentForm
from django.shortcuts import render, get_object_or_404

# Create your views here
class PostList(generic.ListView):
    queryset      = Post.objects.filter(status=1).order_by("-created_on")
    template_name = 'index.html'

class PostDetail(generic.DetailView):
    model         = Post
    template_name = 'post_detail.html'

def post_detail(request, slug):
    template_name = "post_comments.html"
    # post          = Post.objects.get(slug=slug)
    post          = get_object_or_404(Post, slug=slug)
    comments      = Comment.objects.filter(active=True)
    new_comment   = None
    if request.method == 'POST':
        comment_form    = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment      = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
        return render(request, template_name, {
                                            'post': post,
                                            'comments': comments,
                                            'new_comment': new_comment,
                                            'comment_form': comment_form
                                        })
    else:
        comment_form = CommentForm()
        return render(request, template_name, {'comment_form': comment_form, 'comments': comments, 'post': post})
