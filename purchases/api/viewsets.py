from purchases.models import Purchase
from chapters.models import Chapter
from .serializers import PurchaseSerializer
from chapters.api.serializers import ChapterSerializer
from rest_framework.permissions import BasePermission, IsAuthenticated
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.decorators import api_view
from zanko.permissions import JustOwner
from auth.models import User
from books.models import Book
from studies.models import Study
from points.models import Point
import jdatetime as time
import pytz

def study_order():
    time.set_locale("fa_IR")
    timezone = pytz.timezone('Asia/Tehran')
    date = time.datetime.now(timezone)
    order = str(date)[0:19]
    order += ("+" + str(date + time.timedelta(days=1))[0:19])
    return order

class PurchaseViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated,JustOwner]
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer

    def perform_create(self, serializer):
        user = self.request.user
        book_id = self.request.data.get('book')
        book = Book.objects.get(pk=book_id)
        chapters = Chapter.objects.filter(book=book)
        for chapter in chapters:
            points = Point.objects.filter(chapter=chapter)
            for point in points:
                Study.objects.create(point=point, user=user, order=study_order())
        serializer.save(user=user, book=book)    
        
