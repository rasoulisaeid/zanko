from points.models import Point
from studies.models import Study
from bookmarks.models import Bookmark
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from zanko.permissions import JustOwner
from .serializers import StudySerializer
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
import datetime as time
import pytz


def study_order():
    # time.set_locale("fa_IR")
    date = time.datetime.now()
    order = str(date)[0:19]
    order +=("+" + str(date + time.timedelta(days=3)))
    return order


def update_data(self, request):
    # time.set_locale("fa_IR")
    study = self.get_object()
    order = study.order
    level = study.level
    function = study.function
    state = request.data.get('state')
    function += "-" + state
    if state == "1":
        if study.level != 5:
            level += 1
    else:
        level = 1

    next_study = ""
    if level == 1:
        next_study = str(time.datetime.now() + time.timedelta(days=1))[0:19]
    elif level == 2:  
        next_study = str(time.datetime.now() + time.timedelta(days=5))[0:19]
    elif level == 3:
        next_study = str(time.datetime.now() + time.timedelta(days=10))[0:19]
    elif level == 4:
        next_study = str(time.datetime.now() + time.timedelta(days=21))[0:19]
    elif level == 5:
        if study.level == 4:
            next_study = str(time.datetime.now() + time.timedelta(days=45))[0:19]
        elif study.level == 5:
            next_study = str(time.datetime.now() + time.timedelta(days=90))[0:19]

    order = order[:-19] + str(time.datetime.now())[0:19] + "+" + next_study
    
    return order, level, function    


class StudyViewSet(viewsets.ModelViewSet):
    permission_classes = [JustOwner, IsAuthenticated]
    queryset = Study.objects.all()
    serializer_class = StudySerializer

    def perform_create(self, serializer):
        point = Point.objects.get(id=self.request.data.get('point'))
        serializer.save(user=self.request.user, point=point, study_order = study_order())

    def update(self, request, *args, **kwargs):
        study = self.get_object()
        order, level, function  = update_data(self, request)
        study.order = order
        study.level = level
        study.function = function
        study.save()
        return Response({'status': status.HTTP_200_OK, "order": order, 'function': function, "level": level})

