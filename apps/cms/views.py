from django.shortcuts import render
from django.views import View
from django.views.decorators.http import require_POST,require_GET
from apps.articles.models import ArticlesCategory,Articles
from utils import restful
from .forms import EditArticlesCategoryForm,WriteArticlesForm,EditArticlesForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from datetime import datetime
from django.utils.timezone import make_aware
from urllib import parse
from django.db.models.aggregates import Count
from apps.blogauth.decorators import superuser_required
from django.utils.decorators import method_decorator


@superuser_required
def index(request):
    return render(request,'cms/index.html')

# 文章发布
@method_decorator(superuser_required, name='dispatch')
class WriteArticles(View):
    def get(self,request):
        categories = ArticlesCategory.objects.all()
        context = {
            'categories': categories
        }
        return render(request,'cms/write_articles.html',context=context)

    def post(self,request):
        form = WriteArticlesForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            desc = form.cleaned_data.get('desc')
            content = form.cleaned_data.get('content')
            category_id = form.cleaned_data.get('category')
            category = ArticlesCategory.objects.get(pk=category_id)
            Articles.objects.create(title=title, desc=desc, content=content, category=category,
                                author=request.user)
            return restful.ok()
        else:
            return restful.params_error(message=form.get_errors())



# 文章分类
@superuser_required
@require_GET
def articles_category(request):
    category_list = ArticlesCategory.objects.annotate(num_category=Count('articles'))# 注意Count中是关联模型的小写

    context = {
        'category_list':category_list,
    }
    return render(request,'cms/articles_category.html',context=context)

# 添加分类
@superuser_required
@require_POST
def add_articles_category(request):
    name = request.POST.get('name')
    exists = ArticlesCategory.objects.filter(name=name).exists()
    if not exists:
        ArticlesCategory.objects.create(name=name)
        return restful.ok()
    else:
        return restful.params_error(message='该分类已经存在！')
# 更改分类
@superuser_required
@require_POST
def edit_articles_category(request):
    form = EditArticlesCategoryForm(request.POST)
    if form.is_valid():
        pk = form.cleaned_data.get('pk')
        name = form.cleaned_data.get('name')
        try:
            ArticlesCategory.objects.filter(pk=pk).update(name=name)
            return restful.ok()
        except:
            return restful.params_error(message='该分类不存在！')
    else:
        return restful.params_error(message=form.get_error())

@superuser_required
# 删除分类
@require_POST
def delete_articles_category(request):
    form = EditArticlesCategoryForm(request.POST)
    if form.is_valid():
        pk = form.cleaned_data.get('pk')
        try:
            ArticlesCategory.objects.filter(pk=pk).delete()
            return restful.ok()
        except:
            return restful.params_error(message='该分类不存在！')
    else:
        return restful.params_error(message=form.get_error())

# 文章列表
@method_decorator(superuser_required, name='dispatch')
class ArticlesListView(View):

    def get(self,request):
        # request.GET：获取出来的所有数据，都是字符串类型
        page = int(request.GET.get('p', 1))
        start = request.GET.get('start')
        end = request.GET.get('end')
        title = request.GET.get('title')
        category_id = int(request.GET.get('category', 0) or 0)
        articles = Articles.objects.select_related('category', 'author').all()

        if start or end:
            if start:
                start_date = datetime.strptime(start, '%Y/%m/%d')
            else:
                start_date = datetime(year=2020, month=1, day=1)
            if end:
                end_date = datetime.strptime(end, '%Y/%m/%d')
            else:
                end_date = datetime.today()
            articles = articles.filter(pub_time__range=(make_aware(start_date), make_aware(end_date)))

        if title:
            articles = articles.filter(title__icontains=title)

        if category_id:
            articles = articles.filter(category=category_id)

        paginator = Paginator(articles, 2)
        page_obj = paginator.page(page)
        context_data = self.get_pagination_data(paginator, page_obj)

        context={
            'categories': ArticlesCategory.objects.all(),
            'articles':page_obj.object_list,
            'page_obj': page_obj,
            'paginator': paginator,
            'category_id': category_id,
            'start': start,
            'end': end,
            'title': title,
            'url_query':'&'+parse.urlencode(
                {
                    'start': start or '',
                    'end': end or '',
                    'title': title or '',
                    'category': category_id or ''
                }
            )
        }

        context.update(context_data)
        return render(request, 'cms/articles_list.html',context= context)

    def get_pagination_data(self, paginator, page_obj, around_count=2):
        current_page = page_obj.number
        num_pages = paginator.num_pages

        left_has_more = False
        right_has_more = False

        if current_page <= around_count + 2:
            left_pages = range(1, current_page)
        else:
            left_has_more = True
            left_pages = range(current_page - around_count, current_page)

        if current_page >= num_pages - around_count - 1:
            right_pages = range(current_page + 1, num_pages + 1)
        else:
            right_has_more = True
            right_pages = range(current_page + 1, current_page + around_count + 1)

        return {
            # left_pages：代表的是当前这页的左边的页的页码
            'left_pages': left_pages,
            # right_pages：代表的是当前这页的右边的页的页码
            'right_pages': right_pages,
            'current_page': current_page,
            'left_has_more': left_has_more,
            'right_has_more': right_has_more,
            'num_pages': num_pages
        }

# 删除文章

@require_POST
def delete_articles(request):
    articles_id = request.POST.get('articles_id')
    Articles.objects.filter(pk=articles_id).delete()
    return restful.ok()

# 编辑文章
@method_decorator(superuser_required, name='dispatch')
class EditArticlesView(View):
    def get(self,request):
        articles_id = request.GET.get('articles_id')
        articles = Articles.objects.get(pk=articles_id)
        context = {
            'articles': articles,
            'categories': ArticlesCategory.objects.all()
        }
        return render(request,'cms/write_articles.html',context=context)

    def post(self, request):
        form = EditArticlesForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            desc = form.cleaned_data.get('desc')
            content = form.cleaned_data.get('content')
            category_id = form.cleaned_data.get('category')
            pk = form.cleaned_data.get("pk")
            category = ArticlesCategory.objects.get(pk=category_id)
            Articles.objects.filter(pk=pk).update(title=title, desc=desc, content=content,
                                              category=category)
            return restful.ok()
        else:
            return restful.params_error(message=form.get_errors())