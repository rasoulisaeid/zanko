from books.api.viewsets import BookViewSet
from chapters.api.viewsets import ChapterViewSet
from categories.api.viewsets import CategoryViewSet
from points.api.viewsets import PointViewSet
from bookmarks.api.viewsets import BookmarkViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register('categories', CategoryViewSet)
router.register('categories/<int:pk>/', CategoryViewSet)
router.register('books', BookViewSet)
router.register('books/<int:pk>/', BookViewSet)
router.register('chapters', ChapterViewSet)
router.register('chapters/<int:pk>/', ChapterViewSet)
router.register('points', PointViewSet)
router.register('points/<int:pk>/', PointViewSet)
router.register('bookmarks', BookmarkViewSet)
router.register('bookmarks/<int:pk>/', BookmarkViewSet)