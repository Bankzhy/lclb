from django.db import models
from django.utils import timezone
# Create your models here.
class ProjectMaster(models.Model):
    project_id = models.AutoField(primary_key=True)
    project_name = models.CharField(max_length=100, blank=False, null=False)
    method_count = models.PositiveIntegerField(default=0, blank=False, null=False)
    class_count = models.PositiveIntegerField(default=0, blank=False, null=False)
    add_time = models.DateTimeField(default=timezone.now, blank=False, null=False)

    class Meta:
        db_table = "project_master"


class LCProjectMaster(models.Model):
    project_id = models.AutoField(primary_key=True)
    project_name = models.CharField(max_length=100, blank=False, null=False)
    class_count = models.PositiveIntegerField(default=0, blank=False, null=False)
    path = models.CharField(max_length=255, blank=False, null=False, default="")
    add_time = models.DateTimeField(default=timezone.now, blank=False, null=False)

    class Meta:
        db_table = "lc_project_master"


class LCPosClass(models.Model):
    class_id = models.AutoField(primary_key=True)
    class_name = models.CharField(max_length=100, blank=False, null=False)
    extra_method = models.CharField(max_length=255, blank=False, null=False)
    extra_field = models.CharField(max_length=255, blank=False, null=False)
    add_time = models.DateTimeField(default=timezone.now, blank=False, null=False)
    path = models.CharField(max_length=255, blank=False, null=False, default="")
    project_id = models.PositiveIntegerField(default=0, blank=False, null=False)

    class Meta:
        db_table = "lc_pos_class"


class LCNegClass(models.Model):
    class_id = models.AutoField(primary_key=True)
    class_name = models.CharField(max_length=100, blank=False, null=False)
    add_time = models.DateTimeField(default=timezone.now, blank=False, null=False)
    path = models.CharField(max_length=255, blank=False, null=False, default="")
    project_id = models.PositiveIntegerField(default=0, blank=False, null=False)

    class Meta:
        db_table = "lc_neg_class"


class MethodWaitMaster(models.Model):
    method_id = models.AutoField(primary_key=True)
    method_name = models.CharField(max_length=100, blank=False, null=False)
    class_name = models.CharField(max_length=100, blank=False, null=False)
    param_count = models.PositiveIntegerField(default=0, blank=False, null=False)
    return_type = models.CharField(max_length=100, blank=False, null=False)
    project_id = models.PositiveIntegerField(default=0, blank=False, null=False)
    path = models.CharField(max_length=255, blank=False, null=False)
    content = models.TextField(blank=False, null=False, default="")
    add_time = models.DateTimeField(default=timezone.now, blank=False, null=False)
    reviewed = models.BooleanField(default=False)

    class Meta:
        db_table = "method_wait_master"
        unique_together = ('method_id', 'project_id')


class NegMethodMaster(models.Model):
    method_id = models.PositiveIntegerField(primary_key=True)
    method_name = models.CharField(max_length=100, blank=False, null=False)
    class_name = models.CharField(max_length=100, blank=False, null=False)
    param_count = models.PositiveIntegerField(default=0, blank=False, null=False)
    return_type = models.CharField(max_length=100, blank=False, null=False)
    project_id = models.PositiveIntegerField(default=0, blank=False, null=False)
    path = models.CharField(max_length=255, blank=False, null=False)
    content = models.TextField(blank=False, null=False, default="")
    review_time = models.DateTimeField(default=timezone.now, blank=False, null=False)

    class Meta:
        db_table = "neg_method_master"


class QuesMaster(models.Model):
    ques_id = models.AutoField(primary_key=True)
    ques = models.CharField(max_length=100, blank=False, null=False)
    detail = models.CharField(max_length=1000, blank=False, null=False, default="")
    add_time = models.DateTimeField(default=timezone.now, blank=False, null=False)

    class Meta:
        db_table = "ques_master"


