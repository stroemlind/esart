from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from cart.context import cart_contents
from .models import Poster, Motive
from .forms import PosterForm


def posters_all_view(request):
    """
    A view to render the Poster product page
    """

    posters = Poster.objects.all()
    template = 'posters/posters-page.html'
    query = None
    motives = None

    if request.GET:
        if 'motive' in request.GET:
            motives = request.GET['motive'].split(',')
            posters = posters.filter(motive__name__in=motives)
            motives = Motive.objects.filter(name__in=motives)

        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(
                    request,
                    "You need to enter something to search for"
                )
                return redirect(reverse('posters'))

            queries = Q(
                name__icontains=query) | Q(description__icontains=query)
            posters = posters.filter(queries)

    context = {
        'posters': posters,
        'search': query,
        'motives_atm': motives,
    }

    return render(request, template, context)


def poster_detail(request, poster_id):
    """
    A view to show individual poster details
    """

    poster = get_object_or_404(Poster, pk=poster_id)
    cart = cart_contents(request)
    template = 'posters/poster-detail.html'
    liked = False

    if poster.like.filter(id=request.user.id).exists():
        liked = True

    context = {
        'poster': poster,
        'cart': cart,
        'liked': liked,
    }

    return render(request, template, context)


def like_poster(request, pk):
    """
    The function to determine the view if a user has liked a post or not
    """
    poster = get_object_or_404(Poster, pk=pk)

    if poster.like.filter(id=request.user.id).exists():
        poster.like.remove(request.user)
    else:
        poster.like.add(request.user)

    return redirect(reverse('poster-detail', args=[pk]))


@login_required
def posters_liked(request):
    """
    The function to determine the view if a user has liked a post or not
    """
    # Get the user
    user = get_object_or_404(User, username=request.user)
    # Find their likes by their user id
    likes = Poster.objects.filter(like=user.id)

    template = 'posters/liked_posters.html'
    context = {
        'likes': likes,
    }

    return render(request, template, context)


@login_required
def add_poster(request):
    """
    The view and function for adding new poster to the site
    """
    if not request.user.is_superuser:
        messages.error(
            request,
            'Invalid! Are you sure you are a staff member?'
        )
        return redirect(reverse('home'))
    poster_form = PosterForm(request.POST, request.FILES or None)
    if request.method == 'POST':
        if poster_form.is_valid:
            poster_form.save()
            messages.success(request, 'Poster added successfully!')
            return HttpResponseRedirect(reverse('posters'))
        else:
            messages.error(
                request,
                'Failed to add poster. Please check if the form is valid'
            )
    else:
        poster_form = PosterForm

    template = 'posters/add-poster.html'
    context = {
        'poster_form': poster_form,
    }

    return render(request, template, context)


@login_required
def edit_poster(request, id):
    """
    The function and view for edit poster
    """
    if not request.user.is_superuser:
        messages.error(
            request,
            'Invalid! Are you sure you are a staff member?'
        )
        return redirect(reverse('home'))
    poster = get_object_or_404(Poster, id=id)
    if request.method == 'POST':
        poster_form = PosterForm(request.POST, request.FILES, instance=poster)
        if poster_form.is_valid:
            poster_form.save()
            messages.success(request, 'Poster updated successfully!')
            return redirect(reverse('posters'))
        else:
            messages.error(
                request,
                'Failed to add poster. Please check if the form is valid'
            )
    else:
        poster_form = PosterForm(instance=poster)
        messages.info(request, f'You are editing {poster.name}')

    template = 'posters/edit-poster.html'
    context = {
        'poster_form': poster_form,
        'poster': poster,
    }

    return render(request, template, context)


@login_required
def delete_poster(request, id):
    """
    The view and function for deleteing a poster
    """
    if not request.user.is_superuser:
        messages.error(
            request,
            'Invalid! Are you sure you are a staff member?'
        )
        return redirect(reverse('home'))
    poster = get_object_or_404(Poster, id=id)
    poster.delete()
    messages.success(request, f'Poster {poster.name} successfully deleted!')
    return redirect(reverse('posters'))
