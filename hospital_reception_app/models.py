from django.core.urlresolvers import reverse
from django.contrib.auth.models import User


class Receptionist(User):

    def __str__(self):
        return self.first_name+" "+self.last_name+" ( "+self.username+" )"

    class Meta:
        verbose_name = "реєстратор"
        verbose_name_plural = "Peєстратори"

    def get_absolute_url(self):
        return reverse('hospital_reception_app:detail', kwargs={'pk': self.pk})

