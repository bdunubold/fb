
import json
import urllib.request
import facebook
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

# from api.serializers import SinglePostSerializer


def getGraph(request, given_access_token=None):
    user = request.user
    social = user.social_auth.get(provider='facebook')
    extra_data = social.extra_data
    if given_access_token:
        access_token = given_access_token
    else:
        access_token = extra_data.get('access_token')
    graph = facebook.GraphAPI(access_token=access_token, version="2.11")
    return graph



class PagePostListView(APIView):

    def get(self, request, id):

        response_data = self.FbPageDetail(id)
        return Response(response_data)

    def FbPageDetail(self, page_id):
        graph = getGraph(self.request)
        page_only_access = graph.get_object(id=page_id, fields="access_token")
        page_access_token = page_only_access.get('access_token')
        page_graph = getGraph(self.request, page_access_token)
        page = page_graph.get_object(id=page_id, fields="access_token,posts{created_time,id,message,attachments,type,permalink_url}")

        insight_data = []

        for i in page.get('posts').get('data'):
            item = page_graph.get_connections(id=i.get('id'), connection_name='insights/post_video_views')
            insight_data.append(item)

        retinsight_data = {}


        for each in insight_data:

            first_data = each.get('data')[0]
            retinsight_data[first_data.get('id').split('/')[0]] = first_data.get('values')[0].get('value')


        return {'retinsight_data': retinsight_data, 'posts': page.get('posts'), 'access_token': page.get('access_token')}


class PagePostDeleteView(APIView):

    def get(self, request, id):

        response_data = self.FbPageDetail(id)
        return Response(response_data)

    def FbPageDelete(self, page_id):
        graph = getGraph(self.request)
        page = graph.delete_object(id='post_id')
        return Response(page)


class PageNextView(APIView):

    def get(self, request):

        get_data = request.GET
        raw_url = get_data.get('raw_url')
        page_id = get_data.get('page_id')

        response = urllib.request.urlopen(raw_url)
        data = json.load(response)


        graph = getGraph(self.request)
        page_only_access = graph.get_object(id=page_id, fields="access_token")
        page_access_token = page_only_access.get('access_token')
        page_graph = getGraph(self.request, page_access_token)
        page = page_graph.get_object(id=page_id, fields="access_token,posts{created_time,id,message,attachments,type,permalink_url}")

        insight_data = []

        for i in page.get('posts').get('data'):
            item = page_graph.get_connections(id=i.get('id'), connection_name='insights/post_impressions_unique/lifetime?fields=name,id,period,values')
            insight_data.append(item)


        retinsight_data = {}

        for each in insight_data:

            first_data = each.get('data')[0]
            retinsight_data[first_data.get('id').split('/')[0]] = first_data.get('values')[0].get('value')


        # return Response(data)
        return Response({'data': data, 'retinsight_data': retinsight_data})


class PagePostDAddView(APIView):

    def post(self, request, format=None):
        post_data = request.POST
        message = post_data.get('pMessage')
        page_id = post_data.get('page_id')
        access_token = post_data.get('access_token')
        is_published = post_data.get('is_published')

        if is_published == 'on':
            is_published = True
        else:
            is_published = False
        graph = getGraph(self.request, access_token)
        graph.put_object(parent_object=page_id, connection_name='feed', message=message, published=is_published)

        # graph.put_photo(image=open('img.jpg', 'rb'),
        #         message='Look at this cool photo!')


        return Response(status=status.HTTP_200_OK)
