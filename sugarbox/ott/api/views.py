from ott.models import User, Asset,Comment,Rating
from django.http import HttpResponse
from django.views.generic import View
from django.db.models import Count, Avg
import json


class ResponseData(View):
    '''To generate json response'''
    @staticmethod
    def generate_response(data,error):
        '''Post Request '''
        if error:
                status_code = 201
        else:
                status_code = 200
        data1 = {'status': status_code,'result': data}
        json_data = json.dumps(data1)
        return HttpResponse(json_data,content_type='application/json')

    '''validate user data'''
    @staticmethod
    def validate_user(user):
        result={'error':''}
        if user == '' or int(user) <= 0:
            result['error'] = "Please specify valid userid"
        elif User.objects.filter(uid=user).exists is False:
            result['error'] = "User does not exist"
        return result

    '''validate asset data'''
    @staticmethod
    def validate_movie(movie,opt=0):
        result={'error':''}
        if movie == '' and opt == 0:
            result['error'] = "Please specify valid movieid"
        else:
            moviedetail = list(Asset.objects.filter(title=movie).values('asset_id'))
            if len(moviedetail) == 0:
                result['error'] = "Invalid Movie"
            else:
                movieid = moviedetail[0]['aaset_id']
                result['movieid'] = movieid
            return result

    '''To validate post data'''
    @staticmethod
    def validate_data(r, type):
        result = {'error':''}
        userr = ResponseData.validate_user(r['user'])
        if userr['error'] is not '':
            result['error'] = userr['error']
        elif r['movie'] == '':
            result['error'] = "Please specify valid movieid"
        elif type == 'rating' and (r.get('rating') not in range(0,11)):
            result['error'] = "Please specify ratings between 0 to 10"
        elif type == 'comment' and r.get('comment','') is '':
            result['error'] = "Please specify comments"
        elif r['movie'] != '':
            movier = ResponseData.validate_movie(r['movie'])
            if movier['error'] is not '':
                result['error'] = movier['error']
            else:
                result['movieid'] = movier['movieid']
        return result


class MovieData(View):
    ''''Get movie data'''
    def get(self,request,name=''):
        result = []
        error = 0
        movies = Asset.objects.filter(title__contains=name).values('asset_id','title','video_url')
        #movies = Rating.objects.filter(asset_id__title__contains=name).values('asset_id', 'asset_id__title', 'asset_id__video_url').annotate(
        #   avg=Avg('rating'),count=Count('rating'))
        rating = Rating.objects.filter(asset_id__title__contains=name).values('asset_id__title').annotate(avg=Avg('rating'),count=Count('rating'))
        comment = Comment.objects.filter(asset_id__title__contains=name).values('comment','uid__name','asset_id__title')
        dict ={}
        for m in movies:
            dict[m['title']]={'video_url':m['video_url'],'title':m['title']}
        for m in rating:
            dict[m['asset_id__title']]['average_rating']=m['avg']
            dict[m['asset_id__title']]['rating_count'] = m['count']
        for m in comment:
            if 'comments' in dict[m['asset_id__title']]:
                dict[m['asset_id__title']]['comments'].append(m)
            else:
                dict[m['asset_id__title']]['comments'] = [m]
        result = {'movies': dict}
        return ResponseData.generate_response(result,error)


class UserData(View):
    '''Get user data'''
    def get(self,request, id=0):
        result = []
        error  = 0
        vdata = ResponseData.validate_user(id)
        if vdata['error'] is not '':
            error  = 1
            result = vdata
        else:
            r = Rating.objects.filter(uid=id).values('rating','asset_id__title','asset_id')
            comment = Comment.objects.filter(uid=id).values('comment','asset_id__title')
            dict = {}
            for row in r:
                d = row
                dict[row['asset_id__title']] = {'rating':row['rating']}
            for c in comment:
                d = list(c)
                if c['asset_id__title'] in dict:
                    dict[c['asset_id__title']]['comment']=c['comment']
                else:
                    dict[c['asset_id__title']]={'comment':c['comment']}
            result = {'movies':dict}
        return ResponseData.generate_response(result, error)


class RateData(View):

    def post(self, request):
        data ={"msg": ""}
        rdata = json.loads(request.body)
        vdata = ResponseData.validate_data(rdata,'rating')
        if vdata['error'] is not '':
            data = vdata
        else:
            try:
                u   = User(uid=rdata['user'])
                a   = Asset(asset_id=vdata['movieid'])
                row = Rating(asset_id=a,uid=u,rating=rdata['rating'])
                row.save()
            except Exception as e:
                data['error'] = str(e)
            if row.rating_id:
                data['msg'] = 'Rating Added Successfully'
            else:
                data['msg'] = 'Issue while adding rating'
        return ResponseData.generate_response(data)


class CommentData(View):
    def post(self, request):
        result = {"msg":""}
        error = 0
        rdata = json.loads(request.body)
        vdata = ResponseData.validate_data(rdata,'comment')
        if vdata['error'] is not '':
            error = 1
            result = vdata
        else:
            try:
                u = User(uid=rdata['user'])
                a = Asset(asset_id=vdata['movieid'])
                row = Comment(asset_id=a,uid=u,comment=rdata['comment'])
                row.save()
            except Exception as e:
                error = 1
                result['error'] = str(e)
            if row.comment_id:
                result['msg'] = 'Comment Added Successfully'
            else:
                error = 1
                result['msg'] = 'Issue while adding comment'
        return ResponseData.generate_response(result, error)




