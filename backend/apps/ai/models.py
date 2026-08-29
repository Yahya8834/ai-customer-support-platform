from django.db import models
from django.db.models import Q




class LLMModel(models.Model):
    key = models.CharField(max_length=100,unique=True,)
    display_name = models.CharField(max_length=100,)
    description = models.TextField()
    strength = models.CharField(max_length=100,)
    provider = models.CharField(max_length=100,)
    model_name = models.CharField(max_length=100,)
    input_price_per_1k_tokens = models.DecimalField(max_digits=10,decimal_places=6,default=0,)
    output_price_per_1k_tokens = models.DecimalField(max_digits=10,decimal_places=6,default=0,)
    is_active = models.BooleanField(default=True,)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["is_active"],
                condition=Q(is_active=True),
                name="only_one_active_llm_model",
            ),
        ]

    def __str__(self):
        return self.display_name
    
