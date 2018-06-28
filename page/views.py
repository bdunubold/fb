
import facebook

from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from django.views.generic import TemplateView
from django.views.generic import ListView


@method_decorator(login_required(redirect_field_name='home'), name='dispatch')
class HomeView(TemplateView):
    template_name = 'page/home.html'


class PageListView(TemplateView):
    template_name = 'page/pagelist.html'

    def get_context_data(self, **kwargs):
        context = super(PageListView, self).get_context_data(**kwargs)
        accounts = self.FBGraphPageList()
        context['page_list'] = accounts
        return context


    def FBGraphPageList(self):
        user = self.request.user
        social = user.social_auth.get(provider='facebook')
        extra_data = social.extra_data
        access_token = extra_data.get('access_token')
        graph = facebook.GraphAPI(access_token=access_token, version="2.11")

        accounts = graph.request('me/accounts', method='GET')
        return [{'id': each.get('id'), 'category': each.get('category'), 'name': each.get('name')} for each in accounts.get('data')]



class PageDetailView(TemplateView):
    template_name = 'page/pagedetail.html'

    def get_context_data(self, **kwargs):
        context = super(PageDetailView, self).get_context_data(**kwargs)
        page_id = kwargs.get('id')
        context['page_data'] = self.FbPageDetail(page_id)
        return context


    def FbPageDetail(self, page_id):
        user = self.request.user
        social = user.social_auth.get(provider='facebook')
        extra_data = social.extra_data
        access_token = extra_data.get('access_token')
        graph = facebook.GraphAPI(access_token=access_token, version="2.11")
        page = graph.get_object(id=page_id, fields="about,category,description,fan_count,is_published,name,picture")
        return page
