from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic import ListView
from .models import *
from .forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
import datetime
from django.contrib import auth


# --------- списки ------------

def home(request):
    par = {
        'header': 'Home'
    }
    return render(request, 'home.html', context=par)

# список товаров
class ProdactsView(ListView):
    model = Prodact
    template_name = 'prodact_list.html'
    context_object_name = 'prodacts_list'

    paginate_by = 6

    #context['customer'] = auth.get_user(self.request).username
    def get_context_data(self, **kwargs):
        context = super(ProdactsView, self).get_context_data(**kwargs)
        context['isAuth'] = auth.get_user(self.request).username
        if context['isAuth'] !='':
            context['customer'] = models.Customer.objects.get(user=self.request.user)

        return context


# список заказов
class OrderView(ListView):
    model = Order
    template_name = 'order_list.html'
    context_object_name = 'order_list'
    paginate_by = 9

    def get_context_data(self, **kwargs):
        context = super(OrderView, self).get_context_data(**kwargs)

        context['isAuth'] = auth.get_user(self.request).username
        if context['isAuth'] != '':
            context['customer'] = models.Customer.objects.get(user=self.request.user)

        print(self)
        return context


    def get_queryset(self):
        try:
            cust = models.Customer.objects.get(user=self.request.user)
            qs = models.Order.objects.filter(user=cust)
            print(qs)
        except:
            qs = None
        if qs is not None:
            qs = qs.order_by('-order_date')
        return qs

# только для авторизованных пользователей
    @method_decorator(login_required(login_url='authorization'))
    def dispatch(self, request, *args, **kwargs):
       return super(OrderView, self).dispatch(request, *args, **kwargs)


# страница товара
#@login_required(login_url='authorization')
def prodact_page(request, prodact):
    context = {}
    try:
        context['prodact'] = models.Prodact.objects.get(id=prodact)
        context['category'] = context['prodact'].category.all()
        context['order_form'] = OrderForm()
        if len(context['category']) == 0:
            context['category'] = None
    except:
        context['prodact'] = None
    context['isAuth'] = auth.get_user(request).username

    if context['isAuth'] != '':
        context['customer'] = models.Customer.objects.get(user=request.user)

    return render(request, 'prodact_page.html', context)


#  добавление заказа
@login_required(login_url='authorization')
def order_add(request, prodact):
    cust = models.Customer.objects.get(user=request.user)
    prod = models.Prodact.objects.get(id=prodact)
    inits = {
             'user': '{} {}'.format(cust.last_name, cust.first_name),
             'prodact': prod.prodact_name,
             'order_date': datetime.datetime.now(),
             'number': 1,
             'order_price': prod.price }

    if request.method == "POST":
        form = OrderForm(request.POST, initial=inits)
        is_val = form.is_valid()

        print('validation: {}'.format(is_val))
        if is_val:
            data = form.cleaned_data
            if data['number']<=0:
                form.add_error('number', ['Ошибка! Количество должно быть больше нуля.'])
                is_val = False
            #data['order_date'] = timezone.now().date()
        if is_val:
            data['order_price'] = float(data['number']) * float(prod.price)
            #data = form.cleaned_data
            ord = models.Order()
            ord.user = cust
            ord.prodact = prod
            #ord.prodact = models.Prodact.objects.get(prodact_name=data['prodact'])
            ord.order_date = data['order_date']
            ord.number = int(data['number'])
            ord.order_price = float(data['order_price'])
            ord.save()
            return HttpResponseRedirect('/prodact_list')
    else:

        form = OrderForm(initial=inits)

    return render(request, 'order_add.html', {'form': form, 'customer': cust})


#  добавление товара
def prodact_add(request):
    #cust = models.Customer.objects.get(user=request.user)
    if request.method == 'POST':
        form = ProdactAddForm(request.POST, request.FILES)
        is_val = form.is_valid()
        print('validation: {}'.format(is_val))
        if is_val:
            data = form.cleaned_data
            if data['price']<=0:
                form.add_error('price', ['Цена должна быть больше нуля.'])
                is_val = False
        if is_val:
            prodact = form.save(commit=False)
            prodact.save()
            form.save_m2m()
            return HttpResponseRedirect('/prodact/'+str(prodact.id)) #/prodact_list
    else:
        form = ProdactAddForm()

    return render(request, 'prodact_add.html', {'form': form})


# --------- регистрация и авторизация ------------

# регистрация
def registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        is_val = form.is_valid()
        data = form.cleaned_data
        if data['password']!=data['password2']:
            is_val = False
            form.add_error('password2', ['Пароли должны совпадать'])
        if User.objects.filter(username=data['username']).exists():
            form.add_error('username', ['Такой логин уже занят'])
            is_val = False

        if is_val:
            data = form.cleaned_data
            user = User.objects.create_user(data['username'], data['email'], data['password'])
            cust = Customer()
            cust.user = user
            cust.first_name = data['first_name']
            cust.last_name = data['last_name']
            cust.birthday = data ['birthday']
            cust.sex = data['sex']
            cust.save()
            return HttpResponseRedirect('/authorization')
    else:
        form = RegistrationForm()

    return render(request, 'registration.html', {'form': form})


# авторизация django
def authorization(request):

    if request.method == 'POST':
        form = AuthorizationForm(request.POST)
        print(form)
        data = form.cleaned_data

        if form.is_valid():
            user = authenticate(request, username=data['username'], password=data['password'])

            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/success_authorization')
            else:
                form.add_error('username', ['Неверный логин или пароль'])
    else:
        form = AuthorizationForm()

    return render(request, 'authorization.html', {'form': form})


# успешная авторизация вручную
def success_authorization_form(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/authorization')


# успешная авторизация django
@login_required(login_url='/authorization')
def success_authorization(request):
    return HttpResponseRedirect('/')

# выход
def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')


#----ajax-----
#
def ajax_order(request):
    if request.method == "POST":
        #prodact = models.Prodact.objects.get(prodact_name=request.POST['prodact_name'])
        prodact = models.Prodact.objects.get(id=int(request.POST['prodact_id']))
        user = models.Customer.objects.get(user=models.User.objects.get(username=request.POST['username']))
        #order_date = datetime.date(int(request.POST['order_date']))
        #order_date = datetime.date(int(request.POST['year']), int(request.POST['month']), int(request.POST['day']))
        order_date = datetime.datetime.now()
        #order_date = timezone.now()
        number = int(request.POST['number'])
        order_price = float(request.POST['order_price'])

        ord = models.Order()
        ord.user = user
        ord.prodact = prodact
        ord.number = number
        ord.order_date = order_date
        ord.order_price = order_price
        ord.save()
        return HttpResponse('success')


def ajax_last_order(request):
    #prodact = models.Prodact.objects.get(prodact_name=request.GET['prodact_name'])
    prodact = models.Prodact.objects.get(id=request.GET['prodact_id'])
    #print("Pr_ID",request.GET['prodact_id'])
    customer = models.Customer.objects.get(user=models.User.objects.get(username=request.GET['username']))
    order = models.Order.objects.filter(prodact=prodact, user=customer).order_by('-order_date').all()[:5]
    print("Привет",order)
    if len(order) == 0:
        return HttpResponse('-')

    response = "<thead>" \
                    "<tr><th>Заказ</th>" \
                    "<th>Дата заказа</th>" \
                    "<th>Количество товара</th>" \
                    "<th>Стоимость заказа</th></tr>" \
               "</thead>"
    for b in order:
        response += "<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>".format(b.id, b.order_date, b.number, b.order_price)

    return HttpResponse(response)