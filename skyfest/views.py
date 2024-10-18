from django.shortcuts import render
import os, secrets, string
import pandas as pd
import qrcode
from django.conf import settings
from django.templatetags.static import static
from django.http import JsonResponse
from django.shortcuts import render
from PIL import Image
from .models import Attendee

# Create your views here.
def generate_random_string(length=9):
    characters = string.ascii_letters + string.digits
    return ''.join(secrets.choice(characters) for _ in range(length))

def merge_qr_with_invite(invite_path, qr_code_path, output_path, qr_size=(140, 140), padding=(30, 80)):
    invite_img = Image.open(invite_path)
    qr_code_img = Image.open(qr_code_path)
    qr_code_img = qr_code_img.resize(qr_size)

    invite_width, invite_height = invite_img.size
    qr_width, qr_height = qr_code_img.size
    position = (padding[0], invite_height - qr_height - padding[1])

    invite_img.paste(qr_code_img, position, qr_code_img)
    invite_img.save(output_path)

def index(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        attendee_phone = request.POST.get('attendee_phone')
        parent_phone = request.POST.get('parent_phone')
        address = request.POST.get('address')
        pickup_location = request.POST.get('pickup_location')
        
        qr_code = generate_random_string(9)

        qr_content = f"SkYFest-Invite/{qr_code}/{first_name} {last_name}/"
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=2,
        )
        qr.add_data(qr_content)
        qr.make(fit=True)
        
        qr_image = qr.make_image()

        # Save the QR code image to path
        save_dir = os.path.join(settings.BASE_DIR, 'skyfest', 'static', 'qr_codes')
        os.makedirs(save_dir, exist_ok=True)
        qr_code_filename = f"{qr_code}.png"
        qr_code_path = os.path.join(save_dir, qr_code_filename)
        qr_image.save(qr_code_path)

        invite_path = os.path.join(settings.BASE_DIR, 'skyfest', 'static', 'img', 'invite.jpg')
        qr_code_path = os.path.join(settings.BASE_DIR, 'skyfest', 'static', 'qr_codes', f'{qr_code}.png')
        output_path = os.path.join(settings.BASE_DIR, 'skyfest', 'static', 'merged', f'{first_name}_{last_name}_{qr_code}.jpg')
        merge_qr_with_invite(invite_path, qr_code_path, output_path, qr_size=(140, 140), padding=(30, 80))
        
        Attendee.objects.create(
            first_name=first_name,
            last_name=last_name,
            attendee_phone=attendee_phone,
            parent_phone=parent_phone,
            address=address,
            pickup_location=pickup_location,
            qr_code=qr_code
        )
        attendee_details = {
            'first_name': first_name,
            'last_name': last_name,
            'attendee_phone': attendee_phone,
            'parent_phone': parent_phone,
            'address': address,
            'picpickup_location':pickup_location,
            'merged_image_url': static(f'merged/{first_name}_{last_name}_{qr_code}.jpg')
            # 'merged_image_url': f'static/merged/{first_name}_{last_name}_{qr_code}.jpg',
        }
        return JsonResponse({'status': 200, 'attendee': attendee_details})

    return render(request, 'index.html')