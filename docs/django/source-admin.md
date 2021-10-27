# Django - 源码之Admin








<extoc></extoc>

## 介绍

Django为我们提供了一个强大的后台管理页面 , 也就是admin

在我们创建应用时 , 默认的 `urls.py` 中第一条就进行了`admin`分发 , 如下 : 

```python
url(r'^admin/', admin.site.urls)
```

其应用增删改查路由规则如下 : 

这些url都是admin为我们自动生成的 , 这也是我们需要了解的重点

```python
# application:应用名
# table:表名

- /admin/application/table/              # 查询数据
- /admin/application/table/add/          # 添加数据
- /admin/application/table/1/change/     # 修改数据
- /admin/application/table/1/delete/     # 删除数据
```

## admin.site.urls

在源码目录中 , `admin` 下的 `sites.py` 中使用了一个全局对象

```python
# This global object represents the default admin site, for the common case.
# You can instantiate AdminSite in your own code to create a custom admin site.
site = AdminSite()
```

随后访问该实例的urls属性 , 如下 : 

```python
@property
def urls(self):
    return self.get_urls(), 'admin', self.name
```

该属性返回了一个元组 , 并且形式如 : `(list,tuple)` , 在上一篇URL的分析中我们已经知道 , 这正是进行路由分发 , 元组中的第一个元素为分发的子路由

`self.get_urls()`源码如下 : 

```python
def get_urls(self):
    from django.conf.urls import url, include
    # Since this module gets imported in the application's root package,
    # it cannot import models from other applications at the module level,
    # and django.contrib.contenttypes.views imports ContentType.
    from django.contrib.contenttypes import views as contenttype_views

    def wrap(view, cacheable=False):
        def wrapper(*args, **kwargs):
            return self.admin_view(view, cacheable)(*args, **kwargs)
        wrapper.admin_site = self
        return update_wrapper(wrapper, view)

    # Admin-site-wide views.
    # admin本身视图
    urlpatterns = [
        url(r'^$', wrap(self.index), name='index'),
        url(r'^login/$', self.login, name='login'),
        url(r'^logout/$', wrap(self.logout), name='logout'),
        url(r'^password_change/$', wrap(self.password_change, cacheable=True), name='password_change'),
        url(r'^password_change/done/$', wrap(self.password_change_done, cacheable=True),
            name='password_change_done'),
        url(r'^jsi18n/$', wrap(self.i18n_javascript, cacheable=True), name='jsi18n'),
        url(r'^r/(?P<content_type_id>\d+)/(?P<object_id>.+)/$', wrap(contenttype_views.shortcut),
            name='view_on_site'),
    ]

    # Add in each model's views, and create a list of valid URLS for the
    # app_index
    valid_app_labels = []
    for model, model_admin in self._registry.items():
        # model:models.UserInfo
        # model_admin:ModelAdmin(models.UserInfo, admin.site)
        
        # 为self._registry中的model生成增删改查url
        # self._registry默认为空,当我们在应用的admin.py中注册时会进行添加
        # model_admin为ModelAdmin实例
        urlpatterns += [
            url(r'^%s/%s/' % (model._meta.app_label, model._meta.model_name), include(model_admin.urls)),
        ]
        if model._meta.app_label not in valid_app_labels:
            valid_app_labels.append(model._meta.app_label)

    # If there were ModelAdmins registered, we should have a list of app
    # labels for which we need to allow access to the app_index view,
    if valid_app_labels:
        regex = r'^(?P<app_label>' + '|'.join(valid_app_labels) + ')/$'
        urlpatterns += [
            url(regex, wrap(self.app_index), name='app_list'),
        ]
    return urlpatterns
```

## register

注册model到`self._registry` , 是通过`register()`实现的 , 如 : `admin.site.register(models.UserInfo)` 

```python
def register(self, model_or_iterable, admin_class=None, **options):
    """
    Registers the given model(s) with the given admin class.

    The model(s) should be Model classes, not instances.

    If an admin class isn't given, it will use ModelAdmin (the default
    admin options). If keyword arguments are given -- e.g., list_display --
    they'll be applied as options to the admin class.

    If a model is already registered, this will raise AlreadyRegistered.

    If a model is abstract, this will raise ImproperlyConfigured.
    """
    if not admin_class:
        # 默认使用ModelAdmin
        admin_class = ModelAdmin

    if isinstance(model_or_iterable, ModelBase):
        # 将model class放入列表中
        model_or_iterable = [model_or_iterable]
    for model in model_or_iterable:
        if model._meta.abstract:
            raise ImproperlyConfigured(
                'The model %s is abstract, so it cannot be registered with admin.' % model.__name__
            )

        if model in self._registry:
            raise AlreadyRegistered('The model %s is already registered' % model.__name__)

        # Ignore the registration if the model has been
        # swapped out.
        if not model._meta.swapped:
            # If we got **options then dynamically construct a subclass of
            # admin_class with those **options.
            if options:
                # For reasons I don't quite understand, without a __module__
                # the created class appears to "live" in the wrong place,
                # which causes issues later on.
                options['__module__'] = __name__
                admin_class = type("%sAdmin" % model.__name__, (admin_class,), options)

            # Instantiate the admin class to save in the registry
            # 注册后示例:models.UserInfo : ModelAdmin(models.UserInfo, admin.site)
            self._registry[model] = admin_class(model, self)
```

