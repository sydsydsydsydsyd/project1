from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from . import util
import markdown2
from django import forms
from random import *

class SearchForm(forms.Form):
    query = forms.CharField(label="Query")

class CreateForm(forms.Form):
    title = forms.CharField(label="title")
    content = forms.CharField(widget=forms.Textarea)

def index(request):
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data["query"]
            return article(request, query)

    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(), "form": SearchForm()
    })

def article(request, title):
    if title in util.list_entries():
        return render(request, "encyclopedia/article.html", {
            "content": markdown2.markdown(util.get_entry(title)), "title": title,
            "form": SearchForm()
        })
    else:
        return render(request, "encyclopedia/error.html", {
            "form": SearchForm()
        })

#placeholder
def create(request):
    if request.method == "POST":
        form = CreateForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            if title in util.list_entries():
                return render(request, "encyclopedia/error.html")
            else:
                util.save_entry(title, content)
                return render(request, "encyclopedia/article.html", {
                    "content": markdown2.markdown(util.get_entry(title)), "title": title,
                    "form": SearchForm()
                })
    else:
        return render(request, "encyclopedia/create.html", {
            "contentform": CreateForm(), "form": SearchForm()
        })

#placeholder
def random(request):
    list = util.list_entries()
    val = randint(1, (len(list)-1))
    item = (list[val])
    return render(request, "encyclopedia/article.html", {
        "content": markdown2.markdown(util.get_entry(item)), "title": item,
        "form": SearchForm()
    })
