

from multiprocessing import context
from urllib import request
from django.shortcuts import render
from rest_framework.viewsets import ViewSet
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from Api.models import Todo
from Api.serializers import RegistrationSerializer, TodoSerializer
from rest_framework.decorators import action
from django.contrib.auth.models import User
from rest_framework import authentication,permissions

# Create your views here.
class TodoView(ViewSet):
    def list(self,request,*args,**kw):
        qs=Todo.objects.all()
        se=TodoSerializer(qs,many=True)
        return Response(data=se.data)
    
    def create(self,request,*args,**kw):
        se=TodoSerializer(data=request.data)
        if se.is_valid():
            se.save()
            return Response(data=se.data)
        else:
            return Response(data=se.errors)

    def retrieve(self,request,*args,**kw):
        id=kw.get("pk")
        qs=Todo.objects.get(id=id)
        se=TodoSerializer(qs,many=False)
        return Response(data=se.data)

    def destroy(self,request,*args,**kw):
        id=kw.get("pk")
        Todo.objects.get(id=id).delete()
        return Response(data="deleted")

    def update(self,request,*args,**kw):
        id=kw.get("pk")
        obj=Todo.objects.get(id=id)
        se=TodoSerializer(data=request.data,instance=obj)
        if se.is_valid():
            se.save()
            return Response(data=se.data)
        else:
            return Response(data=se.errors)


class TodoModelViews(ModelViewSet):
    authentication_classes=[authentication.BasicAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    # def create(self, request, *args, **kwargs):
    #     se=TodoSerializer(data=request.data)
    #     if se.is_valid():
    #         Todo.objects.create(**se.validated_data,user=request.user)
    #         return Response(data=se.data)
    #     else:
    #         return Response(data=se.errors)
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    # def list(self, request, *args, **kwargs):
    #     qs=Todo.objects.filter(user=request.user)
    #     se=TodoSerializer(qs,many=True)
    #     return Response(data=se.data)
    def get_queryset(self):
        return Todo.objects.filter(user=self.request.user)


    def create(self, request, *args, **kwargs):
        se=TodoSerializer(data=request.data,context={"user":request.user})
        if se.is_valid():
            se.save()
            return Response(data=se.data)
        else:
            return Response(data=se.errors)
    



    queryset=Todo.objects.all()
    serializer_class=TodoSerializer
    
    #localhost:8000/api/v1/todo/pending_todo/
    #get
   
    @action(methods=["GET"],detail=False)
    def pending_todo(self,*args,**kw):
        qs=Todo.objects.filter(status=False)
        se=TodoSerializer(qs,many=True)
        return Response(data=se.data)

    #localhost:8000/api/v1/todo/completed_todo/
    #get
   
    @action(methods=["GET"],detail=False)
    def completed_todo(self,*args,**kw):
        qs=Todo.objects.filter(status=True)
        se=TodoSerializer(qs,many=True)
        return Response(data=se.data)
        
    @action(methods=["POST"],detail=True)
    def mark_as_done(self,request,*args,**kw):
        id=kw.get("pk")
        #Todo.objects.filter(id=id).update(status=True)
        obj=Todo.objects.get(id=id)
        obj.status=True
        obj.save()
        se=TodoSerializer(obj,many=False)
        return Response(data=se.data)

class UsersView(ModelViewSet):
    serializer_class=RegistrationSerializer
    queryset=User.objects.all()

    def  create(self, request, *args, **kwargs):
        se=RegistrationSerializer(data=request.data)
        if se.is_valid():
            usr=User.objects.create_user(**se.validated_data)
            return Response(data=se.data)
        else:
            return Response(data=se.errors)