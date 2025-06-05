# residents/views.py

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.http import JsonResponse, Http404
from django.urls import reverse
from django.contrib import messages
from .models import Resident, Transaction, Official # Make sure Transaction is imported
from .forms import ResidentForm
import json
from django.utils import timezone # If you use it in the view
from django.db.models import Case, When, Value, IntegerField
from django.views.decorators.http import require_http_methods
from django.conf import settings # For accessing settings if you choose Option 2


def get_barangay_officials_api(request):
    """
    API view to fetch active barangay officials.
    Returns a list of all active Kagawads.
    """
    officials_data = {
        'punong_barangay_name': '[Punong Barangay Name]', # Default if not found
        'kagawad_names': [],
        'sk_chairman_name': '[SK Chairwoman Name]', # Default if not found
        'treasurer_name': '[Treasurer Name]', # Default if not found
        'secretary_name': '[Secretary Name]'  # Default if not found
    }

    single_role_positions = [
        'PUNONG_BARANGAY',
        'SK_CHAIRMAN',
        'BARANGAY_TREASURER',
        'BARANGAY_SECRETARY',
    ]

    active_officials = Official.objects.filter(
        is_active=True,
        position__in=single_role_positions + ['BARANGAY_KAGAWAD']
    ).order_by('full_name') # Consider adding specific ordering logic if needed

    temp_kagawads = []

    for official in active_officials:
        name_upper = official.full_name.upper() if official.full_name else "" # Handle potential None
        if official.position == 'PUNONG_BARANGAY' and officials_data['punong_barangay_name'] == '[Punong Barangay Name]': # Take the first one if multiple (should not happen)
            officials_data['punong_barangay_name'] = name_upper
        elif official.position == 'BARANGAY_KAGAWAD':
            temp_kagawads.append(name_upper)
        elif official.position == 'SK_CHAIRMAN' and officials_data['sk_chairman_name'] == '[SK Chairwoman Name]':
            officials_data['sk_chairman_name'] = name_upper
        elif official.position == 'BARANGAY_TREASURER' and officials_data['treasurer_name'] == '[Treasurer Name]':
            officials_data['treasurer_name'] = name_upper
        elif official.position == 'BARANGAY_SECRETARY' and officials_data['secretary_name'] == '[Secretary Name]':
            officials_data['secretary_name'] = name_upper
    
    officials_data['kagawad_names'] = temp_kagawads # Assign collected Kagawads

    return JsonResponse(officials_data)


@login_required
@require_http_methods(["POST"])
def save_transaction_view(request):
    try:
        data = json.loads(request.body)

        resident_instance = None
        resident_id = data.get('resident')
        if resident_id:
            try:
                resident_instance = Resident.objects.get(pk=resident_id)
            except Resident.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': f'Resident with ID {resident_id} not found.'}, status=400)
            except ValueError:
                return JsonResponse({'status': 'error', 'message': f'Invalid Resident ID format: {resident_id}.'}, status=400)

        transaction_data = {
            'resident': resident_instance,
            'transaction_type': data.get('transaction_type'),
            'purpose': data.get('purpose'),
            'cedula_no': data.get('cedula_no'),
            'cedula_date_issued': data.get('cedula_date_issued') if data.get('cedula_date_issued') else None,
            'date_filed': data.get('date_filed') if data.get('date_filed') else timezone.now(),
            'complainant_details': data.get('complainant_details'),
            'respondent_name': data.get('respondent_name'),
            'incident_details': data.get('incident_details'),
            'reference_number': data.get('reference_number'),
            'details': json.loads(data.get('details', '{}')) if isinstance(data.get('details'), str) else data.get('details', {})
        }

        if not transaction_data['date_filed']:
            transaction_data['date_filed'] = timezone.now()
        
        if 'cedula_date_issued' in data and not data['cedula_date_issued']:
            transaction_data['cedula_date_issued'] = None

        new_transaction = Transaction(**transaction_data)
        new_transaction.full_clean()
        new_transaction.save()

        return JsonResponse({'status': 'success', 'message': 'Transaction saved successfully!', 'transaction_id': new_transaction.pk})

    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': 'Invalid JSON in request body.'}, status=400)
    except Exception as e:
        import traceback
        print("Error in save_transaction_view:")
        print(traceback.format_exc())
        return JsonResponse({'status': 'error', 'message': f'An error occurred: {str(e)}'}, status=500)


