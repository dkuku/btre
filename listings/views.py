from django.shortcuts import render, get_object_or_404
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from .models import Listing
from .choices import state_choices, bedroom_choices, price_choices


def index(request):
    listings_list = Listing.objects.order_by("-list_date").filter(
        is_published=True
    )
    paginator = Paginator(listings_list, 6)

    page = request.GET.get("page")
    listings = paginator.get_page(page)

    return render(request, "listings/listings.html", {"listings": listings})


def listing(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    return render(request, "listings/listing.html", {"listing": listing})


def search(request):
    queryset_list = Listing.objects.order_by("-list_date")

    # Keywords
    if "keywords" in request.GET:
        keywords = request.GET["keywords"]
        if keywords:
            queryset_list = queryset_list.filter(
                description__icontains=keywords
            )

    # City
    if "city" in request.GET:
        city = request.GET["city"]
        if city:
            queryset_list = queryset_list.filter(city__iexact=city)

    # State
    if "state" in request.GET:
        state = request.GET["state"]
        if state:
            queryset_list = queryset_list.filter(state__iexact=state)

    # Bedrooms
    if "bedrooms" in request.GET:
        bedrooms = request.GET["bedrooms"]
        if bedrooms:
            queryset_list = queryset_list.filter(bedrooms__gte=bedrooms)

    # Price
    if "price" in request.GET:
        price = request.GET["price"]
        if price:
            queryset_list = queryset_list.filter(price__lte=price)

    context = {
        "state_choices": state_choices,
        "bedroom_choices": bedroom_choices,
        "price_choices": price_choices,
        "listings": queryset_list,
        "values": request.GET,
    }

    return render(request, "listings/search.html", context)
