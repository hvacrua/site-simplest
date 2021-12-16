from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.views import View
from .models import Translator
from .forms import ClientForm
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from mysite.settings import EMAIL_HOST_USER, recipient_list
import json


@method_decorator(csrf_exempt, name='dispatch')
class NewClient(View):
    def get(self, request, *args, **kwargs):
        lang_meta = request.headers.get('mylang', 'en')  # to get value en, ua, ru
        language_dict = {}

        for field in Translator.objects.all():
            language_dict[field.unique_name] = field.__dict__[lang_meta]
        # # getattr(field, lang_meta)   field.en

        tree = {}

        for item in list(language_dict.keys()):
            temp_obj = tree
            parts = item.split('_')

            for part in parts[:-1]:
                if part not in temp_obj.keys():
                    temp_obj[part] = {}
                temp_obj = temp_obj[part]

            temp_obj[parts[-1]] = language_dict[item]

        # print(json.dumps(tree, indent=4))

        return JsonResponse(tree, json_dumps_params={'indent': 4})


        # main_title = get_object_or_404(Field, unique_name='main_title')
        #
        # if not hasattr(main_title, lang_meta):
        #     lang_meta = 'en'
        #
        # return JsonResponse({
        #     'main_title': getattr(main_title, lang_meta)
        # })

        # return render(request, 'base.html', {'form': ClientForm()})


    def post(self, request, *args, **kwargs):

        form = ClientForm(request.POST)
        lang_meta = request.headers.get('mylang', 'en')

        if form.is_valid():
            form.save()

            meeting = request.POST.get('meeting')
            email = request.POST.get('email')
            name = request.POST.get('name')
            phone = request.POST.get('phone')
            result = ['Your registration is successful']
            errors_list = []
            info_dict = {
                'messages': result, 'errors': errors_list,
                'lang_meta': lang_meta
            }

            subject = "New participant of meeting on {}".format(meeting)
            message = "Date: {0}\nEmail: {1}\nName: {2}\nPhone: {3}\n".format(
                meeting, email, name, phone)
            send_mail(subject, message, EMAIL_HOST_USER,
                      recipient_list, fail_silently=False)

            return JsonResponse(info_dict, json_dumps_params={'indent': 4})
        else:
            # print(form.errors.as_json())
            result = []
            errors_list = [value[0]['message'][:-1] for _, value in json.loads(form.errors.as_json()).items()]
            info_dict = {
                'messages': result, 'errors': errors_list, 'lang_meta': lang_meta
            }
            # print(f"type(lang_meta) = {type(lang_meta)}:\nlang_meta = {lang_meta},\n\ntype(lang_header) = {type(lang_header)}:\nlang_header = {lang_header}")

            return JsonResponse(info_dict, json_dumps_params={'indent': 4})


def test_page(request):
    return render(request, 'reg_form.html', {'form': ClientForm()})