from flask import Blueprint, request, redirect, render_template, url_for
from flask.views import MethodView

from flask.ext.mongoengine.wtf import model_form

from tumblelog.auth import requires_auth
from tumblelog.models import Post, BlogPost

admin = Blueprint('admin', __name__, template_folder='templates')


class List(MethodView):
    decorators = [requires_auth]
    cls = Post

    def get(self):
        posts = self.cls.objects.all()
        return render_template('admin/list.html', posts=posts)

class ListView(MethodView):
    decorators = [requires_auth]
    def get(self):
        posts = Post.objects.all()
        return render_template('posts/list.html', posts=posts)


# Register the urls
admin.add_url_rule('/admin/', view_func=List.as_view('index'))
admin.add_url_rule('/admin/list/', view_func=ListView.as_view('list'))
