from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic.list import ListView
from django.views.generic.edit import DeleteView, UpdateView, CreateView
from decorators.check_module_permissions import check_user_permission, class_view_decorator
from roles.models import Roles
from roles.forms import new


@class_view_decorator(check_user_permission("view_roles"))
class AllRoles(ListView):
    queryset = Roles.objects.all().order_by("pk")
    template_name = "roles_permissions/roles.html"
    model = Roles
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context_data = super(AllRoles, self).get_context_data()
        return context_data


@class_view_decorator(check_user_permission("add_roles"))
class AddRoles(CreateView):
    template_name = "roles_permissions/new.html"
    model = Roles
    form_class = new.NewRule

    def get_context_data(self, **kwargs):
        context_data = super(AddRoles, self).get_context_data()
        return context_data

    def form_valid(self, form):
        form.save()
        return redirect(reverse_lazy("roles:view"))


@class_view_decorator(check_user_permission("change_roles"))
class UpdateRoles(UpdateView):
    template_name = "roles_permissions/update.html"
    form_class = new.UpdateRule

    def get_queryset(self):
        role_id = self.kwargs.get("pk")
        return Roles.objects.filter(pk=role_id)

    def form_valid(self, form):
        form.update(self.object)
        return redirect(reverse("roles:view"))

    def get_context_data(self, **kwargs):
        context_data = super(UpdateRoles, self).get_context_data()
        return context_data


@class_view_decorator(check_user_permission("delete_roles"))
class DeleteRoles(DeleteView):
    template_name = "roles_permissions/delete.html"
    model = Roles
    success_url = reverse_lazy("roles:view")
