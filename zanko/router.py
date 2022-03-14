from books.api.viewsets import BookViewSet
from chapters.api.viewsets import ChapterViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register('books', BookViewSet)
router.register('books/<int:pk>/', BookViewSet)
router.register('chapters', ChapterViewSet)