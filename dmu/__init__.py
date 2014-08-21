# -*- coding:utf -8-
import json

from django.shortcuts import HttpResponse


def json_response(data, acao=False):
    try: 
        data = json.dumps(data)
    except Exception, e:
        data = json.dumps({'error': 'json dumps error'})
    finally:
        response = HttpResponse(data, content_type='application/json')
        if acao:
            response['Access-Control-Allow-Origin'] = '*'
        return response


def get_hand_type_fields(model):
    result = ''
    for field in model._meta.fields:
        if not field.has_default() and (not field.blank and not field.null):
            field_type = field.get_internal_type()
            if 'IntegerField' in field_type or 'SmallIntegerField' in field_type:
                result += field.name+"=1, "
            elif 'ForeignKey' in field_type or 'OneToOneField' in field_type:
                result += field.name+"='key', "
            else:
                result += field.name+"='', "


key_counter = {}

def auto_create_objects(model):
    '''
        It's proto feature"
    '''
    fields = ''
    #print ' '
    for field in model._meta.fields:
        if not field.has_default() and (not field.blank and not field.null):
            field_type = field.get_internal_type()
            if 'IntegerField' in field_type or 'SmallIntegerField' in field_type:
                fields += field.name+"=1,"
            elif 'ForeignKey' in field_type or 'OneToOneField' in field_type:
                auto_create_objects(field.rel.to)


                if not key_counter.has_key(model.__name__+'_'+field.rel.to.__name__):
                    key_counter[model.__name__+'_'+field.rel.to.__name__] = -1
                key_counter[model.__name__+'_'+field.rel.to.__name__] += 1

                idx = key_counter[model.__name__+'_'+field.rel.to.__name__]

                key_field = field.rel.to.__name__ + '.objects.all()['+str(idx)+']'
                fields += field.name+"="+key_field+", "


                exec 'from '+field.rel.to.__module__+' import '+field.rel.to.__name__
                #print 'from '+field.rel.to.__module__+' import '+field.rel.to.__name__
            else:
                max_length = 10
                if field.max_length and max_length > field.max_length:
                    max_length = field.max_length
                import random
                dummy = ''.join([chr(random.randint(97, 122)) for _ in xrange(max_length)])
                fields += field.name+"='"+dummy+"', "
    exec 'from '+model.__module__+' import '+model.__name__
    #print 'from '+model.__module__+' import '+model.__name__
    query = model._meta.object_name+'.objects.create('+fields+')'
    #print query+'\n'
    eval(query)
