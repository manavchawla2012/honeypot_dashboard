from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from users.forms.new import NewUser, Users, SignUpUser, UpdateUser
from decorators.check_module_permissions import check_user_permission, class_view_decorator
from django.urls import reverse_lazy
from users.views.password_encryption_decryption import Password
from django.shortcuts import redirect


@class_view_decorator(check_user_permission("add_users"))
class CreateUser(CreateView):
    form_class = NewUser
    template_name = "users/new.html"
    success_url = reverse_lazy("view_users")
    password_enc = Password()

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):
        form.save()
        return redirect(reverse_lazy("view_users"))

    def get_context_data(self, **kwargs):
        context_data = super(CreateUser, self).get_context_data()
        context_data["public_key"] = self.password_enc.get_public_key()
        return context_data


@class_view_decorator(check_user_permission("change_users"))
class UpdateUser(UpdateView):
    form_class = UpdateUser
    template_name = "users/update.html"
    queryset = Users.objects.all()
    password_enc = Password()

    def form_valid(self, form):
        form.save(user=self.object)
        return redirect(reverse_lazy("view_users"))

    def get_context_data(self, **kwargs):
        context_data = super(UpdateUser, self).get_context_data()
        context_data["public_key"] = self.password_enc.get_public_key()
        return context_data


@class_view_decorator(check_user_permission("delete_users"))
class DeleteUser(DeleteView):
    queryset = Users.objects.all()
    success_url = reverse_lazy("view_users")
    template_name = "users/delete.html"


@class_view_decorator(check_user_permission("view_users"))
class DetailUser(DetailView):
    template_name = "users/new.html"
    queryset = Users.objects.all()


@class_view_decorator(check_user_permission("view_users"))
class AllUsers(ListView):
    model = Users
    paginate_by = 10
    template_name = "users/users.html"
    queryset = Users.objects.all().order_by("pk")

    def get_context_data(self, **kwargs):
        context = super(AllUsers, self).get_context_data()
        return context


class Setup(CreateView):
    form_class = SignUpUser
    template_name = "users/first_login.html"
    success_url = reverse_lazy("user_login")
    password_enc = Password()

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):
        form.save()
        return redirect(reverse_lazy("view_users"))

    def get_context_data(self, **kwargs):
        context_data = super(Setup, self).get_context_data()
        context_data["public_key"] = self.password_enc.get_public_key()
        return context_data
