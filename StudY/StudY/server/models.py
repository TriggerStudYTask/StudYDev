from datetime import datetime

from django.contrib.auth.models import User
from django.db import models


class Rate(models.Model):
    class Meta:
        verbose_name = 'Тариф'
        verbose_name_plural = 'Тарифы'

    TYPE_FIELDS = [
        ('1', 'Исполнитель'),
        ('2', 'Заказчик'),
    ]

    type_rate = models.CharField(verbose_name='Тип тарифа', choices=TYPE_FIELDS, max_length=1)
    name = models.CharField(verbose_name='Наименование тарифа', max_length=20)
    price = models.IntegerField(verbose_name='Цена')
    advantage_1 = models.CharField(verbose_name='Преимущество 1', max_length=70)
    advantage_2 = models.CharField(verbose_name='Преимущество 2', max_length=70)
    advantage_3 = models.CharField(verbose_name='Преимущество 3', max_length=70)
    advantage_4 = models.CharField(verbose_name='Преимущество 4', max_length=70)
    advantage_5 = models.CharField(verbose_name='Преимущество 5', max_length=70)
    is_active = models.BooleanField(verbose_name='Активный', default=True)


class RateUser(models.Model):
    class Meta:
        verbose_name = 'Приобретенный тариф'
        verbose_name_plural = 'Приобретенные тарифы'

    TYPE_USER_FIELD = [
        ('1', 'Исполнитель'),
        ('2', 'Заказчик')
    ]

    type_user = models.CharField(verbose_name='Роль пользователя', choices=TYPE_USER_FIELD, max_length=1)
    # user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.PROTECT)
    rate = models.ForeignKey('Rate', verbose_name='Тариф', on_delete=models.PROTECT)
    data_start = models.DateTimeField(verbose_name='Дата начала')
    data_end = models.DateTimeField(verbose_name='Дата конца')
    count_click = models.IntegerField(verbose_name='Количество обращений', default=5)
    vip_status = models.BooleanField(verbose_name='VIP status')
    is_active = models.BooleanField(verbose_name='Активный')


class ParametersReviews(models.Model):
    class Meta:
        verbose_name = 'Параметры отзывов'
        verbose_name_plural = 'Параметры отзывов'

    polite_ratio = models.IntegerField(verbose_name='Коэффициент вежливости')
    quality_ratio = models.IntegerField(verbose_name='Коэффициент качества')
    price_ratio = models.IntegerField(verbose_name='Коэффициент соотношения цены')


class Reviews(models.Model):
    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    dsc = models.CharField(verbose_name='Отзыв', max_length=155)
    order_fields = models.ForeignKey('Order', verbose_name='Заказ', on_delete=models.PROTECT)
    polite = models.IntegerField(verbose_name='Вежливость')
    quality = models.IntegerField(verbose_name='Качество')
    price_ratio = models.IntegerField(verbose_name='Соотношение цены')
    total_rating = models.IntegerField(verbose_name='Общий рейтинг')


class Subject(models.Model):
    class Meta:
        verbose_name = 'Предмет'
        verbose_name_plural = 'Предметы'

    TYPE_FIELDS = [
        ('1', 'Лекции'),
        ('2', 'Лабораторные'),
        ('3', 'Практики'),
        ('4', 'Курсовые'),
        ('5', 'Диплом')
    ]

    name = models.CharField(verbose_name='Наименование', max_length=155)
    type = models.CharField(verbose_name='Тип предмета', choices=TYPE_FIELDS, max_length=1, default=2)
    price = models.IntegerField(verbose_name='Средняя цена', null=True, blank=True)
    count_response = models.IntegerField(verbose_name='Количество откликов')
    list_executor = models.ManyToManyField('UserExecutor', verbose_name='Список исполнителей', blank=True, null=True)
    is_active = models.BooleanField(verbose_name='Активный')
    is_main = models.BooleanField(verbose_name='Отображать на главной стр', default=False)

    def __str__(self):
        return f'{self.get_type_display()}: {self.name}'


class UserSubjects(models.Model):
    class Meta:
        verbose_name = 'Предмет исполнителя'
        verbose_name_plural = 'Предметы исполнителей'

    subjects = models.ForeignKey('Subject', verbose_name='Предмет', on_delete=models.PROTECT)
    order_field = models.ManyToManyField('Order', verbose_name='Список заказов', blank=True, null=True)
    price = models.IntegerField(verbose_name='Цена')
    # is_active = models.BooleanField(verbose_name='Активный', default=True)

    def __str__(self):
        return str(self.subjects)


class Department(models.Model):
    class Meta:
        verbose_name = 'Кафедра'
        verbose_name_plural = 'Кафедры'

    name = models.CharField(verbose_name='Наименование', max_length=155)
    subject_field = models.ManyToManyField('Subject', verbose_name='Предметы')
    is_active = models.BooleanField(verbose_name='Активный')

    def __str__(self):
        return f'{self.subject_field}: {self.name}'


class Faculty(models.Model):
    class Meta:
        verbose_name = 'Факультет'
        verbose_name_plural = 'Факультеты'

    name = models.CharField(verbose_name='Наименование', max_length=155)
    department_field = models.ManyToManyField('Department', verbose_name='Кафедры')
    is_active = models.BooleanField(verbose_name='Активный')


class University(models.Model):
    class Meta:
        verbose_name = 'Университет'
        verbose_name_plural = 'Университеты'

    name = models.CharField(verbose_name='Наименование', max_length=255)
    dsc = models.TextField(verbose_name='Описание')
    user_customer = models.ManyToManyField('UserCustomer', verbose_name='Список заказчиков', null=True, blank=True)
    user_executor = models.ManyToManyField('UserExecutor', verbose_name='Список исполнителей', null=True, blank=True)
    faculty_field = models.ManyToManyField('Faculty', verbose_name='Факультет', null=True, blank=True)
    is_active = models.BooleanField(verbose_name='Активный')


