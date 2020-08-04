from django.core.management.base import BaseCommand
from honeypot_dashboard.command.base import BaseCommands
from rules.models import RuleSource, Tools


class Command(BaseCommand, BaseCommands):

    def __init__(self):
        super(Command, self).__init__()
        BaseCommands.__init__(self, database="default")

    def handle(self, *args, **options):
        try:
            # Handling Rule Source
            self.stdout.write(self.style.WARNING('Handling Rule Source Table'))
            self.truncate_table("rule_src")
            RuleSource.objects.bulk_create([
                RuleSource(name="Subex"),
                RuleSource(name="ET")
            ])
            self.stdout.write(self.style.SUCCESS('Successfully created Rule Source Table'))
            # Handling Tools
            self.stdout.write(self.style.WARNING('Handling Tools Table'))
            self.truncate_table("tools")
            Tools.objects.bulk_create([
                Tools(name="Snort"),
                Tools(name="Yara")
            ])
            self.stdout.write(self.style.SUCCESS('Successfully created Tools Table'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(str(e)))
