from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.shortcuts import render,redirect
from .models import TodoList, Category
from datetime import date
from todolist.forms import SignUpForm
import datetime
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                #login(request,user)
                #index(request)
                #return render(request, "index.html", {"user":user})
                request.session['userid'] = username
                return redirect('/');
            else:
                return HttpResponse("Your account was inactive.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username,password))
            return HttpResponse("Invalid login details given")
    else:
        if 'userid' in request.session:
            del request.session['userid']
        return render(request, 'login.html', {})

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return index(request)

    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})



def index(request): #the index view
    
    
    if 'userid' in request.session:
        userid = request.session['userid']
        todos = TodoList.objects.filter(status="open",userid=userid) #quering all todos with the object manager
        todos_today = TodoList.objects.filter(status="open",userid=userid, due_date=date.today()) #quering all todos with the object manager
        todos_tomorrow = TodoList.objects.filter(status="open",userid=userid, due_date=date.today() + datetime.timedelta(days=1)) #quering all todos with the object manager
        todos_completed = TodoList.objects.filter(status="completed",userid=userid,) #quering all todos with the object manager
        categories = Category.objects.all() #getting all categories with object manager
        todolist = TodoList.objects.all()
        if request.method == "POST": #checking if the request method is a POST
            if "taskAdd" in request.POST: #checking if there is a request to add a todo
                title = request.POST["description"] #title
                date_todo = str(request.POST["date"]) #date
                category = request.POST["category_select"] #category
                content = title + " -- " + date_todo + " " + category #content
                Todo = TodoList(title=title,userid=userid, content=content, due_date=date_todo, category=Category.objects.get(name=category))
                Todo.save() #saving the todo 
                #return redirect("/") #reloading the page        

            if "taskDelete" in request.POST: #checking if there is a request to delete a todo
                strHdnField = request.POST.get("hdnCheckBox");
                
                checkedlist=""
                
                if strHdnField=="All":
                    checkedlist = request.POST.getlist("checkedbox_all")
                elif strHdnField == "Today":
                    checkedlist = request.POST.getlist("checkedbox_today")
                elif strHdnField == "Tomorrow":
                    checkedlist = request.POST.getlist("checkedbox_tomorrow")
                elif strHdnField == "Completed":
                    checkedlist = request.POST.getlist("checkedbox_completed")
                

                #todo_del = TodoList.objects.all().get(id=int(checkedlist)) #getting todo id
                #todo_del.delete() #deleting todo
                
                for todo_id in checkedlist:         
                    try:
                        todo_del = TodoList.objects.all().get(id=int(todo_id)) #getting todo id
                        todo_del.delete() #deleting todo
                    
                    except:
                        print("Next entry.")
                        pass
                             
             
            
            if "taskCompleted" in request.POST: #checking if there is a request to delete a todo
                
                strHdnField = request.POST.get("hdnCheckBox");
                
                checkedlist=""
                
                if strHdnField=="All":
                    checkedlist = request.POST.getlist("checkedbox_all")
                elif strHdnField == "Today":
                    checkedlist = request.POST.getlist("checkedbox_today")
                elif strHdnField == "Tomorrow":
                    checkedlist = request.POST.getlist("checkedbox_tomorrow")
                elif strHdnField == "Completed":
                    checkedlist = request.POST.getlist("checkedbox_completed")
                
                for todo_id in checkedlist:
                    todo_comp = TodoList.objects.all().get(id=int(todo_id)) #getting todo id
                    todo_comp.status = "completed"
                    todo_comp.save() #saving todo
                 

        return render(request, "index.html", {"todos": todos, "categories":categories, "todos_today": todos_today, "todos_tomorrow": todos_tomorrow, "todos_completed": todos_completed})
    else:
        return HttpResponse("Invalid login details given")