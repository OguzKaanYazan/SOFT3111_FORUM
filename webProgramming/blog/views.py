from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import User, Event, Product, News, Post, Reply, Purchase, shuttleHours, Notes
from .forms import PostForm, ReplyForm, NewsForm, ProductForm, EventForm, PurchaseForm, RegisterForm, ShuttleForm, \
    NotesForm
from django.core.paginator import Paginator
from django.db.models import Q


# Create your views here.
def base(request):
    user = get_object_or_404(User, pk=request.session['username'])
    return render(request, 'blog/base.html', {'user': user})


def homepageGuest(request):
    if ('username' in request.session):
        user = get_object_or_404(User, pk=request.session['username'])
        if (user.isAdmin):
            return render(request, 'blog/Admin.html', {})
    newss = News.objects.filter(publishDate__lte=timezone.now()).order_by('publishDate')
    postA = Post.objects.filter(type='announcements')
    postC = Post.objects.filter(type='complaints')
    events = Event.objects.order_by('date')
    return render(request, 'blog/homepageGuest.html',
                  {'newss': newss, 'postA': postA, 'postC': postC, 'events': events})


def posts_list(request):
    posts = Post.objects.filter(publishDate__lte=timezone.now()).order_by('publishDate')
    if ('username' in request.session):
        username = request.session['username']
        user = get_object_or_404(User, username=username)
        return render(request, 'blog/posts_list.html', {'posts': posts, 'user': user})
    else:
        return render(request, 'blog/posts_list.html', {'posts': posts})


def news(request):
    newss = News.objects.filter(publishDate__lte=timezone.now()).order_by('-publishDate')
    paginator = Paginator(newss, 6)
    page = request.GET.get('page')
    newss = paginator.get_page(page)
    return render(request, 'blog/news.html', {'newss': newss})


def news_detail(request, pk):
    news = get_object_or_404(News, pk=pk)
    otherNews = News.objects.filter(publishDate__lte=timezone.now()).order_by('publishDate')
    return render(request, 'blog/openedNews.html', {'news': news, 'otherNews': otherNews})


def Profile(request):
    username = request.session['username']
    user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(username=username)
    replies = Reply.objects.filter(username=username)
    purchases = Purchase.objects.filter(username=username)
    return render(request, 'blog/Profile.html',
                  {'user': user, 'purchases': purchases, 'replies': replies, 'posts': posts})


def store(request):
    products = Product.objects.order_by('Id')
    paginator = Paginator(products, 6)
    page = request.GET.get('page')
    products = paginator.get_page(page)
    if ('username' in request.session):
        username = request.session['username']
        user = get_object_or_404(User, username=username)
        return render(request, 'blog/store.html', {'products': products, 'user': user})
    else:
        return render(request, 'blog/store.html', {'products': products})


def upcomingEvents(request):
    now = timezone.now()
    events = Event.objects.filter(date__gte=now).order_by('date')
    return render(request, 'blog/upcomingEvents.html', {'events': events})


def new_post(request):
    if ('username' not in request.session):
        return redirect('homepageGuest')
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            username = request.session['username']
            findUser = User.objects.get(username=username)
            post.username = findUser
            post.publishDate = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
        else:
            return redirect('posts_list')
    else:
        form = PostForm()
        return render(request, 'blog/newPost.html', {'form': form})


