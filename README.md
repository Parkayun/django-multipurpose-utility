#django-multipurpose-utility

[django-multipurpose-utility](https://github.com/Parkayun/django-multipurpose-utility) is a super simple utility.

# Functions
##Json Response
HTTP Response with application/json type. 
```python
    from dmu import json_response
	def home(request):
	    data = {"some": "data"}
	    return json_response(data)
       
    def acao_home(request):
		data = {"some": "data"}
		#Access-Control-Allow-Origin
		return json_response(data, acao=True)
```
If you use django 1.7 look this [django official docs](https://docs.djangoproject.com/en/1.7/ref/request-response/#jsonresponse-objects)

##AutoCreator
Auto create models objects.
```python
	>>> from dmu import AutoCreator
	>>> from base.models import SampleModel
	>>> 
    >>> print len(SampleModel.objects.all())
	0
    >>>
	>>> for x in xrange(10):
	>>>    AutoCreator().run(SampleModel)
    >>>
	>>> print len(SampleModel.objects.all())
	10
```
If model have ForeignKey, It also automatically create related objects.   
```python
	class ParentModel(models.Model):
    	text = models.TextField()

	class ChildModel(models.Model):
    	parent = models.ForeignKey(ParentModel)
```
This model working like this.
```python
	AutoCreator().run(ChildModel)
    > ParentModel.objects.create(text='blahblah')
    > ChildModel.objects.create(parent=ParentModel.objects.all()[0])
```
Check about [AutoCreator test](https://github.com/Parkayun/django-multipurpose-utility/blob/master/example/base/tests.py)
