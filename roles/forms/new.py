from django import forms
from roles.models import Roles, RolePermissions


class NewRule(forms.ModelForm):
    class Meta:
        model = Roles
        fields = ["name", "description"]

    def clean(self):
        # check role exist
        data = self.cleaned_data
        name = data.get("name")
        if Roles.objects.filter(name=name):
            self.add_error("name", "This Name Already Exists")
        else:
            return data


class UpdateRule(forms.ModelForm):
    class Meta:
        model = Roles
        fields = ["name", "description"]

    def update(self, role):
        clean_data = self.cleaned_data
        if role:
            Roles.objects.filter(pk=role.id).update(**clean_data)


class NewRolePermission(forms.ModelForm):
    role_id = forms.IntegerField(widget=forms.HiddenInput, required=False)

    class Meta:
        model = RolePermissions
        fields = ["permission", "role_id"]

    def clean(self):
        super(NewRolePermission, self).clean()
        clean_data = self.cleaned_data
        permission = clean_data["permission"]
        role_id = clean_data["role_id"]
        if not permission or permission == "":
            self.add_error("permission", "Field cannot be left Null")
        check_role_permission_exist = RolePermissions.objects.filter(role__id=role_id, permission=permission)
        if check_role_permission_exist:
            self.add_error("permission", "Permission already Exists")

    def save(self, commit=True, role_id=None):
        permission = self.cleaned_data.get("permission")
        new_role_permission = RolePermissions(role_id=role_id, permission=permission)
        new_role_permission.save()
