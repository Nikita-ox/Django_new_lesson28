
from django.core.paginator import Paginator
from django.db.models import Count, Avg, Q, F
from django.http import HttpResponse, JsonResponse
from django.views import View
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from authentication.models import User
from goodsite import settings
from vacancies.models import Vacancy, Skill
from vacancies.permissions import VacancyCreatePermission

from vacancies.serializers import VacancyDetaillSerializer, VacancyListSerializer, VacancyCreateSerializer, \
    VacancyUpdateSerializer, VacancyDestroySerializer, SkillSerializer


def hello(request):
    return HttpResponse('Hello, Nikita!')


class SkillsViewSet(ModelViewSet):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer


class VacancyListView(ListAPIView):
    queryset = Vacancy.objects.all()
    serializer_class = VacancyListSerializer

    def get(self, request, *args, **kwargs):
        vacancy_text = request.GET.get('text', None)
        if vacancy_text:
            self.queryset = self.queryset.filter(  # queryset то что мы будем доставать
                text__icontains=vacancy_text  # i перед contains - без учета регистра
            )

        skill = request.GET.getlist('skill', None)  # get - наследник от словаря, getlist - нас списка
        skill_q = None
        for ski in skill:
            if skill_q is None:
                skill_q = Q(skill__name__icontains=ski)
                # специальный служебный класс для сбора условий фильтрации
            else:
                skill_q |= Q(skill__name__icontains=ski)  # |= логическое или
        if skill_q:  # если заполнился
            self.queryset = self.queryset.filter(skill_q)

        slug_name = request.GET.get('slug', None)
        if slug_name:
            self.queryset = self.queryset.filter(  # queryset то что мы будем доставать
                slug__icontains=slug_name)

        return super().get(request, *args, **kwargs)


class VacancyDetailView(RetrieveAPIView):
    queryset = Vacancy.objects.all()
    serializer_class = VacancyListSerializer
    # permission_classes = [IsAuthenticated]  # Проверка доступа на страницу


class VacancyCreateView(CreateAPIView):
    queryset = Vacancy.objects.all()
    serializer_class = VacancyCreateSerializer
    permission_classes = [VacancyCreatePermission]


class VacancyUpdateView(UpdateAPIView):
    queryset = Vacancy.objects.all()
    serializer_class = VacancyUpdateSerializer


class VacancyDeleteView(DestroyAPIView):
    queryset = Vacancy.objects.all()
    serializer_class = VacancyDestroySerializer


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def user_vacancies(request):
    # обьект, который будет создавать запрос в базу данных
    # annotate - добавляет к нашей записи доп колонку(атрибут) о том, что он сделал
    user_qs = User.objects.annotate(vacancies=Count('vacancy'))  # Считаем по полю vacancy

    paginator = Paginator(user_qs, settings.TOTAL_ON_PAGE)
    page_number = request.GET.get("page")
    # достаем page_number
    page_obj = paginator.get_page(page_number)

    users = []
    for user in page_obj:
        users.append({
            "id": user.id,  # id
            "name": user.username,  # имя
            "vacancies": user.vacancies,  # кол-во вакансий
        })
    response = {
        "items": users,
        "total": paginator.count,
        "num_pages": paginator.num_pages,
        # словарь в котором avg= - ключ, ('vacancies') - значение
        # aggregate после нее уже ни чего  нельзя применять, не order_by, анатации, каунты
        "avg": user_qs.aggregate(avg=Avg('vacancies'))['avg'],  # среднее кол-во вакансий на ползователя
    }

    return JsonResponse(response)


class VacacncyLikeView(UpdateAPIView):
    queryset = Vacancy.objects.all()
    serializer_class = VacancyDetaillSerializer

    def put(self, request, *args, **kwargs):
        Vacancy.objects.filter(pk__in=request.data).update(likes=F('likes') + 1)
        # F('likes') - поле текущей записи, F(Вытащи) - Возьми текущее значение и сделай  что-то.

        return JsonResponse(VacancyDetaillSerializer(Vacancy.objects.filter(pk__in=request.data), many=True).data,
                            safe=False)
