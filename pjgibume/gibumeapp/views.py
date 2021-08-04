from django.shortcuts import render, redirect, get_object_or_404
from .models import Perfume
from .models import Comment
from .models import User
from .models import Community
from django.utils import timezone
from django.db.models import Q
from django.contrib import auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.


def home(request):
    return render(request, 'home.html')

@login_required
def mypage(request):
    comments=Comment.objects.all()
    comment_list=comments.filter(author = request.user.username)
    comment_list=list(comment_list)

    community=Community.objects.all()
    community_list=community.filter(writer = request.user.username)
    community_list=list(community_list)
    save_post_list=community.filter(save_users = request.user)

    products=Perfume.objects.all()
    like_product_list=products.filter(like_users = request.user)
    ok_product_list=products.filter(ok_users = request.user)
    dislike_product_list=products.filter(dislike_users = request.user)
    return render(request, 'mypage.html', {'comment_list' : comment_list, 'community_list':community_list, 'save_post_list':save_post_list, 'like_product_list':like_product_list, 'ok_product_list':ok_product_list, 'dislike_product_list':dislike_product_list})

def detail(request):
    return render(request, 'detail.html')

def product(request, name):
    product = Perfume.objects.get(pk=name)
    #comments=Comment.objects.filter(name=name)
    comments=Comment.objects.filter(name=name).order_by('-yes_count') #
    comment_list=list(comments)
    return render(request, 'product.html', {'product' : product, 'comment_list' : comment_list})

@login_required
# 댓글 작성
def writecomment(request, name):
    comment=Comment()
    comment.name = Perfume.objects.get(pk=name)
    comment.content=request.POST.get('content',False)
    comment.pub_date=timezone.datetime.now()
    comment.author=request.user
    comment.save()
    return redirect("product", name)

# 댓글 삭제
@login_required
def deletecomment(request, name, id):
    comment = get_object_or_404(Comment, pk=id)
    if comment.author != request.user.username:
        return redirect("product", name)
    else:
        comment.delete()
        return redirect("product", name)

def community(request):
    community=Community.objects.all()
    return render(request,'community.html', {'community':community})

def community_new(request):
    return render(request, 'community_new.html')

def create(request):
    community=Community()
    community.writer=request.user
    community.title=request.POST.get('title')
    community.body=request.POST.get('body')
    try:
        community.image=request.FILES['image']
    except:
        pass
    community.date=timezone.datetime.now()
    community.save()
    return redirect('/community_detail/'+str(community.id))

def community_detail(request, id):
    community_detail = get_object_or_404(Community, pk=id)
    return render(request, 'community_detail.html', {'community_detail':community_detail})

def community_edit(request, id):
    community=Community.objects.get(id=id)
    return render(request, 'community_edit.html', {'community':community})

def community_update(request, id):
    community = Community.objects.get(id = id)
    if community.writer != request.user.username: #
        return redirect('/community_detail/'+str(community.id))
    else:
        community.title = request.POST.get('title', False)
        community.body = request.POST.get('body', False)
        community.date=timezone.datetime.now()
        community.save() # 꼭 save!
        return redirect('/community_detail/'+str(community.id))

@login_required
def community_delete(request, id):
    community = get_object_or_404(Community, pk=id)
    if community.writer != request.user.username: #
        return redirect('/community/')
    else:
        community.delete()
        return redirect('/community/')

# save
def save_post(request, id):
    community = Community.objects.get(pk=id)
    if request.user.is_authenticated:
        if request.user in community.save_users.all():
            community.save_users.remove(request.user)
            community.save()
        else:
            community.save_users.add(request.user)
            community.save()
        return redirect('/community_detail/'+str(community.id))
    if not request.user.is_authenticated: 
        return redirect("login") 

def perfume(request):
    perfume_list = Perfume.objects.all()
    return render(request, 'perfume.html', {'perfume_list' : perfume_list})

def search(request):
    search_list = Perfume.objects.all()
    search_key = request.POST.get('search_key')
    if search_key:
        search_list = search_list.filter(Q(name__icontains=search_key) | Q(brand__icontains=search_key))
    return render(request, 'search.html', {'search_list' : search_list, 'search_key':search_key})

