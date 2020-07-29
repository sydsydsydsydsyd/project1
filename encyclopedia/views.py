from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from . import util
import markdown2

def index(request):
    if request.method == "POST":
        queryString = request.POST['q']
        print(queryString)
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def article(request, title):
    if title in util.list_entries():
        return render(request, "encyclopedia/article.html", {
            "content": markdown2.markdown(util.get_entry(title)), "title": title
        })
    else:
        return render(request, "encyclopedia/error.html")



#placeholder
def create(request):
    return HttpResponse("create")

#placeholder
def random(request):
    return HttpResponse("random")
