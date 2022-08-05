from django.db import models
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


# Create your models here.

class Word(models.Model):
    langs = (
        ('en', _('English')),
        ('fa', _('Farsi'))
    )
    word = models.CharField(
        _('word'),
        max_length=250,
        unique=True,
        blank=False,
        null=False,
        validators=[MinLengthValidator(2)],
    )
    language = models.CharField(_('language'), max_length=2, choices=langs, blank=False,
                                null=False)

    def save(self, *args, **kwargs):
        self.word = self.word.strip().lower()
        return super(Word, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.word}"

    class Meta:
        verbose_name = _('Word')
        verbose_name_plural = _('Words')


#
# class English(models.Model):
#     word = models.CharField(
#         max_length=250,
#         unique=True,
#         blank=False,
#         null=False,
#         validators=[MinLengthValidator(2)],
#     )
#
#     # synonym_words = models.ManyToManyField('self', related_name='synonyms',
#     #                                        blank=True)
#
#     def save(self, *args, **kwargs):
#         self.word = self.word.strip().lower()
#         return super(English, self).save(*args, **kwargs)
#
#     def __str__(self):
#         return f"{self.word}"
#
#
# class Farsi(models.Model):
#     word = models.CharField(
#         max_length=250,
#         unique=True,
#         blank=False,
#         null=False,
#         validators=[MinLengthValidator(2)],
#     )
#
#     # en_words = models.ManyToManyField(English, related_name='fa_words',
#     #                                   blank=True)
#
#     def save(self, *args, **kwargs):
#         self.word = self.word.strip().lower()
#         return super(Farsi, self).save(*args, **kwargs)
#
#     def __str__(self):
#         return f"{self.word}"


class Entry(models.Model):
    TYPES = (
        ("verb", _("Verb")),
        ("noun", _("Noun")),
        ("adjective", _("Adjective")),
        ("pronoun", _("Pronoun")),
        ("adverb", _("Adverb")),
        ("preposition", _("Preposition")),
        ("conjunction", _("Conjunction")),
        ("interjection", _("Interjection")),
    )
    type = models.CharField(_("type"), choices=TYPES, max_length=12)
    word = models.ForeignKey(Word, related_name="words",
                             on_delete=models.CASCADE, limit_choices_to={'language': 'en'}, verbose_name=_("word"))
    translation = models.ManyToManyField(Word, related_name="translates",
                                         blank=True, limit_choices_to={'language': 'fa'}, verbose_name=_("translation"))
    synonyms = models.ManyToManyField("self", related_name="en_synonyms",
                                      blank=True, verbose_name=_("synonyms"))
    antonyms = models.ManyToManyField("self", related_name="en_antonym",
                                      blank=True, verbose_name=_("antonyms"))

    def __str__(self):
        word = self.word.word + "-" + self.type
        return word

    class Meta:
        verbose_name = _('Entry')
        verbose_name_plural = _('Entries')


class Example(models.Model):
    entry = models.ForeignKey(Entry, related_name="examples",
                              on_delete=models.CASCADE, verbose_name=_("entry"))
    text = models.TextField(_("text"), blank=False, null=False)

    class Meta:
        verbose_name = _('Example')
        verbose_name_plural = _('Examples')


class Image(models.Model):
    entry = models.ForeignKey(Entry, related_name="images",
                              on_delete=models.CASCADE, verbose_name=_("entry"))
    file = models.ImageField(_("file"), upload_to="Images/",
                             blank=False, null=False)

    class Meta:
        verbose_name = _('Image')
        verbose_name_plural = _('Images')


class URL(models.Model):
    entry = models.ForeignKey(Entry, related_name="urls",
                              on_delete=models.CASCADE, verbose_name=_("entry"))
    url = models.URLField(_("url"), blank=False, null=False)

    class Meta:
        verbose_name = _('URL')
        verbose_name_plural = _('URLs')


