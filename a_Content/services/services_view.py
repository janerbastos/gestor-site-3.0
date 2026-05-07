from django.shortcuts import redirect
from django.urls import reverse

class ViewService():
    
    def execute(self, data):
        request = data['request']
        type_ = data['type']
        action = data['action']
        parent = data['parent']
        url = data['url']
        content_id = data['content_id']

        request.session['type'] = type_
        request.session['action'] = action
        request.session['parent_id'] = parent.id if parent else None
        request.session['content_id'] = content_id

        

        return redirect(reverse(f'content:{action}-{type_.lower()}', args=(url,)))