from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.sessions.models import Session
from django.core.files.base import ContentFile
from mysite import models
from .forms import RegisterForm,LoginForm,NewExploitReport,NewInforCollectReport
import hashlib
from jsonfield import JSONField
import json,ast
# Create your views here.
data_list = ['目標關聯',[],'目標簡介說明',[],'目標滲透',[]]
content_title = ['relate','summary','exploit']
photos = ['relate_image','summary_image','exploit_image']

def hash_code(s, salt='ivan'): #密碼加密
    h = hashlib.sha256()
    s = s + salt
    h.update(s.encode())
    return h.hexdigest()

def index(request, pid=None, del_pass=None):
    if request.session.get('is_login',None): #檢查session確定是否登入，不允許重複登入
        username = request.session['username']
        user = models.User.objects.get(username = username)
    else:
        return redirect('/login')
    return render(request, 'index.html',locals())


def sign_in(request):
    if request.session.get('is_login',None): #檢查session確定是否登入，不允許重複登入
        return redirect("/")  #若已登入則導向主頁
    if request.method == "POST":
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password'] 
            try:
                user = models.User.objects.get(username = username)
                if user.password == hash_code(password): #密文處理
                    request.session['is_login'] = True
                    request.session['username'] = user.username
                    request.session['name'] = user.name
                    request.session['rank'] = user.rank
                    return redirect('/')
                else:
                    messages.add_message(request, messages.WARNING, '密碼錯誤')
            except:
                messages.add_message(request, messages.WARNING, '查無使用者')
    login_form = LoginForm()
    return render(request, 'login.html', locals())

def sign_up(request):
    if request.method == "POST":
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            username = register_form.cleaned_data['username'] 
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            rank = register_form.cleaned_data['rank']
            name = register_form.cleaned_data['name']
            if password1 != password2: #若兩次密碼不同
                messages.add_message(request, messages.WARNING, "兩次輸入的密碼不同!")
                return render(request, 'register.html', locals())
            else:
                same_username_user = models.User.objects.filter(username=username) #比對資料庫是否有相同用戶名
                if same_username_user:
                    messages.add_message(request, messages.WARNING, "該帳號已存在!")
                    return render(request, 'register.html', locals())
                same_name_user = models.User.objects.filter(name=name)  #比對資料庫是否有相同信箱
                if same_name_user:
                    messages.add_message(request, messages.WARNING, "已有相同名字，請確認是否已註冊過!")
                    return render(request, 'register.html', locals())
                #若上面條件皆通過，則創建新的用戶
                new_user = models.User()
                new_user.username = username
                new_user.password = hash_code(password1)
                new_user.rank = rank
                new_user.name = name
                new_user.save()
                return redirect('/login') #自動跳轉到登入頁面
    register_form = RegisterForm(request.POST)
    return render(request, 'register.html', locals())

def userinfo(request):    
    if 'username' in request.session:
        username = request.session['username']
        user = models.User.objects.get(username = username)
        if request.method == "POST":
            user.name = request.POST['user_name']
            user.rank = request.POST['user_rank']
            photo = request.FILES.getlist('image')
            content = request.POST['content']
            user.content = content
            print(photo)
            if photo:
                for f in photo:
                    file = models.Images(user = user,image=f)
                    print(f)
                    file.save()
            user.save()
            return redirect('/userinfo')        
    else:
        return redirect('/login')
    return render(request, 'userinfo.html', locals())    


