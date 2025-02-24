import os
import django

# Configura el entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Restaurante.settings')
django.setup()

from gestion.models import Chef, Recipe, Restaurant, RestaurantConfig, RecipeStats
from django.db.models import Count, F

# Creación de chefs
chefs = [
    Chef(name="Gordon Ramsay", specialty="Cocina francesa"),
    Chef(name="Massimo Bottura", specialty="Cocina italiana"),
    Chef(name="Joan Roca", specialty="Cocina española"),
    Chef(name="René Redzepi", specialty="Cocina nórdica"),
    Chef(name="Heston Blumenthal", specialty="Cocina molecular")
]

Chef.objects.bulk_create(chefs)

# Obtener chefs de la base de datos
gordon = Chef.objects.get(name="Gordon Ramsay")
massimo = Chef.objects.get(name="Massimo Bottura")
joan = Chef.objects.get(name="Joan Roca")
rene = Chef.objects.get(name="René Redzepi")
heston = Chef.objects.get(name="Heston Blumenthal")

# Creación de recetas
recipes = [
    Recipe(title="Beef Wellington", preparation_time=120, chef=gordon),
    Recipe(title="Tortellini en crema de parmesano", preparation_time=90, chef=massimo),
    Recipe(title="Cordero a la brasa con hierbas", preparation_time=75, chef=joan),
    Recipe(title="Pato salvaje con bayas nórdicas", preparation_time=110, chef=rene),
    Recipe(title="Helado de huevo y beicon", preparation_time=60, chef=heston),
    Recipe(title="Tarta de chocolate con espuma de frambuesa", preparation_time=45, chef=heston),
    Recipe(title="Paella de mariscos", preparation_time=60, chef=joan),
    Recipe(title="Bacalao con musgo y hierbas", preparation_time=80, chef=rene)
]

Recipe.objects.bulk_create(recipes)

# Creación de restaurantes
restaurants = [
    Restaurant(name="Hell's Kitchen", location="Londres"),
    Restaurant(name="The Savoy Grill", location="Londres"),
    Restaurant(name="Osteria Francescana", location="Módena"),
    Restaurant(name="El Celler de Can Roca", location="Girona"),
    Restaurant(name="Noma", location="Copenhague"),
    Restaurant(name="The Fat Duck", location="Bray"),
    Restaurant(name="DiverXO", location="Madrid"),
    Restaurant(name="Tickets", location="Barcelona")
]

Restaurant.objects.bulk_create(restaurants)

# Obtener restaurantes y recetas de la base de datos
hells_kitchen = Restaurant.objects.get(name="Hell's Kitchen")
savoy = Restaurant.objects.get(name="The Savoy Grill")
osteria = Restaurant.objects.get(name="Osteria Francescana")
celler = Restaurant.objects.get(name="El Celler de Can Roca")
noma = Restaurant.objects.get(name="Noma")
fat_duck = Restaurant.objects.get(name="The Fat Duck")
diverxo = Restaurant.objects.get(name="DiverXO")
tickets = Restaurant.objects.get(name="Tickets")

beef_wellington = Recipe.objects.get(title="Beef Wellington")
tortellini = Recipe.objects.get(title="Tortellini en crema de parmesano")
cordero = Recipe.objects.get(title="Cordero a la brasa con hierbas")
pato = Recipe.objects.get(title="Pato salvaje con bayas nórdicas")
helado = Recipe.objects.get(title="Helado de huevo y beicon")
tarta = Recipe.objects.get(title="Tarta de chocolate con espuma de frambuesa")
paella = Recipe.objects.get(title="Paella de mariscos")
bacalao = Recipe.objects.get(title="Bacalao con musgo y hierbas")

# Asociar recetas a restaurantes
beef_wellington.restaurants.add(hells_kitchen, savoy)
tortellini.restaurants.add(osteria)
cordero.restaurants.add(celler)
pato.restaurants.add(noma)
helado.restaurants.add(fat_duck)
tarta.restaurants.add(fat_duck)
paella.restaurants.add(diverxo)
bacalao.restaurants.add(noma, tickets)

# Creación de estadísticas de recetas
stats = [
    RecipeStats(recipe=beef_wellington, total_orders=500, positive_reviews=450),
    RecipeStats(recipe=tortellini, total_orders=300, positive_reviews=280),
    RecipeStats(recipe=cordero, total_orders=250, positive_reviews=230),
    RecipeStats(recipe=pato, total_orders=200, positive_reviews=180),
    RecipeStats(recipe=helado, total_orders=150, positive_reviews=140),
    RecipeStats(recipe=tarta, total_orders=100, positive_reviews=90),
    RecipeStats(recipe=paella, total_orders=400, positive_reviews=370),
    RecipeStats(recipe=bacalao, total_orders=220, positive_reviews=200)
]

RecipeStats.objects.bulk_create(stats)

# Creación de configuraciones de restaurantes
configs = [
    RestaurantConfig(
        restaurant=hells_kitchen,
        settings={
            "opening_hours": {"weekdays": "12pm-11pm", "weekends": "10am-11pm"},
            "services": ["delivery", "takeaway", "dine-in"],
            "restricted_dishes": {"alcohol": True, "pork": False}
        }
    ),
    RestaurantConfig(
        restaurant=savoy,
        settings={
            "opening_hours": {"weekdays": "1pm-10pm", "weekends": "11am-10pm"},
            "services": ["dine-in"],
            "restricted_dishes": {"alcohol": False, "pork": False}
        }
    ),
    RestaurantConfig(
        restaurant=noma,
        settings={
            "opening_hours": {"weekdays": "5pm-11pm", "weekends": None},
            "services": ["dine-in", "private events"],
            "restricted_dishes": {"alcohol": False, "shellfish": True}
        }
    ),
    RestaurantConfig(
        restaurant=fat_duck,
        settings={
            "opening_hours": {"weekdays": "2pm-9pm", "weekends": "12pm-9pm"},
            "services": ["dine-in", "catering"],
            "restricted_dishes": {"alcohol": True, "gluten": True}
        }
    ),
]

RestaurantConfig.objects.bulk_create(configs)

print("Datos poblados correctamente.")