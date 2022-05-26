from adminPanel.models import VisitorInfo, TotalNumVisitor
import requests

# this function returns visitors ip also
# def get_ip():
#     response = requests.get('https://api64.ipify.org?format=json').json()
#     return response["ip"]

def get_location(ip_adrs):
    response = requests.get(f'https://ipapi.co/{ip_adrs}/json/').json()
    location_data = {
        "city": response.get("city"),
        "region": response.get("region"),
        "country": response.get("country_name"),
        "continent_code": response.get("continent_code"),
        "postal": response.get("postal"),
        "latitude": response.get("latitude"),
        "longitude": response.get("longitude"),
        "timezone": response.get("timezone"),
    }
    return location_data

def get_or_countVisitorInfo(x_forwarded_for, request_obj):

    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()

        visitor_ipList_model = VisitorInfo.objects.filter(visitor_ip=ip).first()

        if visitor_ipList_model is None:
            details_of_crnt_ip = get_location(ip)

            visitorIpListModel = VisitorInfo.objects.create(
                visitor_ip=ip,
                visitors_country=details_of_crnt_ip['country'],
                country_code=details_of_crnt_ip['continent_code'],
                latitude=details_of_crnt_ip['postal'],
                longitude=details_of_crnt_ip['latitude'],
                timezone=details_of_crnt_ip['longitude'],
            )

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

            details_of_crnt_ip = get_location(ip)

            visitorIpListModel = VisitorInfo.objects.create(
                visitor_ip=ip,
                visitors_country=details_of_crnt_ip['country'],
                country_code=details_of_crnt_ip['continent_code'],
                latitude=details_of_crnt_ip['postal'],
                longitude=details_of_crnt_ip['latitude'],
                timezone=details_of_crnt_ip['longitude'],
            )

        # visitor count model
        visitor_count_model = TotalNumVisitor.objects.filter().first()
        if visitor_count_model:
            visitor_count_model.num_of_visitor = visitor_count_model.num_of_visitor + 1
            visitor_count_model.save()
        else:
            visitorCountModel = TotalNumVisitor.objects.create(num_of_visitor=1)

    return True