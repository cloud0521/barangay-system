# residents/forms.py

from django import forms
from .models import Resident

class ResidentForm(forms.ModelForm):
    class Meta:
        model = Resident
        # List the fields you want to include in the form
        fields = [
            'full_name',
            'date_of_birth',
            'gender',
            'purok',
            'religion',
            'email_address',
            'nationality',       # Only one instance of nationality needed
            'civil_status',
            'occupation',
            'contact_information',
            'address',
            'place_of_birth',
            'notes',
            'voter_status',
            'tier',
        ]
        # You can also exclude fields instead:
        # exclude = ['field_to_exclude']

        # Optional: Add widgets to customize form field appearance (e.g., date picker)
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}), # Added a common CSS class
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'civil_status': forms.Select(attrs={'class': 'form-select'}),
            'tier': forms.Select(attrs={'class': 'form-select'}),
            # Add similar for other fields if you want consistent styling
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  # Call the parent's __init__ method first

        # Add placeholder for the full_name field
        self.fields['full_name'].widget.attrs.update({
            'placeholder': 'Last name, First name MI.',
            'class': 'form-control' # Example: adding a Bootstrap class
        })

        self.fields['address'].widget.attrs.update({
            'placeholder': 'House No., Street, Barangay, City/Municipality, Province',
            'rows': 3, # Example for TextField
            'class': 'form-control'
        })
        self.fields['place_of_birth'].widget.attrs.update({
            'placeholder': 'City/Municipality, Province',
            'class': 'form-control'
        })
        self.fields['notes'].widget.attrs.update({
            'placeholder': 'Any additional notes about the resident...',
            'rows': 3, # Example for TextField
            'class': 'form-control'
        })


    def clean(self):
        cleaned_data = super().clean()

        fields_to_uppercase = [
            'full_name',
            'purok',
            'religion', # If it's free text
            'nationality', # If it's free text
            'occupation',
            'address',
            'place_of_birth',
            'notes',
            # 'civil_status' is a choice field, its value will be the key (e.g., 'SINGLE')
            # which is already uppercase based on your model.
        ]

        for field_name in fields_to_uppercase:
            value = cleaned_data.get(field_name)
            if isinstance(value, str):  # Check if the value is a string
                cleaned_data[field_name] = value.upper()
            elif value is None and self.fields[field_name].required is False: # Handle optional fields that are None
                cleaned_data[field_name] = None # or an empty string: '' if you prefer
            elif value is None and self.fields[field_name].required is True:
                # This case should ideally be caught by field-level validation
                # but as a fallback or for specific logic:
                pass # Or raise forms.ValidationError for the specific field if needed

        # Example for contact_information: ensure it starts with +63 if not empty
        # contact_info = cleaned_data.get('contact_information')
        # if contact_info and not contact_info.startswith('+63'):
        #     # This is just an example, your RegexValidator in the model handles format
        #     # but form-level cleaning can add more specific rules.
        #     # For instance, if you want to prepend +63 if only numbers are given.
        #     # self.add_error('contact_information', "Contact should ideally start with '+63'.")
        #     pass


        return cleaned_data