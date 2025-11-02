from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.utils import timezone


class MissingPerson(models.Model):
    name = models.CharField(max_length=200, verbose_name="Full Name")
    age = models.PositiveIntegerField(verbose_name="Age")
    gender = models.CharField(
        max_length=20,
        choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')],
        verbose_name="Gender"
    )
    
    height = models.CharField(max_length=50, blank=True, verbose_name="Height")
    weight = models.CharField(max_length=50, blank=True, verbose_name="Weight")
    hair_color = models.CharField(max_length=50, blank=True, verbose_name="Hair Color")
    eye_color = models.CharField(max_length=50, blank=True, verbose_name="Eye Color")
    distinguishing_features = models.TextField(blank=True, verbose_name="Distinguishing Features")
    
    last_seen_date = models.DateField(verbose_name="Last Seen Date")
    last_seen_location = models.CharField(max_length=300, verbose_name="Last Seen Location")
    circumstances = models.TextField(verbose_name="Circumstances")
    
    contact_name = models.CharField(max_length=200, verbose_name="Contact Person Name")
    contact_phone = models.CharField(max_length=50, verbose_name="Contact Phone Number")
    contact_email = models.EmailField(blank=True, verbose_name="Contact Email")
    police_case_number = models.CharField(max_length=100, blank=True, verbose_name="Police Case Number")
    police_department = models.CharField(max_length=200, blank=True, verbose_name="Police Department")
    
    photo = models.ImageField(upload_to='missing_persons/photos/%Y/%m/', verbose_name="Person's Photo")
    digital_flyer = models.FileField(
        upload_to='missing_persons/flyers/%Y/%m/',
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'jpg', 'jpeg', 'png'])],
        verbose_name="Digital Flyer",
        blank=True,
        null=True
    )
    ar_marker_image = models.ImageField(
        upload_to='missing_persons/markers/%Y/%m/',
        blank=True,
        null=True,
        verbose_name="AR Marker Image"
    )
    
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='missing_persons', verbose_name="Uploaded By")
    upload_date = models.DateTimeField(default=timezone.now, verbose_name="Upload Date")
    last_updated = models.DateTimeField(auto_now=True, verbose_name="Last Updated")
    is_active = models.BooleanField(default=True, verbose_name="Active Status")
    notes = models.TextField(blank=True, verbose_name="Internal Notes")
    
    class Meta:
        verbose_name = "Missing Person"
        verbose_name_plural = "Missing Persons"
        ordering = ['-upload_date']
    
    def __str__(self):
        return f"{self.name} - Last seen: {self.last_seen_date}"
    
    def get_physical_description(self):
        desc_parts = []
        if self.height:
            desc_parts.append(f"Height: {self.height}")
        if self.weight:
            desc_parts.append(f"Weight: {self.weight}")
        if self.hair_color:
            desc_parts.append(f"Hair: {self.hair_color}")
        if self.eye_color:
            desc_parts.append(f"Eyes: {self.eye_color}")
        return ", ".join(desc_parts) if desc_parts else f"{self.gender.title()}, {self.age} years old"