from django.db import connections


class BaseCommands:

    def __init__(self, database):
        self.cursor = connections[database].cursor()

    def set_fk_check_false(self):
        self.cursor.execute("SET FOREIGN_KEY_CHECKS = 0; ")

    def set_fk_check_true(self):
        self.cursor.execute("SET FOREIGN_KEY_CHECKS = 1; ")

    def truncate_table(self, table_name):
        self.set_fk_check_false()
        self.cursor.execute(f"truncate {table_name}")
        self.set_fk_check_true()