def new_exploit_report(request):
    if request.session.get('is_login',None): #檢查session確定是否登入，不允許重複登入
        username = request.session['username']
        user = models.User.objects.get(username = username)
        if request.method == "POST":
            new_ex_report = NewExploitReport(request.POST, request.FILES)
            if new_ex_report.is_valid():
                new_report = models.ExploitReport()
                new_report.user = user.username
                new_report.excute_date = new_ex_report.cleaned_data['excute_date']
                new_report.target_name = new_ex_report.cleaned_data['target_name']
                new_report.target_url = new_ex_report.cleaned_data['target_url']
                new_report.target_ip = new_ex_report.cleaned_data['target_ip']
                new_report.target_port = new_ex_report.cleaned_data['target_port']
                new_report.target_version = new_ex_report.cleaned_data['target_version']
                new_report.weakness = new_ex_report.cleaned_data['weakness']
                new_report.search_time = new_ex_report.cleaned_data['search_time']
                new_report.vpn_ip = new_ex_report.cleaned_data['vpn_ip']
                new_report.source = new_ex_report.cleaned_data['source']
                new_report.IC_type = new_ex_report.cleaned_data['IC_type']
                new_report.excute_location = new_ex_report.cleaned_data['excute_location']
                new_report.use = new_ex_report.cleaned_data['use']
                new_report.admin = new_ex_report.cleaned_data['admin']
                new_report.people = new_ex_report.cleaned_data['people']
                new_report.expected = new_ex_report.cleaned_data['expected']
                new_report.follow_up = new_ex_report.cleaned_data['follow_up']

                relate = request.POST.getlist('relate_content')
                summary = request.POST.getlist('summary_content')
                exploit = request.POST.getlist('exploit_content')
                data_list[1] = relate
                data_list[3] = summary
                data_list[5] = exploit
                new_report.content = data_list
                new_report.save()
                for photo in photos:
                    img = request.FILES.getlist(photo)
                    print(img,photo)
                    x = 0
                    for f in img:
                        print(img)
                        file = models.Images(ex_post = new_report,image=f,content_id=x,content=photo)
                        file.save()
                        x+=1
                
                return redirect('/Report_List/EX/My_Report')                            
    else:
        return redirect('/login')
    
    new_ex_report = NewExploitReport(request.POST)
    return render(request, 'New_Exploit_Report.html', locals())    

def new_inforcollect_report(request):
    if request.session.get('is_login',None): #檢查session確定是否登入，不允許重複登入
        username = request.session['username']
        user = models.User.objects.get(username = username)
        if request.method == "POST":
            new_ic_report = NewInforCollectReport(request.POST, request.FILES)
            if new_ic_report.is_valid():
                report_user = user.username
                excute_date = new_ic_report.cleaned_data['excute_date']
                target_name = new_ic_report.cleaned_data['target_name']
                target_location = new_ic_report.cleaned_data['target_location']
                target_url = new_ic_report.cleaned_data['target_url']
                target_ip = new_ic_report.cleaned_data['target_ip']
                target_port = new_ic_report.cleaned_data['target_port']
                target_warzone = new_ic_report.cleaned_data['target_warzone']
                weakness = new_ic_report.cleaned_data['weakness']
                search_time = new_ic_report.cleaned_data['search_time']
                vpn_ip = new_ic_report.cleaned_data['vpn_ip']
                content = new_ic_report.cleaned_data['content']
                # image = request.FILES['image']
                follow_up = new_ic_report.cleaned_data['follow_up']
                new_report = models.InforCollectReport(user=report_user,target_location=target_location,excute_date=excute_date,target_name=target_name,target_url =target_url,target_ip=target_ip,target_port=target_port,target_warzone=target_warzone,weakness=weakness,search_time=search_time,vpn_ip=vpn_ip,content=content,follow_up=follow_up,status='待審核')
                new_report.save()
                return redirect('/Report_List/IC/My_Report')
    else:
        return redirect('/login')
    new_ic_report = NewInforCollectReport(request.POST)
    return render(request, 'New_InforCollect_Report.html', locals()) 

def report_list(request, judge, slug):
    if request.session.get('is_login',None):
        username = request.session['username']
        user = models.User.objects.get(username = username)
        if judge == "EX":
            if slug == "ALL":
                post_list = models.ExploitReport.objects.filter(status = '已審核')
                validation = False
            elif slug == "My_Report":
                post_list = models.ExploitReport.objects.filter(user = username)
                validation = True
            elif slug == "Passing_Report":
                post_list = models.ExploitReport.objects.filter(status = '待審核')
                validation = False
            elif slug == "Passed_Report":
                post_list = models.ExploitReport.objects.filter(status = '已審核')
                validation = False        
        if judge == "IC":
            if slug == "ALL":
                post_list = models.ExploitReport.objects.filter(status = '已審核')
                validation = False
            elif slug == "My_Report":
                post_list = models.InforCollectReport.objects.filter(user = username)
                validation = True
            elif slug == "Passing_Report":
                post_list = models.InforCollectReport.objects.filter(status = '待審核')
                validation = False
            elif slug == "Passed_Report":
                post_list = models.InforCollectReport.objects.filter(status = '已審核')
                validation = False        
    else:
        return redirect('/login')
    return render(request, 'Report_List.html', locals())

