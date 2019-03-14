import random

from elasticsearch_dsl import Search

from django.views.generic import View
from django.shortcuts import render
from django.urls import reverse
#from django.template.response import RequestContext

from main.models import Product
from main.forms import SearchForm

class HomeView(View):
    def get(self, request):
        form = SearchForm(request.GET)
        ctx = {
            'form': form
        }
        if form.is_valid():
            name_query = form.cleaned_data['name']
            if name_query:
                search = Search(index = 'sample_index').query('match', name = name_query)
            else:
                search = Search(index = 'sample_index')
            
            min_price = form.cleaned_data['min_price']
            max_price = form.cleaned_data['max_price']
            if max_price is not None and min_price is not None:
                price_query = {}
                if max_price is not None:
                    price_query['lte'] = max_price
                if min_price is not None:
                    price_query['gte'] = min_price
                search = search.query('range', price = price_query)

            search.aggs.bucket('categories', 'terms', field = 'category',)

            if request.GET.get('category'):
                search = search.query('match', category = request.GET['category'])

            result = search.execute()
            ctx['products'] = result.hits

            category_aggregations = list()
            for bucket in result.aggregations.categories.buckets:
                category_name = bucket.key
                doc_count = bucket.doc_count

                category_url_params = request.GET.copy()
                category_url_params['category'] = category_name
                category_url = '{}?{}'.format(
                    reverse('home'),
                    category_url_params.urlencode(),
                )

                category_aggregations.append({
                    'name' : category_name,
                    'doc_count' : doc_count,
                    'url': category_url
                })

            ctx['category_aggs'] = category_aggregations
            
        if "category" in request.GET:
            remove_category_search_params = request.GET.copy()
            del remove_category_search_params["category"]
            remove_category_url = "{}?{}".format(reverse("home"), remove_category_search_params.urlencode())
            ctx["remove_category_url"] = remove_category_url
        return render(request, 'home.html', ctx)
