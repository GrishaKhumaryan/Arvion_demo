from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.core.management import call_command
from .models import (
    Gender, BloodGroup, Condition, Medication, Surgery, Allergy,
    CustomUser, DoctorProfile, PatientProfile,
    PatientCondition, PatientMedication, PatientSurgery
)


@admin.action(description="Train face recognition model")
def train_model_action(modeladmin, request, queryset):
    try:
        call_command("train_face_model")
        modeladmin.message_user(request, "✅ Face model training has been successfully initiated.", level='SUCCESS')
    except Exception as e:
        modeladmin.message_user(request, f"❌ Error during model training: {e}", level='ERROR')


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    actions = [train_model_action]

    list_display = (
        "username", "email", "first_name", "last_name",
        "is_staff", "is_superuser", "is_active", "profile_image_url"
    )
    list_filter = ("is_staff", "is_superuser", "is_active", "gender")
    search_fields = ("username", "email", "first_name", "last_name")
    ordering = ("id",)

    readonly_fields = ('profile_image_url',)

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Անձնական տվյալներ", {
            "fields": (
                "first_name", "last_name", "email", "date_of_birth", "gender",
                "phone_number", "address", "emergency_contact_phone",
                "profile_picture", "profile_image_url",
            )
        }),
        ("Թույլտվություններ", {
            "fields": (
                "is_active", "is_staff", "is_superuser",
                "groups", "user_permissions"
            )
        }),
        ("Ամսաթվեր", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "username", "email", "first_name", "last_name", "password",
                "date_of_birth", "gender", "phone_number", "address", "emergency_contact_phone",
                "profile_picture",
                "is_active", "is_staff", "is_superuser"
            ),
        }),
    )


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
