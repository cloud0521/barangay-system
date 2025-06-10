# residents/models.py

from django.db import models
from django.core.validators import RegexValidator # Import RegexValidator
# from django.contrib.auth.models import User # No longer needed for issued_by
from django.utils import timezone

class Resident(models.Model):
    # Resident ID is automatically created by Django as an auto-incrementing primary key

    # Define choices for the gender field
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Others', 'Others'),
    ]
    # Define choices for the tier field (1 to 6)
    TIER_CHOICES = [(str(i), str(i)) for i in range(1, 7)]

    # Define choices for civil status
    CIVIL_STATUS_CHOICES = [
        ('SINGLE', 'Single'),
        ('MARRIED', 'Married'),
        ('WIDOWED', 'Widowed'),
        ('DIVORCED', 'Divorced'),
        ('SEPARATED', 'Separated'),
        ('ANNULLED', 'Annulled'),
        ('COMMON-LAW / LIVE-IN PARTNER', 'Common-law / Live-in Partner'),
    ]

    # Validator for contact information: allows only digits and '+'
    contact_validator = RegexValidator(
        regex=r'^[0-9+]*$', # Allows digits (0-9) and the plus sign (+)
        message='Contact information can only contain digits (0-9) and the plus sign (+).'
    )

    full_name = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    purok = models.CharField(max_length=225)
    religion = models.CharField(max_length=100, blank=True, null=True)
    email_address = models.EmailField(max_length=255, blank=True, null=True)
    address = models.TextField()
    place_of_birth = models.TextField()
    contact_information = models.CharField(max_length=100, blank=True, null=True, default='+63', validators=[contact_validator]) # Optional
    civil_status = models.CharField(max_length=50, choices=CIVIL_STATUS_CHOICES) # Applied new choices
    nationality = models.CharField(max_length=100, default='Filipino', blank=True, null=True)
    occupation = models.CharField(max_length=100, blank=True, null=True) # Optional
    voter_status = models.BooleanField(default=False) # True if registered voter
    tier = models.CharField( max_length=10, blank=True, null=True, choices=TIER_CHOICES )
    notes = models.TextField(blank=True, null=True) # Optional

    def __str__(self):
        return self.full_name

class Transaction(models.Model):
    """
    Model to store all barangay transactions.
    Fields like status, date_completed, issued_by, and remarks have been removed for simplification.
    Added cedula fields, renamed complainant_name to complainant_details, added incident_details, and purpose.
    """
    TRANSACTION_TYPE_CHOICES = [
        ('BARANGAY_CLEARANCE', 'Barangay Clearance'),
        ('CERTIFICATE_OF_RESIDENCY', 'Certificate of Residency'),
        ('CERTIFICATE_OF_INDIGENCY', 'Certificate of Indigency'),
        ('BLOTTER_COMPLAINT', 'Blotter/Complaint'),
        ('BUSINESS_PERMIT', 'Business Permit'),
        ('CONSTRUCTION_PERMIT', 'Construction Permit'),
        ('SENIOR_CITIZEN_ID', 'Senior Citizen ID Application'),
        ('PWD_ID', 'PWD ID Application'),
        ('OTHER', 'Other'),
    ]

    # transaction_id is automatically created by Django as an auto-incrementing primary key (id field)

    resident = models.ForeignKey(Resident, on_delete=models.SET_NULL, null=True, blank=True, related_name='transactions', help_text="The resident involved in the transaction. Optional for some types like general blotter entries not tied to a specific known resident initially.")
    transaction_type = models.CharField(max_length=50, choices=TRANSACTION_TYPE_CHOICES)
    date_filed = models.DateTimeField(default=timezone.now, help_text="Date and time when the transaction was filed/requested.")
    
    purpose = models.TextField(blank=True, null=True, help_text="Purpose of the transaction (e.g., for employment, medical assistance, local travel).")

    # Cedula information (often for clearances)
    cedula_details = models.TextField(max_length=200, blank=True, null=True, help_text="Cedula (Community Tax Certificate) Number, if applicable.")
    
    # Blotter/Complaint specific fields
    complainant_details = models.TextField(blank=True, null=True, help_text="Details of the complainant (e.g., name, address), if applicable (e.g., for blotter).")
    respondent_name = models.CharField(max_length=255, blank=True, null=True, help_text="Respondent name if applicable (e.g., for blotter).")
    incident_details = models.TextField(blank=True, null=True, help_text="Narrative or details of the incident, if applicable (e.g., for blotter). This can include place, date, and time of incident.")

    # General fields
    details = models.JSONField(default=dict, blank=True, help_text="Specific details of the transaction not covered by other fields (e.g., business type for permit, length of residency).")
    reference_number = models.CharField(max_length=100, blank=True, null=True, unique=True, help_text="Optional unique reference number for the transaction (e.g., OR Number, Document Control Number).")


    def __str__(self):
        # Updated to use complainant_details. If it's too long, you might want to truncate it or use a different field for display.
        applicant_info = self.resident.full_name if self.resident else (self.complainant_details.splitlines()[0] if self.complainant_details else 'N/A')
        return f"{self.get_transaction_type_display()} for {applicant_info} - {self.date_filed.strftime('%Y-%m-%d')}"

    class Meta:
        ordering = ['-date_filed'] # Order transactions by most recent first
        verbose_name = "Transaction"
        verbose_name_plural = "Transactions"

    # Example of how you might want to structure data in the 'details' JSONField:
    # For Barangay Clearance (if additional details are needed beyond purpose and cedula):
    # {
    #   "additional_notes": "For local employment only."
    # }
    # For Blotter (if incident_date, time, place are not part of incident_details TextField or for other structured data):
    # {
    #   "complainant_contact": "09123456789", 
    #   "respondent_address": "Purok 2",
    #   "incident_date": "2024-05-28", 
    #   "incident_time": "14:30",       
    #   "incident_place": "Market"     
    # }
    # For Business Permit:
    # {
    #   "business_name": "My Sari-Sari Store",
    #   "business_address": "Purok 3",
    #   "business_type": "Retail",
    #   "owner_name": "Juan Dela Cruz" // If owner is not the 'resident' linked
    # }
    # For Construction Permit:
    # {
    #   "construction_location": "Purok Saging",
    #   "type_of_construction": "Residential House - Two Story"
    # }
    # For Certificate of Residency:
    # {
    #  "length_of_residency_years": 5
    # }

