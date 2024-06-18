from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.urls import is_valid_path

from .models import Profile, Post, FriendRequest, Comment, User
from .forms import ProfileForm, PostForm, FriendRequestForm, CommentForm
from django.contrib.auth.decorators import login_required


def home(request):
    if request.user.is_authenticated:
        posts = Post.objects.all().order_by('-created_at')
        comment_form = CommentForm()
        post_form = PostForm()
        return render(request, 'network/home.html', {'posts': posts, 'comment_form': comment_form, 'post_form': post_form})
    else:
        return redirect('login')


@login_required
def followed_feed(request):
    friends = request.user.profile.friends.all()
    posts = Post.objects.filter(author__profile__in=friends).order_by('-created_at')
    comment_form = CommentForm()
    post_form = PostForm()
    return render(request, 'network/followed_feed.html', {'posts': posts, 'comment_form': comment_form, 'post_form': post_form})


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'network/register.html', {'form': form})


@login_required
def profile(request, username):
    user = get_object_or_404(User, username=username)
    profile = Profile.objects.get(user=user)
    posts = Post.objects.filter(author=user)
    is_own_profile = user == request.user
    sent_requests = FriendRequest.objects.filter(from_user=request.user)
    received_requests = FriendRequest.objects.filter(to_user=request.user)
    comment_form = CommentForm()

    if is_own_profile:
        if request.method == 'POST':
            form = ProfileForm(request.POST, request.FILES, instance=profile)
            if form.is_valid():
                form.save()
                return redirect('profile', username=user.username)
        else:
            form = ProfileForm(instance=profile)
    else:
        form = None

    return render(request, 'network/profile.html', {
        'profile': profile,
        'posts': posts,
        'form': form,
        'is_own_profile': is_own_profile,
        'sent_requests': sent_requests,
        'received_requests': received_requests,
        'comment_form': comment_form,
    })


def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('home')
    else:
        form = PostForm()
    return render(request, 'network/create_post.html', {'form': form})



@login_required
def send_friend_request(request, username):
    to_user = get_object_or_404(User, username=username)
    FriendRequest.objects.get_or_create(from_user=request.user, to_user=to_user)
    return redirect('profile', username=username)


@login_required
def accept_friend_request(request, request_id):
    friend_request = get_object_or_404(FriendRequest, id=request_id)
    if friend_request.to_user == request.user:
        request.user.profile.friends.add(friend_request.from_user.profile)
        friend_request.from_user.profile.friends.add(request.user.profile)
        friend_request.delete()
    return redirect('profile', username=request.user.username)


@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    # Get the URL of the previous page
    previous_page = request.META.get('HTTP_REFERER')
    # Redirect to the previous page
    return redirect(previous_page)


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.save()

    # Get the URL of the previous page
    previous_page = request.META.get('HTTP_REFERER')
    # Redirect to the previous page
    return redirect(previous_page)


@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user == post.author:
        post.delete()
        return redirect('profile', username=request.user.username)
    else:
        return HttpResponseForbidden("You are not allowed to delete this post.")
