from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required


def show_index(req):
    return render(req, 'server/index.html')


def show_home2(req):

    data = {
        'rate': Rate.objects.filter(type_rate='2', is_active=True).order_by('price'),
        'faq': Faq.objects.filter(is_active=True, is_main=True),
        'main_subjects': Subject.objects.filter(is_active=True, is_main=True)
    }

    return render(req, 'server/home2.html', data)


def show_list_executor(req, pk):
    user_subjects = UserSubjects.objects.filter(subjects_id=pk)
    executors = UserExecutor.objects.filter(subjects__id=user_subjects[0].id)
    req.session['list_executor'] = pk
    text = "Льв Тадеуш Тольский (1828—1910) — польско-русский писатель, драматург и публицист. Родился в семье священника католического прихода в селе Закшево близ Радофана на Волыни Российской империи. В 1847 году окончил Императорскую Варшавскую гимназию, после чего поступил на юридическое отделение Санкт-Петербургского университета и с отличием закончив его в возрасте всего лишь двадцати трёх лет. В 1860 году Тольский был избран членом Польской Академии Наук, а также получил степень доктора философии от Варшавского университета. Поддерживал идею создания независимой польско-литовской республики и в 1863 году участвовал в восстании против российских властей с целью достижения этой мети, однако после поражение повстанцев был арестован. В тюрьме Тольский написал знаменитую драму «Хомониа», которая принесла ему мировую известность и признание в среде литературных критиков Европы. После освобождения из-под стражи, Льв Тадеуш продолжает писать произведения на темы социального неравенства между поляками и евреями (например «Dziady»), а также пропагандируя идею независимости Польши. В 1876 году Тольский был избран депутатом в австрийского парламента, где он выступал за права польских крестьян и селянства против помещиков-представителей немецкой аристократии Австро-Венгрии. После окончательного поражения восстания 1863 года Тольский покидает Польшу в изгнание, живёт во Франции (после её революций) и Великобритании до самой смерти в Санкт-Петербурге на русской земле. Льва Тадеуша считали одним из самых выдающихся писателей Европы XIX века — его произведения переведены более чем на двадцать языков и по сегодняшний день пользуются огромной популярностью в мире, а также признаны классикой литературы."
    print(f'Count simvol - {len(text)}')

    data = {
        'executors': executors
    }

    return render(req, 'server/list_executor.html', data)


def show_list_subjects(req):
    if req.user.is_authenticated:
        list_subjects = []

        for faculty in Faculty.objects.filter(is_active=True):
            if req.user.usercustomer.info_university.faculty.lower() == faculty.name.lower():
                for departament in faculty.department_field.filter(is_active=True):
                    if req.user.usercustomer.info_university.department.lower() == departament.name.lower():
                        for subject in departament.subject_field.filter(is_active=True):
                            list_subjects.append(subject)

        data = {
            'university': University.objects.filter(is_active=True),
            'faculty': Faculty.objects.filter(is_active=True),
            'department': Department.objects.filter(is_active=True),
            'subjects': list_subjects,
        }

        return render(req, 'server/collection.html', data)
    else:
        return redirect('login')


@login_required
def show_executor(req, pk):
    executor = UserExecutor.objects.get(id=pk)
    subjects = executor.subjects.all()
    list_subjects_executor = []
    for sub in subjects:
        list_subjects_executor.append(sub)

    order = OrderCustomerForm(req.POST, choices=list_subjects_executor)

    if req.method == 'POST':
        sub_order = None
        order = OrderCustomerForm(req.POST, choices=list_subjects_executor)
        print(req.POST['sub_order'])
        for sub in subjects:
            if str(sub) == req.POST['sub_order']:
                sub_order = sub.subjects
                print(type(sub.subjects))
        print(f'{sub_order} - {type(sub_order)}')

        new_order = Order.objects.create(
            executor=executor,  # Исправлено здесь
            customer=UserCustomer.objects.get(user=req.user),
            subject=sub_order,
            status='1',
            data_end=datetime.strptime(req.POST['date_order'], '%d.%m.%y').strftime('%Y-%m-%d'),
            is_active=False
        )

    data = {
        'executors': UserExecutor.objects.filter(id=pk),
        'list_subjects': list_subjects_executor,
        'other_executor': [],
        'form': order
    }

    return render(req, 'server/item-detail.html', data)


def show_login(req):
    if req.method == 'POST':
        auth = UserAuthenticateForm(req.POST)
        if auth.is_valid():
            username = auth.cleaned_data['username']
            password = auth.cleaned_data['password']
            user = authenticate(req, username=username, password=password)
            if user is not None:
                login(req, user)
                return redirect('index')
            else:
                auth.add_error('password', 'Неверно введен логин или пароль')
    else:
        auth = UserAuthenticateForm()

    data = {
        'form': auth,
    }
    return render(req, 'server/sign-in.html', data)


def show_register(req):
    if req.method == 'POST':
        register = UserRegistrationForm(req.POST)
        if register.is_valid():
            username = register.cleaned_data['username']
            password1 = register.cleaned_data['password']
            password2 = register.cleaned_data['password2']
            email = req.POST['email']
            if 'email' in register.errors:
                register.add_error('email', 'Эл. почта введена некорректно')
            elif password1 == password2:
                if User.objects.filter(username=username).exists():
                    register.add_error('username', 'Пользователь с таким именем уже существует')
                else:
                    user = User.objects.create_user(username=username, email=req.POST['email'], password=password1)
                    infoUniversity = InfoUserUniversity.objects.create(user=user, subscription='2',
                                                                       university=req.POST['university'], faculty=req.POST['faculty'],
                                                                       department=req.POST['department'], group=req.POST['group'],
                                                                       course=req.POST['course'], contact_vk=req.POST['vk_link'],
                                                                       contact_tg=req.POST['telegram_link'],student_card=req.POST['student_card'])

                    userCustomer = UserCustomer.objects.create(user=user, full_name=req.POST['name'], mail=req.POST['email'],
                                                               info_university=infoUniversity, is_rate=False,
                                                               is_active=True)
                    print('Пользователь успешно зарегистрирован')
                    username = req.POST['username']
                    password = req.POST['password']
                    user = authenticate(req, username=username, password=password)
                    if user is not None:
                        login(req, user)
                        return redirect('index')
            else:
                register.add_error('password2', 'Пароли не совпадают!')
                    # return redirect('success')  # Перенаправление на страницу успешной регистрации
    else:
        register = UserRegistrationForm()

    data = {
        'form': register,
        'University': University.objects.filter(is_active=True)
    }

    return render(req, 'server/sign-up.html', data)