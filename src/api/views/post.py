from django.http import JsonResponse
from user_site.models import Post


class PostView():
    def get(request):

        qs = list(Post.objects.values('title','content','img','date'))

        result= {'data':qs}
        print(result)


        return JsonResponse(result)
