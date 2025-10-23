from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
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
    nickname = models.CharField(default="Anonymous", max_length=20)
    title = models.CharField(max_length=60)
    review_text = models.TextField()
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    post_date = models.DateTimeField(default=timezone.now)
    edit_code = models.CharField(max_length=12, blank=True)
    
    def gen_edit_code(self):
        alphabet = string.ascii_letters + string.digits
        self.edit_code = ''.join(secrets.choice(alphabet) for i in range(12))
        
    def save(self, *args, **kwargs):
        if not self.edit_code:
            self.gen_edit_code()
        return super().save(*args, **kwargs)