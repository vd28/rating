
from django.http import JsonResponse
from user_site.models import Cooperating


class CooperatingViev():
    def get(request):

        qs = list(Cooperating.objects.values('organization_name','number'))

        result= {'data':qs}
        print(result)


        return JsonResponse(result)