def education(request):
    return render(request, 'education.html')

#like
# @login_required
def like_post(request, name):
    product = Perfume.objects.get(pk=name)
    if request.user.is_authenticated: #
        if request.user in product.like_users.all():
            product.like_users.remove(request.user)
            # product.like_count -= 1
            product.save()
        else:
            if request.user in product.ok_users.all():
                product.ok_users.remove(request.user)
                #product.ok_count -= 1
                product.like_users.add(request.user)
                #product.like_count += 1
                product.save()

            if request.user in product.dislike_users.all():
                product.dislike_users.remove(request.user)
                #product.dislike_count -= 1
                product.like_users.add(request.user)
                #product.like_count += 1
                product.save()
            else:
                product.like_users.add(request.user)
                #product.like_count += 1
                product.save()
        return redirect("product", name)

    if not request.user.is_authenticated: #
        return redirect("login") # 

#ok
# @login_required
def ok_post(request, name):
    product = Perfume.objects.get(pk=name)
    if request.user.is_authenticated: #
        if request.user in product.ok_users.all():
            product.ok_users.remove(request.user)
            # product.ok_count -= 1
            product.save()
        else:
            if request.user in product.like_users.all():
                product.like_users.remove(request.user)
                #product.like_count -= 1
                product.ok_users.add(request.user)
                #product.ok_count += 1
                product.save()

            if request.user in product.dislike_users.all():
                product.dislike_users.remove(request.user)
                #product.dislike_count -= 1
                product.ok_users.add(request.user)
                #product.ok_count += 1
                product.save()

            else:
                product.ok_users.add(request.user)
                #product.ok_count += 1
                product.save()
        return redirect("product", name)
    
    if not request.user.is_authenticated: #
        return redirect("login") # 

#dislike
# @login_required
def dislike_post(request, name):
    product = Perfume.objects.get(pk=name)
    if request.user.is_authenticated: #
        if request.user in product.dislike_users.all():
            product.dislike_users.remove(request.user)
            #product.dislike_count -= 1
            product.save()
        else:
            if request.user in product.like_users.all():
                product.like_users.remove(request.user)
                #product.like_count -= 1
                product.dislike_users.add(request.user)
                #product.dislike_count += 1
                product.save()

            if request.user in product.ok_users.all():
                product.ok_users.remove(request.user)
                #product.ok_count -= 1
                product.dislike_users.add(request.user)
                #product.dislike_count += 1
                product.save()

            else:
                product.dislike_users.add(request.user)
                #product.dislike_count += 1
                product.save()
        return redirect("product", name)

    if not request.user.is_authenticated: #
        return redirect("login") # 

# 댓글 좋아요
# @login_required
def yesUp(request,name,id):
    yes = get_object_or_404(Comment, id=id)
    if request.user.is_authenticated: #
        if request.user in yes.yes_users.all():
            yes.yes_users.remove(request.user)
            yes.yes_count-=1 ###
            yes.save() ###
        else:
            if request.user in yes.no_users.all():
                yes.no_users.remove(request.user)
                yes.no_count-=1 ###
                yes.yes_users.add(request.user)
                yes.yes_count+=1 ###
                yes.save() ###
            else:
                yes.yes_users.add(request.user)
                yes.yes_count+=1 ###
                yes.save() ###
        return redirect("product", name)

    if not request.user.is_authenticated: #
        return redirect("login") # 

# 댓글 싫어요
# @login_required
def noUp(request,name,id):
    no = get_object_or_404(Comment, id=id)
    if request.user.is_authenticated: #
        if request.user in no.no_users.all(): 
            no.no_users.remove(request.user)
            no.no_count-=1 ###
            no.save() ###
        else:
            if request.user in no.yes_users.all():
                no.yes_users.remove(request.user)
                no.yes_count-=1 ###
                no.no_users.add(request.user)
                no.no_count+=1 ###
                no.save() ###
            else:
                no.no_users.add(request.user)
                no.no_count+=1 ###
                no.save() ###
        return redirect("product", name)

    if not request.user.is_authenticated: #
        return redirect("login") # 