def report_post(request, judge, slug, id):
    if request.session.get('is_login',None):
        relate_imgs,summary_imgs,exploit_imgs = [],[],[]
        username = request.session['username']
        user = models.User.objects.get(username = username)
        if judge == "EX": 
            post = models.ExploitReport.objects.get(id = id)
            list123 = post.content
            string = ast.literal_eval(list123)
            relate_content = string[1]
            summary_content = string[3]
            exploit_content = string[5]

            for x in content_title:
                locals()[ x + '_num'] = len(locals()[ x + '_content']) -1 
                locals()[ x + '_count'] = range(len(locals()[ x + '_content']))
                locals()[ x + '_img'] = models.Images.objects.filter(ex_post_id = id,content= (x + '_image'))
                for i in locals()[ x + '_img']:
                   locals()[ x + '_imgs'].append(i.image.url)
            
            if slug == "view": 
                change = False
                new_ex_report = models.ExploitReport.objects.get(id = id)     
            if slug == "modify":      
                change = True          
                data = {'excute_date': post.excute_date,'target_name': post.target_name,'target_url':post.target_url,'target_ip':post.target_ip,'target_port':post.target_port,'target_version':post.target_version,'weakness':post.weakness,'search_time':post.search_time,'vpn_ip':post.vpn_ip,'content':post.content,'use':post.use,'admin':post.admin,'people':post.people,'expected':post.expected,'follow_up':post.follow_up,'source': post.source,'IC_type': post.IC_type,'excute_location': post.excute_location}
                new_ex_report = NewExploitReport(initial=data)                
                if request.method == "POST":
                    new_ex_report = NewExploitReport(request.POST, request.FILES)
                    if new_ex_report.is_valid():
                        new_report = models.ExploitReport.objects.get(id = id)
                        new_report.excute_date = new_ex_report.cleaned_data['excute_date']
                        new_report.target_name = new_ex_report.cleaned_data['target_name']
                        new_report.target_url = new_ex_report.cleaned_data['target_url']
                        new_report.target_ip = new_ex_report.cleaned_data['target_ip']
                        new_report.target_port = new_ex_report.cleaned_data['target_port']
                        new_report.target_version = new_ex_report.cleaned_data['target_version']
                        new_report.weakness = new_ex_report.cleaned_data['weakness']
                        new_report.search_time = new_ex_report.cleaned_data['search_time']
                        new_report.vpn_ip = new_ex_report.cleaned_data['vpn_ip']
                        new_report.source = new_ex_report.cleaned_data['source']
                        new_report.IC_type = new_ex_report.cleaned_data['IC_type']
                        new_report.excute_location = new_ex_report.cleaned_data['excute_location']
                        new_report.use = new_ex_report.cleaned_data['use']
                        new_report.admin = new_ex_report.cleaned_data['admin']
                        new_report.people = new_ex_report.cleaned_data['people']
                        new_report.expected = new_ex_report.cleaned_data['expected']
                        new_report.follow_up = new_ex_report.cleaned_data['follow_up']

                        relate = request.POST.getlist('relate_content')
                        summary = request.POST.getlist('summary_content')
                        exploit = request.POST.getlist('exploit_content')

                        
                        data_list[1] = relate
                        data_list[3] = summary
                        data_list[5] = exploit
                        new_report.content = data_list
                        new_report.save()

                        for photo in photos:
                            title = photo.split('_')
                            img = request.FILES.getlist(photo)
                            print(img,photo)
                            x = 0
                            for f in img:
                                if f != "":
                                    print(f)
                                    filedel = models.Images.objects.filter(ex_post_id = id,content= (title[0] + '_image'),content_id = x)
                                    filedel.delete()
                                    fileadd = models.Images(ex_post = new_report,image=f,content_id=x,content=photo)
                                    fileadd.save()
                                    x+=1

                        return redirect('/Report_Post/EX/view/' + str(id))
            return render(request, 'Ex_Report_Post.html', locals())
        elif judge == "IC":
            if slug == "view":
                new_ic_report = models.InforCollectReport.objects.get(id = id)
                judge = False
            if slug == "modify":
                post = models.InforCollectReport.objects.get(id = id)
                data = {'excute_date': post.excute_date,'target_name': post.target_name,'target_location':post.target_location,'target_url':post.target_url,'target_ip':post.target_ip,'target_port':post.target_port,'target_warzone':post.target_warzone,'weakness':post.weakness,'search_time':post.search_time,'vpn_ip':post.vpn_ip,'content':post.content,'follow_up':post.follow_up}
                new_ic_report = NewInforCollectReport(initial=data)
                if request.method == "POST":
                    new_ic_report = NewInforCollectReport(request.POST, request.FILES)
                    if new_ic_report.is_valid():
                        report_user = user.username
                        excute_date = new_ic_report.cleaned_data['excute_date']
                        target_name = new_ic_report.cleaned_data['target_name']
                        target_location = new_ic_report.cleaned_data['target_location']
                        target_url = new_ic_report.cleaned_data['target_url']
                        target_ip = new_ic_report.cleaned_data['target_ip']
                        target_port = new_ic_report.cleaned_data['target_port']
                        target_warzone = new_ic_report.cleaned_data['target_warzone']
                        weakness = new_ic_report.cleaned_data['weakness']
                        search_time = new_ic_report.cleaned_data['search_time']
                        vpn_ip = new_ic_report.cleaned_data['vpn_ip']
                        content = new_ic_report.cleaned_data['content']
                        follow_up = new_ic_report.cleaned_data['follow_up']
                        new_report = models.InforCollectReport(user=report_user,target_location=target_location,excute_date=excute_date,target_name=target_name,target_url =target_url,target_ip=target_ip,target_port=target_port,target_warzone=target_warzone,weakness=weakness,search_time=search_time,vpn_ip=vpn_ip,content=content,follow_up=follow_up,status=1)
                        new_report.save()
            return render(request, 'Ic_Report_Post.html', locals())
    else:
        return redirect('/login')
    
