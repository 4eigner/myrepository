from django.forms import ModelForm, TextInput, Textarea, URLInput

from main.models import Experience, Education

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

class EducationForm(ModelForm):
    class Meta:
        model = Education
        fields = {
            "institution",
            "degree",
            "field_of_study",
            "description",
            "start_year",
            "end_year",
        }

        labels = {
            "institution": "Masukkan nama institusi",
            "degree": "Masukkan derajat sekolah",
            "field_of_study": "Masukkan bidang pendidikan",
            "description": "Deskripsi pendidikan",
            "start_year": "Tahun memulai",
            "end_year": "Tahun berakhir",
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

