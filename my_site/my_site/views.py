from django.shortcuts import render

# Create your views here.
def index(request):
    user = request.user
    if user.is_authenticated:
        user_photo = request.user.image
        if user_photo != "":
            user_photo = f"../../../media/{user_photo}"
        else:
            user_photo = None
        return render(request, 'my_site/index.html', context={'user_photo': user_photo})
    else:
        return render(request, 'my_site/index.html')
