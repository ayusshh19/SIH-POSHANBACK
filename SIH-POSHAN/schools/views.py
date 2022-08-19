from importlib.metadata import PackageNotFoundError
from multiprocessing import context
import re
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required, user_passes_test
from .permissions import is_in_group_schools
from .forms import ClassForm, MealForm, StudentForm, SchoolForm
from django.utils import timezone
from django.contrib import messages
from django.views.generic import TemplateView, CreateView, ListView, DeleteView, DetailView, UpdateView
from .models import Student, Class, Meal,Attendence
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from photocalpro.modelfile2 import return_calories_proteins
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from .serializers import Attendanceserializer, Mealserializers, studentSerializers
from schools import serializers

# Create your views here.
@user_passes_test(is_in_group_schools, login_url='/')
@login_required
def dashboardView(request):
    return render(request, 'schools/index.html')


@user_passes_test(is_in_group_schools, login_url='/')
@login_required
def profileView(request):
    return render(request, 'schools/profile.html')


@user_passes_test(is_in_group_schools, login_url='/')
@login_required
def attendenceView(request):
    return render(request, 'schools/attendence.html')



@user_passes_test(is_in_group_schools, login_url='/')
@login_required
def update_profile_pic(request):
    myschool = request.user.schools
    print(request)
    if request.method == 'POST':
        form = SchoolForm(request.POST, request.FILES, instance=myschool)
        if form.is_valid():
            print(form)
            form.save()
            print('saved')
            return redirect('schools:profile')

    else:
        print('NO POST REQUEST')
        form = SchoolForm(instance=myschool)
        print(type(form))
        return render(request, 'schools/update_profile_pic.html', {'form': form})


class ClassCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Class
    form_class = ClassForm
    template_name = "schools/create_new_class.html"
    success_url: reverse_lazy('schools:dashboard')

    def test_func(self):
        cond1 = is_in_group_schools(self.request.user)
        return cond1

    def form_valid(self, form):
        form.instance.school = self.request.user.schools
        print('this validity')
        return super().form_valid(form)


class ClassUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Class
    form_class = ClassForm
    template_name = "schools/update_class.html"
    # success_url = reverse_lazy('schools:dashboard')

    def test_func(self):
        cond1 = is_in_group_schools(self.request.user)
        cond2 = self.request.user.schools.classes.filter(
            pk=self.kwargs['pk']).exists()
        return cond1 and cond2


@user_passes_test(is_in_group_schools, login_url='/')
@login_required
def ClassDeleteView(request, pk):
    getclass = get_object_or_404(Class, pk=pk)
    if request.user.schools.classes.filter(pk=pk).exists():
        getclass.delete()
        return HttpResponseRedirect(reverse('schools:manage_class'))
    else:
        return render(request, '403.html')


class ClassDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Class
    template_name = "schools/class_detail.html"
    context_object_name = 'class'

    def test_func(self):
        cond1 = is_in_group_schools(self.request.user)
        cond2 = self.request.user.schools.classes.filter(
            pk=self.kwargs['pk']).exists()
        return cond1 and cond2

    def get_context_data(self, **kwargs):
        context = super(ClassDetailView, self).get_context_data(**kwargs)
        myclass = get_object_or_404(Class, pk=self.kwargs['pk'])
        context["student_list"] = myclass.students.all()
        return context


class ClassListView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    model = Class
    template_name = "schools/manage_class.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['class_list'] = self.request.user.schools.classes.all()
        return context

    def test_func(self):
        cond1 = is_in_group_schools(self.request.user)
        return cond1


class MealDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Meal
    context_object_name = 'meal'
    template_name = "schools/meal_detail.html"

    def test_func(self):
        cond1 = is_in_group_schools(self.request.user)
        cond2 = self.request.user.schools.meals.filter(
            pk=self.kwargs['pk']).exists()
        return cond1 and cond2

# class MealCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
#     model = Meal
#     fields = '__all__'
#     template_name = "schools/todays-meal.html"
#     success_url: reverse_lazy('schools:dashboard')

