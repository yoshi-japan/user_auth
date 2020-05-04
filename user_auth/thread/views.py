from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView,\
    DetailView, FormView, CreateView

from . forms import TopicCreateForm, TopicForm
from .models import Topic


# Create your views here.


class TopicListView(ListView):
    template_name = "thread/list_practice.html"
    # model is deleted and there is one line instead
    # model = Topic
    queryset = Topic.objects.order_by('-created')
    context_object_name = "topic_list"

class TopicListView2(ListView):
    template_name = "thread/list_practice.html"
    #  {% for topic in topic_list %} on list_practice.html
    # as default, context_object_name of ListView is automatically created that named
    # (ModelName)+ _list in this case, Topic model is used so context_object_name
    # is automatically "topic_list" even though you don't specify that.
    # you shouldn't write the line below, but it makes more clear for people.
    context_object_name = "topic_list"

# this loads objects at every request time, on the other hand queryset variable is
    # just once when you run server.
    def get_queryset(self):
        return Topic.objects.order_by('created')


class TopicDetailView(DetailView):
    template_name = "thread/detail_topic.html"
    model = Topic
    context_object_name = 'topic' # {{topic.xxx}} on html
    # DetailViewはtemplate_nameとmodelに値を渡してあげると、
    # URLで渡されたpk(primary key)に対応したオブジェクトを呼び出してテンプレートに
    # 渡してくれます。その際、例えばTopicオブジェクトならばtopicという名前で渡されます。もしテンプレートに渡す名前を指定したい場合は
    # context_object_nameで指定します。
    # context_object_nameがなくても機能する。


class TopicTemplateView_InsteadOfDetailView(TemplateView):
    template_name = 'thread/detail_topic.html'


    # as permise following, {'pk':1} if url is http:.../detail/
    def get_context_data(self, **kwargs):# pk = 1 is passed into this **kwargs if
        context = super().get_context_data(**kwargs)
        print(context)
        print(kwargs) # dict object {'pk':1} if url is http:.../detail/1

        # {{topiccc.category.name}}, {{topiccc.title}}, on detail_topic.html
        print(type(kwargs),type(kwargs))
        print(type(self.kwargs), type(self.kwargs))
        context['topiccc'] = get_object_or_404(Topic, id=self.kwargs.get('pk', ''))
        # topic is class in models.py.
        return

    # function version of DetailView
def detail_topic(request):
    ctx = {}
    template_name = 'thread/detail_topic.html'
    if request.method == 'GET':
        ctx['topic'] = get_object_or_404(Topic, request.kwargs.get('pk', ''))
        # get() queryset version
        # Topic.objects.get(pk='pk')
        return render(request, template_name, ctx)



def topic_create(request):
    template_name = "thread/create_topic.html"
    context = {}
    if request.method == 'GET':
        context['form'] = TopicCreateForm()
        return render(request, template_name, context)

    if request.method == 'POST':
        topic_form = TopicCreateForm(request.POST)
        # .is_valid()
        #今回はModelFormを使用しているためTopicモデルが有している情報に適しているか精査されます。
        # 文字の長さやNullの許容等が正しくない場合は精査に失敗します。
        # この方法はModelFormの場合のみ使える方法です。
        if topic_form.is_valid():
            topic_form.save()
            return redirect(reverse_lazy('thread:list'))
        else:
            context['form'] = topic_form
            return render(request, template_name, context)


def topic_create_function(request):
    template_name = "thread/create_topic.html"
    context = {}
    if request.method == "GET":
        form = TopicForm()
        context['form'] = form
        return render(request, template_name, context)

    if request.method == "POST":
        topic_form = TopicForm(request.POST)
        if topic_form.is_valid():
            # topic_form.save() this is ModelForm view.
            topic = Topic()
            cleaned_data = topic_form.cleaned_data
            topic.title = cleaned_data['title']
            topic.message = cleaned_data['message']
            topic.user_name = cleaned_data['user_name']
            topic.category = cleaned_data['category']
            topic.save()
            return redirect(reverse_lazy("base:topview"))
        else:
            context['form'] = topic_form
            return render(request, template_name, context)

        #Topicオブジェクトの保存の仕方が変更されたことにお気づきでしょうか？
        # Formの場合はis_valid()関数が呼ばれた後にcleaned_dataから検証済みのデータを取り出し、
        # Modelのオブジェクトに値をセットしてオブジェクトのsave()関数を呼び保存します。
        # 尚、データの検証はFormに書かれた各フィールドの内容に応じてチェックされます。



class TopicFormView(FormView):
    template_name = 'thread/create_topic.html'
    form_class = TopicCreateForm
    success_url = reverse_lazy('base:topview')

    def form_valid(self, form):
        form.save()
        return super().form_valid()
# ここで行っている処理自体は書き直す前の関数と同じ処理です。
# FormViewはTemplateViewを継承しているのでGETで受けた場合には
# template_nameで指定されたテンプレートを表示します。
# その際にform_classで指定されたフォームを’form’という名前で
# コンテキストとして渡します。
# POSTされた際にはform_valid関数が呼ばれデータの精査が行われ、
# 成功すればsuccess_urlに遷移します。
# もし失敗した場合はエラー情報をフォームに格納して
# 再度template_nameのテンプレートを表示します。
# 今回はform_valid関数をオーバーライドして保存処理を行っています。


class TopicCreateView(CreateView):
    template_name = 'thread/create_topic.html'
    form_class = TopicCreateForm
    # on the TopicFormView, we define definision of
    # validation but here we just put model
    model = Topic
    success_url = reverse_lazy('base:topview')

    # https: // django.kurodigi.com / create_class_base_view /


class TopicCreateView2(CreateView):
    template_name = 'thread/create_topic.html'
    form_class = TopicCreateForm
    model = Topic
    success_url = reverse_lazy('base:top')

    def form_valid(self, form):
        context = {'form':form}
        if self.request.POST.get('next', '') == 'confirm':
            return render(self.request,
                          'thread/confirm_topic.html', context)
        if self.request.POST.get('next', '') == 'back':
            return render(self.request, 'thread/create_topic.html', context)
        if self.request.POST.get('next', '') == 'create':
            return super().form_valid(form)
        else:
            return redirect(reverse_lazy('base:topview'))
