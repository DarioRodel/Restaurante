from gestion.models import Chef, Recipe, Restaurant

#Creacion de funcion de añadir chefs
def anadir_chefs():
    chefs=[
        Chef(name="Gordon Ramsay",specialty="Cocina francesa")
    ]
#Creacion de funcion de añadir recetas
def anadir_recetas():
    gordon = Chef.objects.get(name="Gordon Ramsay")
    recipes = [
        Recipe(title="Beef Wellington", preparation_time=120, chef=gordon)
    ]
    Recipe.objects.bulk_create(recipes)
    beef_wellington = Recipe.objects.get(title="Beef Wellington")
    hells_kitchen = Restaurant.objects.get(name="Hell's Kitchen")
    savoy = Restaurant.objects.get(name="The Savoy Grill")
    beef_wellington.restaurants.add(hells_kitchen, savoy)
#Creacion de funcion de añadr restaurantes
def anadir_restaurantes():
    restaurantes = [
        Restaurant(name="Hell's Kitchen", location="Londres"),
        Restaurant(name="The Savoy Grill", location="Londres"),
    ]