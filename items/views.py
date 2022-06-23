from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.urls import reverse_lazy
from django.shortcuts import render
from django.views.generic import TemplateView, ListView, FormView, DeleteView, UpdateView, DetailView, CreateView
from django.db.models import Q
from django.contrib.auth.decorators import (
    login_required,
    permission_required,
)

from items.models import Company, Item, Unit, Category
from items.forms import CompanyModelForm


def items(request):
    items_list = Item.objects.all()
    page = request.GET.get('page', 1)

    paginator = Paginator(items_list, 10)
    try:
        items_list = paginator.page(page)
    except PageNotAnInteger:
        items_list = paginator.page(1)
    except EmptyPage:
        items_list = paginator.page(paginator.num_pages)
    return render(
        request,
        template_name='items/items.html',
        context={'items': items_list},
    )


class ItemCreateView(CreateView):
    model = Item
    template_name = "form.html"
    fields = "__all__"
    success_url = reverse_lazy("items_app:items-list-view")


class CompanyUpdateView(UpdateView):
    model = Company
    fields = "__all__"
    template_name = "form.html"
    success_url = reverse_lazy("items_app:company-list-view")


class ItemUpdateView(UpdateView):
    model = Item
    fields = "__all__"
    exclude = ("registration_date", )
    template_name = "form.html"
    success_url = reverse_lazy("items_app:items-list-view")


class CompanyDeleteView(DeleteView):
    model = Company
    template_name = "items/delete.html"
    success_url = reverse_lazy("items_app:companies-template-view")


class ItemDeleteView(DeleteView):
    model = Item
    template_name = "items/delete.html"
    success_url = reverse_lazy("items_app:items-list-view")


class CompanyTemplateView(TemplateView):
    template_name = "items/companies.html"
    extra_context = {"companies": Company.objects.all()}


class CompanyDetailView(DetailView):
    model = Company
    template_name = "items/my_company.html"


class ItemDetailView(DetailView):
    model = Item
    template_name = "items/my_item.html"


class CompanyListView(ListView):
    # permission_required =
    template_name = "items/list_view.html"
    model = Company


class ItemListView(ListView):
    template_name = "items/list_view.html"
    model = Item


class CompanyModelFormView(FormView):
    template_name = "form.html"
    form_class = CompanyModelForm
    success_url = reverse_lazy('items_app:company-template-view')

    def form_valid(self, form):
        result = super().form_valid(form)
        form.save()
        return result


def index(request):
    return render(
        request,
        template_name="items/index.html"
    )


@permission_required("units.view_units", raise_exception=True)
@login_required
def units(request):
    return render(
        request,
        template_name="units/units.html",
        context={"units": Unit.objects.all()}
    )


class UnitCreateView(CreateView):
    model = Unit
    template_name = "form.html"
    fields = "__all__"
    success_url = reverse_lazy("items_app:units-list-view")


class UnitDeleteView(DeleteView):
    model = Unit
    template_name = "units/delete_units.html"
    success_url = reverse_lazy("items_app:units-list-view")


class UnitDetailView(DetailView):
    model = Unit
    template_name = "units/my_units.html"


class UnitListView(ListView):
    model = Unit
    template_name = "units/list_view_units.html"


class UnitUpdateView(UpdateView):
    model = Unit
    fields = ("unit", "description")
    template_name = "form.html"
    success_url = reverse_lazy("items_app:units-list-view")


@permission_required("units.view_category", raise_exception=True)
@login_required
def category(request):
    return render(
        request,
        template_name="category/category.html",
        context={"category": Category.objects.all()}
    )


class CategoryCreateView(CreateView):
    model = Category
    template_name = "form.html"
    fields = "__all__"
    success_url = reverse_lazy("items_app:category-list-view")


class CategoryDeleteView(DeleteView):
    model = Category
    template_name = "category/delete_category.html"
    success_url = reverse_lazy("items_app:category-list-view")


class CategoryDetailView(DetailView):
    model = Category
    template_name = "category/my_category.html"


class CategoryListView(ListView):
    model = Category
    template_name = "category/list_view_category.html"


class CategoryUpdateView(UpdateView):
    model = Category
    fields = ("name", "description")
    template_name = "form.html"
    success_url = reverse_lazy("items_app:category-list-view")


class SearchResultsView(ListView):
    model = Item
    template_name = "items/items_search.html"

    def get_queryset(self):
        query = self.request.GET.get("q")
        object_list = Item.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )
        return object_list
