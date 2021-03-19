from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from .models import *
from django.http import HttpResponse
from django.db.models import Q
import json
from django.core.paginator import Paginator
import math
from .cf import CF

# Create your views here.


#爬虫接口，通过这个接口把数据存进数据库
@csrf_exempt
def push(request):
    raw = json.loads(request.body.decode('utf-8'))
    director = raw['director']
    score = raw['score']
    name = raw['name']
    movietype = raw['movietype']

    if Movie.objects.filter(director=director, score=score, name=name, movietype=movietype).first():
        print('该条数据已经存在')
        return HttpResponse('该条数据已经存在')
    else:
        Movie.objects.create(director=director, score=score, name=name, movietype=movietype)
        print('成功插入一条数据')
        return HttpResponse('成功插入一条数据')


#首页的代码逻辑，获取高评分的电影展示在首页
def index(request):
    ctx = {}
    #.objects.filter()找到数据库中的所有电影
    movies = Movie.objects.all()

    high_score_list = []
    for m in movies: #queryset对象
        s = int(m.score[0])
        if s > 8:
            high_score_list.append(m)

    # ctx['high_score_list'] = high_score_list
    paginator = Paginator(high_score_list, 10)
    page = request.GET.get('page')
    ctx['pager'] = pager = paginator.get_page(page)

    ctx['high_score_list'] = high_score_list[pager.start_index()-1:pager.end_index()]
    ctx['user_id'] = request.session['user_id']

    #ctx是传给前台页面的数据

    return render(request, 'user_home.html', ctx)


#通过前台传过来的电影类型，从数据库中查找符合该类型的电影，然后展示在页面上。
def movietype(request, movietype):
    ctx = {}

    movies = Movie.objects.filter(Q(movietype__contains=movietype))

    if movies:
        paginator = Paginator(movies, 10)
        page = request.GET.get('page')
        ctx['pager'] = pager = paginator.get_page(page)
        ctx['movies'] = movies[pager.start_index()-1:pager.end_index()]
    return render(request, 'search_result.html', ctx)


#y用户退出。删除session中保存的用户id，用户名称
def user_logout(request):
    if 'user_id' in request.session:
        del request.session['user_id']
        del request.session['name']
    return redirect(user_login)



#用户登录
def user_login(request):
    ctx = {}
    #接收前台页面post方法过来的数据
    if request.method == 'POST':

        #前台两个input过来的值
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        #表名.objects.filter()
        user = User.objects.filter(username=username, password=password).first()
        if not user:
            ctx['error'] = '用户名密码错误'
            return render(request, 'login.html', ctx)

        request.session['user_id'] = str(user.id)
        request.session['name'] = user.name

        return redirect(index)

    #渲染login.html页面
    return render(request, 'login.html', ctx)


#用户注册，根据前台页面的form表单，穿过来的数据，把用户信息的数据存进数据库。
def user_register(request):
    ctx = {}

    if request.method == 'POST':
        name = request.POST.get('name', '')
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        mobile = request.POST.get('mobile', '')
        interesting = request.POST.get('interesting', '')

        if User.objects.filter(username=username).first():
            ctx['error'] = '该用户名已存在'
            return render(request, 'user_register.html', ctx)
        if not name:
            ctx['error'] = '姓名必填！'
            return render(request, 'user_register.html', ctx)
        if not username:
            ctx['error'] = '用户名必填'
            return render(request, 'user_register.html', ctx)
        if not password:
            ctx['error'] = '密码必填'
            return render(request, 'user_register.html', ctx)

        User.objects.create(name=name, username=username, password=password, mobile=mobile, interesting=interesting)
        ctx['success'] = '注册成功，请登录'
        return redirect(user_login)

    return render(request, 'user_register.html', ctx)


#电影详情的代码。根据前台穿过的电影id，查找数据库中的电影，然后传给电影详情页面
def movie_detail(request, movie_id):

    ctx = {}
    movie = Movie.objects.filter(id=movie_id).first()
    ctx['movieUserComment'] = MovieUserComment.objects.filter(movie=movie)
    ctx['m'] = movie
    return render(request, 'movie_detail.html', ctx)


