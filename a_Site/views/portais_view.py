from django.shortcuts import render, get_object_or_404

from a_Site.models import FactoryClassModel

def index(request, url):

    print(url)

    Site = FactoryClassModel.get_class('site')
    site = get_object_or_404(Site, url=url)

    context = {
        'site' : site
    }

    return render(request, 'layouts/comum/index.html', context)