from django.contrib import admin
from .models import Organization, Ticket, Message, Role, AdminProfile, AdminProfile



# @admin.register(Organization)
# class OrganizationAdmin(admin.ModelAdmin):
#     list_display = ('name',)
#     filter_horizontal = ('users',)


# @admin.register(AdminProfile)
# class AdminProfileAdmin(admin.ModelAdmin):
#     list_display = ('user', 'organization', 'role')
#     list_filter = ('organization', 'role')
#     search_fields = ('user__username',)


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name',)
    filter_horizontal = ('users',)


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('title', 'description', 'user__username')


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('ticket', 'sender', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('content', 'sender__username', 'ticket__title')
    raw_id_fields = ('ticket', 'sender', 'parent')


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('name', 'organization')
    filter_horizontal = ('users',)
    list_filter = ('name', 'organization')


@admin.register(AdminProfile)
class AdminProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'organization', 'role')
    list_filter = ('organization', 'role')
    search_fields = ('user__username',)