@login_required
def search_residents_ajax(request):
    query = request.GET.get('q', '')
    residents_data = []

    if query and len(query) >= 2:
        residents = Resident.objects.filter(
            Q(full_name__icontains=query)
        ).order_by('full_name')[:10]

        for resident in residents:
            residents_data.append({
                'id': resident.pk,
                'full_name': resident.full_name,
                'address': resident.address,
                'purok': resident.purok,
                'gender': resident.gender,
                'date_of_birth': resident.date_of_birth.strftime('%Y-%m-%d') if resident.date_of_birth else None,
                'civil_status_key': resident.civil_status,
                'civil_status_display': resident.get_civil_status_display(),
            })
    return JsonResponse({'residents': residents_data})


@login_required
def index(request):
    all_residents = Resident.objects.all()
    query = request.GET.get('q')

    if query:
        all_residents = all_residents.filter(
            Q(full_name__icontains=query) |
            Q(address__icontains=query) |
            Q(occupation__icontains=query)
        ).distinct()

    all_residents = all_residents.order_by('full_name')
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    if is_ajax:
        data = []
        current_path_encoded = request.get_full_path()
        for resident in all_residents:
            data.append({
                'id': resident.pk,
                'full_name': resident.full_name,
                'address': resident.address,
                'tier': resident.tier,
                'current_path': current_path_encoded,
            })
        return JsonResponse({'residents': data})
    else:
        context = {
            'residents_list': all_residents,
            'page_title': 'List of Residents',
            'query': query
        }
        return render(request, 'residents/index.html', context)


@login_required
def add_resident(request):
    if request.method == 'POST':
        form = ResidentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Resident added successfully!')
            return redirect('index')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ResidentForm()
    return render(request, 'residents/add_resident.html', {'form': form, 'page_title': 'Add New Resident'})


@login_required
def resident_detail(request, resident_id):
    try:
        resident = get_object_or_404(Resident, pk=resident_id)
    except Http404:
        messages.warning(request, f"The resident with ID {resident_id} was not found or has been deleted.")
        return redirect('index')
    context = {
        'resident': resident,
        'page_title': f'Details for {resident.full_name}'
    }
    return render(request, 'residents/resident_detail.html', context)


@login_required
def edit_resident(request, resident_id):
    try:
        resident = get_object_or_404(Resident, pk=resident_id)
    except Http404:
        messages.warning(request, f"The resident you tried to edit (ID: {resident_id}) was not found.")
        return redirect('index')

    next_url = request.GET.get('next', reverse('resident_detail', args=[resident.pk]))

    if request.method == 'POST':
        form = ResidentForm(request.POST, instance=resident)
        if form.is_valid():
            form.save()
            messages.success(request, f'{resident.full_name} updated successfully!')
            return redirect(next_url)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ResidentForm(instance=resident)
    context = {
        'form': form,
        'resident': resident,
        'page_title': f'Edit {resident.full_name}',
        'next_url': next_url
    }
    return render(request, 'residents/edit_resident.html', context)


