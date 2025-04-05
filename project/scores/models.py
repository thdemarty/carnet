from django.db import models
from django.urls import reverse
import uuid


class Piece(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    name = models.CharField(max_length=100)
    comment = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Instrument(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField()

    def __str__(self):
        return self.name


class Score(models.Model):
    piece = models.ForeignKey(Piece, on_delete=models.CASCADE)
    instrument = models.ForeignKey(Instrument, on_delete=models.CASCADE)
    score = models.FileField(upload_to="uploads/")

    def get_absolute_url(self):
        return reverse("scores:score", args=[self.piece.uuid, self.instrument.slug])

    def get_xml_url(self):
        return reverse("scores:score_xml", args=[self.piece.uuid, self.instrument.slug])

    def __str__(self):
        return f"{self.piece} - {self.instrument}"
