from django.contrib import messages


def delete_obj(request, obj):
    obj.delete()
    messages.success(request, "Successfully deleted!")
    return True