class AuthRouter:
    route_app_labels = {'auth', 'contenttypes', 'users', 'sessions', 'roles', 'admin', 'graphs'}

    def db_for_read(self, model, **hints):
        """
        Attempts to read auth and contenttypes models go to auth_db.
        """
        if model._meta.app_label in self.route_app_labels:
            return 'subexsecure_auth'
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write auth and contenttypes models go to subexsecure_auth.
        """
        if model._meta.app_label in self.route_app_labels:
            return 'subexsecure_auth'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the auth or contenttypes apps is
        involved.
        """
        if (
            obj1._meta.app_label in self.route_app_labels or
            obj2._meta.app_label in self.route_app_labels
        ):
           return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure the auth and contenttypes apps only appear in the
        'subexsecure_auth' database.
        """
        if db == "subexsecure_auth":
            if app_label in self.route_app_labels:
                return True
            else:
                return False
        else:
            if app_label in self.route_app_labels:
                return False
            else:
                return None