class Official(models.Model):
    """
    Model to store information about barangay officials.
    """
    # Define choices for common barangay positions
    POSITION_CHOICES = [
        ('PUNONG_BARANGAY', 'Punong Barangay (Barangay Captain)'),
        ('BARANGAY_KAGAWAD_1', 'Barangay Kagawad 1(Barangay Councilor)'),
        ('BARANGAY_KAGAWAD_2', 'Barangay Kagawad 2(Barangay Councilor)'),
        ('BARANGAY_KAGAWAD_3', 'Barangay Kagawad 3(Barangay Councilor)'),
        ('BARANGAY_KAGAWAD_4', 'Barangay Kagawad 4(Barangay Councilor)'),
        ('BARANGAY_KAGAWAD_5', 'Barangay Kagawad 5(Barangay Councilor)'),
        ('BARANGAY_KAGAWAD_6', 'Barangay Kagawad 6(Barangay Councilor)'),
        ('BARANGAY_KAGAWAD_7', 'Barangay Kagawad 7(Barangay Councilor)'),
        ('SK_CHAIRMAN', 'SK Chairman (Sangguniang Kabataan Chairman)'),
        ('BARANGAY_SECRETARY', 'Barangay Secretary'),
        ('BARANGAY_TREASURER', 'Barangay Treasurer'),
        ('CHIEF_TANOD', 'Chief Tanod (Head of Barangay Peacekeeping Force)'),
        ('BARANGAY_TANOD', 'Barangay Tanod (Barangay Peacekeeping Officer)'),
        ('LUPON_MEMBER', 'Lupon Member (Member of the Lupong Tagapamayapa)'),
        ('BHW', 'Barangay Health Worker (BHW)'),
        ('DAY_CARE_WORKER', 'Day Care Worker'),
        ('OTHER', 'Other Official Position'),
    ]

    # id is automatically created by Django as an auto-incrementing primary key
    full_name = models.CharField(max_length=255, help_text="Full name of the official.")
    position = models.CharField(max_length=100, choices=POSITION_CHOICES, help_text="Position held by the official.")
    term_start_date = models.DateField(blank=True, null=True, help_text="Start date of the official's term.")
    term_end_date = models.DateField(blank=True, null=True, help_text="End date of the official's term (if applicable).")
    contact_number = models.CharField(max_length=20, blank=True, null=True, help_text="Contact number of the official.")
    email_address = models.EmailField(max_length=255, blank=True, null=True, help_text="Email address of the official.")
    notes = models.TextField(blank=True, null=True, help_text="Any additional notes or remarks about the official.")
    is_active = models.BooleanField(default=True, help_text="Is the official currently active in their position?")


    def __str__(self):
        return f"{self.full_name} - {self.get_position_display()}"

    class Meta:
        ordering = ['position', 'full_name'] # Order by position, then by name
        verbose_name = "Official"
        verbose_name_plural = "Officials"