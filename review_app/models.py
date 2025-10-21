from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
import secrets
import string

# Create your models here.
class Game(models.Model):
    name = models.CharField(max_length=200)
    rawg_id = models.IntegerField()
    release_date = models.DateField()
    img_url = models.URLField()

class Review(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE) # If Game is deleted, all reviews are also deleted. Also creates game_id
    review_text = models.TextField()
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    post_date = models.DateTimeField()
    edit_code = models.CharField(max_length=12)
    
    def gen_edit_code(self):
        alphabet = string.ascii_letters + string.digits
        return ''.join(secrets.choice(alphabet) for i in range(12))