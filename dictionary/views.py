import json

from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.http import JsonResponse, Http404, HttpResponseBadRequest
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import permission_required
from django.views.decorators.http import require_POST

from .forms import SuggestionForm, CommentForm
from .models import Entry, Word, Comment, Suggest, CommentsFeedback, IpModel
from nltk.stem import PorterStemmer

ps = PorterStemmer()


# Create your views here. def get_synonym_of_word(request, word): check_word
# = English.objects.filter(word=word) is_persian = False if len(check_word)
# > 0: en_synonms = EnToEn.objects.filter(en_id__word=word).values_list(
# 'synonym_en_id__word') en_synonms = [w[0] for w in en_synonms] fa_synonms
# = EnToFa.objects.filter(en_id__word=word).values_list('fa_id__word')
# fa_synonms = [w[0] for w in fa_synonms] context = {'word': word,
# 'en_synonms': en_synonms, 'fa_synonms': fa_synonms, 'is_persian':
# is_persian} return render(request, 'dictionary/index.html',
# context=context) else: en_translate = EnToFa.objects.filter(
# fa_id__word=word).values_list('en_id__word') en_translate = [w[0] for w in
# en_translate] context = {'word': word, 'en_translate': en_translate,
# 'is_persian': not is_persian} return render(request,
# 'dictionary/index.html', context=context)

def home(request):
    return render(request, 'dictionary/home.html')


# def get_synonym_of_word(request, word):
#     is_persian = True
#     farsi_word = Farsi.objects.filter(word=word)
#     english_word = English.objects.filter(word=word)
#     if len(farsi_word) > 0:
#         en_translate = farsi_word[0].en_words.all()
#         if len(en_translate) < 1:
#             return HttpResponse('Word has not synonym!')
#         context = {'en_translate': en_translate, 'is_persian': is_persian,
#                    'word': word}
#         return render(request, 'dictionary/result.html', context=context)
#     elif len(english_word) > 0:
#         fa_synonms = english_word[0].fa_words.all()
#         en_synonms = english_word[0].synonym_words.all()
#         if len(fa_synonms) < 1 and len(en_synonms) < 1:
#             return HttpResponse('Word has not synonym!')
#         context = {'word': word, 'en_synonms': en_synonms,
#                    'fa_synonms': fa_synonms, 'is_persian': not is_persian}
#         return render(request, 'dictionary/result.html', context=context)
#     return HttpResponse("Word Not Found!")
#
#
# def get_suggested_words(request, letter):
#     suggested_words = Farsi.objects.filter(word__contains=letter).union(
#         English.objects.filter(word__contains=letter))
#     if len(suggested_words) < 1:
#         return JsonResponse(
#             {'status': 'error', 'data': [], 'message': 'word not found'},
#             status=404)
#     suggested_words = [w.word for w in suggested_words]
#     return JsonResponse({'status': 'success', 'data': suggested_words},
#                         status=200)

def get_word_detail(request, word):
    try:
        word_obj = Word.objects.get(word=word)
        if word_obj.language == 'en':
            entries = Entry.objects.filter(word__word=word)
            comments = Comment.objects.filter(word__word=word, active=True, reply_to=None)
            comment_form = CommentForm()
            return render(request, 'dictionary/result-english-word.html', {
                'entries': entries,
                'word': word_obj,
                'comments': comments,
                'comment_form': comment_form
            })
        elif word_obj.language == 'fa':
            entires = Entry.objects.filter(translation__word=word)
            words = list(set(list(map(lambda x: x.word.word, entires))))
            paginator = Paginator(words, 5)
            page = request.GET.get('page')
            try:
                words = paginator.page(page)
            except PageNotAnInteger:
                words = paginator.page(1)
            except EmptyPage:
                words = paginator.page(paginator.num_pages)
            return render(request, 'dictionary/result-farsi-word.html', {
                'words': words,
                'word': word,
                'page': page
            })
    except ObjectDoesNotExist:
        return render(request, 'dictionary/word_not_found.html', {
            'word': word,
        })


