from django.http import JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import UpdateView

from companies.models import Company


@method_decorator(csrf_exempt, name='dispatch')
class CompanyImageView(UpdateView):
    model = Company
    fields = ['name', 'logo']

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        # Тут лежит все, что послал подльзователь в качестве файлов
        self.object.logo = request.FILES["logo"]
        self.object.save()

        return JsonResponse({
            "id": self.object.id,
            "name": self.object.name,
            #Выводим не картинку, а ее урл и оброботаем, если лого нет
            "logo": self.object.logo.url if self.object.logo else None
        })

