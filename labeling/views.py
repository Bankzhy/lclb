import csv
import datetime
import json
from pathlib import Path

from django.core import serializers
from django.db.models import Q
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponse
from django.shortcuts import render
from django.utils import timezone

# Create your views here.
from django.views.decorators.csrf import csrf_exempt


from lib.sitter.ast2core import ASTParse

from labeling.models import PosMethodMaster, NegMethodMaster, ProjectMaster, MethodWaitMaster

from labeling.models import QuesMaster

from labeling.models import MethodQues

from lib.reflect.metrics import ClassLevelMetrics

from labeling.models import LCProjectMaster

from labeling.models import LCPosClass, LCNegClass

from labeling.models import LCAllClass


def index(request):
    user = request.user if request.user.is_authenticated else None
    context = {
        'active_menu': 'homepage',
        'user': user
    }
    return render(request, 'labeling/index.html', context)

def lc_index(request):
    user = request.user if request.user.is_authenticated else None
    context = {
        'active_menu': 'homepage',
        'user': user
    }
    return render(request, 'labeling/lc_index.html', context)

@csrf_exempt
def create_lc_project(request):
    data = json.loads(request.body)
    print(data)
    project_path = Path(data["path"])
    class_count = 0
    ast = ASTParse(project_path, "java")
    ast.setup()
    sr_project = ast.do_parse()
    result_list = []
    for program in sr_project.program_list:
        for cls in program.class_list:
            class_count += 1

    method_count = 0
    new_project = LCProjectMaster(
        project_name=data['name'],
        class_count=class_count,
        path=project_path
    )
    new_project.save()
    return JsonResponse(data, safe=False)


@csrf_exempt
def create_project(request):
    data = json.loads(request.body)
    print(data)
    project_path = Path(data["path"])
    method_count = 0
    class_count = 0
    new_project = ProjectMaster(
        project_name=data['name'],
        method_count=method_count,
        class_count=class_count
    )
    new_project.save()
    try:
        ast = ASTParse(project_path, "java")
        ast.setup()
        sr_project = ast.do_parse()
        for program in sr_project.program_list:
            class_count += len(program.class_list)
            for clas in program.class_list:
                # method_count += len(clas.method_list)
                for method in clas.method_list:
                    loc = method.get_method_LOC()
                    if loc < 5:
                        continue
                    try:
                        new_method = MethodWaitMaster(
                            method_name=method.method_name,
                            class_name=clas.class_name,
                            param_count=len(method.param_list),
                            return_type=method.return_type,
                            project_id=new_project.project_id,
                            path=program.program_name,
                            content=method.to_string(space=0)
                        )
                        new_method.save()
                        method_count += 1
                    except Exception as e:
                        print(e)
                        continue
        new_project.method_count = method_count
        new_project.class_count = class_count
        new_project.save()

        return JsonResponse(data, safe=False)
    except Exception as e:
        print(e)
        return HttpResponseBadRequest()


@csrf_exempt
def lc_project_list(request):
    project_list = LCProjectMaster.objects.all()
    re = serializers.serialize('json', project_list)

    return HttpResponse(re, content_type="text/json-comment-filtered")

@csrf_exempt
def project_list(request):
    project_list = ProjectMaster.objects.all()
    re = serializers.serialize('json', project_list)

    return HttpResponse(re, content_type="text/json-comment-filtered")

@csrf_exempt
def ques_list(request):
    ques_list = QuesMaster.objects.all()
    re = serializers.serialize('json', ques_list)

    return HttpResponse(re, content_type="text/json-comment-filtered")


@csrf_exempt
def method_list(request):
    pid = request.GET['pid']
    method_list = MethodWaitMaster.objects.filter(
        project_id=pid,
        reviewed=False,
    )
    re = serializers.serialize('json', method_list)

    print(pid)
    return HttpResponse(re, content_type="text/json-comment-filtered")


