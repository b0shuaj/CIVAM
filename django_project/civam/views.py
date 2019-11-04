from django.shortcuts import render, get_object_or_404, redirect, HttpResponse, HttpResponseRedirect
from guardian.shortcuts import assign_perm, remove_perm, get_objects_for_user
from guardian.decorators import permission_required
from .models import *
from .forms import *


# Create your views here.
def index(request):
    return HttpResponse("index")

def collection_list(request):
    collection_list = Collection.objects.filter(public=True)
    collection_list = get_objects_for_user(request.user, 'civam.view_collection', collection_list, accept_global_perms=False)
    context = {'collection_list' : collection_list}
    return render(request, 'civam/collection_list.html', context)

def new_collection(request):
    form = CollectionForm(request.POST or None)
    if(request.method == 'POST'):
        if form.is_valid():
            col_instance = form.save(commit=False)
            col_instance.created_by = request.user
            col_instance.modified_by = request.user
            col_instance.save()
            return redirect("collection", collection_id = col_instance.id)

    context = {'collection_form': form}
    return render(request, 'civam/new_collection.html', context)

@permission_required('civam.view_item', (Item, 'id', 'item_id'), return_403=True)
def item(request, collection_id, item_id):
    item = get_object_or_404(Item, pk=item_id)
    if(request.method == 'POST'):
        form = StoryForm(request.POST)
        if form.is_valid():
            story_instance = form.save(commit=False)
            story_instance.item = item 
            story_instance.created_by = request.user
            story_instance.modified_by = request.user
            story_instance.save()
            return HttpResponseRedirect("")

    stories = Story.objects.filter(item_id=item_id)
    try :
        image = Image.objects.filter(item_id=item_id)
    except Image.DoesNotExist:
        image = None
    
    form = StoryForm()
    if request.user.has_perm("civam.view_item",item):
        #add edit and delete options in template
        context = {'item': item, 'stories': stories, 'form': form, 'images': image}
        return render(request, 'civam/item.html', context)
    else:
        return HttpResponse(str(request.user)+" cannot view this item")

def new_item(request, collection_id):
    collection = get_object_or_404(Collection, pk=collection_id)
    if(request.method== 'POST'):
        item_form = ItemForm(request.POST, prefix='item')
        video_form = VideoForm(request.POST, prefix='video')
        if item_form.is_valid():
            item_instance = item_form.save(commit=False)
            item_instance.collection = collection
            item_instance.created_by = request.user
            item_instance.modified_by = request.user
            item_instance.save()
            for image in request.FILES.getlist('images'):
                image_instance = Image(item=item_instance,content=image)
                image_instance.save()
            if video_form.is_valid():
                link = video_form.cleaned_data['link']
                video_instance = Video(link=link, item=item_instance)
                video_instance.save()
            return redirect("collection", collection_id=collection_id)
    #regular GET
    item_form = ItemForm(prefix = 'item')
    image_form = ImageForm(prefix = 'image')
    video_form = VideoForm(prefix = 'video')
    context = {'item_form': item_form, 'image_form': image_form, 'video_form': video_form, 'collection': collection}
    return render(request, 'civam/new_item.html', context)


@permission_required('civam.view_collection', (Collection, 'id', 'collection_id'), return_403=True)
def collection(request, collection_id):
    collection = get_object_or_404(Collection, pk=collection_id)
    item_list = Item.objects.filter(collection=collection)
    item_list = get_objects_for_user(request.user, 'civam.view_item', item_list, accept_global_perms=False)
    context = {'item_list': item_list, 'collection': collection}
    #add edit and delete options in template
    return render(request, 'civam/collection.html', context)

def grant_perm(request, obj_type, obj, permi):
    if not obj:
        return HttpResponse("Select an object to give permissions to")
    elif obj_type.casefold() == "item":
        item = Item.objects.get(name__iexact=obj)
    elif obj_type.casefold() == "collection":
        item = Collection.objects.get(title__iexact=obj)
    else:
        return HttpResponse("Select an object type of the object")

    if not permi:
        return HttpResponse("No permission to grant")
    elif request.user.has_perm("civam."+permi, item):
        return HttpResponse("Permission *"+obj_type.capitalize()+" "+str(permi)+"* already granted")
    else:
        assign_perm("civam."+permi, request.user, item)
        return HttpResponse("Permission *"+obj_type.capitalize()+" "+str(permi)+"* granted")
      
def revoke_perm(request, obj_type, obj, permi):
    if not obj:
        return HttpResponse("Select an object to revoke permissions of")
    elif obj_type.casefold() == "item":
        item = Item.objects.get(name__iexact=obj)
    elif obj_type.casefold() == "collection":
        item = Collection.objects.get(title__iexact=obj)
    else:
        return HttpResponse("Select an object type of the object")

    if not permi:
        return HttpResponse("No permission to revoke")
    elif not request.user.has_perm("civam."+permi,item):
        return HttpResponse("Permission *"+obj_type.capitalize()+" "+str(permi)+"* already revoked")
    else:
        remove_perm(permi, request.user, item)
        return HttpResponse("Permission *"+obj_type.capitalize()+" "+str(permi)+"* revoked")

