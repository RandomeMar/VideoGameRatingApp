from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class Game(models.Model):
    name = models.CharField(max_length=200)
    rawg_id = models.IntegerField()
    release_date = models.CharField()
    img_url = models.URLField()

class Review(models.Model):
    game = models.ForeignKey(Game)
    review_text = models.TextField()
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    post_date = models.DateTimeField()
    edit_code = models.CharField