class InfoUserUniversity(models.Model):
    class Meta:
        verbose_name = 'Карточка Вуза пользователя'
        verbose_name_plural = 'Карточки Вуза пользователя'

    USER_FIELDS = [
        ('1', 'Исполнитель'),
        ('2', 'Заказчик'),
    ]

    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.PROTECT)
    subscription = models.CharField(verbose_name='Тип роли', choices=USER_FIELDS, max_length=1, default='2')
    university = models.CharField(verbose_name='Университет', max_length=255)
    faculty = models.CharField(verbose_name='Факультет', max_length=255)
    department = models.CharField(verbose_name='Кафедра', max_length=255)
    course = models.IntegerField(verbose_name='Курс')              # todo Сделать проверку на максимальное значение
    group = models.CharField(verbose_name='Шифр группы', max_length=20)
    student_card = models.ImageField(verbose_name='Студенческий билет', upload_to='info_user/student_card/%Y/%m/%d/')
    contact_vk = models.CharField(verbose_name='Ссылка ВК', max_length=155)
    contact_tg = models.CharField(verbose_name='Ссылка ТГ', max_length=155)


class Order(models.Model):
    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    STATUS_FIELD = [
        ('1', 'В ожидании'),
        ('2', 'Приступил'),
        ('3', 'Сделал'),
        ('4', 'Уточнение по заказу'),
        ('5', 'Отменен заказчиком'),
        ('6', 'Отменен исполнителем'),
        ('7', 'Гарантированный срок'),
        ('8', 'Отказ исполнителем')
    ]

    executor = models.ForeignKey('UserExecutor', verbose_name='Исполнитель', on_delete=models.PROTECT)
    customer = models.ForeignKey('UserCustomer', verbose_name='Заказчик', on_delete=models.PROTECT)
    subject = models.ForeignKey(Subject, verbose_name='Предмет', on_delete=models.PROTECT)
    # dsc = models.CharField(verbose_name='Краткое описание', max_length=500)
    # price = models.IntegerField(verbose_name='Цена', default=100, null=True, blank=True)
    status = models.CharField(verbose_name='Статус заказа', choices=STATUS_FIELD, max_length=1, default=1)
    data_start = models.DateTimeField(verbose_name='Дата начала', auto_created=True, default=datetime.now)
    data_end = models.DateTimeField(verbose_name='Дата окончания', null=True, blank=True)
    is_active = models.BooleanField(verbose_name='Активный')
    # private_key = models.CharField(verbose_name='Приватный ключ', max_length=25)


class UserCustomer(models.Model):
    class Meta:
        verbose_name = 'Заказчик'
        verbose_name_plural = 'Заказчики'

    user = models.OneToOneField(User, verbose_name='Заказчик', on_delete=models.CASCADE)
    full_name = models.CharField(verbose_name='ФИО', max_length=255)
    mail = models.EmailField(verbose_name='Эл почта')
    info_university = models.ForeignKey(InfoUserUniversity, verbose_name='Карточка Вуза заказчика',
                                        on_delete=models.PROTECT)
    rate = models.OneToOneField(RateUser, verbose_name='Тариф', on_delete=models.PROTECT, null=True, blank=True)
    is_rate = models.BooleanField(verbose_name='Наличие тарифа')
    reviews_field = models.ManyToManyField(Reviews, verbose_name='Отзывы', null=True, blank=True)
    is_active = models.BooleanField(verbose_name='Активный')


class UserExecutor(models.Model):
    class Meta:
        verbose_name = 'Исполнитель'
        verbose_name_plural = 'Исполнители'

    user = models.OneToOneField(User, verbose_name='Исполнитель', on_delete=models.CASCADE)
    login_id = models.CharField(verbose_name='LOGIN ID', max_length=5)
    login = models.CharField(verbose_name='LOGIN', max_length=15)
    photo = models.ImageField(verbose_name='Фотография', upload_to='executor/profile_photo/%Y/%m/%d/')
    full_name = models.CharField(verbose_name='ФИО', max_length=255)
    mail = models.EmailField(verbose_name='Эл почта')
    info_university = models.ForeignKey(InfoUserUniversity, verbose_name='Карточка Вуза заказчика',
                                        on_delete=models.PROTECT)
    dsc = models.TextField(verbose_name='Описание о себе')
    subjects = models.ManyToManyField('UserSubjects', verbose_name='Предметы', null=True, blank=True)
    price = models.IntegerField(verbose_name='Средняя цена', blank=True, null=True)
    rate = models.OneToOneField(RateUser, verbose_name='Тариф', on_delete=models.PROTECT, null=True, blank=True)
    is_rate = models.BooleanField(verbose_name='Наличие тарифа')
    reviews_field = models.ManyToManyField(Reviews, verbose_name='Отзывы', null=True, blank=True)
    order_field = models.ManyToManyField(Order, verbose_name='Заказы', null=True, blank=True)
    is_active = models.BooleanField(verbose_name='Активный')


class Faq(models.Model):
    class Meta:
        verbose_name = 'Популярный вопрос'
        verbose_name_plural = 'Популярные вопросы'

    question = models.CharField(verbose_name='Вопрос', max_length=100)
    ask = models.CharField(verbose_name='Ответ', max_length=500)
    is_main = models.BooleanField('Отображать на гл стр')
    is_active = models.BooleanField(verbose_name='Активный')
