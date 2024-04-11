from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.template import loader
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from .models import Student, Report, Map
from .forms import StudentForm, StudentStatusForm, HazardReportForm

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

@login_required(login_url='/login/')
def qr_scan(request):
    students = Student.objects.all()
    form = StudentStatusForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        student_id = request.POST.get('student_id')
        student = get_object_or_404(Student, num_id=student_id)
        student.status = form.cleaned_data['status']
        student.save()
    return render(request, 'QR/update_qr.html', {'students': students, 'form': form})

def testing(request):
    students = Student.objects.all()
    form = StudentStatusForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        student_id = request.POST.get('student_id')
        student = get_object_or_404(Student, num_id=student_id)
        student.status = form.cleaned_data['status']
        student.save()
    return render(request, '_debug/template.html', {'students': students, 'form': form})

