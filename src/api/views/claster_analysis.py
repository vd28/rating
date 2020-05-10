from django.http import JsonResponse
from user_site.models import ClasterAnalysis


class ClasterAnalysisView():
    def get(request):

        qs = list(ClasterAnalysis.objects.values())

        result= {'data':qs}
        print(result)


        return JsonResponse(result)
