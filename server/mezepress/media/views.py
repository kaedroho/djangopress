from django.contrib.contenttypes.models import ContentType
from meze.decorators import meze_view
from meze.response import MezeResponse

from .forms import ImageForm
from .models import MediaAsset


@meze_view
def index(request):
    assets = MediaAsset.objects.all()

    return MezeResponse(
        request,
        "MediaIndex",
        {
            "assets": [
                {
                    "title": asset.title,
                    "edit_url": reverse("media_edit", args=[post.id]),
                }
                for asset in assets
            ]
        },
        title="Media | Mezepress",
    )


@meze_view
def add(request):
    form = ImageForm()

    if form.is_valid():
        image = form.save(commit=False)
        image.media_type = ContentType.objects.get_for_model(Image)
        image.save()

    return MezeResponse(
        request,
        "ImageForm",
        {
            "form": form,
        },
    )


@meze_view
def edit(request, mediaasset_id):
    # TODO: Check media type
    image = get_object_or_404(Image, id=mediaasset_id)
    form = ImageForm()

    if form.is_valid():
        form.save()

    return MezeResponse(
        request,
        "ImageForm",
        {
            "form": form,
        },
    )


@meze_view
def delete(request, mediaasset_id):
    asset = get_object_or_404(MediaAsset, id=mediaasset_id)

    return MezeResponse(
        request,
        "CommonConfirmDelete",
        {},
    )