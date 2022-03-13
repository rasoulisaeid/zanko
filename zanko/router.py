from books.api.viewsets import BookViewSet
from chapters.api.viewsets import ChapterViewSet
from auth.views import ValidatePhoneSendOTP
from rest_framework import routers

router = routers.DefaultRouter()
router.register('books', BookViewSet)
router.register('chapters', ChapterViewSet)