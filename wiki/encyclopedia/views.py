from django.shortcuts import render
import random as ran
from . import util
import markdown2


def convert_md(title):
    content = util.get_entry(title)
    markdowner = markdown2.Markdown()
    if content is None:
        return None
    else:
        return markdowner.convert(content)


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, title):
    html = convert_md(title)
    if html is None:
        return render(request, "encyclopedia/error.html", {
            "message": "Entry does not exist"
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "page": html
        })


def search(request):
    if request.method == "POST":
        entry = request.POST['q']
        html = convert_md(entry)
        if html is not None:
            return render(request, "encyclopedia/entry.html", {
                "title": entry,
                "page": html
            })
        else:
            reco = []
            pages = util.list_entries()
            for page in pages:
                if entry.lower() in page.lower():
                    reco.append(page)
            return render(request, "encyclopedia/search.html", {
                "reco": reco,
            })


def create(request):
    if request.method == "GET":
        return render(request, "encyclopedia/create.html")
    else:
        title = request.POST['title']
        content = request.POST['content']
        preTitle = util.get_entry(title)
        if preTitle is not None:
            return render(request, 'encyclopedia/error.html', {
                "message": "Page already exists",
            })
        else:
            util.save_entry(title, content)
            html = convert_md(title)
            return render(request, "encyclopedia/entry.html", {
                "title": entry,
                "page": html
            })


def edit(request):
    if request.method == "POST":
        title = request.POST['edit_title']
        content = util.get_entry(title)
    return render(request, "encyclopedia/edit.html", {
        "title": title,
        "content": content,
    })


def saveedit(request):
    if request.method == "POST":
        title = request.POST['edit_title']
        content = request.POST['content']
        util.save_entry(title, content)
        html = convert_md(title)
        return render(request, "encyclopedia/entry.html", {
            "title": entry,
            "page": html
        })


def random(request):
    pages = util.list_entries()
    rand_page = ran.choice(pages)
    html = convert_md(rand_page)
    return render(request, "encyclopedia/entry.html", {
        "title": rand_page,
        "page": html
    })
