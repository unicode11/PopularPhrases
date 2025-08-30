import random

from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect

from .models import Quote, QuoteForm


# Create your views here.

def index(request):
    quotes_list = list(Quote.objects.all())

    if not quotes_list:
        return render(request, "main.html", {"quotes": []})

    selected_quotes = set()
    while len(selected_quotes) < 4 and quotes_list:
        selected = random.choices(
            quotes_list,
            weights=[q.weight for q in quotes_list],
            k=1
        )[0]
        selected_quotes.add(selected)

    for quote in selected_quotes:
        quote.views += 1
        quote.save(update_fields=['views'])

    return render(request, "main.html", {
        "quotes": list(selected_quotes)
    })


def vote_quote(request, quote_id, vote_type):
    session_key = request.session.session_key
    if not session_key:
        request.session.create()
        session_key = request.session.session_key

    quote = get_object_or_404(Quote, id=quote_id)

    voted = request.session.get(f"voted_{quote_id}")
    if voted:
        return JsonResponse({
            "likes": quote.likes,
            "dislikes": quote.dislikes,
            "message": "Вы уже голосовали за эту цитату!"
        })

    if vote_type == "like":
        quote.likes += 1
    elif vote_type == "dislike":
        quote.dislikes += 1
    quote.save()

    request.session[f"voted_{quote_id}"] = True

    return JsonResponse({
        "likes": quote.likes,
        "dislikes": quote.dislikes,
    })


def add_quote(request):
    titles = Quote.objects.values_list("title", flat=True).distinct()
    title_error = None

    if request.method == "POST":
        form = QuoteForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            count = Quote.objects.filter(title=title).count()
            if count >= 3:
                title_error = f"Нельзя добавлять больше 3 цитат от '{title}'"
            else:
                form.save()
                return redirect("index")
    else:
        form = QuoteForm()

    return render(request, "add_quote.html", {
        "form": form,
        "titles": titles,
        "title_error": title_error,
    })


def top(request):
    quotes = Quote.objects.order_by('-likes')[:10]
    return render(request, "top.html", {"quotes": quotes})


def check_title_limit(request):
    title = request.GET.get('title', '')
    count = Quote.objects.filter(title=title).count()
    if count >= 3:
        return JsonResponse({'limit_reached': True, 'message': f"Нельзя добавлять больше 3 цитат от '{title}'"})
    else:
        return JsonResponse({'limit_reached': False})