@login_required
def delete_resident(request, resident_id):
    try:
        resident = get_object_or_404(Resident, pk=resident_id)
    except Http404:
        messages.warning(request, f"The resident you tried to delete (ID: {resident_id}) was not found.")
        return redirect('index')

    next_url_param = request.GET.get('next')
    if next_url_param and f'/residents/{resident_id}/' in next_url_param:
        next_url = reverse('index')
    elif next_url_param:
        next_url = next_url_param
    else:
        next_url = reverse('index')

    if request.method == 'POST':
        resident_name = resident.full_name
        resident.delete()
        messages.success(request, f'Resident {resident_name} deleted successfully.')
        return redirect(next_url)

    context = {
        'resident': resident,
        'page_title': f'Delete {resident.full_name}',
        'next_url': next_url
    }
    return render(request, 'residents/confirm_delete.html', context)


@login_required
def transactions_list_view(request):
    # --- Option 1: Define directly in the view (Current Implementation) ---
    barangay_name = "Biaknabato"  # Replace with your actual barangay name
    municipality_name = "La Castellana" # Replace with your actual municipality name
    province_name = "Negros Occidental" # Replace with your actual province name
    
    # Fetch Punong Barangay name for BARANGAY_CAPTAIN_NAME context variable
    # This serves as a fallback for JS or if used directly in template static parts.
    # The JS API call will try to get the most current one from Officials model.
    punong_barangay_official = Official.objects.filter(position='PUNONG_BARANGAY', is_active=True).first()
    if punong_barangay_official and punong_barangay_official.full_name:
        barangay_captain_name = punong_barangay_official.full_name.upper()
    else:
        barangay_captain_name = "MARTINEZ, JOSELITO R. JR." # Default fallback if no active PB found


    # --- Option 2: Fetch from Django Settings (settings.py) ---
    # barangay_name = getattr(settings, 'BARANGAY_NAME', '[Your Barangay Name]')
    # municipality_name = getattr(settings, 'MUNICIPALITY_NAME', '[Your Municipality Name]')
    # province_name = getattr(settings, 'PROVINCE_NAME', '[Your Province Name]')
    # barangay_captain_name = getattr(settings, 'BARANGAY_CAPTAIN_NAME', '[Your Barangay Captain Name]')

    # --- Option 3: Fetch from a Database Model (e.g., BarangayProfile) ---
    # try:
    #     # Assuming a model named BarangayProfile, and you want the first active one
    #     # current_profile = BarangayProfile.objects.filter(is_active=True).first()
    #     # if current_profile:
    #     #     barangay_name = current_profile.name
    #     #     municipality_name = current_profile.municipality
    #     #     province_name = current_profile.province
    #     # else:
    #     #     # Fallbacks if no profile found
    #     #     barangay_name = "[Your Barangay Name]"
    #     #     municipality_name = "[Your Municipality Name]"
    #     #     province_name = "[Your Province Name]"
    #
    #     # For captain, you might re-fetch or rely on the officials API.
    #     # If fetching here for context:
    #     # captain_official = Official.objects.filter(position="PUNONG_BARANGAY", is_active=True).first()
    #     # if captain_official:
    #     #     barangay_captain_name = captain_official.full_name # Adjust formatting as needed
    #     # else:
    #     #     barangay_captain_name = "[Your Barangay Captain Name]" # Fallback
    #
    # except Exception as e:
    #     # Log error, provide defaults
    #     barangay_name = "[Your Barangay Name]"
    #     municipality_name = "[Your Municipality Name]"
    #     province_name = "[Your Province Name]"
    #     barangay_captain_name = "[Your Barangay Captain Name]"


    context = {
        'page_title': 'Transactions',
        'BARANGAY_NAME': barangay_name,
        'MUNICIPALITY_NAME': municipality_name,
        'PROVINCE_NAME': province_name,
        'BARANGAY_CAPTAIN_NAME': barangay_captain_name, # For JS fallback & potential static template use
        # 'transactions': Transaction.objects.all().order_by('-date_filed') # Example
    }
    return render(request, 'residents/transactions.html', context)


@login_required
def reporting_page_view(request):
    all_residents = Resident.objects.all()
    context = {
        'page_title': 'Reporting',
        'all_residents_for_reporting': all_residents,
    }
    return render(request, 'residents/reporting.html', context)