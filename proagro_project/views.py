from django.shortcuts import redirect


def home(request):
   return redirect("view_proagro:home")