def class_list(request):
    pid = request.GET['pid']
    if pid == '2':
        cls_list = LCAllClass.objects.filter(label='wait', is_eval=True)
    elif pid == '3':
        cls_list = LCAllClass.objects.filter(extract_methods='', is_eval=True, label='pos')
    else:
        cls_list = LCAllClass.objects.filter(label='wait').order_by('?')[:100]
    result_list = []
    print(cls_list)
    for dcls in cls_list:
        ast = ASTParse('', "java")
        ast.setup()
        sr_project = ast.do_parse_one_file(dcls.path)
        for program in sr_project.program_list:
            for cls in program.class_list:
                if "Test" in cls.class_name or "test" in cls.class_name:
                    continue

                if len(cls.method_list) <= 0:
                    continue

                re_field_l = []
                re_method_l = []
                print(cls.class_name)
                for f in cls.field_list:
                    new_re_field = {
                        "id": f.id,
                        "str": f.to_string()
                    }
                    re_field_l.append(new_re_field)

                for m in cls.method_list:
                    metrics = ClassLevelMetrics(sr_class=cls)
                    loc = metrics.get_method_loc(m)
                    cc = metrics.get_method_cc(m)
                    pc = metrics.get_method_pc(m)
                    new_re_method = {
                        "id": m.id,
                        "method_name": m.method_name,
                        "loc": loc,
                        "cc": cc,
                        "pc": pc

                    }
                    re_method_l.append(new_re_method)
                method_field_d, field_method_d = parse_class(cls)
                new_re = {
                    "re_field_l": re_field_l,
                    "re_method_l": re_method_l,
                    "method_field_d": method_field_d,
                    "field_method_d": field_method_d,
                    "class_name": cls.class_name,
                    "path": str(program.program_name),
                    "class_content": cls.to_string(),
                    "class_id": dcls.class_id,
                    "cloc": dcls.loc,
                    "cwmc": dcls.wmc,
                    "clcom": dcls.lcom

                }
                result_list.append(new_re)
    return JsonResponse(result_list, safe=False)

@csrf_exempt
def class_list_t(request):
    pid = request.GET['pid']
    pj = LCProjectMaster.objects.get(project_id=pid)
    project_path = Path(pj.path)
    pos_l = LCPosClass.objects.values_list("class_name", flat=True).filter(project_id=pid)
    neg_l = LCNegClass.objects.values_list("class_name", flat=True).filter(project_id=pid)
    pos_l = list(pos_l)
    neg_l = list(neg_l)
    ast = ASTParse(project_path, "java")
    ast.setup()
    sr_project = ast.do_parse()
    result_list = []
    for program in sr_project.program_list:
        for cls in program.class_list:
            if cls.class_name in pos_l or cls.class_name in neg_l:
                continue

            if "Test" in cls.class_name or "test" in cls.class_name:
                continue

            if len(cls.method_list) <= 0:
                continue

            re_field_l = []
            re_method_l = []
            for f in cls.field_list:
                new_re_field = {
                    "id": f.id,
                    "str": f.to_string()
                }
                re_field_l.append(new_re_field)

            for m in cls.method_list:
                metrics = ClassLevelMetrics(sr_class=cls)
                loc = metrics.get_method_loc(m)
                cc = metrics.get_method_cc(m)
                pc = metrics.get_method_pc(m)
                new_re_method = {
                    "id": m.id,
                    "method_name": m.method_name,
                    "loc": loc,
                    "cc": cc,
                    "pc": pc

                }
                re_method_l.append(new_re_method)
            method_field_d, field_method_d = parse_class(cls)
            new_re = {
                "re_field_l": re_field_l,
                "re_method_l": re_method_l,
                "method_field_d": method_field_d,
                "field_method_d": field_method_d,
                "class_name": cls.class_name,
                "path": str(program.program_name)
            }
            result_list.append(new_re)

    return JsonResponse(result_list, safe=False)

def parse_class(cls):
    f_n_l = [o.field_name for o in cls.field_list]
    method_field_d = {}
    for m in cls.method_list:
        method_fields = []
        for st in m.statement_list:
            for word in st.word_list:
                if word in f_n_l:
                    f_index = f_n_l.index(word)
                    f_id = cls.field_list[f_index].id
                    method_fields.append(f_id)
        method_fields = list(set(method_fields))
        method_field_d[m.id] = method_fields

    field_method_d = {}
    for mf in method_field_d:
        for f in method_field_d[mf]:
            if f in field_method_d.keys():
                field_method_d[f].append(mf)
            else:
                field_method_d[f] = [mf]
    return method_field_d, field_method_d


@csrf_exempt
def code_table(request):
    data = json.loads(request.body)
    print(data)
    class_name = data['class_name']
    method_name = data['method_name']
    pc = data['pc']
    project_path = Path(data["path"])
    project_path = project_path

    try:
        ast = ASTParse(project_path, "java")
        ast.setup()
        sr_project = ast.do_parse_one_file(project_path)
        for program in sr_project.program_list:
            for clas in program.class_list:
                for method in clas.method_list:
                    if method.method_name == method_name \
                            and clas.class_name == class_name \
                            and str(len(method.param_list)) == str(pc):
                        method.refresh_sid()
                        stb = method.to_string_table()
                        return JsonResponse(stb, safe=False)
        return HttpResponseBadRequest()
    except Exception as e:
        print(e)
        return HttpResponseBadRequest()

