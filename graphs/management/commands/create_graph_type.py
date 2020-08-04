from django.core.management.base import BaseCommand
from graphs.models import GraphType
from honeypot_dashboard.command.base import BaseCommands


class Command(BaseCommand, BaseCommands):
    help = "Create New Roles"

    def __init__(self):
        super().__init__()
        BaseCommands.__init__(self, database="subexsecure_auth")

    def handle(self, *args, **options):
        try:
            self.truncate_table("graph_type")
            GraphType.objects.bulk_create([
                GraphType(name="Pie Chart"),
                GraphType(name="Donut Chart"),
                GraphType(name="Bar Chart"),
                GraphType(name="Comparison Chart")
            ])
            self.stdout.write(self.style.SUCCESS('Successfully created Graph Types'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(str(e)))