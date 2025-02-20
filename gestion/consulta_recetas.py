from gestion import models
from gestion.models import Recipe, Chef, Restaurant

#2.Creamos la query para filtrar por la palabra beef,otro para convertir el primero en lista y por ultimo para ordenarlo por tiempo de preparacion
recipes_beef = Recipe.objects.filter(title__icontains="Beef")
recipes_list = list(recipes_beef)
recipes_results = recipes_beef.order_by("preparation_time")#No se ejecuta la primera query porque recipes_results esta basada en la primera query solo se ejecuta cuando lo necesitemos

#3.Creamos la query para el tiempo de preparación esté entre 30 y 90 minutos,tambien para que su titulo se chocolate y por ultimo la query de especialidad francesa
recipes_in_range = Recipe.objects.filter(preparation_time__range=(30,90))
recipes_chocolate = Recipe.objects.filter(title__startswith="Chocolate")
recipes_no_french = Recipe.objects.exclude(chef__specialty="Cocina francesa")

#4.Creamos una query para encontrar todas las recetas del restaurante de londres,una lista de los chefs que tienen una receta  en "Hell's Kitchen",query para los restaurantes que tienen más de 5 recetas en su menú
recipes_london = Recipe.objects.filter(restaurants__location="Londres")
chefs_hells_kitchen = Chef.objects.filter(recipe__restaurants__name="Hell's Kitchen").distinct()
restaurants_5_recipes = Restaurant.objects.annotate(num_recipes=models.Count("recipe")).filter(num_recipes__gt=5)

