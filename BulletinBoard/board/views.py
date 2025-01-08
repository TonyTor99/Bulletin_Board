from django.shortcuts import render
from django.urls import reverse_lazy
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
            queryset = queryset.filter(title__icontains=search_query)

        return queryset


class AdDetail(DetailView):
    model = Ad
    template_name = 'ad_detail.html'
    context_object_name = 'ad'


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


class MyResponses(ListView):
    model = Response
    ordering = '-created_at'
    template_name = 'my_responses.html'
    context_object_name = 'responses'

    def get_queryset(self):
        ads = Ad.objects.filter(author=self.request.user.profile)
        return Response.objects.filter(ad__in=ads).order_by(self.ordering)
