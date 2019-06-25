from django.contrib import admin
from .models import *
from django.urls import reverse
from django.utils.html import format_html
from .adminforms import PostAdminForm
from typeidea.base_admin import BaseOwnerAdmin
from typeidea.custom_site import custom_site
from django.contrib.admin.models import LogEntry

# Register your models here.

# 同一页面编辑关联数据
class PostInline(admin.TabularInline):
    fields = ('title','desc')
    # 控制额外多个
    extra = 1
    model = Post

@admin.register(Category,site=custom_site)
class CategoryAdmin(BaseOwnerAdmin):
    # 展示界面过滤的字段
    list_display = ('name','status','is_nav','created_time','owner','post_count')
    # 添加界面过滤的字段
    fields = ('name','status','is_nav')

    # 同一页面编辑关联数据
    inlines = [PostInline]

    # 自定义方法,展示分类下有多少文章
    def post_count(self,obj):
        return obj.post_set.count()
    post_count.short_description = '文章数量'

    # 自动设置owner,request当前请求,request.user当前登录用户,form表但提交的对象,change本次保存是新增还是更新
    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(CategoryAdmin,self).save_model(request,obj,form,change)


@admin.register(Tag,site=custom_site)
class TagAdmin(BaseOwnerAdmin):
    list_display = ('name','status','created_time','owner','tag_count')
    fields = ('name','status')

    def tag_count(self,obj):
        return obj.post_set.count()
    tag_count.short_description = '文章数量'

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(TagAdmin,self).save_model(request,obj,form,change)


# 定制权限
class CategoryOwnerFilter(admin.SimpleListFilter):
    '''
    自定义过滤器只展示当前用户分类,继承自方法SimpleListFilter
    方法:lookups:返回展示的内容和查询用的id  queryset:根据url query的内容返回列表数据
    '''
    title = '分类过滤器'
    parameter_name = 'owner_category'

    def lookups(self, request, model_admin):
        return Category.objects.filter(owner=request.user).values_list('id','name')

    def queryset(self, request, queryset):
        category_id = self.value()
        if category_id:
            return queryset.filter(category_id=self.value())
        return queryset


@admin.register(Post,site=custom_site)
class PostAdmin(BaseOwnerAdmin):
    list_display = [
        'title','category','status','created_time','owner','operator'
    ]
    # 那些字段可以作为点击链接
    list_display_links = []
    # list_filter = ['category',]
    list_filter = [CategoryOwnerFilter]
    # 搜索字段
    search_fields = ['title','category__name']
    # 展示位置
    actions_on_top = True
    actions_on_bottom = True

    # 编辑页面
    save_on_top = True

    # 自定义form,文章描述字段
    form = PostAdminForm

    # 去除不需要展示的字段
    exclude = ('owner',)

    # 限定展示的字段和展示字段的顺序
    # fields = (
    #     ('category','title'),
    #     'desc',
    #     'status',
    #     'content',
    #     'tag',
    # )
    # 控制页面布局
    fieldsets = (
        ('基础配置',{
            'description':'基础配置描述',
            'fields':(
                ('title','category'),
                'status'
            ),
        }),
        ('内容', {
            'fields': (
                'desc',
                'content'
            ),
        }),
        ('额外信息', {
            'classes':('collapse',),
            'fields':('tag',),
        }),
    )

    def operator(self,obj):
        return format_html('<a href="{}">编辑</a>',reverse('cus_admin:blog_post_change',args=(obj.id,)))
    # 指定表头的展示文案
    operator.short_description ='操作'

    # def save_model(self, request, obj, form, change):
    #     obj.owner = request.user
    #     return super(PostAdmin,self).save_model(request,obj,form,change)
    #
    # # 过滤列表页
    # def get_queryset(self, request):
    #     qs = super(PostAdmin, self).get_queryset(request)
    #     return qs.filter(owner=request.user)

    # 自定义引入静态资源
    # class Media:
    #     css = {
    #         'all':("https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/css/bootstrap.min.css",),
    #     }
    #     js = ('https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/js/bootstrap.bundle.js',)


@admin.register(LogEntry,site=custom_site)
class LogEntryAdmin(admin.ModelAdmin):
    list_display = ['object_repr','object_id','action_flag','user','change_message']
