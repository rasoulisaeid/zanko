from books.api.viewsets import BookViewSet
from chapters.api.viewsets import ChapterViewSet
from points.api.viewsets import PointViewSet
from bookmarks.api.viewsets import BookmarkViewSet
from tags.api.viewsets import TagViewSet
from studies.api.viewsets import StudyViewSet
from purchases.api.viewsets import PurchaseViewSet
from auth.api.viewsets import UserViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register('users', UserViewSet)
router.register('users/update_user', UserViewSet)
router.register('users/user_info', UserViewSet)
router.register('books', BookViewSet)
router.register('purchases', PurchaseViewSet)
router.register('books/<int:pk>/', BookViewSet)
router.register('chapters', ChapterViewSet)
router.register('chapters/<int:pk>/', ChapterViewSet)
router.register('points', PointViewSet)
router.register('points/<int:pk>/', PointViewSet)
router.register('bookmarks', BookmarkViewSet)
router.register('bookmarks/points', BookmarkViewSet)
router.register('bookmarks/<int:pk>/', BookmarkViewSet)
router.register('tags', TagViewSet)
router.register('tags/<int:pk>/', TagViewSet)
router.register('tags/<int:pk>/points', TagViewSet)
router.register('tags/<int:pk>/set_tag', TagViewSet)
router.register('studies', StudyViewSet)
router.register('studies/<int:pk>/', StudyViewSet)