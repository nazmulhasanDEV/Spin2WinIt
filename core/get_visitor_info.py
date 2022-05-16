from adminPanel.models import VisitorInfo, TotalNumVisitor
def get_or_countVisitorInfo(x_forwarded_for, request_obj):

    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()

        visitor_ipList_model = VisitorInfo.objects.filter(visitor_ip=ip).first()

        if visitor_ipList_model is None:
            visitorIpListModel = VisitorInfo.objects.create(visitor_ip=ip)

        # visitor count model
        visitor_count_model = TotalNumVisitor.objects.filter().first()
        if visitor_count_model:
            visitor_count_model.num_of_visitor = visitor_count_model.num_of_visitor + 1
            visitor_count_model.save()
        else:
            visitorCountModel = TotalNumVisitor.objects.create(num_of_visitorf=1)

    else:
        ip = request_obj.META.get('REMOTE_ADDR')
        visitor_ipList_model = VisitorInfo.objects.filter(visitor_ip=ip).first()

        if visitor_ipList_model is None:
            visitorIpListModel = VisitorInfo.objects.create(visitor_ip=ip)

        # visitor count model
        visitor_count_model = TotalNumVisitor.objects.filter().first()
        if visitor_count_model:
            visitor_count_model.num_of_visitor = visitor_count_model.num_of_visitor + 1
            visitor_count_model.save()
        else:
            visitorCountModel = TotalNumVisitor.objects.create(num_of_visitor=1)

    return True