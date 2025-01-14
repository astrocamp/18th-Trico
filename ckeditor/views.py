from django.http import JsonResponse
from django.conf import settings
import os


from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core.files.storage import default_storage


@csrf_exempt
def file_upload_view(request):
    if request.method == "POST" and request.FILES.get("upload"):
        file = request.FILES["upload"]
        file_path = os.path.join(settings.MEDIA_ROOT, "uploads", file.name)
        file_url = os.path.join(settings.MEDIA_URL, "uploads", file.name)
        default_storage.save(file_path, file)

        default_storage.save(file_path, file)
        file_url = default_storage.url(file_path)  # 確保返回正確的圖片 URL
        
        return JsonResponse({
            "url": file_url,
            "uploaded": True,
        })

    return JsonResponse({"uploaded": False, "error": {"message": "Invalid upload request"}})





def file_browse_view(request):
    upload_dir = os.path.join(settings.MEDIA_ROOT, "uploads")
    files = []

    if os.path.exists(upload_dir):
        for file_name in os.listdir(upload_dir):
            file_url = os.path.join(settings.MEDIA_URL, "uploads", file_name)
            files.append({
                "url": file_url,
                "name": file_name
            })

    return JsonResponse({"files": files})

