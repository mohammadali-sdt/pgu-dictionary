import string
from django.contrib import admin
from .models import Word, Entry, Image, URL, Example, Suggest, \
    Comment, CommentsFeedback, IpModel


# Register your models here.

class EntryAlphabetFilter(admin.SimpleListFilter):
    title = 'Alphabet'
    parameter_name = 'alphabet'

    def lookups(self, request, model_admin):
        abc = list(string.ascii_lowercase)
        return ((c.upper(), c.upper()) for c in abc)

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(word__word__startswith=self.value())


class ExampleInline(admin.StackedInline):
    model = Example


class ImageInline(admin.StackedInline):
    model = Image


class URLInline(admin.StackedInline):
    model = URL


@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    inlines = [
        ExampleInline,
        ImageInline,
        URLInline,
    ]
    list_display = ('word', 'type')
    list_filter = ('type', EntryAlphabetFilter)
    ordering = ('word__word', 'type')
    search_fields = ('word__word', 'type')
    filter_horizontal = ("translation", "synonyms", "antonyms")
    # raw_id_fields = ('en_word', )


@admin.register(Word)
class WordAdmin(admin.ModelAdmin):
    list_display = ('word', 'language')
    search_fields = ('word',)
    ordering = ('word',)
    list_filter = ('language',)


#
#
# @admin.register(Farsi)
# class FarsiAdmin(admin.ModelAdmin):
#     search_fields = ('word',)
#     ordering = ('word',)


@admin.register(Suggest)
class SuggestAdmin(admin.ModelAdmin):
    list_display = ('firstname', 'lastname', 'word', 'text', 'active', 'created_at')
    list_filter = ('created_at', 'word')
    search_fields = ('firstname', 'lastname', 'text', 'word')
    ordering = ('firstname', 'lastname', 'created_at')


class CommentsFeedbackInline(admin.StackedInline):
    model = CommentsFeedback


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('firstname', 'lastname', 'email', 'word', 'text', 'active', 'created_at')
    list_filter = ('created_at', 'word')
    inlines = [
        CommentsFeedbackInline,
    ]
    raw_id_fields = ('word',)


@admin.register(CommentsFeedback)
class CommentsFeedbackAdmin(admin.ModelAdmin):
    pass


@admin.register(IpModel)
class IpModelAdmin(admin.ModelAdmin):
    pass


@admin.register(Example)
class ExampleAdmin(admin.ModelAdmin):
    list_display = ('entry', 'text')
    list_filter = ('entry__type',)
    raw_id_fields = ('entry',)


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('entry',)
    list_filter = ('entry__type',)
    raw_id_fields = ('entry',)


@admin.register(URL)
class URLAdmin(admin.ModelAdmin):
    list_display = ('entry', 'url')
    list_filter = ('entry__type',)
    raw_id_fields = ('entry',)

# admin.site.register(Example)
# admin.site.register(Image)
# admin.site.register(URL)

# admin.site.register(English)
# admin.site.register(Farsi)
# admin.site.register(Type)
# admin.site.register(EnToEn)
# admin.site.register(EnToFa)
