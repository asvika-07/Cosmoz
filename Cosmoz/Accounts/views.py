from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import get_object_or_404
from django.conf import settings
from Accounts.forms import SignUpForm, AccountAuthenticationForm, UserUpdateForm
from Accounts.models import User
from django.urls import reverse
from django.db.models.signals import pre_save
import os
from django.dispatch import receiver
from Connect.utils import get_friend_request_or_false
from Connect.friend_request_status import FriendRequestStatus
from Connect.models import FriendList, FriendRequest
from Dashboard.models import Post
from Forum.models import Question,Answer


def SignUpView(request, *args, **kwargs):
    user = request.user
    if user.is_authenticated:
        user.FirstName = request.user.FirstName
        print(user.FirstName)
        return HttpResponse(f"You are already authenticated as {user.email}")
    context = {}

    if request.POST:
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get("email").lower()
            raw_password = form.cleaned_data.get("password1")
            account = authenticate(email=email, password=raw_password)
            login(request, account)
            destination = kwargs.get("next")
            if destination:
                return redirect(destination)
            return redirect("home")
        else:
            context["form"] = form
    else:
        form = SignUpForm()
        context["form"] = form
    return render(request, "Accounts/SignUp.html", {"form": form})


def LogoutView(request):
    logout(request)
    return redirect("home")


def LoginView(request, *args, **kwargs):
    context = {}
    user = request.user
    if user.is_authenticated:
        return redirect("home")

    destination = get_redirect_if_exists(request)
    print("destination: " + str(destination))

    if request.POST:
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            email = request.POST["email"]
            password = request.POST["password"]
            user = authenticate(email=email, password=password)

            if user:
                login(request, user)
                context["user"] = user
                if destination:
                    return redirect(destination)
                return redirect("home")

    else:
        form = AccountAuthenticationForm()

    context["form"] = form

    return render(request, "Accounts/Login.html", context)


def get_redirect_if_exists(request):
    redirect = None
    if request.GET:
        if request.GET.get("next"):
            redirect = str(request.GET.get("next"))
    return redirect


def account_view(request, *args, **kwargs):
    context = {}
    user_id=  kwargs.get("email")
    # account=User.objects.get(pk=user_id)
    try:
        account = User.objects.get(pk=user_id)
    except:
    	return HttpResponse("Something went wrong.")
    
    user_posts = Post.objects.filter(Author=account.email)
    context['user_posts'] = user_posts

    user_question = Question.objects.filter(Author=account.email)
    context['user_question'] = user_question

    user_answer = Answer.objects.filter(Author=account.email)
    context['user_Answer'] = user_answer
    
    if account:
        context['FirstName'] = account.FirstName
        context['LastName']= account.LastName
        context['RegistrationID'] = account.RegistrationID
        context['username'] = account.username
        context['email'] = account.email
        context['ProfilePicture'] = account.ProfilePicture.url
        context['UserType'] = account.UserType
        context['DateOfBirth'] =account.DateOfBirth
        context['MobileNumber'] = account.MobileNumber
        context['Description'] = account.Description
        
        try:
            friend_list = FriendList.objects.get(user=account)
        except FriendList.DoesNotExist:
            friend_list = FriendList(user=account)
            friend_list.save()
        friends = friend_list.friends.all()
        context['friends'] = friends

        is_self = True
        is_friend = False
        request_sent = FriendRequestStatus.NO_REQUEST_SENT.value
        friend_requests = None
        user = request.user
        if user.is_authenticated and user != account:
            is_self = False
            if friends.filter(pk=user.email):
                is_friend = True
            else:
                is_friend = False
                if get_friend_request_or_false(sender=account, receiver=user) != False:
                    request_sent = FriendRequestStatus.THEM_SENT_TO_YOU.value
                    context['pending_friend_request_id'] = get_friend_request_or_false(
                        sender=account, receiver=user).pk
                elif get_friend_request_or_false(sender=user, receiver=account) != False:
                    request_sent = FriendRequestStatus.YOU_SENT_TO_THEM.value
                else:
                    request_sent = FriendRequestStatus.NO_REQUEST_SENT.value

        elif not user.is_authenticated:
            is_self = False
        else:
            try:
                friend_requests = FriendRequest.objects.filter(
                    receiver=user, is_active=True)
            except:
                pass

        context["is_self"] = is_self
        context['is_friend'] = is_friend
        context['request_sent'] = request_sent
        context['friend_requests'] = friend_requests
        context["BASE_URL"] = settings.BASE_URL

        return render(request, "Accounts/UserProfile.html", context)

def profile_edit(request, email):
    if not request.user.is_authenticated:
        return redirect("Login")
    account = get_object_or_404(User, email=email)
    if account.pk != request.user.pk:
        return HttpResponse("You cannot edit someone elses profile.")
    context = {}
    if request.method == "POST":
        form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            print(request.FILES)
            form.save()
            # request.user.ProfilePicture=request.FILES["ProfilePicture"]
            # request.user.save()
            return HttpResponseRedirect(
                reverse("account_view", kwargs={"email": account.email})
            )
        else:
            form = UserUpdateForm(instance=request.user)
            context["form"] = form
    else:
        form = UserUpdateForm(instance=request.user)
        context["form"] = form

    return render(request, "Accounts/ProfileEdit.html", context)


def account_search_view(request, *args, **kwargs):
    context = {}
    
    if request.method == "GET":
        search_query = request.GET.get("q")
        if len(search_query) > 0:
            search_results = User.objects.filter(email__icontains=search_query).filter(
                username__icontains=search_query).distinct()
            user = request.user
            print(user)
            accounts = []
            if user.is_authenticated:
                auth_user_friend_list = FriendList.objects.get(user=user)
                for account in search_results:
                    accounts.append((account, auth_user_friend_list.is_mutual_friend(account)))
                context['accounts'] = accounts
            else:
                for account in search_results:
                    accounts.append((account, False))
                context['accounts'] = accounts
    return render(request, "friend/Connect.html", context)

# def UserPost(request,email_id):
#     # email_id=kwargs.get("email")
#     context={}
#     try:
#         post=Post.objects.select_related().filter(Author=email_id)
#     except:
#         post=None
#     context["post"]=post
#     return render(request, "Accounts/UserProfile.html",context)

@receiver(pre_save, sender=User)
def delete_file_on_change_extension(sender, instance, **kwargs):
    if instance.pk:
        try:
            old_profilepic = User.objects.get(
                RegistrationID=instance.RegistrationID
            ).ProfilePicture
        except User.DoesNotExist:
            return
        else:
            new_profilepic = instance.ProfilePicture
            if old_profilepic and old_profilepic.url != new_profilepic.url:
                old_profilepic.delete(save=False)


