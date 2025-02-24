from django.db.models import Count, F
from gestion.models import Chef, Recipe, Restaurant, RecipeStats, RestaurantConfig

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
recipes_results = recipes.order_by("preparation_time")  # No se ejecuta la primera query porque recipes_results está basada en la primera query, solo se ejecuta cuando lo necesitemos.

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
from django.db.models import Count

restaurants_5_recipes = Restaurant.objects.annotate(num_recipes=Count("recipe")).filter(num_recipes__gt=5)
"""
5.Filtrar las recetas que tienen mas opiniones positivas,
incremento el numero de pedidos para las recetas 10 veces,
calcular el porcentaje de opiniones positivas para cada receta.
"""
recipes_more_reviews = RecipeStats.objects.filter(positive_reviews__gt=F('total_orders'))
RecipeStats.objects.update(total_orders=F('total_orders') + 10)
#Este mirar
RecipeStats.objects.update(positive_review_percentage=100 * F('positive_reviews') / F('total_orders'))
"""
6. Insertamos la configuración para "Hell's Kitchen" con el JSON,
filtramos las configuraciones donde el servicio "delivery" esté disponible,
filtramos los platos con alcohol  restringidos,
las configuraciones por la mañana con horario 10am y 
encontrar la configuracion que tengan mas de 2 servicios
"""
#Este mirar
hells_kitchen_config = RestaurantConfig(
    restaurant=hells_kitchen,
    settings={
        "opening_hours": {"weekdays": "12pm-11pm", "weekends": "10am-11pm"},
        "services": ["delivery", "takeaway", "dine-in"],
        "restricted_dishes": {"alcohol": True, "pork": False}
    }
)
hells_kitchen_config.save()
configs_delivery = RestaurantConfig.objects.filter(settings__services__contains="delivery")
configs_alcohol = RestaurantConfig.objects.filter(settings__restricted_dishes__alcohol=True)
configs_10am = RestaurantConfig.objects.filter(settings__opening_hours__weekends__startswith="10am")
configs_2_services = RestaurantConfig.objects.filter(settings__services__len__gt=2)

#Consulta recetas específicas atravesando relaciones con chefs y restaurantes:
"""
1.Encontrar todas las recetas creadas por un chef con una especialidad especifica
"""
recipes_especific = Recipe.objects.filter(chef__specialty="Cocina española")
"""
2.Listar todas las recetas disponibles en un restaurante en "Madrid"
"""
recipes_madrid = Recipe.objects.filter(restaurants__location="Madrid")
"""
3.Encontrar todas las recetas de un chef llamado "Gordon Ramsay" que están en el restaurante "Hell's Kitchen"
"""
recipes_gordon_hells_kitchen = Recipe.objects.filter(chef__name="Gordon Ramsay", restaurants__name="Hell's Kitchen")
"""
4.Listar todos los chefs que tienen al menos una receta en un restaurante en "Barcelona"
"""
chefs_barcelona = Chef.objects.filter(recipe__restaurants__location="Barcelona").distinct()
"""
5. Encontrar todas las recetas que tardan menos de 30 minutos y están disponibles en  "The Savoy Grill".
"""
recipes_30_mins= Recipe.objects.filter(preparation_time__lt=30, restaurants__name="The Savoy Grill")
"""
6. Obtener todas las recetas en restaurantes que tienen más de 5 recetas.
"""
recipes_restaurants_5 = Recipe.objects.filter(restaurants__in=Restaurant.objects.annotate(num_recipes=Count('recipe')).filter(num_recipes__gt=5))


#Usa F Expressions para actualizar dinámicamente las estadísticas de las recetas.
"""
1.Incrementar el número de pedidos totales en 10 para todas las recetas
"""
RecipeStats.objects.update(total_orders=F('total_orders') + 10)

"""
2.Incrementar el número de opiniones positivas en un 5%
"""
RecipeStats.objects.update(positive_reviews=F('positive_reviews') * 1.05)

"""
3.Calcular y anotar el porcentaje de opiniones positivas para cada receta.
"""
#Este mirar
RecipeStats.objects.update(positive_review_percentage=100 * F('positive_reviews') / F('total_orders'))

"""
4.Encontrar recetas que tienen más opiniones positivas que pedidos totales
"""
recipes_positive = RecipeStats.objects.filter(positive_reviews__gt=F('total_orders'))

"""
 5.Duplicar el número de pedidos totales para todas las recetas con más de 100 pedidos actualmente.
"""
RecipeStats.objects.filter(total_orders__gt=100).update(total_orders=F('total_orders') * 2)

"""
6.Resetear el número de pedidos totales y opiniones positivas para recetas que no tienen pedidos registrados
"""
RecipeStats.objects.filter(total_orders=0).update(total_orders=0, positive_reviews=0)

# Filtros avanzados en el campo JSONField.
#Este mirar
"""
1.Encontrar configuraciones de restaurantes que ofrecen servicio de "delivery".
"""
configs_deliver = RestaurantConfig.objects.filter(settings__services__contains="delivery")

"""
2.Filtrar configuraciones donde los horarios de fin de semana comiencen a las "10am".
"""
configs_weekend_10 = RestaurantConfig.objects.filter(settings__opening_hours__weekends__startswith="10am")

"""
3.Obtener configuraciones donde los platos con alcohol estén restringidos.
"""
configs_alcohol_restricted = RestaurantConfig.objects.filter(settings__restricted_dishes__alcohol=True)

"""
4.Encontrar configuraciones que tengan más de dos servicios habilitados.
"""
configs_more_2_services = RestaurantConfig.objects.filter(settings__services__len__gt=2)

#Este mirar
"""
5.Filtrar restaurantes que tengan horarios de apertura entre semana que incluyan "8am-10pm".
"""
configs_8am_10pm = RestaurantConfig.objects.filter(settings__opening_hours__weekdays__contains="8am-10pm")

"""
6.Encontrar configuraciones donde el restaurante esté cerrado los fines de semana.
"""
configs_closed = RestaurantConfig.objects.filter(settings__opening_hours__weekends=None)

"""
7.Consultar configuraciones que ofrezcan servicios específicos como "internet gratuito".
"""
configs_free_internet = RestaurantConfig.objects.filter(settings__services__icontains="internet gratuito")

"""
8.Encontrar configuraciones donde exista una sección restringida para "platos exclusivos".
"""
configs_exclusive = RestaurantConfig.objects.filter(settings__restricted_dishes__has_key="platos exclusivos")