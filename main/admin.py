from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.core.management import call_command
from .models import (
    Gender, BloodGroup, Condition, Medication, Surgery, Allergy,
    CustomUser, DoctorProfile, PatientProfile,
    PatientCondition, PatientMedication, PatientSurgery
)

# ➕ Admin Action՝ train մոդելը
@admin.action(description="Train face recognition model")
def train_model_action(modeladmin, request, queryset):
    call_command("train_face_model")
    modeladmin.message_user(request, "✅ Face model training complete.")

# ➕ Մեր UserAdmin դասը CustomUser-ի համար
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = (
        "username", "email", "first_name", "last_name",
        "is_staff", "date_of_birth", "gender", "phone_number",
    )
    list_filter = ("is_staff", "is_superuser", "gender", "is_active")
    search_fields = ("username", "email", "first_name", "last_name", "phone_number")
    ordering = ("id",)
    actions = [train_model_action]  # ← Ավելացրու մեր train գործողությունը

# Մնացած մոդելների գրանցում
admin.site.register(Gender)
admin.site.register(BloodGroup)
admin.site.register(Condition)
admin.site.register(Medication)
admin.site.register(Surgery)
admin.site.register(Allergy)
admin.site.register(DoctorProfile)
admin.site.register(PatientProfile)
admin.site.register(PatientCondition)
admin.site.register(PatientMedication)
admin.site.register(PatientSurgery)
