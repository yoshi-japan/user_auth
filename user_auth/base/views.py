from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from django.views.generic import TemplateView

# Create your views here.


def top(request):
    # 　you don't have to use variable named template, jsut whatever you want to.
    templatesan = loader.get_template('base/base.html')
    context = {'title': 'Django learning! this sucks :('}
    # return HttpResponse(templatesan.render(context, request))
    return render(request,'base/base.html', context=context)


def second(request):
    template = "base/home.html"
    # context associates template tags and contents.
    return render


def top2(request):
    return render(request, "base/top.html", context={"simple_text":"this is simple text"})


class TopView(TemplateView):
    # this variable designates what template is used by this function.
    # this variable can't be different name, always be 'template_name'
    template_name = 'base/top.html'

# we need to just memorize this.
    # #super is parent function(method).
    # get_context_data is used at another function so we need to use this for consistency.
    def get_context_data(self, **kwargs):
        # get_context_data will take the template tag's name as dictionary, then key is
        # going to be the text inside {{  }} on html
        # (in this case, on top.html there is {{ simple_text }})
        # on html file that you loaded at this view(template_naem).
        context = super().get_context_data(**kwargs) # this gets keys on html template {{ }}
        context['simple_text'] = 'IT learning Django'
        return context