def get_suggestion_words(request, word):
    word = ps.stem(word.lower())
    suggestions = Word.objects.filter(word__contains=word)
    generated_html = render_to_string('dictionary/suggest_word-partial.html',
                                      context={'suggestions': suggestions})
    return JsonResponse({'html': generated_html}, status=200)


def add_new_suggestion(request):
    if request.method == 'POST':
        form = SuggestionForm(data=request.POST)
        print(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'dictionary/add-suggestion-success.html')
        else:
            return HttpResponseBadRequest('Bad Request !')
    else:
        raise Http404()


def add_new_comment(request, word_id):
    word = get_object_or_404(Word, id=word_id)
    if request.method == 'POST':
        form = CommentForm(data=request.POST)
        print(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.word = word
            new_comment.save()
            return render(request, 'dictionary/add-comment-success.html', {
                'word': word
            })
    else:
        form = CommentForm()
    return redirect('dictionary:get_word_detail', word.word)


def add_new_reply(request, word_id, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    word = get_object_or_404(Word, id=word_id)
    if request.method == 'POST':
        reply_form = CommentForm(data=request.POST)
        if reply_form.is_valid():
            new_reply = reply_form.save(commit=False)
            new_reply.reply_to = comment
            new_reply.word = word
            new_reply.save()
            return render(request, 'dictionary/add-comment-success.html', {
                'word': word
            })
    else:
        form = CommentForm()
    return redirect('dictionary:get_word_detail', word.word)


@permission_required('dictionary.view_active_suggestions', raise_exception=True)
def get_actived_suggests(request):
    actived_suggests = Suggest.objects.filter(active=True)
    paginator = Paginator(actived_suggests, 4)
    page = request.GET.get('page')
    try:
        actived_suggests = paginator.page(page)
    except PageNotAnInteger:
        actived_suggests = paginator.page(1)
    except EmptyPage:
        actived_suggests = paginator.page(paginator.num_pages)
    return render(request, 'dictionary/actived_suggestions.html',
                  {'actived_suggests': actived_suggests, 'page': page})


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


@require_POST
def add_feedback_comment(request):
    data = json.loads(request.body)
    action = data.get('action')
    comment = data.get('comment')
    ip = get_client_ip(request)
    if action and comment:
        try:
            comment = Comment.objects.get(id=int(comment))

            if not IpModel.objects.filter(ip=ip).exists():
                ip = IpModel.objects.create(ip=ip)
            else:
                ip = IpModel.objects.get(ip=ip)

            if not CommentsFeedback.objects.filter(user_ip=ip, comment=comment).exists():
                comment_feedback = CommentsFeedback.objects.create(comment=comment, user_ip=ip)
                if action == 'like':
                    if comment_feedback:
                        comment_feedback.type = 'L'
                        comment_feedback.save()
                elif action == 'dislike':
                    if comment_feedback:
                        comment_feedback.type = 'D'
                        comment_feedback.save()
            else:
                comment_feedback = CommentsFeedback.objects.get(comment=comment, user_ip=ip)
                if action == 'like':
                    comment_feedback.type = 'L'
                    comment_feedback.save()
                elif action == 'dislike':
                    comment_feedback.type = 'D'
                    comment_feedback.save()

            comment_likes = comment.get_total_likes
            comment_dislikes = comment.get_total_dislikes
            return JsonResponse({'status': 'success',
                                 'likes': comment_likes,
                                 'dislikes': comment_dislikes}, status=200)
        except ObjectDoesNotExist:
            pass
    return JsonResponse({'status': 'fail'}, status=400)


def get_popup(request, word):
    word = ps.stem(word.lower())
    print(word)
    entries = Entry.objects.filter(word__word=word)
    if len(entries) == 0:
        return JsonResponse({'status': "fail"}, status=400)
    html = render_to_string('dictionary/popup.html', {'entries': entries})
    return JsonResponse({'status': "success", 'data': html}, status=200)
