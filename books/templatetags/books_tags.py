from django import template
from books.models import Books, Category

register = template.Library()

@register.simple_tag(name='getcats')
def get_categories(filter=None):
    if not filter:
        return Category.objects.all()
    else:
        return Category.objects.filter(pk=filter)

@register.inclusion_tag('books/list_categories.html')
def show_categories(sort=None, cat_selected=0):
    if not sort:
        cats = Category.objects.all()
    else:
        cats = Category.objects.order_by(sort)
        
    return {'cats': cats, 'cat_selected': cat_selected}


#index
@register.simple_tag(name='getinds')
def get_indexes(filter=None):
    if not filter:
        return Books.objects.all()
    else:
        return Books.objects.filter(pk=filter)

