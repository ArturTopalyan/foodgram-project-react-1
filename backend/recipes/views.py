from rest_framework.viewsets import ReadOnlyModelViewSet

from .models import Ingredient
from .serializers import IngredientSerializer


class IngridientsViewSet(ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
