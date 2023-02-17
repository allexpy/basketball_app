# Third-party
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

# Local
from accounts.models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ("email",)

    def save(self, commit=True):
        user = super(CustomUserCreationForm, self).save(commit=False)
        if commit:
            user.save()
        return user


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = "__all__"

    def save(self, commit=True):
        user = super(CustomUserChangeForm, self).save(commit=False)
        if commit:
            user.save()
        return user


class CustomUserAdmin(UserAdmin):
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    list_display = ("email", "first_name", "last_name", "is_superuser", "type")
    list_filter = ["is_staff", "is_superuser", "is_active"]
    ordering = ("email",)
    search_fields = ("email",)
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "email",
                    "first_name",
                    "last_name",
                    "password",
                    "is_superuser",
                    "is_staff",
                    "is_active",
                    "type",
                    "groups",
                    "user_permissions",
                    "last_login",
                    "date_joined",
                )
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "fields": (
                    "email",
                    "first_name",
                    "last_name",
                    "password1",
                    "password2",
                    "is_superuser",
                    "is_staff",
                    "is_active",
                    "type",
                    "groups",
                    "user_permissions",
                    "last_login",
                    "date_joined",
                )
            },
        ),
    )


admin.site.register(CustomUser, CustomUserAdmin)
