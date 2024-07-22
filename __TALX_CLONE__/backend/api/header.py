from .models import *
from .serializers import *
from validations import *
def get_object(request):
    data = request.data or None
    cls_name = data.get("class") or None
    obj_id = data.get("ID") or None

    if cls_name not in classes:
        return (False, f"Invalid class name: {cls_name}")

    query_obj = classes[cls_name].objects.filter(ID=obj_id).first()
    serial_obj = query_obj.to_dict() if query_obj else None
    if serial_obj:
        return (True, serial_obj, data.get("new") or None, query_obj)

    issues = []
    if data is None:
        issues.append("request data missing")
    if cls_name is None:
        issues.append("object class name missing")
    if obj_id is None:
        issues.append("object ID missing")
    if query_obj is None:
        issues.append("object not found")
    if serial_obj is None:
        issues.append("serialization issue")

    return (False, ", ".join(issues))
'''
def get_object(request):
    data = request.data or None
    cls_name = data.get("class") or None
    obj_id = data.get("ID") or None
    query_obj = classes[cls_name].objects.filter(ID=obj_id).first()
    serial_obj = query_obj.to_dict()  if query_obj else None
    if serial_obj:
        return (True, serial_obj, data.get("new") or None, query_obj)
    issues  = ""
    issues += "request data" if data is None else ""
    issues += ", object class name " if cls_name is None else ""
    issues += f" ,id object {obj_id} issue" if query_obj is None else ""
    issues += f" ,serialize issue" if serial_obj is None else ""
    return (False, issues)
'''
def update_user(user_obj, news_dict):
    pass
