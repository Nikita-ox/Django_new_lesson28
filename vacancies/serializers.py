from rest_framework import serializers

from vacancies.models import Vacancy, Skill


#
# class VacancySerializer(serializers.Serializer):
#     id = serializers.IntegerField()
#     text = serializers.CharField(max_length=2000)
#     slug = serializers.CharField(max_length=50)
#     status = serializers.CharField(max_length=6)
#     created = serializers.DateField()
#     username = serializers.CharField(max_length=100)

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = '__all__'


class VacancyListSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=100)
    skill = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name'
    )

    class Meta:
        model = Vacancy
        fields = ['id', 'text', 'slug', 'status', 'created', 'username', 'skill']


class VacancyDetaillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vacancy
        fields = '__all__'


class VacancyCreateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    skill = serializers.SlugRelatedField(
        required=False,  # не обязательно
        many=True,  # много
        queryset=Skill.objects.all(),
        slug_field='name'
    )

    class Meta:
        model = Vacancy
        fields = '__all__'

    def is_valid(self, raise_exception=False):
        self._skill = self.initial_data.pop('skill', [])  # вытащим из данных по ключу
        return super().is_valid(raise_exception=raise_exception)

    def create(self, validate_data):
        vacancy = Vacancy.objects.create(**validate_data)

        for skill in self._skill:
            skill_obj, _ = Skill.objects.get_or_create(
                name=skill)

            vacancy.skill.add(skill_obj)
        vacancy.save()
        return vacancy


class VacancyUpdateSerializer(serializers.ModelSerializer):
    skill = serializers.SlugRelatedField(
        required=False,  # не обязательно
        many=True,  # много
        queryset=Skill.objects.all(),
        slug_field='name'
    )

    user = serializers.PrimaryKeyRelatedField(read_only=True)#менять их нельзя
    created = serializers.DateField(read_only=True)#менять их нельзя


    class Meta:
        model = Vacancy
        fields = ['id', 'text', 'status', 'slug', 'user', 'created', 'skill']

    def is_valid(self, raise_exception=False):
        self._skill = self.initial_data.pop('skill', [])  # вытащим из данных по ключу
        return super().is_valid(raise_exception=raise_exception)

    def save(self):
        vacancy = super().save()

        for skill in self._skill:
            skill_obj, _ = Skill.objects.get_or_create(
                name=skill)
            vacancy.skill.add(skill_obj)

        vacancy.save()
        return vacancy


class VacancyDestroySerializer(serializers.ModelSerializer):
    class Meta:
        model = Vacancy
        fields = ['id']

