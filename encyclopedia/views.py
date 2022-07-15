import markdown2
from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
import random

from . import util, mdConvert


class SearchForm(forms.Form):
    search= forms.CharField(label="Search Encyclopedia")


class EntryForm(forms.Form):
    pageName = forms.CharField(label="Page Title:")
    entryMD = forms.CharField(label="",widget=forms.Textarea(attrs={'style': 'resize: none; height: 200vh;'}))


class EditEntryForm(forms.Form):
    # omit pageName field for editing pages.
    entryMD = forms.CharField(label="",widget=forms.Textarea(attrs={'style': 'resize: none; height: 200vh;'}))
class ToggleMD(forms.Form):
    useCustomMD = forms.BooleanField(label="ToggleCustomMDConversion",required=False)

def index(request):
    if request.method == "POST":
        toggle = ToggleMD(request.POST)
        useCustomMDvar = request.POST.get("useCustomMD",False)
        if toggle.is_valid():
            request.session["useCustomMD"] = useCustomMDvar    
        else:
            return render(request, "encyclopedia/errorPage.html", {
        "form": SearchForm(),
        "Title": "Error"})

    entries = util.list_entries()
    counter = 0
    for i in entries:     
        entries[counter] = (f'<a href="wiki/{i}">{i}</a>')
        counter +=1
    if "useCustomMD" not in request.session:
        return render(request, "encyclopedia/index.html", {
            "form": SearchForm(),
            "entries": entries,
            "ToggleButton": ToggleMD()
        })
    else:
        toggle = ToggleMD(initial={'useCustomMD': request.session["useCustomMD"]})

        return render(request, "encyclopedia/index.html", {
            "form": SearchForm(),
            "entries": entries,
            "ToggleButton": toggle
        })


def find(request,name):
    if util.get_entry(name):
        if "useCustomMD" in request.session:
            if request.session["useCustomMD"]:
                html = mdConvert.convert(name)
            else:
                html =  markdown2.markdown(util.get_entry(name))
        else:
            html =  markdown2.markdown(util.get_entry(name))
        return render(request,"encyclopedia/wiki/defaultPage.html", {
            "form": SearchForm(),
            "Title": name,
            "entries": html
        })
    return render(request, "encyclopedia/errorPage.html", {
        "form": SearchForm(),
        "Title": name
    })


def randomPage(request):
    listLength = len(util.list_entries()) - 1
    page = util.list_entries()[random.randrange(0,listLength)]
    return HttpResponseRedirect(reverse('findwiki',args=(page,)))

 
def searchWiki(request): 
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            counter = 0
            matchingSearches = []
            searches = str.lower(form.cleaned_data["search"])

            for i in util.list_entries(): #create list of matching pages, case insensitive
                temp = i
                i = str.lower(i)
                if i == searches:
                    return HttpResponseRedirect(reverse('findwiki',args=(temp,)))

                if searches in i:
                    matchingSearches.append(util.list_entries()[counter]) 
                counter +=1
                #endfor
            counter = 0
            #Convert list to links
            for i in matchingSearches:     
                matchingSearches[counter] = (f'<a href="wiki/{i}">{i}</a>')
                counter +=1
            return render(request,"encyclopedia/searchResults.html",{
                "form": SearchForm(),
                "Title": "Search Result",
                "entries": matchingSearches,
                "search": searches

            })
        else:
             return render(request, "encyclopedia/errorPage.html", {
        "form": SearchForm(),
        "Title": "Error"
    })


def createPage(request):
    if request.method == "POST":
        entryForm = EntryForm(request.POST)
        if entryForm.is_valid():
            titletemp = entryForm.cleaned_data["pageName"]
            title = ''
            for i in titletemp: #Gets rid of spaces in title.
                if i != ' ':
                    title += i
            entry = entryForm.cleaned_data["entryMD"]
            if util.get_entry(title) == None:
                util.save_entry(title,entry)
                return HttpResponseRedirect(reverse('findwiki',args=(title,)))
            else:
                return render(request,"encyclopedia/createPage.html",{"form": SearchForm(),"entryMD": entryForm,"badsubmit": True})
    else:
        return render(request,"encyclopedia/createPage.html",{"form": SearchForm(),"entryMD": EntryForm(),"badsubmit": False})


def editPage(request,name):
    if request.method == "POST":
        entryForm = EditEntryForm(request.POST)
        if entryForm.is_valid():
            entry = entryForm.cleaned_data["entryMD"]
            util.save_entry(name,entry)
            return HttpResponseRedirect(reverse('findwiki',args=(name,)))
        else:
            return render(request,"encyclopedia/editPage.html",{"form": SearchForm(),"entryMD": entryForm,"badsubmit": True})
    else:
        form = EditEntryForm(initial={'entryMD': mdConvert.cleanLines(util.get_entry(name))})

        #print(form)
        return render(request,"encyclopedia/editPage.html",{"title": name, "form": SearchForm(),"entryMD": form,"badsubmit": False})