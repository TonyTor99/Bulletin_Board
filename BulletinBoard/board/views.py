from django.core.cache import cache
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils.timezone import now
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView

from .models import Ad, Response
from .forms import AdForm


def welcome(request):
    return render(request, 'welcome.html')


class AdList(ListView):
    model = Ad
    ordering = '-created_at'
    template_name = 'ad_list.html'
    context_object_name = 'ads'
    paginate_by = 5

    def get_queryset(self):
        search_query = self.request.GET.get('search', '')
        queryset = super().get_queryset()

        if search_query:
            queryset = queryset.filter(title__iregex=search_query)

        return queryset


class MyAdList(ListView):
    model = Ad
    ordering = '-created_at'
    template_name = 'my_ads.html'
    context_object_name = 'ads'
    paginate_by = 5

    def get_queryset(self):
        user = self.request.user
        return Ad.objects.filter(author=user.profile.id).order_by(self.ordering)

    def get_object(self, *args, **kwargs):
        obj = cache.get(f'product-{self.kwargs["pk"]}', None)

        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'product-{self.kwargs["pk"]}', obj)
        return obj


class AdDetail(DetailView):
    model = Ad
    template_name = 'ad_detail.html'
    context_object_name = 'ad'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ad = context['ad']
        user_response = Response.objects.filter(ad=ad, author__user=self.request.user).exists()
        context['user_response'] = user_response
        return context

    def get_object(self, *args, **kwargs):
        obj = cache.get(f'ad-{self.kwargs["pk"]}', None)

        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'ad-{self.kwargs["pk"]}', obj)
        return obj


class AdCreate(CreateView):
    model = Ad
    form_class = AdForm
    success_url = reverse_lazy('ad_list')
    template_name = 'ad_create.html'

    def form_valid(self, form):  # Объявление автором авторезированного пользователя
        form.instance.author = self.request.user.profile
        return super().form_valid(form)


class AdUpdate(UpdateView):
    model = Ad
    form_class = AdForm
    success_url = reverse_lazy('ad_list')
    template_name = 'ad_update.html'


class AdDelete(DeleteView):
    model = Ad
    template_name = 'ad_delete.html'
    success_url = reverse_lazy('ad_list')

    def get_object(self, queryset=None):
        ad = super().get_object(queryset)
        # Проверка, что текущий пользователь является автором или администратором
        if ad.author.user != self.request.user and not self.request.user.is_staff:
            raise PermissionDenied("У вас нет прав для удаления этого объявления")
        return ad


class MyResponses(ListView):
    model = Response
    ordering = '-created_at'
    template_name = 'my_responses.html'
    context_object_name = 'responses'

    def get_queryset(self):
        ads = Ad.objects.filter(author=self.request.user.profile)
        return Response.objects.filter(ad__in=ads).order_by(self.ordering)

    def post(self, request, *args, **kwargs):
        # Проверка действий подтверждения или удаления отклика
        response_id = request.POST.get('response_id')
        action = request.POST.get('action')

        if not response_id or not action:
            return redirect('my_responses')  # Если что-то не так, возвращаем на страницу откликов

        response = get_object_or_404(Response, id=response_id)

        # Если отклик не принадлежит автору объявления, запрещаем
        if response.ad.author.user != request.user:
            return PermissionDenied("У вас нет прав для выполнения этого действия")

        if action == 'accept':
            response.is_accepted = True
            response.save()

        elif action == 'delete':
            response.delete()

        return redirect('my_responses')


def ad_response(request, pk):  # Создание отклика
    ad = get_object_or_404(Ad, id=pk)

    if request.method == 'POST':
        text = request.POST.get('response_text')

        Response.objects.create(
            ad=ad,
            author=request.user.profile,
            created_at=now(),
            content=text
        )
        return redirect('ad_detail', pk=ad.id)
    else:
        return render(request, 'ad_detail', {'ad': ad})
