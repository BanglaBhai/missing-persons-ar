from django.contrib import admin
from django.utils.html import format_html
from django.core.files.base import ContentFile
from .models import MissingPerson
from .flyer_generator import generate_flyer_image


@admin.register(MissingPerson)
class MissingPersonAdmin(admin.ModelAdmin):
    list_display = ['photo_thumbnail', 'name', 'age', 'last_seen_date', 'last_seen_location', 'is_active', 'upload_date', 'owner']
    list_filter = ['is_active', 'gender', 'upload_date', 'last_seen_date', 'owner']
    search_fields = ['name', 'last_seen_location', 'contact_name', 'police_case_number']
    readonly_fields = ['owner', 'upload_date', 'last_updated', 'photo_preview', 'flyer_preview']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'age', 'gender')
        }),
        ('Physical Description', {
            'fields': ('height', 'weight', 'hair_color', 'eye_color', 'distinguishing_features'),
            'classes': ('collapse',)
        }),
        ('Incident Details', {
            'fields': ('last_seen_date', 'last_seen_location', 'circumstances')
        }),
        ('Contact Information', {
            'fields': ('contact_name', 'contact_phone', 'contact_email', 'police_case_number', 'police_department')
        }),
        ('Media Files', {
            'fields': ('photo', 'photo_preview', 'digital_flyer', 'flyer_preview', 'ar_marker_image'),
            'description': 'Upload a photo. The flyer will be auto-generated when you save.'
        }),
        ('Status & Metadata', {
            'fields': ('is_active', 'notes', 'owner', 'upload_date', 'last_updated'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        # Set owner on creation
        if not change:
            obj.owner = request.user
        
        # Auto-generate flyer if photo exists
        if obj.photo:
            try:
                # Generate flyer
                flyer_buffer = generate_flyer_image(obj)
                filename = f"flyer_{obj.name.replace(' ', '_')}.png"
                
                # Save flyer to model
                obj.digital_flyer.save(filename, ContentFile(flyer_buffer.read()), save=False)
                
                self.message_user(request, f"✅ Flyer auto-generated successfully for {obj.name}!", level='SUCCESS')
            except Exception as e:
                self.message_user(request, f"⚠️ Could not auto-generate flyer: {str(e)}", level='WARNING')
        
        super().save_model(request, obj, form, change)
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(owner=request.user)
    
    def has_change_permission(self, request, obj=None):
        if obj is None:
            return True
        if request.user.is_superuser:
            return True
        return obj.owner == request.user
    
    def has_delete_permission(self, request, obj=None):
        if obj is None:
            return True
        if request.user.is_superuser:
            return True
        return obj.owner == request.user
    
    def photo_thumbnail(self, obj):
        if obj.photo:
            return format_html(
                '<img src="{}" style="width: 50px; height: 50px; object-fit: cover; border-radius: 5px;" />',
                obj.photo.url
            )
        return "-"
    photo_thumbnail.short_description = "Photo"
    
    def photo_preview(self, obj):
        if obj.photo:
            return format_html(
                '<img src="{}" style="max-width: 300px; max-height: 300px; border-radius: 10px;" />',
                obj.photo.url
            )
        return "No photo uploaded"
    photo_preview.short_description = "Photo Preview"
    
    def flyer_preview(self, obj):
        if obj.digital_flyer:
            file_url = obj.digital_flyer.url
            return format_html(
                '<img src="{}" style="max-width: 300px; border-radius: 10px;" /><br><a href="{}" target="_blank" style="display:inline-block;margin-top:10px;padding:10px 20px;background:#417690;color:white;text-decoration:none;border-radius:5px;">📥 Download Flyer</a>',
                file_url,
                file_url
            )
        return "No flyer (will be auto-generated when you save with a photo)"
    flyer_preview.short_description = "Flyer Preview"
    
    actions = ['mark_as_inactive', 'mark_as_active', 'regenerate_flyers']
    
    def mark_as_inactive(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f"{updated} record(s) marked as inactive.")
    mark_as_inactive.short_description = "Mark selected as inactive"
    
    def mark_as_active(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f"{updated} record(s) marked as active.")
    mark_as_active.short_description = "Mark selected as active"
    
    def regenerate_flyers(self, request, queryset):
        count = 0
        for obj in queryset:
            if obj.photo:
                try:
                    flyer_buffer = generate_flyer_image(obj)
                    filename = f"flyer_{obj.name.replace(' ', '_')}.png"
                    obj.digital_flyer.save(filename, ContentFile(flyer_buffer.read()), save=True)
                    count += 1
                except Exception as e:
                    self.message_user(request, f"Error regenerating flyer for {obj.name}: {str(e)}", level='ERROR')
        self.message_user(request, f"✅ Regenerated {count} flyer(s) successfully!")
    regenerate_flyers.short_description = "🔄 Regenerate flyers for selected"