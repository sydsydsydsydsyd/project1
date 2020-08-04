from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from . import util
import markdown2
from django import forms
from random import *

class SearchForm(forms.Form):
    query = forms.CharField(label="query")

class CreateForm(forms.Form):
    title = forms.CharField(label="title")
    content = forms.CharField(widget=forms.Textarea)

class EditForm(forms.Form):
    changes = forms.CharField(widget=forms.Textarea)

def index(request):
    entries = util.list_entries()
    if request.method == "POST":
        searchform = SearchForm(request.POST)
        if searchform.is_valid():
            query = searchform.cleaned_data["query"]
            if query not in entries:
                return render(request, "encyclopedia/results.html", {
                    "query": query, "entries": entries, "form": SearchForm()
                })
            else:
                return redirect(article, query)

    if request.method == "GET":
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

def random(request):
    list = util.list_entries()
    val = randint(1, (len(list)-1))
    item = (list[val])
    return redirect(article, item)

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
                return redirect(article, title)
    else:
        return render(request, "encyclopedia/create.html", {
            "contentform": CreateForm(), "form": SearchForm()
        })

def edit(request, title):
    if request.method == "GET":
        return render(request, "encyclopedia/edit.html", {
            "title": title, "editform": EditForm(), "form": SearchForm()
        })

    if request.method == "POST":
        form = EditForm(request.POST)
        if form.is_valid():
            changes = form.cleaned_data["changes"]
            util.save_entry(title, changes)
            return redirect(article, title)
        else:
            return render(request, "encyclopedia/error.html", {
                "form": SearchForm()
            })
