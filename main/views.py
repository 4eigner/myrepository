from django.shortcuts import render

from main.models import Experience, Education


def show_main(request):
    context = {
        "name": "Maurilla Maharani Nur Abdul",
        "npm": "2506588374",
        "study_program": "S1 Sistem Informasi",
        "bio": (
            "Mahasiswa Sistem Informasi Universitas Indonesia yang tertarik "
            "pada pengembangan perangkat lunak dan pendidikan."
        ),
    }
    return render(request, "index.html", context)


def show_experience(request):
    context = {
        "name": "Maurilla Maharani Nur Abdul",
        "experience_list": Experience.objects.all(),
    }
    return render(request, "experience.html", context)

def show_education(request):
    context = {
        "name": "Maurilla Maharani Nur Abdul",
        "education_list": Education.objects.all().order_by('-start_year'),
    }
    return render(request, "education.html", context)