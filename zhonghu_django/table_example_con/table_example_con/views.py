from django.shortcuts import render
from django.db import models
from django.http import HttpResponse
import csv
import django_tables2 as tables
import pymysql
import datetime
import pytz
from django_tables2.config import RequestConfig
import itertools
from django.db import connection
from django.http import Http404
from django.shortcuts import render
import pandas as pd
# from djqscsv import render_to_csv_response

##### Modify with your database here #####
db = pymysql.connect(host="localhost", user="django_user", password="mypassword", db="zhonghu_test" , charset='utf8')
cursor = db.cursor()

category_list = ['All', 'iPhone应用推荐', 'iPhone新闻', 'Win10快讯', 'Win10设备', '业界', '人工智能', '人物', '天文航天', '奇趣电子', '安卓应用推荐',
                 '安卓手机', '安卓新闻', '影像器材', '新能源汽车', '智能家居', '智能家电', '活动互动', '游戏快报', '电商', '电子竞技', '电脑硬件', '科技前沿', '科普常识',
                 '笔记本', '网络', '苹果', '车联网', '软件快报', '辣品广告', '通信']


class news(models.Model):
    time = models.CharField(max_length=10, blank=True, null=True)
    title = models.CharField(max_length=10, blank=True, null=True)
    category = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        db_table = "news"


class newsTable(tables.Table):
    counter = tables.Column(verbose_name="No", empty_values=(), orderable=False)
    time = tables.Column(verbose_name="Time")
    title = tables.Column(verbose_name="Title")
    category = tables.Column(verbose_name="Category")

    def render_counter(self):
        self.row_counter = getattr(self, 'row_counter', itertools.count(1))
        return next(self.row_counter)

    class Meta:
        model = news
        attrs = {
            "class": "info-table",
        }
        fields = ("counter", "time", "title", "category")


def to_render(html_render, data, table):
    html_render['table'] = table
    html_render['category_list'] = category_list


def table_show(request):
    data = news.objects.all()
    data = data.values('time', 'title', 'category')

    table = newsTable(data)  # , row_attrs={'id': lambda record: record['sn']}, order_by="-updated_time")
    RequestConfig(request, paginate={'per_page': 100}).configure(table)

    html_render = {}
    to_render(html_render, data, table)
    return render(request, "index.html", html_render)


# rendering "Search by Title"
def news_search(request):
    data = news.objects.all()
    html_render = {}

    data = data.filter(models.Q(title__icontains=request.GET['keywd_input']))
    data = data.values("time", "title", "category")
    table = newsTable(data)  # , order_by="-time")
    RequestConfig(request, paginate={'per_page': 100}).configure(table)
    to_render(html_render, data, table)
    html_render['keywd_input'] = request.GET['keywd_input']

    return render(request, "index.html", html_render)


# rendering "Filter"
def news_filter(request):
    data = news.objects.all()
    html_render = {}

    if request.GET['filter_category'] == 'All':
        pass
    else:
        data = data.filter(models.Q(category__icontains=request.GET['filter_category']))

    data = data.values("time", "title", "category")
    table = newsTable(data)
    RequestConfig(request, paginate={'per_page': 100}).configure(table)
    to_render(html_render, data, table)
    html_render['filter_category'] = request.GET['filter_category']

    return render(request, "index.html", html_render)

def download_excel(request):
    # 
    data = news.objects.values("time", "title", "category")

    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="table_download.csv"'

    writer = csv.writer(response)

    writer.writerow(["time", "title", "category"])
   
    for row in data:
        writer.writerow([row["time"], row["title"], row["category"]])

    return response

# def list_tables(request):
#     """展示数据库中所有表名"""
#     table_names = connection.introspection.table_names()
#     return render(request, "list_tables.html", {"tables": table_names})

def list_tables(request):
    tables = connection.introspection.table_names()
    keywd = request.GET.get('keywd_input', '').strip()
    if keywd:
        tables = [t for t in tables if keywd.lower() in t.lower()]

    filter_category = request.GET.get('filter_category', 'All')
    if filter_category and filter_category != 'All':
        tables = [t for t in tables if t.startswith(filter_category)]

    # 举例：category_list 可以是首字母分组或你自定义的分组
    all_tables = connection.introspection.table_names()
    letters = sorted(set([t[0].upper() for t in all_tables if t]))
    category_list = ['All'] + letters

    return render(request, 'list_tables.html', {
        'tables': tables,
        'category_list': category_list,
        'filter_category': filter_category,
        'keywd_input': keywd,
    })


def show_table(request, table_name):
    """展示指定表的内容，复用 index.html """
    table_names = connection.introspection.table_names()
    if table_name not in table_names:
        raise Http404("表不存在")

    with connection.cursor() as cursor:
        cursor.execute(f"SELECT * FROM `{table_name}` LIMIT 200")
        rows = cursor.fetchall()
        columns = [col[0] for col in cursor.description]

    # 动态生成 Table 类
    class GenericTable(tables.Table):
        class Meta:
            attrs = {"class": "info-table"}

    for col in columns:
        GenericTable.base_columns[col] = tables.Column(verbose_name=col)

    # 组装成字典数据（django_tables2 需要）
    data = [dict(zip(columns, row)) for row in rows]

    table = GenericTable(data)
    RequestConfig(request, paginate={'per_page': 50}).configure(table)

    html_render = {
        "table": table,
        "category_list": [],  # 避免模板报错
        "filter_category": None,
        "keywd_input": None,
    }
    return render(request, "index.html", html_render)
