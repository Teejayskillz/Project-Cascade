from django.contrib import admin
from django.contrib import messages
from .models import CustomUser, AuthorApplication

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    # Your existing admin configurations for CustomUser
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active', 'role')
    search_fields = ('username', 'email', 'first_name', 'last_name')

@admin.register(AuthorApplication)
class AuthorApplicationAdmin(admin.ModelAdmin):
    list_display = ('user', 'status', 'created_at', 'updated_at', 'get_reason_display')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username', 'user__email', 'reason')
    readonly_fields = ('user', 'reason', 'created_at', 'updated_at')

    def get_reason_display(self, obj):
        # Display a truncated version of the reason in the list view
        return obj.reason[:50] + '...' if len(obj.reason) > 50 else obj.reason
    get_reason_display.short_description = 'Reason'

    actions = ['approve_applications', 'reject_applications']

    def approve_applications(self, request, queryset):
        """
        Approves selected applications and promotes the user to an author.
        """
        for application in queryset:
            # Change the user's role to 'author'
            user = application.user
            user.role = 'author'
            user.save()
            
            # Update the application status
            application.status = 'approved'
            application.save()
            
        self.message_user(request, f"{queryset.count()} application(s) approved. Users have been promoted to author.", messages.SUCCESS)
    
    approve_applications.short_description = "Approve selected applications"
    
    def reject_applications(self, request, queryset):
        """
        Rejects selected applications.
        """
        for application in queryset:
            application.status = 'rejected'
            application.save()
            
        self.message_user(request, f"{queryset.count()} application(s) rejected.", messages.ERROR)
    
    reject_applications.short_description = "Reject selected applications"