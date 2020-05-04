from django.forms import ModelForm
from .models import Topic, Category
from django import forms

class TopicCreateForm(ModelForm):
    # without Meta this doesn't work
#     model = Topic
#     fields = [
#         'title',
#         'user_name',
#         'category',
#         'message',
#     ]
    class Meta:
        model = Topic
        fields = [
            'title',
            'user_name',
            'category',
            'message',
        ]
        widgets = {
            # atrributes of Topic : forms.u
            'title' : forms.TextInput(attrs={'class':'hoge'}),
            'user_name' : forms.TextInput(attrs={'value': 'anonymous'})
        }
    # ModelFormの場合、プロパティを直接変更できないため、
    # __init__関数をオーバライドして対応します。
    # この方法はインプットタグのclass要素を修正したい場合にも使えます。
    # また、ModelFormでwidgetを変更する場合には以下のように
    # 変更することが出来ます。
    # widgetの指定をしながらタグの要素を指定するのです。

    def __init__(self, *args, **kwargs):
        # kwargs.setdefault('label_suffix', '')
        super().__init__(*args, **kwargs)
        self.fields['category'].empty_label = '選択して下さい'
        self.fields['user_name'].widget.attrs['value'] = '匿名'
        #ModelFormの場合、プロパティを直接変更できないため、__init__関数をオーバライドして対応します。この方法はインプットタグのclass要素を修正したい場合にも使えます。また、ModelFormでwidgetを変更する場合には以下のように変更することが出来ます。widgetの指定をしながらタグの要素を指定するのです。



class TopicForm(forms.Form):
    title = forms.CharField(
        label='title',
        max_length=225,
        required=True,)
    user_name = forms.CharField(
        label='name',
        max_length=30,
        required=True,
        #
        widget=forms.TextInput(attrs={'value': 'Anonymous'}),)
    # TextInput creates input tag that has type=text attritube.
    category = forms.ModelChoiceField(
        label='Category',
        queryset=Category.objects.all(),
        required=True,
        # choiceField
        empty_label='Please pick one'
        # if there is no empty_label in choiceField, it's replaced by ----.
        )
    message = forms.CharField(
        label='main text',
        widget=forms.Textarea,required=True,)

    # widget is set value of select tag as default.
    # so we change widget into Textarea or TextInput here.

    # カテゴリーはセレクトタグを使用していますが、（正確にはデフォルトのwidgetがselectという意味）このセレクトタグの未選択状態では「——–」
    # というように点線で表現されています。この文言を変更したいという需要は多いと思います。Formの場合は以下のようにempty_labelを指定するだけです。また、入力値の初期値を与えるなどタグの要素を変更する場合は以下のようにします。

    def __init__(self, *args, **kwargs):
        # this is python built-in function
        kwargs.setdefault('label_suffix', '')
        super().__init__(*args, **kwargs)
        # https: // django.kurodigi.com / form /

