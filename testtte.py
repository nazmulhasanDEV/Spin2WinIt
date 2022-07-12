# {% if profile_pic_list_of_ltst_accnts %}
#
#                                       {% for pic in profile_pic_list_of_ltst_accnts %}
#                                       {% if pic.user.pk == member.pk %}
#                                       <img src="{{pic.pic.url}}" style="width: 60px; height: 60px;" alt="User Image">
#                                       {% else %}
#                                       <img src="{% static 'backEnd/dist/img/avatar.png' %}" style="width: 60px; height: 60px;" alt="User Image">
#                                       {% endif %}
#                                       {% endfor %}
#
#                                       {% endif %}

a = [1, 'a', 3, 4, 5]
b = ['a', 'b', 'c']

for a in a:
    for b in b:
        if b == a:
            print(a)
        else:
            print(b)