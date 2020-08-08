from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from . import util
import markdown2
from django import forms
from random import *

class SearchForm(forms.Form):
    query = forms.CharField(label="Search", widget=forms.TextInput(attrs=
        {'class':'search'}))

class CreateForm(forms.Form):
    title = forms.CharField(label="Title")
    content = forms.CharField(widget=forms.Textarea(attrs={'class':'textarea'}))

def index(request):
    entries = util.list_entries()

    # if a search is submitted
    if request.method == "POST":
        searchform = SearchForm(request.POST)
        if searchform.is_valid():
            query = searchform.cleaned_data["query"]

            # if no search results, show a list of possibilities
            if query not in entries:
                return render(request, "encyclopedia/results.html", {
                    "query": query, "entries": entries, "form": SearchForm()
                })
            # if a real article then redirect to it
            else:
                return redirect(article, query)

    # if rendering the search page just show list of articles
    if request.method == "GET":
        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries(), "form": SearchForm()
        })

def article(request, title):
    # display article if it exists
    if title in util.list_entries():
        return render(request, "encyclopedia/article.html", {
            "content": markdown2.markdown(util.get_entry(title)), "title": title,
            "form": SearchForm()
        })
    #if it doesnt exist display an error page
    else:
        return render(request, "encyclopedia/error.html", {
            "form": SearchForm()
        })

# return a random article
def random(request):
    list = util.list_entries()
    val = randint(1, (len(list)-1))
    item = (list[val])
    return redirect(article, item)

def create(request):
    # if creation submitted
    if request.method == "POST":
        form = CreateForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            # *** if already exists display other error
            if title in util.list_entries():
                return render(request, "encyclopedia/existingerror.html", {
                    "title": title, "form": SearchForm()
                })
            # save entry and redirect to it
            else:
                util.save_entry(title, content)
                return redirect(article, title)
    # render blank create form
    else:
        return render(request, "encyclopedia/create.html", {
            "contentform": CreateForm(), "form": SearchForm()
        })

def edit(request, title):
    # if edit submitted
    if request.method == "POST":
        #pull content from textarea, save and redirect to it
        newcontent = request.POST.get("newcontent")
        util.save_entry(title, newcontent)
        return redirect(article, title)
    # render edit form
    if request.method == "GET":
        return render(request, "encyclopedia/edit.html", {
            "title": title, "form": SearchForm(), "content": util.get_entry(title)
        })
