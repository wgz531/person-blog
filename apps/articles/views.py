from django.shortcuts import render,redirect,reverse
from django.conf import settings
from .models import Articles,ArticlesCategory
from utils import restful
from .serializers import ArticlesSerializer,CommentSerializer
from django.http import Http404
from .forms import CommentForm
from .models import Comment
from apps.blogauth.decorators import blog_login_required
from django.db.models import Count,Q
from django.core.paginator import Paginator



def index(request):
    count = settings.ONE_PAGE_ARTICLES_COUNT
    articles_recent = Articles.objects.all()[0:3]
    keywords = request.GET.get('keywords')
    categories = ArticlesCategory.objects.all()
    dates = Articles.objects.dates('pub_time', 'day', order='DESC')

    if not keywords :
        articles = Articles.objects.select_related('category','author').all()[0:count]
        context = {
            'keywords':keywords,
            'articles_recent':articles_recent,
            'articles': articles,
            'categories': categories,
            'dates': dates,
        }
    else:
        articles = Articles.objects.filter(Q(title__icontains=keywords)|Q(content__icontains=keywords))[0:count]
        context = {
            'keywords': keywords,
            'articles_recent': articles_recent,
            'articles': articles,
            'categories': categories,
            'dates': dates,
        }
    return render(request, 'index/index.html', context=context)


def articles_list(request):
    # 通过p参数，来指定要获取第几页的数据
    # 并且这个p参数，是通过查询字符串的方式传过来的/news/list/?p=2
    page = int(request.GET.get('p', 1))
    # 分类为0：代表不进行任何分类，直接按照时间倒序排序
    category_id = int(request.GET.get('category_id', 0))
    start = (page - 1) * settings.ONE_PAGE_ARTICLES_COUNT
    end = start + settings.ONE_PAGE_ARTICLES_COUNT
    keywords = request.GET.get('keywords')

    if not keywords:
        print(keywords)
        if category_id == 0:
            # QuerySet
            # {'id':1,'title':'abc',category:{"id":1,'name':'热点'}}
            articles = Articles.objects.select_related('category', 'author').all()[start:end]
        else:
            articles = Articles.objects.select_related('category', 'author').filter(category__id=category_id)[start:end]
    else:

        if category_id == 0:
            articles = Articles.objects.select_related('category', 'author').filter(Q(title__icontains=keywords) | Q(content__icontains=keywords))[start:end]
        else:
            articles = Articles.objects.select_related('category', 'author').filter(Q(category__id=category_id) & (Q(title__icontains=keywords) | Q(content__icontains=keywords)))[start:end]

    serializer = ArticlesSerializer(articles, many=True) # 是一个queryset对象
    data = serializer.data
    return restful.result(data=data)

def articles_detail(request,articles_id):
    articles_all = Articles.objects.all()[0:3]
    keywords = request.GET.get('keywords')
    dates = Articles.objects.dates('pub_time','day',order='DESC')
    page = int(request.GET.get('p', 1))
    try:
        comments_conut = Articles.objects.annotate(comments_count=Count('comments')).get(pk=articles_id)
        articles = Articles.objects.select_related('category', 'author').prefetch_related("comments__author").get(
            pk=articles_id)

        comments = articles.comments.all()
        paginator = Paginator(comments, 5)
        page_obj = paginator.page(page)
        context_data = get_pagination_data(paginator, page_obj)

        context = {
            'dates':dates,
            'keywords':keywords,
            'comments_count': comments_conut,
            'articles_all': articles_all,
            'articles': articles,
            'page_obj': page_obj,
            'paginator': paginator,
            'comments':page_obj.object_list,
        }
        context.update(context_data)
        return render(request, 'index/articles_detail.html', context=context)
    except Articles.DoesNotExist:
        raise Http404

def get_pagination_data(paginator, page_obj, around_count=2):
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

@blog_login_required
def comment(request):
    form = CommentForm(request.POST)
    if form.is_valid():
        articles_id = form.cleaned_data.get('articles_id')
        content = form.cleaned_data.get('content')
        articles = Articles.objects.get(pk=articles_id)
        comment = Comment.objects.create(content=content, articles=articles, author=request.user)
        serialize = CommentSerializer(comment) # 是一个comment对象
        return restful.result(data=serialize.data)
    else:
        return restful.params_error(message=form.get_errors())






def timecate(request,year,month,day):
    articles = Articles.objects.filter(pub_time__year=year,
                                    pub_time__month=month,pub_time__day=day)
    dates = Articles.objects.dates('pub_time', 'day', order='DESC')
    print(type(dates))
    print(dates)
    print(dates[0])
    print(articles)
    articles_all = Articles.objects.all()[0:3]
    categories = ArticlesCategory.objects.all()
    context = {
            'articles_all': articles_all,
            'articles': articles,
            'categories': categories,
            'dates':dates,
    }
    return render(request,'index/data.html',context=context)

def aboutme(request):
    return render(request,'index/about.html')