@csrf_exempt
def post_pos_class(request):
    data = json.loads(request.body)
    lc_cls = LCAllClass.objects.get(class_id=data["class_id"])
    lc_cls.label = "pos"
    lc_cls.extract_methods = data['extra_methods']
    lc_cls.add_time = str(timezone.now())
    lc_cls.save()
    # new_pos = LCPosClass(
    #     class_name=data["class_name"],
    #     extra_method=data['extra_method'],
    #     extra_field=data['extra_field'],
    #     path=data["path"],
    #     project_id=data["project_id"]
    # )
    # new_pos.save()
    return JsonResponse(data, safe=False)

@csrf_exempt
def post_neg_class(request):
    data = json.loads(request.body)
    lc_cls = LCAllClass.objects.get(class_id=data["class_id"])
    lc_cls.label = "neg"
    lc_cls.add_time = str(timezone.now())
    lc_cls.save()
    # new_neg = LCNegClass(
    #     class_name=data["class_name"],
    #     path=data["path"],
    #     project_id=data["project_id"]
    # )
    # new_neg.save()
    return JsonResponse(data, safe=False)

@csrf_exempt
def post_del_class(request):
    data = json.loads(request.body)
    lc_cls = LCAllClass.objects.get(class_id=data["class_id"])
    lc_cls.label = "del"
    lc_cls.add_time = str(timezone.now())
    lc_cls.save()
    # new_neg = LCNegClass(
    #     class_name=data["class_name"],
    #     path=data["path"],
    #     project_id=data["project_id"]
    # )
    # new_neg.save()
    return JsonResponse(data, safe=False)

@csrf_exempt
def post_pos(request):
    data = json.loads(request.body)
    method_id = data["method_id"]
    method_name = data["method_name"]
    class_name = data["class_name"]
    param_count =data["param_count"]
    return_type = data["return_type"]
    project_id = data["project_id"]
    path = data["path"]
    content = data["content"]
    level = data["level"]
    ex_pos = data["ex_pos"]

    new_pos = PosMethodMaster(
        method_id=method_id,
        method_name=method_name,
        class_name=class_name,
        param_count=param_count,
        return_type=return_type,
        project_id=project_id,
        path=path,
        content=content,
        level=level,
        ex_pos=ex_pos
    )
    new_pos.save()

    method_w = MethodWaitMaster.objects.get(method_id=method_id)
    method_w.reviewed = True
    method_w.save()
    return JsonResponse(data, safe=False)

@csrf_exempt
def post_neg(request):
    data = json.loads(request.body)
    method_id = data["method_id"]
    method_name = data["method_name"]
    class_name = data["class_name"]
    param_count =data["param_count"]
    return_type = data["return_type"]
    project_id = data["project_id"]
    path = data["path"]
    content = data["content"]
    new_neg = NegMethodMaster(
        method_id=method_id,
        method_name=method_name,
        class_name=class_name,
        param_count=param_count,
        return_type=return_type,
        project_id=project_id,
        path=path,
        content=content
    )
    new_neg.save()

    method_w = MethodWaitMaster.objects.get(method_id=method_id)
    method_w.reviewed = True
    method_w.save()
    return JsonResponse(data, safe=False)

@csrf_exempt
def post_ques(request):
    data = json.loads(request.body)
    ques_id = data['ques_id']
    method_id = data['method_id']
    answer = data['answer']
    new_method_ques = MethodQues(
        ques_id=ques_id,
        method_id=method_id,
        answer=answer
    )
    new_method_ques.save()
    return JsonResponse(data, safe=False)

@csrf_exempt
def export_csv(request):
    data = json.loads(request.body)
    save_path = Path(data["save_path"])
    project_id = data["project_id"]
    project_name = ProjectMaster.objects.get(project_id=project_id).project_name
    pos_method_l = PosMethodMaster.objects.filter(project_id=project_id)
    neg_method_l = PosMethodMaster.objects.filter(project_id=project_id)
    method_l = []
    method_l.extend(pos_method_l)
    method_l.extend(neg_method_l)

    node_field_order = ["id", 'path', 'class_name', 'method_name', 'param_count', 'return_type', 'ex_pos', 'level', 'project']
    with open(save_path / "index.csv", 'w', encoding="utf-8", newline='') as csvfile:
        writer = csv.DictWriter(csvfile, node_field_order)
        writer.writeheader()
        for m in method_l:
            writer.writerow(dict(zip(node_field_order, [m.method_id, m.path,
                                                        m.class_name, m.method_name,
                                                        m.param_count, m.return_type,
                                                        m.ex_pos, m.level, project_name])))

    return JsonResponse(data, safe=False)


def review(request):
    user = request.user if request.user.is_authenticated else None
    context = {
        'active_menu': 'review',
        'user': user
    }
    return render(request, 'labeling/review.html', context)


def lc_review(request):
    user = request.user if request.user.is_authenticated else None
    context = {
        'active_menu': 'lc_review',
        'user': user
    }
    return render(request, 'labeling/lc_review.html', context)