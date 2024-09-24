from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from website.models import SubmissionCount

class Command(BaseCommand):
    help = 'Sets the submission deadline'

    def handle(self, *args, **kwargs):
        deadline = timezone.now() + timedelta(weeks=1)
        counter, created = SubmissionCount.objects.get_or_create(pk=1)
        counter.deadline = deadline
        counter.save()
        self.stdout.write(self.style.SUCCESS(f'Successfully set deadline to {deadline}'))
