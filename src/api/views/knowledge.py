
from django.http import JsonResponse
from user_site.models import Doc_knowledge


class KnowledgeView():
    def get(request):
        uid = request.GET.get("universityId")

        qs = list(Doc_knowledge.objects.values('field_of_knowledge','number'))

        result= {'data':qs}
        print(result)


        return JsonResponse(result)