#     def test_func(self):
#         cond1 = is_in_group_schools(self.request.user)
#         return cond1

#     def form_invalid(self, form):
#         calpro=return_calories_proteins(form.fields['meal_pic'])
#         print(form.errors)
#         meal_pic=form.cleaned_data['meal_pic']
#         print(meal_pic)
#         return render(self.request,'schools/todays-meal2.html',{'form':form,'calories':calpro['calories'],'proteins':calpro['proteins'],'error':form.errors,'meal_pic':meal_pic})

#     def form_valid(self, form):
#         form.instance.school = self.request.user.schools
#         print('this validity')
#         return super().form_valid(form)
    
# class MealCreateView2(LoginRequiredMixin, UserPassesTestMixin, CreateView):
#     model = Meal
#     fields = ('school','name','date','meal_pic')
#     template_name = "schools/todays-meal.html"
#     success_url: reverse_lazy('schools:todays_meal2')

#     def test_func(self):
#         cond1 = is_in_group_schools(self.request.user)
#         return cond1

#     def form_valid(self, form):
#         print('this validity')
#         calpro=return_calories_proteins(form.fields['meal_pic'])
#         return super().form_valid(form)

class StudentCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Student
    form_class = StudentForm
    template_name = "schools/register_new_students.html"

    def test_func(self):
        cond1 = is_in_group_schools(self.request.user)
        return cond1

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['current_class'].queryset = self.request.user.schools.classes.all()
        return form

# class StudentDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
#     model = Student
#     template_name = "schools/student_detail.html"
#     context_object_name = 'student'
 
#     def test_func(self):
        
#         return cond1 and cond2   
    

class register_stu(APIView):
    def post(self,request,*args, **kwargs) :
        print(request.data)
        serializer=studentSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'profile created'},status=status.HTTP_201_CREATED)
        return Response({'msg':serializer.errors},status=status.HTTP_403_FORBIDDEN)
    
    def get(self,request,*args, **kwargs):
        return Response({'msg':'Hi ! You can proceed to Resgister'},status=status.HTTP_200_OK)
    
class Meal_add(APIView):
    def post(self,request,*args, **kwargs):
        data=request.data
        if data['calories'] and data['protiens']:
            serializer=Mealserializers(data=data)
            data['school']=17
            if serializer.is_valid():
                serializer.save()
                return Response({'msg':'Your meal has been added!!!'},status=status.HTTP_201_CREATED)
            return Response({'some error':serializer.errors},status=status.HTTP_200_OK)
        else:
            calpro=return_calories_proteins(data['meal_pic'])
            print(data['meal_pic'])
            return Response({'calories':calpro['calories'],'proteins':calpro['proteins'],'name':data['name'],'meal_pic':data['meal_pic']},status=status.HTTP_200_OK)
        
        
    def get(self,request,*args, **kwargs):
        return Response({'msg':'yo user'},status=status.HTTP_200_OK)
    
class profile_get(APIView):
    def get(self,request,*args, **kwargs):
        cond1 = is_in_group_schools(self.request.user)
        print(self.kwargs['pk'])
        mystudent = Student.objects.get(id=self.kwargs['pk'])
        serialized_data=studentSerializers(mystudent)
        cond2 = mystudent.current_class.school.user == self.request.user
        print(serialized_data)
        return Response({'msg':serialized_data.data},status=status.HTTP_200_OK)
    
    def put(self,request,*args, **kwargs):
        data=request.data
        serializer=studentSerializers(id=self.kwargs['pk'],data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'successfully edited!!'},status=status.HTTP_200_OK)
        return Response({'msg':serializer.errors},status=status.HTTP_201_CREATED)
    
class attendance(APIView):
    def get(self,request,*args, **kwargs):
        stu=Student.objects.all()
        print(stu)
        serializer=Attendanceserializer(stu, many=True)
        print(serializer.data)
        return Response({'msg':serializer.data},status=status.HTTP_200_OK)
    