def search(request):
    search_post = request.GET.get('search')
    # if search_post:
    #     posts = models.ExploitReport.objects.filter(Q(title__icontains=search_post) | Q(content__icontains=search_post)
    # else:
    #     # If not searched, return default posts
    #     posts = models.ExploitReport.objects.all().order_by("-date_created")

def delete_post(request, judge , slug, id):
    if request.session.get('is_login',None):
        if judge == "IC":
            models.InforCollectReport.objects.get(id = id).delete()
            url = '/Report_List/' + judge + '/' + slug
            return redirect(url)
        elif judge == "EX":
            models.ExploitReport.objects.get(id = id).delete()
            url = '/Report_List/' + judge + '/' + slug
            return redirect(url)
    else:
        return redirect('/login')

def judge_post(request, judge, slug, success, id):
    if request.session.get('is_login',None):
        if judge == "IC":
            if success == "success":
                new_report = models.InforCollectReport.objects.get(id = id)
                new_report.status = '已審核'
            elif  success == "return":
                new_report = models.InforCollectReport.objects.get(id = id)
                new_report.status = '被退回'
            new_report.save()
            url = '/Report_List/' + judge + '/' + slug
            return redirect(url)
        elif judge == "EX":
            if success == "success":
                new_report = models.ExploitReport.objects.get(id = id)
                new_report.status = '已審核'
            elif  success == "return":
                new_report = models.ExploitReport.objects.get(id = id)
                new_report.status = '被退回'
            new_report.save()
            url = '/Report_List/' + judge + '/' + slug
            return redirect(url)
    else:
        return redirect('/login')

def log_out(request):
    request.session.flush() #一次性將session內容全部清除
    return redirect('/login') 

