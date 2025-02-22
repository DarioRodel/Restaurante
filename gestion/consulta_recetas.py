from django.db.models import Count, F

from gestion.models import Chef, Recipe, Restaurant, RecipeStats

"""
1. Creación de chef con su especialidad,
creamos receta con su tiempo de preparación creada por chef Gordon,
creamos dos restaurantes en Londres y
añadimos la receta a los restaurantes.
"""

gordon = Chef(name="Gordon Ramsay", specialty="Cocina francesa")
gordon.save()
beef_wellington = Recipe(title="Beef Wellington", preparation_time=120, chef=gordon)
beef_wellington.save()
hells_kitchen = Restaurant(name="Hell's Kitchen", location="Londres")
hells_kitchen.save()
savoy_grill = Restaurant(name="The Savoy Grill", location="Londres")
savoy_grill.save()
beef_wellington.restaurants.add(hells_kitchen, savoy_grill)

"""
2. Creamos la query para filtrar por la palabra "beef",
otro para convertir el primero en lista y 
por último para ordenarlo por tiempo de preparación.
"""
recipes = Recipe.objects.filter(title__icontains="Beef")
recipes_list = list(recipes)
recipes_results = recipes.order_by(
    "preparation_time")  # No se ejecuta la primera query porque recipes_results está basada en la primera query, solo se ejecuta cuando lo necesitemos.

""" 
3. Creamos la query para el tiempo de preparación esté entre 30 y 90 minutos,
también para que su título sea "Chocolate" y
por último la query de especialidad francesa.
"""
recipes_time = Recipe.objects.filter(preparation_time__range=(30, 90))
recipes_chocolate = Recipe.objects.filter(title__startswith="Chocolate")
recipes_no_french = Recipe.objects.exclude(chef__specialty="Cocina francesa")

""" 
4. Creamos una query para encontrar todas las recetas del restaurante de Londres,
una lista de los chefs que tienen una receta en "Hell's Kitchen",
query para los restaurantes que tienen más de 5 recetas en su menú.
"""
recipes_london = Recipe.objects.filter(restaurants__location="Londres")
chefs_hells_kitchen = Chef.objects.filter(recipe__restaurants__name="Hell's Kitchen").distinct()
restaurants_5_recipes = Restaurant.objects.annotate(num_recipes=Count("recipe")).filter(num_recipes__gt=5)

"""
5.Filtrar las recetas que tienen mas opiniones positivas,
incremento el numero de pedidos para las recetas 10 veces,
calcular el porcentaje de opiniones positivas para cada receta.
"""
recipes_more_reviews = RecipeStats.objects.filter(positive_reviews__gt=F('total_orders'))
RecipeStats.objects.update(total_orders=F('total_orders') + 10)
RecipeStats.objects.update(positive_review_percentage=100 * F('positive_reviews') / F('total_orders'))