class Suggest(models.Model):
    word = models.CharField(_("word"), max_length=255, blank=False, null=False)
    firstname = models.CharField(_("firstname"), max_length=255, blank=False, null=False)
    lastname = models.CharField(_("lastname"), max_length=255, blank=True)
    email = models.EmailField(_("email"), blank=True)
    url = models.URLField(_("url"), blank=True)
    social_media_id = models.CharField(_("social_media_id"), max_length=500, blank=True)
    text = models.TextField(_("text"), blank=False, null=False)
    created_at = models.DateTimeField(_("created_at"), auto_now_add=True)
    active = models.BooleanField(_("active"), default=False)

    def __str__(self):
        return self.firstname + ' ' + self.lastname

    class Meta:
        verbose_name = _('Suggest')
        verbose_name_plural = _('Suggests')
        permissions = [
            ('view_active_suggestions', _('Can view acived suggestions'))
        ]


class Comment(models.Model):
    word = models.ForeignKey(Word, related_name='comments',
                             on_delete=models.CASCADE, limit_choices_to={'language': 'en'}, verbose_name=_("word"))
    firstname = models.CharField(_("firstname"), max_length=255, blank=False, null=False)
    lastname = models.CharField(_("lastname"), max_length=255, blank=True)
    email = models.EmailField(_("email"), blank=True)
    text = models.TextField(_("text"), blank=False, null=False)
    reply_to = models.ForeignKey('self', related_name='replies',
                                 on_delete=models.CASCADE, blank=True,
                                 null=True, verbose_name=_("reply_to"))
    created_at = models.DateTimeField(_("created_at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated_at"), auto_now=True)
    active = models.BooleanField(_("active"), default=False)

    @property
    def get_total_likes(self):
        return len([feedback for feedback in self.feedbacks.all() if feedback.type == 'L'])

    @property
    def get_total_dislikes(self):
        return len([feedback for feedback in self.feedbacks.all() if feedback.type == 'D'])

    def __str__(self):
        return f'{self.firstname} {self.lastname} comment on {self.word}'

    class Meta:
        verbose_name = _('Comment')
        verbose_name_plural = _('Comments')
        ordering = ('created_at',)


class IpModel(models.Model):
    ip = models.CharField(max_length=100)

    def __str__(self):
        return self.ip


class CommentsFeedback(models.Model):
    FEEDBACK = (
        ('L', _('Like')),
        ('D', _('Dislike'))
    )
    # user = models.ForeignKey(User, related_name='feedback',
    #                          on_delete=models.PROTECT, verbose_name=_("user"))
    user_ip = models.ForeignKey(IpModel, related_name='feedbacks', on_delete=models.PROTECT,
                                verbose_name=_('user_ip'))
    type = models.CharField(_("type"), max_length=1, choices=FEEDBACK)
    comment = models.ForeignKey(Comment, related_name='feedbacks',
                                on_delete=models.PROTECT, verbose_name=_("comment"))

    def __str__(self):
        return f'feedback {self.type} on {self.comment.firstname} {self.comment.lastname} with ip {self.user_ip}'

    class Meta:
        verbose_name = _('Comments Feedback')
        verbose_name_plural = _('Comments Feedbacks')

#
# class EnToEn(models.Model): en_id = models.ForeignKey(English,
# on_delete=models.CASCADE, related_name='%(class)s_word_id') synonym_en_id
# = models.ForeignKey(English, on_delete=models.CASCADE, related_name='%(
# class)s_synonym_id')
#
#     def __str__(self):
#         return f'{self.en_id.word}:{self.synonym_en_id.word}'
#
#
# class EnToFa(models.Model): en_id = models.ForeignKey(English,
# on_delete=models.CASCADE, related_name='%(class)s_word_id') fa_id =
# models.ForeignKey(Farsi, on_delete=models.CASCADE, related_name='%(
# class)s_synonym_id')
#
#     def __str__(self):
#         return f'{self.en_id.word}:{self.fa_id.word}'
