from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from auth_api.models import User
# Register your models here.

class UserAdmin(BaseUserAdmin):
  # The fields to be used in displaying the User model.
  # These override the definitions on the base UserAdmin
  # that reference specific fields on auth.User.
  list_display = ["id" ,"name", "email","tc", "is_admin"]
  list_filter = ["is_admin"]
  fieldsets = [
      ("User Credentials", {"fields": ["email", "password"]}),
      ("Personal info", {"fields": ["name"]}),
      ("Permissions", {"fields": ["is_admin" , "tc"]}),
  ]
  # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
  # overrides get_fieldsets to use this attribute when creating a user.
  add_fieldsets = [
      (
          None,
          {
              "classes": ["wide"],
              "fields": ["name", "email", "tc", "password1", "password2"],
          },
      ),
  ]
  search_fields = ["email"]
  ordering = ["email", "id"]
  filter_horizontal = []


# Now register the new UserAdmin...
admin.site.register(User, UserAdmin)