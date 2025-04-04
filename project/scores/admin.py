from django.contrib import admin
from scores.models import Piece, Score, Instrument


@admin.register(Piece)
class PieceAdmin(admin.ModelAdmin):
    list_display = ("name", "uuid")


@admin.register(Score)
class ScoreAdmin(admin.ModelAdmin):
    list_display = ("piece", "instrument")
    list_filter = ("instrument",)


@admin.register(Instrument)
class InstrumentAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
