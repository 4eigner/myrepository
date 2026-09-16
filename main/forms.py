from django.forms import ModelForm, TextInput, Textarea, URLInput

from main.models import Experience

class ExperienceForm(ModelForm):
    class Meta:
        model = Experience
        fields = {
            "title",
            "description",
            "category",
            "thumbnail",
            "started_at",
            "ended_at",
        }

        labels = {
            "title": "Nama Pengalaman",
            "description": "Deskripsi Pengalaman",
            "category": "Kategori Pengalaman",
            "thumbnail": "Foto Pengalaman",
            "started_at": "Tahun dimulai",
            "ended_at": "Tahun Berakhir",
        }

        widgets = {
            "title": TextInput(
                attrs={
                    "placeholder": "Software Engineer Intern",
                    "maxlength": 255,
                }
            ),
            "description": Textarea(
                attrs={
                    "placeholder": "Ceritakan pengalamanmu",
                    "rows": 3,
                }
            ),
            "thumbnail": URLInput(
                attrs={
                    "placeholder": "/static/img/MaurillaPortofolioPhoto.png",
                }
            ),
        }