from flask import Blueprint, request, redirect, render_template, url_for
from flask.views import MethodView

from flask.ext.mongoengine.wtf import model_form
from tumblelog.models import Post, BlogPost

posts = Blueprint('posts', __name__, template_folder='templates')


class DetailView(MethodView):


    def get_context(self, slug):
        post = Post.objects.get_or_404(slug=slug)

        context = {
            "post": post
        }
        return context

    def get(self, slug):
        context = self.get_context(slug)
        return render_template('posts/detail.html', **context)

    def post(self, slug):
        context = self.get_context(slug)
        post = context.get('post')
        post.save()

        return redirect(url_for('posts.detail', slug=slug))
        return render_template('posts/detail.html', **context)

class ResultView(MethodView):

    def get(self):
        return render_template('posts/summitOk.html')

class Detail(MethodView):

    # decorators = [requires_auth]
    # Map post types to models
    class_map = {
        'post': BlogPost
    }

    def get_context(self, slug=None):

        if slug:
            post = Post.objects.get_or_404(slug=slug)
            # Handle old posts types as well
            cls = post.__class__ if post.__class__ != Post else BlogPost
            form_cls = model_form(cls,  exclude=('created_at', 'comments'))
            if request.method == 'POST':
                form = form_cls(request.form, inital=post._data)
            else:
                form = form_cls(obj=post)
        else:
            # Determine which post type we need
            cls = self.class_map.get(request.args.get('type', 'post'))
            post = cls()
            form_cls = model_form(cls,  exclude=('created_at', 'comments'))
            form = form_cls(request.form)
        context = {
            "post": post,
            "form": form,
            "create": slug is None
        }
        return context

    def get(self, slug):
        context = self.get_context(slug)
        return render_template('admin/detail.html', **context)

    def post(self, slug):
        context = self.get_context(slug)
        form = context.get('form')

        if form.validate():
            post = context.get('post')
            form.populate_obj(post)
            post.save()
            return redirect('/summitOk')
        return redirect('/')
        
            
# Register the urls
posts.add_url_rule('/', defaults={'slug': None}, view_func=Detail.as_view('create'))
posts.add_url_rule('/<slug>/', view_func=DetailView.as_view('detail'))
posts.add_url_rule('/summitOk/', view_func=ResultView.as_view('ResultView'))