class PosMethodMaster(models.Model):
    method_id = models.PositiveIntegerField(primary_key=True)
    method_name = models.CharField(max_length=100, blank=False, null=False)
    class_name = models.CharField(max_length=100, blank=False, null=False)
    param_count = models.PositiveIntegerField(default=0, blank=False, null=False)
    return_type = models.CharField(max_length=100, blank=False, null=False)
    project_id = models.PositiveIntegerField(default=0, blank=False, null=False)
    path = models.CharField(max_length=255, blank=False, null=False)
    content = models.TextField(blank=False, null=False, default="")
    review_time = models.DateTimeField(default=timezone.now, blank=False, null=False)
    level = models.PositiveIntegerField(default=0, blank=False, null=False)
    ex_pos = models.CharField(max_length=100,default="", blank=False, null=False)

    class Meta:
        db_table = "pos_method_master"


class MethodQues(models.Model):
    method_ques_id = models.AutoField(primary_key=True)
    ques_id = models.PositiveIntegerField(default=0, blank=False, null=False)
    method_id = models.PositiveIntegerField(default=0, blank=False, null=False)
    answer = models.CharField(max_length=100, blank=False, null=False)

    class Meta:
        db_table = "method_ques"
        unique_together = ('ques_id', 'method_id')


class LCAllClass(models.Model):
    class_id = models.AutoField(primary_key=True)
    class_name = models.CharField(max_length=255, blank=False, null=False)
    project_name = models.CharField(max_length=100, blank=False, null=False, default="")
    path = models.CharField(max_length=1000, blank=False, null=False, default="")
    loc = models.FloatField(blank=False, null=False)
    nom = models.FloatField(blank=False, null=False)
    cis = models.FloatField(blank=False, null=False)
    noa = models.FloatField(blank=False, null=False)
    nopa = models.FloatField(blank=False, null=False)
    atfd = models.FloatField(blank=False, null=False)
    wmc = models.FloatField(blank=False, null=False)
    tcc = models.FloatField(blank=False, null=False)
    lcom = models.FloatField(blank=False, null=False)
    dcc = models.FloatField(blank=False, null=False)
    cam = models.FloatField(blank=False, null=False)
    dit = models.FloatField(blank=False, null=False)
    noam = models.FloatField(blank=False, null=False, default=0)
    field_t = models.TextField(blank=False, null=False, default="")
    method_t = models.TextField(blank=False, null=False, default="")
    is_merged = models.BooleanField(default=False)
    is_eval = models.BooleanField(default=False)
    merged_type = models.CharField(max_length=100, blank=False, null=False, default="")
    label = models.CharField(max_length=100, blank=False, null=False, default="")
    extract_methods = models.CharField(max_length=10000, blank=False, null=False, default="")
    add_time = models.DateTimeField(default=timezone.now, blank=False, null=False)

    class Meta:
        db_table = "lc_all_class"
        unique_together = ('class_name', 'project_name')


class LCEvalRefactoringResults(models.Model):
    lc_eval_refactoring_id = models.AutoField(primary_key=True)
    class_id = models.PositiveIntegerField(default=0, blank=False, null=False)
    class_name = models.CharField(max_length=255, blank=False, null=False, default='')
    gcn_results = models.TextField(blank=False, null=False, default="")
    sage_results = models.TextField(blank=False, null=False, default="")
    gat_results = models.TextField(blank=False, null=False, default="")
    hac_results = models.TextField(blank=False, null=False, default="")

    class Meta:
        db_table = "lc_eval_refactoring_results"

class LMGen(models.Model):
    method_id = models.AutoField(primary_key=True)
    method_name = models.CharField(max_length=255, blank=False, null=False)
    project_name = models.CharField(max_length=100, blank=False, null=False, default="")
    path = models.CharField(max_length=1000, blank=False, null=False, default="")
    extract_statement = models.CharField(max_length=10000, blank=False, null=False, default="")
    add_time = models.DateTimeField(default=timezone.now, blank=False, null=False)

    class Meta:
        db_table = "lm_gen"

class LMNEval(models.Model):
    lmn_eval_id = models.AutoField(primary_key=True)
    method_name = models.CharField(max_length=255, blank=False, null=False)
    review_extract_st = models.CharField(max_length=255, blank=False, null=False)
    am_extract_st = models.CharField(max_length=255, blank=False, null=False)
    jdeo_extract_st = models.CharField(max_length=255, blank=False, null=False)

    class Meta:
        db_table = "lmn_eval"