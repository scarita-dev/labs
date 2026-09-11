from django.db import models


class Exam(models.Model):
    """Examen compuesto por varias preguntas."""
    title = models.CharField(
        max_length=200,
        verbose_name="título",
        help_text="Título del examen (máx. 200 caracteres)."
    )
    description = models.TextField(
        blank=True,
        verbose_name="descripción",
        help_text="Descripción opcional del examen."
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="fecha de creación"
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "examen"
        verbose_name_plural = "exámenes"

    def __str__(self):
        return self.title


class Question(models.Model):
    """Pregunta perteneciente a un examen."""
    exam = models.ForeignKey(
        Exam,
        on_delete=models.CASCADE,
        related_name="questions",
        verbose_name="examen"
    )
    text = models.CharField(
        max_length=255,
        verbose_name="enunciado"
    )
    score = models.PositiveIntegerField(
        default=1,
        verbose_name="puntaje"
    )

    class Meta:
        ordering = ["id"]
        verbose_name = "pregunta"
        verbose_name_plural = "preguntas"

    def __str__(self):
        return f"{self.exam.title} - {self.text[:50]}"


class Choice(models.Model):
    """Opción de respuesta de una pregunta."""
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name="choices",
        verbose_name="pregunta"
    )
    text = models.CharField(
        max_length=255,
        verbose_name="texto de la opción"
    )
    is_correct = models.BooleanField(
        default=False,
        verbose_name="¿es correcta?"
    )

    class Meta:
        ordering = ["id"]
        verbose_name = "opción"
        verbose_name_plural = "opciones"

    def __str__(self):
        return self.text