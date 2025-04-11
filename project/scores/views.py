from django.shortcuts import render, get_object_or_404, redirect
from scores.models import Piece, Instrument, Score
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, permission_required


@login_required
def list_pieces(request):
    if request.method == "POST":
        ### We want to change the instrument for the user
        selected = request.POST.get("instrument", None)
        instrument = get_object_or_404(Instrument, pk=selected)
        context = {
            "instruments": Instrument.objects.all().order_by("name"),
            "selected_instrument": instrument,
            "scores": Score.objects.filter(instrument=instrument).order_by(
                "piece__name"
            ),
        }

        response = render(request, "pieces/list.html", context)
        response.set_cookie("instrument_slug", instrument.slug)
        return response

    instrument_slug = request.COOKIES.get("instrument_slug", None)

    if instrument_slug:
        instrument = get_object_or_404(Instrument, slug=instrument_slug)
        context = {
            "instruments": Instrument.objects.all().order_by("name"),
            "selected_instrument": instrument,
            "scores": Score.objects.filter(instrument=instrument).order_by(
                "piece__name"
            ),
        }
        response = render(request, "pieces/list.html", context)
        return response
    else:
        # Set default instrument
        instrument = Instrument.objects.first()
        context = {
            "instruments": Instrument.objects.all().order_by("name"),
            "selected_instrument": instrument,
            "scores": Score.objects.filter(instrument=instrument).order_by(
                "piece__name"
            ),
        }
        response = render(request, "pieces/list.html", context)

        if instrument:
            # Set the cookie for the default instrument
            response.set_cookie("instrument_slug", instrument.slug)
        return response


@login_required
def view_score(request, piece_pk, instrument_slug):
    score = get_object_or_404(
        Score, piece__uuid=piece_pk, instrument__slug=instrument_slug
    )
    context = {"score": score, "instruments": Instrument.objects.all()}
    return render(request, "scores/view.html", context)


@login_required
def view_piece(request, piece_pk):
    piece = Piece.objects.get(uuid=piece_pk)
    context = {"piece": piece}
    return render(request, "pieces/view.html", context)


@login_required
def score_xml(request, piece_pk, instrument_slug):
    score = get_object_or_404(
        Score, piece__uuid=piece_pk, instrument__slug=instrument_slug
    )
    with open(score.score.path, "r") as f:
        response = HttpResponse(f.read(), content_type="application/xml")
    return response


@login_required
@permission_required("scores.add_score", raise_exception=True)
def add_piece(request):
    if request.method == "POST":
        piece = Piece()
        piece.name = request.POST.get("title")
        piece.description = request.POST.get("description", "")
        piece.save()

        for instrument_file in request.FILES.keys():
            instrument_slug = instrument_file.split("_")[0]
            instrument = get_object_or_404(Instrument, slug=instrument_slug)
            score = Score()
            score.piece = piece
            score.instrument = instrument
            score.score = request.FILES[instrument_file]
            score.save()

        return redirect("scores:list")

    context = {
        "instruments": Instrument.objects.all().order_by("name"),
    }
    return render(request, "pieces/add.html", context)