`self._registry` 是一个字典 , 最后注册完成后 , 字典的元素的key 为 `modes.UserInfo`  , 而value则是一个ModelAdmin对象 , 对于model的url生成 , 就藏在ModelAdmin中

## ModelAdmin

提取ModelAdmin中的部分内容

因为在分发的过程中 , 执行了`include(model_admin.urls)` 

```python
@property
def urls(self):
    return self.get_urls()
```

`self.get_urls()`

```python
    def get_urls(self):
        from django.conf.urls import url

        def wrap(view):
            def wrapper(*args, **kwargs):
                return self.admin_site.admin_view(view)(*args, **kwargs)
            wrapper.model_admin = self
            return update_wrapper(wrapper, view)

        info = self.model._meta.app_label, self.model._meta.model_name
        # 自动生成url列表
        urlpatterns = [
            url(r'^$', wrap(self.changelist_view), name='%s_%s_changelist' % info),
            url(r'^add/$', wrap(self.add_view), name='%s_%s_add' % info),
            url(r'^(.+)/history/$', wrap(self.history_view), name='%s_%s_history' % info),
            url(r'^(.+)/delete/$', wrap(self.delete_view), name='%s_%s_delete' % info),
            url(r'^(.+)/change/$', wrap(self.change_view), name='%s_%s_change' % info),
            # For backwards compatibility (was the change url before 1.9)
            url(r'^(.+)/$', wrap(RedirectView.as_view(
                pattern_name='%s:%s_%s_change' % ((self.admin_site.name,) + info)
            ))),
        ]
        return urlpatterns
```

上面自动生成的url对应视图如下 : 

```python
class ModelAdmin(BaseModelAdmin):
    
    def __init__(self, model, admin_site):
        self.model = model
        self.opts = model._meta
        self.admin_site = admin_site
        super(ModelAdmin, self).__init__()

    @csrf_protect_m
    def changelist_view(self, request, extra_context=None):
        """
        查看model列表
        """
        pass
    
    def add_view(self, request, form_url='', extra_context=None):
        """
        添加数据
        """
        return self.changeform_view(request, None, form_url, extra_context)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        """
        编辑数据
        """
        return self.changeform_view(request, object_id, form_url, extra_context)
    
    @csrf_protect_m
    def delete_view(self, request, object_id, extra_context=None):
        """
        删除数据
        """
        with transaction.atomic(using=router.db_for_write(self.model)):
            return self._delete_view(request, object_id, extra_context)

    def history_view(self, request, object_id, extra_context=None):
        """
        查看历史记录
        """
        pass
```

## 自定制Admin

当我们在`admin.py` 中间注册我们的model时 , 一般我们只需要传入一个参数 , 就是我们的model , 因为django为我们默认是用了ModelAdmin , 也就是`admin_class`参数 , 当然我们可以自己传入这个`admin_class` , 这样我们就可以完全定制属于我们自己admin了

定制之前 , 我们需要知道在ModelAdmin中的定制配置

```python
@python_2_unicode_compatible
class ModelAdmin(BaseModelAdmin):
    "Encapsulates all admin options and functionality for a given model."
	# 定制显示的列
    list_display = ('__str__',)
    # 定制可跳转的列
    list_display_links = ()
    # 定制右侧快速筛选
    list_filter = ()
    # 定制连表查询自动select_related
    list_select_related = False
    # 定制页面显示条数
    list_per_page = 100
    # 定制显示全部条数大小,只有当真实数据小于该值才应用
    list_max_show_all = 200
    # 定制可编辑的列
    list_editable = ()
    # 定制模糊搜索功能
    search_fields = ()
    # 对Date和DateTime类型进行搜索
    date_hierarchy = None
    # 详细页面,按钮为"Sava as new"或"Sava and add another"
    save_as = False
    # 点击保存并继续编辑
    save_as_continue = True
    # 详细页面,在页面上方是否也显示保存删除等按钮
    save_on_top = False
    # 分页插件
    paginator = Paginator
    # 
    preserve_filters = True
    # 详细页面,如果有其他表和当前表做外键关联,那么详细页面可以进行动态增加和删除
    inlines = []

    # Custom templates (designed to be over-ridden in subclasses)
    add_form_template = None
    change_form_template = None
    change_list_template = None
    delete_confirmation_template = None
    delete_selected_confirmation_template = None
    object_history_template = None
    popup_response_template = None

    # Actions
    # 定制action中的操作
    actions = []
    action_form = helpers.ActionForm
    # Action选项在页面上方显示
    actions_on_top = True
    # Action选项在页面下方显示
    actions_on_bottom = False
    # 显示选择个数
    actions_selection_counter = True
    checks_class = ModelAdminChecks
```

后期补充 ...

