from zanko.api.viewsets import BookViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register('books', BookViewSet)