#####################################################################################################
# from django.shortcuts import render
# from django.db import models
# from django.http import HttpResponse
# import csv
# import django_tables2 as tables
# from django_tables2.config import RequestConfig
# import itertools

# ##### 分类列表 #####
# category_list = [
#     'All', 'iPhone应用推荐', 'iPhone新闻', 'Win10快讯', 'Win10设备', '业界', '人工智能', '人物', 
#     '天文航天', '奇趣电子', '安卓应用推荐', '安卓手机', '安卓新闻', '影像器材', '新能源汽车', 
#     '智能家居', '智能家电', '活动互动', '游戏快报', '电商', '电子竞技', '电脑硬件', '科技前沿', 
#     '科普常识', '笔记本', '网络', '苹果', '车联网', '软件快报', '辣品广告', '通信'
# ]

# class news(models.Model):
#     time = models.CharField(max_length=20, blank=True, null=True)  # 原来 10 太短
#     title = models.CharField(max_length=200, blank=True, null=True)
#     category = models.CharField(max_length=200, blank=True, null=True)

#     class Meta:
#         db_table = "news"

# class newsTable(tables.Table):
#     counter = tables.Column(verbose_name="No", empty_values=(), orderable=False)
#     time = tables.Column(verbose_name="Time")
#     title = tables.Column(verbose_name="Title")
#     category = tables.Column(verbose_name="Category")

#     def render_counter(self):
#         self.row_counter = getattr(self, 'row_counter', itertools.count(1))
#         return next(self.row_counter)

#     class Meta:
#         model = news
#         attrs = {"class": "info-table"}
#         fields = ("counter", "time", "title", "category")


# def to_render(html_render, table):
#     """统一模板上下文"""
#     html_render['table'] = table
#     html_render['category_list'] = category_list
#     return html_render


# def table_show(request):
#     data = news.objects.all()
#     table = newsTable(data)
#     RequestConfig(request, paginate={'per_page': 100}).configure(table)
#     return render(request, "index.html", to_render({}, table))


# def news_search(request):
#     keywd = request.GET.get('keywd_input', '')
#     data = news.objects.all()
#     if keywd:
#         data = data.filter(title__icontains=keywd)

#     table = newsTable(data)
#     RequestConfig(request, paginate={'per_page': 100}).configure(table)

#     context = to_render({}, table)
#     context['keywd_input'] = keywd
#     return render(request, "index.html", context)


# def news_filter(request):
#     category = request.GET.get('filter_category', 'All')
#     data = news.objects.all()

#     if category != 'All':
#         data = data.filter(category__icontains=category)

#     table = newsTable(data)
#     RequestConfig(request, paginate={'per_page': 100}).configure(table)

#     context = to_render({}, table)
#     context['filter_category'] = category
#     return render(request, "index.html", context)


# def download_excel(request):
#     """导出 CSV"""
#     data = news.objects.values("time", "title", "category")

#     response = HttpResponse(content_type="text/csv")
#     response["Content-Disposition"] = 'attachment; filename="table_download.csv"'

#     writer = csv.writer(response)
#     writer.writerow(["time", "title", "category"])

#     for row in data:
#         writer.writerow([row["time"], row["title"], row["category"]])

#     return response
########################################################################################################
# from django.shortcuts import render
# from django.http import HttpResponse, Http404
# from django.db import connection
# import csv

# def index(request):
#     """显示所有表"""
#     with connection.cursor() as cursor:
#         cursor.execute("SHOW TABLES;")
#         tables = [row[0] for row in cursor.fetchall()]
#     return render(request, "index.html", {"tables": tables})

# def table_detail(request, table_name):
#     """显示指定表的数据"""
#     with connection.cursor() as cursor:
#         # 检查表名是否存在，防止 SQL 注入
#         cursor.execute("SHOW TABLES LIKE %s;", [table_name])
#         if not cursor.fetchone():
#             raise Http404("Table not found")

#         # 获取字段名
#         cursor.execute(f"DESCRIBE `{table_name}`;")
#         columns = [col[0] for col in cursor.fetchall()]

#         # 获取数据
#         cursor.execute(f"SELECT * FROM `{table_name}` LIMIT 200;")
#         rows = cursor.fetchall()

#     return render(request, "table_detail.html", {
#         "table_name": table_name,
#         "columns": columns,
#         "rows": rows
#     })

# def download_csv(request, table_name):
#     """导出指定表为 CSV"""
#     with connection.cursor() as cursor:
#         cursor.execute("SHOW TABLES LIKE %s;", [table_name])
#         if not cursor.fetchone():
#             raise Http404("Table not found")

#         cursor.execute(f"DESCRIBE `{table_name}`;")
#         columns = [col[0] for col in cursor.fetchall()]

#         cursor.execute(f"SELECT * FROM `{table_name}`;")
#         rows = cursor.fetchall()

#     response = HttpResponse(content_type="text/csv")
#     response["Content-Disposition"] = f'attachment; filename="{table_name}.csv"'

#     writer = csv.writer(response)
#     writer.writerow(columns)
#     for row in rows:
#         writer.writerow(row)

#     return response
