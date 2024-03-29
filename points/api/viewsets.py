from chapters.models import Chapter
from points.models import Point, TagPoint
from studies.models import Study
from bookmarks.models import Bookmark
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from zanko.permissions import JustOwner
from .serializers import PointSerializer
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
import datetime as time
import pytz
import requests
from django.core.files.base import ContentFile
from requests import request, HTTPError
import csv
import codecs
from books.models import Book
from tags.models import Tag

def save_point(point, user, chapter):
    text = point['subject']
    text = text.replace('*', '©')
    text = text.replace('@', '¥')
    text = text.replace('`', '¢')
    text = text.replace('!', '@')
    text = text.replace('#', '!')
    text = text.replace('~', '*')
    title = ""
    type = "regular"
    saved_point = Point.objects.create(chapter=chapter, user=user, text=text, title=title, type=type)
    if point['imageUrl'] != "empty":
        image = requests.get(point['imageUrl'])
        saved_point.image.save(point['imageUrl'].split("/")[-1], ContentFile(image.content))
    if point['audioUrl'] != "empty":
        voice = requests.get(point['audioUrl'])
        saved_point.voice.save(point['audioUrl'].split("/")[-1], ContentFile(voice.content)) 
    return saved_point       


def set_tags(tags, point, user):
    for tag in tags:
        check_tag = Tag.objects.filter(name=tag['name'], user=user)
        if check_tag.exists():
            point_tag = TagPoint.objects.filter(point=point, tag=check_tag.first())
            if not point_tag.exists():
                TagPoint.objects.create(tag=check_tag[0], point=point)
        else:
            new_tag = Tag.objects.create(name=tag['name'], user=user) 
            TagPoint.objects.create(point=point, tag=new_tag)  


def save_book(book, user):
    name = book['name']
    description = ''
    category = 'medical'
    saved_book = Book.objects.create(name=name, description=description, category=category, user=user)
    return saved_book

def save_chapter(chapter, book, user):
    name = chapter['name']
    saved_chapter = Chapter.objects.create(name=name, book=book, user=user)
    return saved_chapter

def read_csv(file):
    words_dict = dict()
    words = list(csv.reader(codecs.iterdecode(file, 'utf-8')))
    for row in words[1:]:
        words_dict[row[3]] = words_dict.setdefault(row[3], []) + [(row[0], row[1])]     
    return words_dict  
    
def read_csv_(file):
    words_list = list()
    words = list(csv.reader(codecs.iterdecode(file, 'utf-8')))
    for row in words[1:]:
            words_list.append((row[0], row[1]))
    return words_list     

def study_order():
    date = time.datetime.now()
    order = str(date)[0:19]
    order += ("+" + str(date + time.timedelta(days=1))[0:19])
    return order

def filter_list(filter, point, f_list):
    if filter == "all":
        filter_list.append(point)
    elif filter == "star":
        if point.bookmark == True:
            f_list.append(point) 
    elif filter == "one":
        if point.level == "1":
            f_list.append(point)      
    elif filter == "two":
        if point.level == "2":
            f_list.append(point) 
    elif filter == "three":
        if point.level == "3":
            f_list.append(point) 
    elif filter == "four":
        if point.level == "4":
            f_list.append(point) 
    elif filter == "five":
        if point.level == "5":
            f_list.append(point)                                       


class PointViewSet(viewsets.ModelViewSet):
    permission_classes = [JustOwner, IsAuthenticated]
    queryset = Point.objects.all()
    serializer_class = PointSerializer


    def perform_create(self, serializer):
        cond = False
        if cond:
            book_req = requests.get("https://residenti.ofoghekonkoor.ir/api/v1/books")  
            user = self.request.user
            for book in book_req.json()['data']:
                if book['id'] != 1:
                    continue
                #saved_book = save_book(book, user)
                saved_book = Book.objects.get(id=28)
                chapter_req = requests.get("https://residenti.ofoghekonkoor.ir/api/v1/" + str(book['id']) + '/chapters')
                for chapter in chapter_req.json()['data'][25:27]:  
                    saved_chapter = save_chapter(chapter, saved_book, user)
                    topic_req = requests.get("https://residenti.ofoghekonkoor.ir/api/v1/" + str(chapter['id']) + '/topics')
                    for topic in topic_req.json()['data']:
                        point_req = requests.get("https://residenti.ofoghekonkoor.ir/api/v1/" + str(topic['id']) + '/points')
                        for point in point_req.json()['data']:  
                            saved_point = save_point(point, user, saved_chapter)
                            set_tags(point['tags'], saved_point, user)     
            return Response(request)
        else:    
            chapter = Chapter.objects.get(id=self.request.data.get('chapter'))
            user = self.request.user
            if user.balance < 1:
                return Response(data=[{'status': status.HTTP_402_PAYMENT_REQUIRED, "message":'no-balance'}])
            else:
                user.balance -= 1
                user.save()
                serializer.save(user=user, chapter=chapter)
            
     # words_list = read_csv_(self.request.data.get('words'))
     # for item in words_list:
     #   title = item[1]
     #   text = item[0]
     #   chapter = Chapter.objects.get(id=self.request.data.get('chapter'))
     #   user = self.request.user
     #   type = 'flashcard'
     #   Point.objects.create(chapter=chapter, user=user, text=text, title=title, type=type)
#       
        


    def list(self, request):
        # Note that we can't use request.data
        filter = request.data.get('filter')
        chapter_id = request.query_params.get('chapter', None)
        chapter = Chapter.objects.get(pk=chapter_id)
        book = chapter.book
        points = chapter.points.order_by('-id')
        for point in points:
            point.info = chapter.name + "_" + book.name
            # Add study
            study = Study.objects.filter(point=point, user=request.user)
            if study:
                next_time = study[0].order.split("+")[-1]
                study[0].ready = time.datetime.strptime(next_time, "%Y-%m-%d %H:%M:%S") < time.datetime.now()
                point.study = study
            else:
                point.study = [Study.objects.create(user=request.user, point=point, order=study_order())]

            # Add bookmark    
            bookmark = Bookmark.objects.filter(point=point, user=request.user).first()
            if bookmark:
                point.bookmark = True       
        serializer = PointSerializer(points, many=True)
        return Response(serializer.data)


    def destroy(self, request, *args, **kwargs):
        point = self.get_object()
        point.delete()
        return Response(data=[{'status': status.HTTP_200_OK, "message":'deleted'}]) 

    def update(self, request, *args, **kwargs):
        point = self.get_object()
        point.text = request.data.get('text')
        point.title = request.data.get('title')
        attachments = request.data.get('attachments')
        image_old = attachments.split('_')[0]
        voice_old = attachments.split('_')[1]
        
        if image_old != "yes":
            point.image = request.data.get('image')
        if voice_old != "yes":
            point.voice = request.data.get('voice')
        
        point.save()
        return Response({'status': status.HTTP_200_OK, "message":'updated'})

