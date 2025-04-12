from django.shortcuts import render, get_object_or_404
from django.http import FileResponse, Http404
from .models import GeneratedImage
from .utils import generate_image
import os
from django.conf import settings
from django.utils.timezone import now


def generate_view(request):
    if request.method == 'POST':
        prompt = request.POST.get('prompt', '').strip()

        if not prompt:
            return render(request, 'generator/generate.html', {'error': 'Prompt cannot be empty'})

        # Sanitize prompt and create output path
        sanitized_prompt = prompt[:10].replace(" ", "_")
        filename = f"{sanitized_prompt}_{int(now().timestamp())}.png"  # Unique filename
        output_path = os.path.join(settings.MEDIA_ROOT, 'generated', filename)

        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        try:
            generate_image(prompt, output_path)
        except Exception as e:
            return render(request, 'generator/generate.html', {'error': f'Error generating image: {str(e)}'})

        # Save the generated image with timestamp
        generated_image = GeneratedImage.objects.create(
            prompt=prompt,
            image=f'generated/{filename}',  # Save relative path
            timestamp=now()
        )

        return render(request, 'generator/result.html', {'image': generated_image})

    return render(request, 'generator/generate.html')


def download_image(request, image_id):
    try:
        generated_image = get_object_or_404(GeneratedImage, id=image_id)
        image_path = os.path.join(settings.MEDIA_ROOT, generated_image.image.name)

        if not os.path.exists(image_path):
            raise Http404("Image file not found.")

        return FileResponse(open(image_path, 'rb'), as_attachment=True, filename=os.path.basename(image_path))
    except GeneratedImage.DoesNotExist:
        raise Http404("Image not found.")


def history_view(request):
    # Fetch all images, ensuring only the latest image for each unique prompt is displayed
    history = GeneratedImage.objects.order_by('-id')
    unique_images = {}

    for img in history:
        image_path = os.path.join(settings.MEDIA_ROOT, str(img.image))
        if os.path.exists(image_path):  # Check if the file exists before adding to history
            if img.prompt not in unique_images:
                unique_images[img.prompt] = img

    return render(request, 'generator/history.html', {'history': unique_images.values()})