from django.contrib import messages

def activate_status(request, obj):
    obj.status = True
    obj.save()
    messages.success(request, "Successfully activated!")
    return True

def deactivate_status(request, obj):
    obj.status = False
    obj.save()
    messages.success(request, "Successfully de-activated!")
    return True