def loginpage(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        admin = User.objects.filter(username=username, password=password, isAdmin=True)
        user = User.objects.filter(username=username, password=password, isAdmin=False)
        if user:
            username = request.POST['username']
            request.session['username'] = username
            return redirect('homepageGuest')
        if admin:
            username = request.POST['username']
            request.session['username'] = username
            return redirect('adminPanel')
    return render(request, 'registration/login.html', {})


def logout(request):
    del request.session['username']
    return redirect('homepageGuest')


def addNews(request):
    if request.method == "POST":
        form = NewsForm(request.POST, request.FILES)
        if form.is_valid():
            news = form.save(commit=False)
            news.publishDate = timezone.now()
            news.save()
            return redirect('news_detail', pk=news.pk)
        else:
            return redirect('homepageGuest')
    else:
        form = NewsForm()
        return render(request, 'blog/addNews.html', {'form': form})


def AddProduct(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.save()
            return redirect('store')
    else:
        form = ProductForm()
        return render(request, 'blog/addProduct.html', {'form': form})


def addEvent(request):
    if request.method == "POST":
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            Event = form.save(commit=False)
            date = request.POST.get('date')
            Event.date = date
            Event.save()
            return redirect('upcomingEvents')
    else:
        form = EventForm()
        return render(request, 'blog/addEvent.html', {'form': form})


def Admin(request):
    return render(request, 'blog/Admin.html', {})


def purchaseForm(request, pk):
    if ('username' not in request.session):
        return redirect('homepageGuest')
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        form = PurchaseForm(request.POST)
        if form.is_valid():
            Purchase = form.save(commit=False)
            username = request.session['username']
            findUser = User.objects.get(username=username)
            Purchase.username = findUser
            findId = Product.objects.get(Id=pk)
            Purchase.productId = findId
            Purchase.totalPrice = product.price * Purchase.amount
            Purchase.save()

            return redirect('store')
    else:
        form = PurchaseForm()
        return render(request, 'blog/purchaseForm.html', {'form': form, 'product': product})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    replies = Reply.objects.filter(topic=pk)
    paginator = Paginator(replies, 6)
    page = request.GET.get('page')
    replies = paginator.get_page(page)
    if request.method == "POST":
        form = ReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            username = request.session['username']
            findUser = User.objects.get(username=username)
            reply.username = findUser
            findTopic = Post.objects.get(topic=pk)
            reply.topic = findTopic
            reply.save()
            return redirect('posts_list')
    else:
        form = ReplyForm()
        return render(request, 'blog/post_detail.html', {'post': post, 'form': form, 'replies': replies})


def Register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            User = form.save(commit=False)
            User.save()
            return redirect('homepageGuest')
    else:
        form = RegisterForm()
        return render(request, 'blog/Register.html', {'form': form})


def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    return render(request, 'blog/event_details.html', {'Event': event})


def editProfile(request):
    username = request.session['username']
    user = get_object_or_404(User, username=username)
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('psw')
        program = request.POST.get('program')
        gender = request.POST.get('gender')
        User.objects.filter(username=user.username).update(email=email, program=program, gender=gender,
                                                           password=password)
        return redirect('profile')
    else:
        return render(request, 'blog/editProfile.html', {'user': user})


def deletePost(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('posts_list')


def deleteProduct(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.delete()
    return redirect('store')


def shuttle(request):
    mShuttles = shuttleHours.objects.filter(Q(name='Maslak-Kampüs') | Q(name='Şile-Kampüs') | Q(name='Kadıköy-Kampüs'))
    kShuttles = shuttleHours.objects.filter(Q(name='Kampüs-Kadıköy') | Q(name='Kampüs-Şile') | Q(name='Kampüs-Maslak'))
    fShuttles = shuttleHours.objects.filter(Q(name='Kampüs-Çekmeköy') | Q(name='Çekmeköy-Kampüs'))
    if ('username' in request.session):
        username = request.session['username']
        user = get_object_or_404(User, username=username)
        return render(request, 'blog/shuttle.html',
                      {'mShuttles': mShuttles, 'kShuttles': kShuttles, 'fShuttles': fShuttles, 'user': user})
    return render(request, 'blog/shuttle.html',
                  {'mShuttles': mShuttles, 'kShuttles': kShuttles, 'fShuttles': fShuttles})


def deleteShuttle(request, pk):
    shuttle = get_object_or_404(shuttleHours, pk=pk)
    shuttle.delete()
    return redirect('shuttle')


def addShuttle(request):
    if request.method == "POST":
        form = ShuttleForm(request.POST)
        if form.is_valid():
            shuttle = form.save(commit=False)
            shuttle.save()
            return redirect('shuttle')
    else:
        form = ShuttleForm()
        return render(request, 'blog/addShuttle.html', {'form': form})


def courseNotes(request):
    notes = Notes.objects.order_by('id')
    paginator = Paginator(notes,6)
    page = request.GET.get('page')
    notes = paginator.get_page(page)
    if ('username' in request.session):
        username = request.session['username']
        user = get_object_or_404(User, username=username)
        return render(request, 'blog/courseNotes.html', {'notes': notes, 'user': user})
    else:
        return render(request, 'blog/courseNotes.html', {'notes': notes})


def pdf_view(request, pk):
    note = get_object_or_404(Notes, pk=pk)
    with open(note.note.path, 'rb') as pdf:
        response = HttpResponse(pdf.read(), content_type='application/pdf')
        return response


def deleteNotes(request, pk):
    note = get_object_or_404(Notes, pk=pk)
    note.delete()
    return redirect('courseNotes')


def addNotes(request):
    if request.method == "POST":
        form = NotesForm(request.POST, request.FILES)
        if form.is_valid():
            note = form.save(commit=False)
            note.save()
            return redirect('courseNotes')
    else:
        form = NotesForm()
        return render(request, 'blog/addNote.html', {'form': form})
