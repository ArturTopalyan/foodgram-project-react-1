from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from .filters import IngredientFilter, RecipeFilter
from .models import Ingredient, Recipe
from .permissions import AuthorOrReadOnly
from .serializers import IngredientSerializer, RecipeGetSerializer


class IngredientsViewSet(ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    filter_backends = (DjangoFilterBackend,)
    filter_class = IngredientFilter


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = (AuthorOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filter_class = RecipeFilter

    def get_serializer_class(self):
        if self.request.method in ('PUT', 'PATCH', 'POST',):
            ...
        return RecipeGetSerializer
