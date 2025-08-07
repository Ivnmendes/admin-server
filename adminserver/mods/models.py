from django.db import models

class Mod(models.Model):
    class Meta:
        verbose_name = 'Mod'
        verbose_name_plural = 'Mods'
        ordering = ['-suggested_at']

    mod_id = models.CharField(
        max_length=50,
        unique=True,
        help_text='Insira o ID do mod.',
        primary_key=True
    )

    workshop_id = models.CharField(
        max_length=50,
        unique=True,
        help_text='Insira o ID do workshop do mod.',
    )

    STATUS_CHOICES = [
        ('enabled', 'Habilitado'),
        ('disabled', 'Desabilitado'),
    ]

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='disabled',
    )

    name = models.CharField(
        max_length=100,
        help_text='Insira o nome do mod.',
    )

    mod_link = models.URLField(
        max_length=200,
        blank=True,
        help_text='Insira o link do mod.',
    )

    suggested_by = models.ForeignKey(
        'auth.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text='Insira o nome do usuário que sugeriu o mod.',
    )

    suggested_at = models.DateTimeField(
        auto_now_add=True,
        help_text='Data e hora em que o mod foi sugerido.',
    )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('mods:mod_detail', args=[str(self.mod_id)])