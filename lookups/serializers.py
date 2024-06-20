from rest_framework import serializers
from .models import Industry, Country, State, City, Designation, Department, Source, DegreeType, EmployeeType, JobType, Relation, Skill, Language

class IndustrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Industry
        fields = '__all__'

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'

class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = '__all__'

class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'

class DesignationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Designation
        fields = '__all__'

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'

class SourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Source
        fields = '__all__'

class DegreeTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DegreeType
        fields = '__all__'

class EmployeeTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeType
        fields = '__all__'

class JobTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobType
        fields = '__all__'

class RelationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Relation
        fields = '__all__'

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = '__all__'

class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = '__all__'