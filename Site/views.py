from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect
from .models import Wall, Section, SectionField
from django.contrib.auth.models import User, Group
import requests
from django.contrib.auth import load_backend, login
from .models import Template
from django.template import engines
from django.http import Http404
from AapoonSite import settings

def index(request):
    context = {

    }
    if request.method == 'POST':

        phone_number = request.POST["phone_number"]
        country_code = request.POST["country_code"]
        url = "http://localhost:8001/api/v1/site_send_otp/"

        r = requests.post(url, data={'phone_number': phone_number, "country_code": country_code})

        if r.status_code == 200:
            request.session['phone_number'] = phone_number
            request.session['country_code'] = country_code
            # return redirect('verify_otp', foo='bar')
            return redirect('verify_otp')
        if r.status_code == 400:
            context["error"] = r.json()["detail"]
    template = loader.get_template('Site/login.html')


    return HttpResponse(template.render(context, request))


def verify_otp(request):
    if request.method == 'POST':

        phone_number = request.session['phone_number']
        country_code = request.session['country_code']
        otp = request.POST["otp"]
        url = "http://localhost:8001/api/v1/login_otp/"

        r = requests.post(url, data={'phone_number': phone_number, "country_code": country_code, "otp": otp})
        if r.status_code == 200:
            username = country_code+phone_number
            user, created = User.objects.get_or_create(username=username, is_staff=True)

            site_user_group = Group.objects.get(name='site_user')
            site_user_group.user_set.add(user)

            login(request, user)
            return redirect('/admin')
    template = loader.get_template('Site/verify_otp.html')
    context = {
        "phone_number": request.session['phone_number'],
        "country_code": request.session['country_code']
    }

    return HttpResponse(template.render(context, request))


def site_template(request, site=None):
    template = loader.get_template('Site/site.html')
    sites = Wall.objects.filter(created_by=request.user)
    if site:
        current_site = Wall.objects.get(id=site)
    else:
        current_site = sites[0]
    sections = Section.objects.filter(page=current_site.id)
    all_sections = []
    for section in sections:
        all_sections.append({"section_detail": section, "section_related_detail": [{'section_field': section_field} for section_field in SectionField.objects.filter(section=section)]})
    context = {
        "sites": sites,
        "current_site": current_site,
        "sections": all_sections,
        "circles": current_site.circles.all(),
        "AAPOON_SITE": settings.AAPOON_SITE
    }
    return HttpResponse(template.render(context, request))


def site(request, slug=None):
    wall_link = slug
    try:
        # Fetch the Wall Detail
        wall = Wall.objects.get(wall_link=wall_link)
    except:
        raise Http404

    # Fetch Wall Template
    db_template = Template.objects.get(id=wall.template_id)
    django_engine = engines['django']
    template = django_engine.from_string(db_template.content)

    # Fetch Section Detail
    sections = Section.objects.filter(page=wall.id)

    all_sections = []
    for section in sections:
        all_sections.append({"section_detail": section,
                             "section_related_detail": [{'section_field': section_field} for section_field in
                                                        SectionField.objects.filter(section=section)]})
    context = {
        "current_site": wall,
        "sections": all_sections
    }

    return HttpResponse(template.render(context, request))
