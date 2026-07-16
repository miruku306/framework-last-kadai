from django.shortcuts import render, redirect, get_object_or_404
from .models import Video
from .forms import VideoForm


def video_list(request):
    """
    ビデオ一覧画面
    """

    videos = Video.objects.all()

    context = {
        "videos": videos,
        "total_count": videos.count(),
        "rented_count": sum(video.rented for video in videos),
        "out_of_stock_count": sum(1 for video in videos if video.available_stock == 0),
    }

    return render(
        request,
        "video_rental/video_list.html",
        context,
    )


def video_create(request):
    """
    ビデオ登録画面
    """

    if request.method == "POST":
        form = VideoForm(request.POST, request.FILES)

        if form.is_valid():

            video = form.save(commit=False)

            # 商品コード自動採番
            last_video = Video.objects.order_by("-id").first()

            if last_video:
                number = int(last_video.product_code[1:]) + 1
            else:
                number = 1

            video.product_code = f"V{number:04d}"

            video.save()

            return redirect("video_rental:video_list")

    else:
        form = VideoForm()

    context = {
        "form": form,
    }

    return render(
        request,
        "video_rental/video_form.html",
        context,
    )


def video_update(request, pk):
    """
    ビデオ編集
    """

    video = get_object_or_404(Video, pk=pk)

    if request.method == "POST":
        form = VideoForm(
            request.POST,
            request.FILES,
            instance=video,
        )

        if form.is_valid():
            form.save()
            return redirect("video_rental:video_list")

    else:
        form = VideoForm(instance=video)

    return render(
        request,
        "video_rental/video_form.html",
        {
            "form": form,
            "is_edit": True,
        },
    )


def video_delete(request, pk):
    """
    ビデオ削除
    """

    video = get_object_or_404(Video, pk=pk)

    if request.method == "POST":
        video.delete()
        return redirect("video_rental:video_list")

    return render(
        request,
        "video_rental/video_confirm_delete.html",
        {
            "video": video,
        },
    )
