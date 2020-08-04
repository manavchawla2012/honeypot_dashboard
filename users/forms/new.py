from django import forms
from users.models import Users
from roles.models import Roles
from users.views.password_encryption_decryption import Password


class NewUser(forms.ModelForm):
    name = forms.CharField(max_length=20, label="Username", min_length=5)
    role = forms.ModelChoiceField(queryset=Roles.objects.all(), empty_label="None", to_field_name="id", required=False)
    login_expiry = forms.CharField(widget=forms.DateTimeInput(attrs={"type": "datetime-local"}), required=False)
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Password'}), label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Repeat Password'}), label="Password Conformation")
    middle_name = forms.CharField(max_length=20, required=False)

    class Meta:
        model = Users
        fields = ["name", "email_id", "first_name", "middle_name", "last_name", "role", "login_expiry", "password1",
                  "password2"]

    def clean(self):
        return clean(self, NewUser)

    def save(self, commit=True, new_user=False):
        save(self, new_user=False)


class SignUpUser(forms.ModelForm):
    name = forms.CharField(max_length=20, label="Username", min_length=5)
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Password'}), label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Repeat Password'}), label="Password Conformation")
    middle_name = forms.CharField(max_length=20, required=False)

    class Meta:
        model = Users
        fields = ["name", "email_id", "first_name", "middle_name", "last_name", "password1",
                  "password2"]

    def clean(self):
        return clean(self, SignUpUser)

    def save(self, commit=True):
        save(self, new_user=True)


class UpdateUser(forms.ModelForm):
    name = forms.CharField(max_length=20, label="Username", min_length=5)
    role = forms.ModelChoiceField(queryset=Roles.objects.all(), empty_label="None", to_field_name="id", required=False)
    login_expiry = forms.CharField(widget=forms.DateTimeInput(attrs={"type": "datetime-local"}), required=False)
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Password'}), label="Password", required=False)
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Repeat Password'}), label="Password Conformation", required=False)
    middle_name = forms.CharField(max_length=20, required=False)

    class Meta:
        model = Users
        fields = ["name", "email_id", "first_name", "middle_name", "last_name", "role", "login_expiry", "password1",
                  "password2"]

    def clean(self):
        super(UpdateUser, self).clean()
        cleaned_data = self.cleaned_data
        password_enc = Password()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        if password1 or password2:
            password1 = password_enc.decode_password(password1)
            password2 = password_enc.decode_password(password2)
            if password1 != password2:
                self.add_error("password2", "Passwords do not match")
            else:
                cleaned_data.update(password=password1)

    def save(self, commit=True, user=None):
        clean_data = self.cleaned_data
        if user:
            password = clean_data["password"]
            login_expiry = clean_data["login_expiry"]
            user.login_expiry = None if not login_expiry else login_expiry
            Users.objects.update_user(user, password)
        pass


def clean(self, form):
    super(form, self).clean()
    clean_data = self.cleaned_data
    password_enc = Password()
    password1 = password_enc.decode_password(clean_data.get("password1"))
    password2 = password_enc.decode_password(clean_data.get("password2"))
    login_expiry = self.cleaned_data.get("login_expiry")
    if not login_expiry:
        login_expiry = None
    clean_data.update(password1=password1, password2=password2, login_expiry=login_expiry)
    if password1 != password2:
        self.add_error("password2", "Passwords do not match")
    # print(self.errors)
    return self.cleaned_data


def save(self, new_user):
    clean_data = self.cleaned_data
    password = clean_data.get("password1")
    username = clean_data.get("name")
    first_name = clean_data.get("first_name")
    middle_name = clean_data.get("middle_name")
    last_name = clean_data.get("last_name")
    role = None if new_user else clean_data.get("role")
    login_expiry = None if new_user else clean_data.get("login_expiry")
    email = clean_data.get("email_id")
    Users.objects.create_user(name=username, password=password, first_name=first_name, email=email, role=role,
                              middle_name=middle_name, last_name=last_name, login_expiry=login_expiry,
                              is_superuser=False)
