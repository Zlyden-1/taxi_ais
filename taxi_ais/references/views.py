from django.shortcuts import render
from django.http import HttpResponseRedirect

from .models import Contractor, Driver, Vehicle


def contractors(request):
    contractors_list = Contractor.objects.all().order_by('-renting_date')
    context = {'contractors': contractors_list,
               'drivers': Driver.objects.all(),
               'vehicles': Vehicle.objects.all()}
    return render(request, 'references/contractors.html', context)


def add_contractor(request):
    try:
        new_contractor = Contractor(driver=Driver.objects.get(pk=request.POST['driver']),
                                    vehicle=Vehicle.objects.get(pk=request.POST['vehicle']),
                                    renting_date=request.POST['renting_date'])
    except KeyError:
        return render(request, 'references/error.html', {
            'error_message': "You didn't select a choice.",
        })
    else:
        new_contractor.save()
        return HttpResponseRedirect(redirect_to='/references/contractors')
