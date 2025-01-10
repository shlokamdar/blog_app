from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import PostForm, UserRegisterForm
from .models import Post
import razorpay
from django.conf import settings
from django.http import HttpResponse
from django.core.mail import send_mail
import logging

# Logger setup
logger = logging.getLogger(__name__)

# View for homepage or index
def index(request):
    if request.user.is_authenticated:
        return redirect('user_dashboard')
    return render(request, 'index.html')

# View to create a new post
@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('user_dashboard')
    else:
        form = PostForm()
    return render(request, 'create_post.html', {'form': form})

# View to show user dashboard with posts
def user_dashboard(request):
    posts = Post.objects.filter(author=request.user, is_deleted=False)
    return render(request, 'dashboard.html', {'posts': posts})

# View to edit a post
@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('user_dashboard')
    else:
        form = PostForm(instance=post)
    return render(request, 'edit_post.html', {'form': form})

# View to delete a post (mark as deleted)
@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)
    post.is_deleted = True
    post.save()
    return redirect('user_dashboard')

# User registration view
def user_register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect('user_dashboard')
    else:
        form = UserRegisterForm()
    return render(request, 'registration.html', {'form': form})

# User login view
def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('user_dashboard')
            else:
                form.add_error(None, 'Invalid username or password')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

# User logout view
def user_logout(request):
    logout(request)
    return redirect('user_login')

# Subscription page view
def subscription_page(request):
    return render(request, 'subscription.html')

# Payment page view
def payment_page(request, amount):
    logger.debug("Entered process_payment view.")
    
    if request.method == 'POST':
        try:
            
            client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
            payment = client.order.create({
                "amount": amount * 100, 
                "currency": "USD",
                "payment_capture": "1"
            })
            if not request.user.email:
                return HttpResponse("User email is not set. Please update your profile.")
            send_mail(
                'Subscription Successful',
                f'Thank you for subscribing to the {amount} USD plan.',
                'your_email@example.com',
                [request.user.email],
            )
            return render(request, 'confirmation.html', {'amount': amount})
        except Exception as e:
            logger.error(f"An unexpected error occurred: {str(e)}")
            return HttpResponse(f"An error occurred: {str(e)}")

    return render(request, 'payment.html', {'amount': amount})

# Payment success page view
def payment_success(request):
    return render(request, 'confirmation.html')
