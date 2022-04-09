from books.api.viewsets import BookViewSet
from chapters.api.viewsets import ChapterViewSet
from points.api.viewsets import PointViewSet
from bookmarks.api.viewsets import BookmarkViewSet
from tags.api.viewsets import TagViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register('books', BookViewSet)
router.register('books/<int:pk>/', BookViewSet)
router.register('chapters', ChapterViewSet)
router.register('chapters/<int:pk>/', ChapterViewSet)
router.register('points', PointViewSet)
router.register('points/<int:pk>/', PointViewSet)
router.register('bookmarks', BookmarkViewSet)
router.register('bookmarks/<int:pk>/', BookmarkViewSet)
router.register('tags', TagViewSet)
router.register('tags/<int:pk>/', TagViewSet)
router.register('tags/<int:pk>/points', TagViewSet)
router.register('tags/<int:pk>/set_tag', TagViewSet)