#电影评分。通过前台html页面传过来的电影id和分数，查找电影，然后把用户评价的分数，存进MovieUserSCore表中
def movie_score(request, score, movie_id):

    ctx = {}

    movie = Movie.objects.filter(id=movie_id).first()

    user_id = request.session['user_id']
    user = User.objects.filter(id=user_id).first()

    #然后把用户评价的分数，存进MovieUserSCore表中
    movieUserScore = MovieUserScore.objects.filter(movie=movie, user=user).first()
    if not movieUserScore:
        MovieUserScore.objects.create(movie=movie, user=user, score=score)
    else:
        movieUserScore.score = score
        movieUserScore.save()

    ctx['scored'] = '1'
    ctx['m'] = movie
    ctx['movieUserComment'] = MovieUserComment.objects.filter(movie=movie)

    return render(request, 'movie_detail.html', ctx)

#个人中心代码逻辑，根据用户id，在数据中找到用户的信息，然后展示在页面上
def profile(request, user_id):

    ctx = {}
    user = User.objects.filter(id=user_id).first()



    user_movie_score = MovieUserScore.objects.filter(user=user)
    types = []
    for _ in user_movie_score:
        if int(_.score) > 3:
            if _.movie.movietype in types:
                continue

            types.append(_.movie.movietype)

    # allMovies = Movie.objects.all()
    # recommend = []
    # for _ in allMovies:
    #     if _.movietype in types and int(_.score[0]) > 8:
    #         recommend.append(_)

    if True:
        # 获取所有的电影
        #   格式 [ id, name, type ]
        allMovies = Movie.objects.all()
        all_movies = [[movie.id, movie.name, movie.movietype] for movie in allMovies]

        # 获取所有的用户信息
        #   格式 [ uid, mid, rating, time ]
        allUserScores = MovieUserScore.objects.all()
        all_user_scores = [[s.user_id, s.movie_id, s.score, 0] for s in allUserScores]

        model = CF(all_movies, all_user_scores, k=5)
        model.recommendByUser(user_id)
        rec_list = [e[1] for e in model.recommandList]

        movie_list = []
        for id in rec_list:
            m = Movie.objects.get(id=id)
            movie_list.append(m)

        recommend = movie_list

        if recommend:
            paginator = Paginator(recommend, 10)
            page = request.GET.get('page')
            ctx['pager'] = pager = paginator.get_page(page)
            ctx['recommend'] = recommend[pager.start_index()-1:pager.end_index()]

    ctx['user'] = user
    ctx['movieUserScore'] = MovieUserScore.objects.filter(user=user)


    return render(request, 'profile.html', ctx)


#首页的搜索框，通过搜索框的form表单，把搜索的值传过来。然后根据这个值，查数据中跟这个查询条件相关的数据，然后展示给用户
def search(request):

    ctx = {}
    if request.method == 'POST':
        q = request.POST.get('q', '')

        movies = Movie.objects.filter(Q(director__contains=q) | Q(name__contains=q) | Q(movietype__contains=q))

        if movies:
            paginator = Paginator(movies, 10)
            page = request.GET.get('page')
            ctx['pager'] = pager = paginator.get_page(page)
            ctx['movies'] = movies[pager.start_index()-1:pager.end_index()]

        return render(request, 'search_result.html', ctx)

def movie_recommend(request, movie_id):

    ctx = {}
    movie = Movie.objects.filter(id=movie_id).first()
    user_id = request.session['user_id']
    user = User.objects.filter(id=user_id).first()

    if request.method == 'POST':
         recommend = request.POST.get('recommend', '')
         MovieUserComment.objects.create(user=user, movie=movie, comment=recommend)

    ctx['movieUserComment'] = MovieUserComment.objects.filter(movie=movie)
    ctx['m'] = movie

    return render(request, 'movie_detail.html', ctx)


def movie_recommend_uid(request, uid):
    # 获取所有的电影
    #   格式 [ id, name, type ]
    allMovies = Movie.objects.all()
    all_movies = [ [ movie.id, movie.name, movie.movietype ] for movie in allMovies ]

    # 获取所有的用户信息
    #   格式 [ uid, mid, rating, time ]
    allUserScores = MovieUserScore.objects.all()
    all_user_scores = [ [ s.user_id, s.movie_id, s.score, 0 ] for s in allUserScores ]

    model = CF(all_movies, all_user_scores, k=5)
    model.recommendByUser(uid)
    rec_list = [ e[1] for e in model.recommandList ]

    movie_list = []
    for id in rec_list:
        m = Movie.objects.get(id=id)
        obj = [ id, m.name, m.director, m.movietype ]
        movie_list.append(obj)

    return HttpResponse('{}, {}'.format(len(allMovies), movie_list))