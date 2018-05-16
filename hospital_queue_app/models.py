from django.db import models
from django.contrib.auth.models import AbstractBaseUser

# Статуси пацієнта
PATIENT_STATUSES = (
    (1, "Звичайний"),
    (2, "VIP"),
    (3, "Нагальний"),
)

# Стани пацієнта
PATIENT_STATES = (
    (1, "відсутній"),
    (2, "відійшов"),
    (3, "в черзі"),
    (4, "очікування"),
    (5, "на процедурах"),
)


# Модель що забезпечує список пацієнтів
class Patient(AbstractBaseUser):
    USERNAME_FIELD = 'email'
    email = models.EmailField(max_length=255, verbose_name="Електронна адреса", unique=True)
    surname = models.CharField(max_length=255, verbose_name="Прізвище")
    name = models.CharField(max_length=255, verbose_name="Ім'я")
    father_name = models.CharField(max_length=255, verbose_name="По-Батькові")
    date_of_birth = models.DateField(verbose_name="Дата народження")
    phone = models.CharField(max_length=20, verbose_name="Номер мобільного")
    patient_status = models.IntegerField(choices=PATIENT_STATUSES, default=1)
    patient_present_state = models.SmallIntegerField(verbose_name="Стан присутністі пацієнта", default=1,
                                                     choices=PATIENT_STATES)
    patient_present_time = models.DateTimeField(verbose_name="Час появи в черзі", auto_now_add=True)
    balance_of_funds = models.FloatField(verbose_name="Баланс коштів", default=0.0)

    class Meta:
        verbose_name_plural = "Пацієнти"
        verbose_name = "пацієнт"

    def __str__(self):
        return self.surname + " " + self.name + " " + self.father_name

    def get_short_name(self):
        return self.surname+" "+self.name

    def get_full_name(self):
        return self.surname + " " + self.name+" "+self.father_name


# Модель що забезпечує список кабінетів
class Cabinet(models.Model):
    name = models.CharField(max_length=100, verbose_name="Назва кабінету")
    number = models.CharField(max_length=15, verbose_name="Номер кабінету")
    floor = models.CharField(max_length=10, verbose_name="Поверх")

    class Meta:
        verbose_name_plural = "Кабінети"
        verbose_name = "кабінет"

    def __str__(self):
        return self.name


# Модель що використовується для визначення професії лікаря
class Profession(models.Model):
    profession_name = models.CharField(max_length=255, verbose_name="Назва професії")
    profession_description = models.TextField(blank=True, verbose_name="Повний опис професії", null=True)

    class Meta:
        verbose_name_plural = "Професії"
        verbose_name = "професія"

    def __str__(self):
        return self.profession_name


# Модель для лікарів
class Doctor(AbstractBaseUser):
    USERNAME_FIELD = 'email'
    surname = models.CharField(max_length=255, verbose_name="Прізвище")
    name = models.CharField(max_length=255, verbose_name="Ім'я")
    father_name = models.CharField(max_length=255, verbose_name="По-Батькові")
    profession = models.ForeignKey(Profession, on_delete=models.SET_NULL, blank=True, null=True)
    cabinet = models.ForeignKey(Cabinet, on_delete=models.SET_NULL, blank=True, null=True)
    email = models.EmailField(max_length=255, verbose_name="Електронна адреса", unique=True)

    class Meta:
        verbose_name_plural = "Лікарі"
        verbose_name = "лікар"

    def __str__(self):
        return self.surname + " " + self.name + " " + self.father_name + " - " + self.profession.profession_name

    def get_short_name(self):
        return self.surname+" "+self.name

    def get_full_name(self):
        return self.surname + " " + self.name+" "+self.father_name


class Procedure(models.Model):
    name = models.CharField(max_length=100, verbose_name="Назва процедури")
    doctors = models.ManyToManyField(Doctor, verbose_name="Лікарі які проводять процедуру")
    incompatible_procedures = models.ManyToManyField('Procedure', verbose_name="Несумісні процедури", blank=True)
    available_to_registrars = models.BooleanField(verbose_name="Дана професія є доступною для реєстраторів",
                                                  default=False)
    cost = models.FloatField(verbose_name="Вартість процедури", default=0.0)

    class Meta:
        verbose_name_plural = "Проседури"
        verbose_name = "процедура"

    def __str__(self):
        return self.name


# Купа всіх черг
class Heap(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, verbose_name="Пацієнт")
    procedure = models.ForeignKey(Procedure, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Процедура")
    procedure_count = models.SmallIntegerField(verbose_name="Кількість сеансів", default=1)
    procedure_finished_count = models.SmallIntegerField(verbose_name="Кількість завершених сеансів",
                                                        default=0)
    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        verbose_name="Лікар",
        # limit_choices_to={"id": 1}
    )
    creation_time = models.DateTimeField(verbose_name="Час додавання в чергу", auto_now_add=True, blank=True)
    first_seance_time = models.DateTimeField(verbose_name="Час сеансу", auto_now_add=True, blank=True)

    class Meta:
        verbose_name_plural = "Записи"
        verbose_name = "запис"
        unique_together = ('patient', 'procedure',)

    def __str__(self):
        return str(self.patient) + " - " + str(self.procedure)


class HistoryHeap(Heap):
    class Meta:
        verbose_name_plural = "Історія записів"
        verbose_name = "виконаний запис"
