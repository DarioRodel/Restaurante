from django.db import models

# Modelo Chef
class Chef(models.Model):
    name = models.CharField(max_length=100)
    specialty = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# Modelo Restaurant
class Restaurant(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# Modelo Recipe
class Recipe(models.Model):
    title = models.CharField(max_length=200)
    preparation_time = models.IntegerField()  # Tiempo en minutos
    chef = models.ForeignKey(Chef, on_delete=models.CASCADE)
    restaurants = models.ManyToManyField(Restaurant)

    def __str__(self):
        return self.title

# Modelo RecipeStats
class RecipeStats(models.Model):
    recipe = models.OneToOneField(Recipe, on_delete=models.CASCADE)
    total_orders = models.IntegerField()
    positive_reviews = models.IntegerField()

    def __str__(self):
        return f"Estadísticas de {self.recipe.title}"

# Modelo RestaurantConfig
class RestaurantConfig(models.Model):
    restaurant = models.OneToOneField(Restaurant, on_delete=models.CASCADE)
    settings = models.JSONField()

    def __str__(self):
        return f"Configuración de {self.restaurant.name}"
