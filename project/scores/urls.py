from django.urls import path
from scores.views import list_pieces, view_piece, view_score, score_xml

app_name = "scores"

urlpatterns = [
    path("", list_pieces, name="list"),
    path("<uuid:piece_pk>/", view_piece, name="view"),
    path("<uuid:piece_pk>/<slug:instrument_slug>/", view_score, name="score"),
    path("<uuid:piece_pk>/<slug:instrument_slug>/xml", score_xml, name="score_xml"),
]
