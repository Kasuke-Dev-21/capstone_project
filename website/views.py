from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.template import loader
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from .models import Student, Report
from .models import Map
from .forms import StudentForm
from .forms import HazardReportForm

def main(request):
  context = {}
  context['user'] = request.user
  return render(request, 'topnav/home.html', context)

def contact(request):
  context = {}
  context['user'] = request.user
  return render(request, 'topnav/contact.html', context)

def about(request):
  context = {}
  context['user'] = request.user
  return render(request, 'topnav/about.html', context)

def members(request):
  students = Student.objects.all().order_by('-level', 'strand', 'firstname').values()
  template = loader.get_template('database/database.html')
  context = {
    'students': students,
  }
  return HttpResponse(template.render(context, request))

def profile(request, id):
  student = Student.objects.get(id=id)
  template = loader.get_template('database/desc.html')
  context = {
    'student': student,
  }
  return HttpResponse(template.render(context, request))


@login_required(login_url='/login/')
def change(request, student_id):
  student = get_object_or_404(Student, id=student_id)

  if request.method == 'POST':
    form = StudentForm(request.POST, instance=student)
    if form.is_valid():
      form.save()
      return HttpResponseRedirect(reverse('profile', args=[student_id]))
  else:
    form = StudentForm(instance=student)

  context = {'form': form}
  return render(request, 'database/changedesc.html', context)

def map_view(request):
  maps = Map.objects.all()
  return render(request, 'maps/maps.html', {'maps': maps})

def report(request):
    # Check if user has exceeded rate limit
    user_ip = request.META.get('REMOTE_ADDR')
    key = f'rate_limit:{user_ip}'
    count = cache.get(key)

    if count and count >= 5:  # Limit to 5 submissions per IP address
        return HttpResponseForbidden('Rate limit exceeded.')

    if request.method == 'POST':
        form = HazardReportForm(request.POST)
        if form.is_valid():
            form.save()
            # Increment count
            cache.set(key, count + 1 if count else 1, timeout=3600)  # Set expiry to 1 hour
            return HttpResponseRedirect(reverse('maps'))  # Redirect to success page
    else:
        form = HazardReportForm()
    return render(request, 'maps/report.html', {'form': form})

@login_required(login_url='/login/')
def search_reports(request):
    reports = Report.objects.all()
    return render(request, 'maps/filed_cards.html', {'reports': reports})

def update_status(request):
    if request.method == 'POST':
        report_id = request.POST.get('report_id')
        new_status = request.POST.get('new_status')

        # Update the status of the report
        report = Report.objects.get(pk=report_id)
        report.status = new_status
        report.save()

        if new_status == 'Removed':
            report.delete()

        return redirect('search_reports')

def map_edit(request):
  maps = Map.objects.all()
  return render(request, 'maps/map-edit.html', {'maps': maps})

def qr_scan(request):
    if request.method == 'POST':
        num_id = request.POST.get('num_id')
        student = get_object_or_404(Student, num_id=num_id)
        data = {
            'firstname': student.firstname,
            'lastname': student.lastname,
            'fullname': student.fullname,
            'level': student.get_level_display(),
            'strand': student.get_strand_display(),
            'status': student.get_status_display()
        }
        return JsonResponse(data)
    return render(request, 'QR/update_qr.html')

def get_student_by_num_id(request):
    num_id = request.GET.get('num_id')
    try:
        student = Student.objects.get(num_id=num_id)
        # Serialize the student object to JSON
        student_data = {
            'firstname': student.firstname,
            'lastname': student.lastname,
            'num_id': student.num_id,
        }
        return JsonResponse(student_data)
    except Student.DoesNotExist:
        return JsonResponse({'error': 'Student not found'}, status=404)

def testing(request):
    reports = Report.objects.all()
    return render(request, '_debug/template.html', {'reports': reports})

