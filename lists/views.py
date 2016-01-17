from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.http import HttpResponse
from lists.models import Item, List
from lists.forms import ExistingListItemForm, ItemForm, NewListForm


User = get_user_model()

def home_page(request):
    # if request.method == 'POST':
    #     Item.objects.create(text=request.POST['item_text'])
    #     # return redirect('/')
    #     return redirect('/lists/the-only-list-in-the-world/')

    # items = Item.objects.all()
    # return render(request, 'home.html', {'items': items})
    return render(request, 'home.html', {'form': ItemForm()})


def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    # error = None
    # items = Item.objects.filter(list=list_)
    # form = ItemForm()
    form = ExistingListItemForm(for_list=list_)
    if request.method == 'POST':
        # try:
        #     item = Item(text=request.POST['text'], list=list_)
        #     item.full_clean()
        #     item.save()
        #     # return redirect('/lists/%d/' % (list_.id,))
        #     return redirect(list_)
        # except ValidationError:
        #     error = "You can't have an empty list item"
        
        # form = ItemForm(data=request.POST)
        form = ExistingListItemForm(for_list=list_, data=request.POST)
        if form.is_valid():
            # Item.objects.create(text=request.POST['text'], list=list_)
            form.save()
            return redirect(list_)
    
    return render(request, 'list.html', {
        'list': list_, 'form': form #, 'error': error
    })


# def new_list(request):
#     # list_ = List.objects.create()
#     # item = Item.objects.create(text=request.POST['text'], list=list_)
#     # try:
#     #     item.full_clean()
#     #     item.save()
#     # except ValidationError:
#     #     list_.delete()
#     #     error = "You can't have an empty list item"
#     #     return render(request, 'home.html', {"error" : error})
#     # # return redirect('/lists/the-only-list-in-the-world/')
#     # # return redirect('/lists/%d/' % (list_.id,))
#     # return redirect(list_)

#     form = ItemForm(data=request.POST)
#     if form.is_valid():
#         # Item.objects.create(text=request.POST['text'], list=list_)
#         # list_ = List.objects.create()

#         list_ = List()
#         if request.user.is_authenticated():
#             list_.owner = request.user
#         list_.save()
#         form.save(for_list=list_)
#         return redirect(list_)
#     else:
#         return render(request, 'home.html', {'form': form})


# def new_list2(request):
def new_list(request):
    form = NewListForm(data=request.POST)
    if form.is_valid():
        list_ = form.save(owner=request.user)
        return redirect(list_)
    return render(request, 'home.html', {'form': form})


def my_lists(request, email):
    owner = User.objects.get(email=email)
    return render(request, 'my_lists.html', {'owner': owner})


# def add_item(request, list_id):
#     list_ = List.objects.get(id=list_id)
#     Item.objects.create(text=request.POST['item_text'], list=list_)
#     return redirect('/lists/%d/' % (list_.id,))