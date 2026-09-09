from django.shortcuts import render

from main.models import Experience


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
        "name": "Maurilla",
        "experience_list": Experience.objects.all(),
    }
    return render(request, "experience.html", context)