from django.db import models


class Student(models.Model):
  firstname = models.CharField(max_length=255)
  lastname = models.CharField(max_length=255)
  fullname = models.CharField(max_length=255, null=True)
  grades = {
    "11": "Grade 11",
    "12": "Grade 12",
  }
  level = models.CharField(max_length=2, choices=grades)
  study = {
    "STEM": "Science, Technology, Engineering, and Mathematics",
    "ABM": "Accountancy, Business, and Management",
    "HUMSS": "Humanities and Social Sciences",
  }
  strand = models.CharField(max_length=5, choices=study)
  age = models.IntegerField(null=True)
  mail_address = models.CharField(max_length=255, null=True)
  mail = {
    "Gmail": "Gmail",
    "Outlook": "Microsoft Outlook",
    "Yahoo": "Yahoo!"
  }
  mail_type = models.CharField(max_length=15, choices=mail)
  contact = models.CharField(max_length=255)
  guardian_No = models.CharField(max_length=255, null=True)
  safety = {
    "Present": "Present",
    "Absent": "Absent",
    "Missing": "Missing",
    "Injured": "Injured",
    "Unknown": "Unknown",
  }
  status = models.CharField(max_length=10, choices=safety)
  num_id = models.CharField(max_length=12, null=True)
  address = models.CharField(max_length=255, null=True)


class Map(models.Model):
  title = models.CharField(max_length=255)
  image_path = models.CharField(max_length=255, null=True)

  def __str__(self):
    return self.title


class Report(models.Model):
  map = models.ForeignKey(Map, on_delete=models.CASCADE, null=True)  # Assuming Map is your existing model for building maps
  location = models.CharField(max_length=100)
  description = models.TextField()
  date_reported = models.DateTimeField(auto_now_add=True)
  category = {
    "Accident": "Accident",
    "Damaged Area": "Damaged Area",
    "Design Flaw": "Design Flaw",
    "Electrical Appliance": "Electrical Appliance",
    "Flammable": "Flammable",
    "Explosive": "Explosive",
    "Liquid Substance": "Slippery or Corrosive Substance",
    "Unknown": "Unknown"
  }
  type = models.CharField(max_length=255, choices=category, null=True)
  greenlit = {
    "Standby": "Not Used",
    "Active": "In Use",
    "Removed": "Removed",
  }
  status = models.CharField(max_length=255, choices=greenlit, null=True)

  def __str__(self):
    return f"Hazard Report - {self.map} - {self.get_type_display()}"
