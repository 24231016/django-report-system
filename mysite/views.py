from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from mysite import models
from .forms import RegisterForm,LoginForm,NewExploitReport
import hashlib,ast,os
from django.db.models import Q
from docxtpl import DocxTemplate,InlineImage
from mynewsite.settings import MEDIA_URL
from docx.shared import Mm
from django.http import HttpResponse, Http404
from django.utils.http import urlquote

data_list = ['目標關聯',[],'目標簡介說明',[],'目標滲透',[]]
content_title = ['relate','summary','exploit']

def index(request):
    if request.session.get('is_login',None): #檢查session確定是否登入，不允許重複登入
        username = request.session['username']
        user = models.User.objects.get(username = username)
        search_post = request.GET.get('search')
        if search_post:
            search = models.ExploitReport.objects.filter(Q(target_name__icontains=search_post) | Q(target_url__icontains=search_post) | Q(target_ip__icontains=search_post) | Q(content__icontains=search_post))
            title = "%s的搜尋結果，共%s筆"%(search_post,len(search))

        else:
            # messages.add_message(request, messages.WARNING, '找不到啦')
            title = "%s的搜尋結果，共0筆"
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
                if user.password == password: #密文處理
                    request.session['is_login'] = True
                    request.session['username'] = user.username
                    request.session['name'] = user.name
                    request.session['rank'] = user.rank
                    url = '/Report_List/EX/ALL'
                    return redirect(url)
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
                    messages.add_message(request, messages.WARNING, "該帳號已存在!，請確認是否已註冊過!")
                    return render(request, 'register.html', locals())
                same_name_user = models.User.objects.filter(name=name)  #比對資料庫是否有相同信箱
                if same_name_user:
                    messages.add_message(request, messages.WARNING, "已有相同名字，請確認是否已註冊過!")
                    return render(request, 'register.html', locals())
                #若上面條件皆通過，則創建新的用戶
                new_user = models.User()
                new_user.username = username
                new_user.password = password1
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

                relate_con = request.POST.getlist('relate_content')
                summary_con = request.POST.getlist('summary_content')
                exploit_con = request.POST.getlist('exploit_content')
                
                data_list[1] = relate_con
                data_list[3] = summary_con
                data_list[5] = exploit_con
                new_report.content = data_list
                new_report.save()
                for photos in content_title:
                    img = []
                    cnt =  range(len(locals()[ photos + '_con']))
                    for count in cnt:
                        tmp = request.FILES.get(photos + '_imageInput_' +str(count))
                        if tmp is None:
                            tmp = ""
                        img.append(tmp)
                    imgText = request.POST.getlist(photos+'_imgText')
                    x = 0
                    for f in img:
                        try:
                            text = imgText[x]
                        except:
                            text = ""
                        file = models.Images(ex_post = new_report,image=f,content_id=x,content=(photos+'_image'),description=text)
                        file.save()
                        x+=1

                return redirect('/Report_List/EX/My_Report')                            
    else:
        return redirect('/login')
    
    new_ex_report = NewExploitReport(request.POST)
    return render(request, 'New_Exploit_Report.html', locals())    

def report_post(request, slug, id):
    if request.session.get('is_login',None):
        relate_imgs,summary_imgs,exploit_imgs,relate_imgText,summary_imgText,exploit_imgText =[],[],[],[],[],[]
        post = models.ExploitReport.objects.get(id = id)
        list123 = post.content
        string = ast.literal_eval(list123)
        relate_content = string[1]
        summary_content = string[3]
        exploit_content = string[5]

        for x in content_title:
            locals()[ x + '_num'] = len(locals()[ x + '_content']) -1 
            locals()[ x + '_count'] = range(len(locals()[ x + '_content']))
            try:
                locals()[ x + '_img'] = models.Images.objects.filter(ex_post_id = id,content= (x + '_image'))
                for i in locals()[ x + '_img']:
                    locals()[ x + '_imgs'].append(i.image.url)
                    locals()[ x + '_imgText'].append(i.description)
            except:
                pass
            locals()[ x + '_length'] = len(locals()[ x + '_imgs']) 
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

                    relate_con = request.POST.getlist('relate_content')
                    summary_con = request.POST.getlist('summary_content')
                    exploit_con = request.POST.getlist('exploit_content')
                    
                    data_list[1] = relate_con
                    data_list[3] = summary_con
                    data_list[5] = exploit_con
                    new_report.content = data_list
                    new_report.save()
                    
                    for photos in content_title:  #3個類別做一個for迴圈
                        img = []
                        x = 0
                        changecount =  len(locals()[ photos + '_con'])  #更改後的數量
                        origincount =  len(locals()[ photos + '_content'])  #原資料庫的數量
                        imgText = request.POST.getlist(photos+'_imgText')  #更改後圖片說明
                        for count in range(changecount):
                            tmp = request.FILES.get(photos + '_imageInput_' +str(count))   #取得各類的圖片
                            if tmp is None:  #如果沒圖片給圖片陣列一個空值
                                tmp = ""
                            img.append(tmp)
                        if changecount == origincount:   #如果內容數量不變，則更新
                            for f in img:
                                try:
                                    fileadd = models.Images.objects.get(ex_post_id = id,content= (photos + '_image'),content_id = x) 
                                    if f != "":                                                               
                                        try:
                                            text = imgText[x]
                                        except:
                                            text = ""
                                        fileadd.description=text
                                        fileadd.image = f
                                        fileadd.save()                                
                                    elif imgText[x] !="" :
                                        if fileadd.image !="":
                                            fileadd.description=imgText[x]
                                            fileadd.save()
                                    x+=1    
                                except:
                                    if f != "": 
                                        try:
                                            text = imgText[x]
                                        except:
                                            text = ""
                                        file = models.Images(ex_post = new_report,image=f,content_id=x,content=(photos+'_image'),description=text)
                                        file.save()
                                    elif imgText[x] !="" :
                                        if fileadd.image !="":
                                            fileadd.description=imgText[x]
                                            fileadd.save()
                                    x+=1    
                        elif changecount > origincount:   #如果變更數大於資料庫，則更新後新增   
                            for f in img:
                                try:
                                    fileadd = models.Images.objects.get(ex_post_id = id,content= (photos + '_image'),content_id = x)
                                    if f != "":                                                               
                                        try:
                                            text = imgText[x]
                                        except:
                                            text = ""
                                        fileadd.description=text
                                        fileadd.image = f
                                        fileadd.save()  
                                    elif imgText[x] !="" :
                                        if fileadd.image !="":
                                            fileadd.description=imgText[x]
                                            fileadd.save()
                                    x+=1    
                                except:
                                    pass
                            for i in range(origincount,changecount):
                                try:
                                    text = imgText[i]
                                except:
                                    text = ""
                                file = models.Images(ex_post = new_report,image=img[i],content_id=i,content=(photos+'_image'),description=text)
                                file.save()
                        elif changecount < origincount:   #如果變更數小於資料庫，則更新後刪除
                            for f in img:
                                try:
                                    fileadd = models.Images.objects.get(ex_post_id = id,content= (photos + '_image'),content_id = x) 
                                    if f != "":                                                               
                                        try:
                                            text = imgText[x]
                                        except:
                                            text = ""
                                        fileadd.description=text
                                        fileadd.image = f
                                        fileadd.save()                                
                                    elif imgText[x] !="" :      #
                                        if fileadd.image !="":
                                            fileadd.description=imgText[x]
                                            fileadd.save()
                                    x+=1    
                                except:
                                    pass
                            for i in range(changecount,origincount):  #改變之後數量少於原本資料庫的都刪除
                                try:
                                    models.Images.objects.get(ex_post_id = id,content= (photos + '_image'),content_id = i).delete()
                                except:
                                    pass
                        else:
                            print("我錯了嗎?")  #若是CMD跑出這個 代表我程式寫錯了
                            
                    return redirect('/Report_Post/view/' + str(id))
        return render(request, 'Ex_Report_Post.html', locals())
    else:
        return redirect('/login')

def new_unitedjudge(request):
    if request.session.get('is_login',None): #檢查session確定是否登入，不允許重複登入
        exname = []
        username = request.session['username']
        user = models.User.objects.get(username = username)    
        expost = models.ExploitReport.objects.all()
        if request.method == "POST":
                new_UnJudge = models.UnitedJudge()
                user = models.User.objects.get(username = username)
                new_UnJudge.user = user
                relate_con = request.POST.getlist('relate_content')
                summary_con = request.POST.getlist('summary_content')
                exploit_con = request.POST.getlist('exploit_content')
                
                data_list[1] = relate_con
                data_list[3] = summary_con
                data_list[5] = exploit_con

                target_name = request.POST.get('target_name')
                if target_name != "0":
                    new_UnJudge.target_name = target_name

                new_UnJudge.content = data_list
                new_UnJudge.save()
                for photos in content_title:
                    img = []
                    cnt =  range(len(locals()[ photos + '_con']))
                    for count in cnt:
                        tmp = request.FILES.get(photos + '_imageInput_' +str(count))
                        if tmp is None:
                            tmp = ""
                        img.append(tmp)
                    imgText = request.POST.getlist(photos+'_imgText')
                    x = 0
                    for f in img:
                        try:
                            text = imgText[x]
                        except:
                            text = ""
                        file = models.Images(uni_judge = new_UnJudge,image=f,content_id=x,content=(photos+'_image'),description=text)
                        file.save()
                        x+=1

                return redirect('/Report_List/UN/My_Report') 
        return render(request, 'New_UnitedJudge.html', locals())                         
    else:
        return redirect('/login')
      

def unitedjudge_post(request, slug, id):
    if request.session.get('is_login',None):
        relate_imgs,summary_imgs,exploit_imgs,relate_imgText,summary_imgText,exploit_imgText =[],[],[],[],[],[]
        new_UnJudge = models.UnitedJudge.objects.get(id = id)
        list123 = new_UnJudge.content
        string = ast.literal_eval(list123)
        relate_content = string[1]
        summary_content = string[3]
        exploit_content = string[5]
        expost = models.ExploitReport.objects.all()

        for x in content_title:
            locals()[ x + '_num'] = len(locals()[ x + '_content']) -1 
            locals()[ x + '_count'] = range(len(locals()[ x + '_content']))
            try:
                locals()[ x + '_img'] = models.Images.objects.filter(uni_judge_id = id,content= (x + '_image'))
                for i in locals()[ x + '_img']:
                    locals()[ x + '_imgs'].append(i.image.url)
                    locals()[ x + '_imgText'].append(i.description)
            except:
                pass
            locals()[ x + '_length'] = len(locals()[ x + '_imgs']) 
        if slug == "view": 
            change = False
        if slug == "modify":      
            change = True                          
            if request.method == "POST":
                relate_con = request.POST.getlist('relate_content')
                summary_con = request.POST.getlist('summary_content')
                exploit_con = request.POST.getlist('exploit_content')
                
                data_list[1] = relate_con
                data_list[3] = summary_con
                data_list[5] = exploit_con

                target_name = request.POST.get('target_name')
                if target_name != "0":
                    new_UnJudge.target_name = target_name
                new_UnJudge.content = data_list
                new_UnJudge.save()
                
                for photos in content_title:  #3個類別做一個for迴圈
                    img = []
                    x = 0
                    changecount =  len(locals()[ photos + '_con'])  #更改後的數量
                    origincount =  len(locals()[ photos + '_content'])  #原資料庫的數量
                    imgText = request.POST.getlist(photos+'_imgText')  #更改後圖片說明
                    for count in range(changecount):
                        tmp = request.FILES.get(photos + '_imageInput_' +str(count))   #取得各類的圖片
                        if tmp is None:  #如果沒圖片給圖片陣列一個空值
                            tmp = ""
                        img.append(tmp)
                    if changecount == origincount:   #如果內容數量不變，則更新
                        for f in img:
                            try:
                                fileadd = models.Images.objects.get(uni_judge_id = id,content= (photos + '_image'),content_id = x) 
                                if f != "":                                                               
                                    try:
                                        text = imgText[x]
                                    except:
                                        text = ""
                                    fileadd.description=text
                                    fileadd.image = f
                                    fileadd.save()                                
                                elif imgText[x] !="" :
                                    if fileadd.image !="":
                                        fileadd.description=imgText[x]
                                        fileadd.save()
                                x+=1    
                            except:
                                if f != "": 
                                    try:
                                        text = imgText[x]
                                    except:
                                        text = ""
                                    file = models.Images(uni_judge = new_UnJudge,image=f,content_id=x,content=(photos+'_image'),description=text)
                                    file.save()
                                elif imgText[x] !="" :
                                    if fileadd.image !="":
                                        fileadd.description=imgText[x]
                                        fileadd.save()
                                x+=1    
                    elif changecount > origincount:   #如果變更數大於資料庫，則更新後新增   
                        for f in img:
                            try:
                                fileadd = models.Images.objects.get(uni_judge_id = id,content= (photos + '_image'),content_id = x)
                                if f != "":                                                               
                                    try:
                                        text = imgText[x]
                                    except:
                                        text = ""
                                    fileadd.description=text
                                    fileadd.image = f
                                    fileadd.save()  
                                elif imgText[x] !="" :
                                    if fileadd.image !="":
                                        fileadd.description=imgText[x]
                                        fileadd.save()
                                x+=1    
                            except:
                                pass
                        for i in range(origincount,changecount):
                            try:
                                text = imgText[i]
                            except:
                                text = ""
                            file = models.Images(uni_judge = new_UnJudge,image=img[i],content_id=i,content=(photos+'_image'),description=text)
                            file.save()
                    elif changecount < origincount:   #如果變更數小於資料庫，則更新後刪除
                        for f in img:
                            try:
                                fileadd = models.Images.objects.get(uni_judge_id = id,content= (photos + '_image'),content_id = x) 
                                if f != "":                                                               
                                    try:
                                        text = imgText[x]
                                    except:
                                        text = ""
                                    fileadd.description=text
                                    fileadd.image = f
                                    fileadd.save()                                
                                elif imgText[x] !="" :      #
                                    if fileadd.image !="":
                                        fileadd.description=imgText[x]
                                        fileadd.save()
                                x+=1    
                            except:
                                pass
                        for i in range(changecount,origincount):  #改變之後數量少於原本資料庫的都刪除
                            try:
                                models.Images.objects.get(uni_judge_id = id,content= (photos + '_image'),content_id = i).delete()
                            except:
                                pass
                    else:
                        print("我錯了嗎?")  #若是CMD跑出這個 代表我程式寫錯了
                        
                return redirect('/UnitedJudge_Post/view/' + str(id))
        return render(request, 'UnitedJudge_Post.html', locals())
    else:
        return redirect('/login')

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
        elif judge == "UN":
            if slug == "ALL":
                post_list = models.UnitedJudge.objects.filter(status = '已審核')
                validation = False
            elif slug == "My_Report":
                post_list = models.UnitedJudge.objects.filter(user = username)
                validation = True
            elif slug == "Passing_Report":
                post_list = models.UnitedJudge.objects.filter(status = '待審核')
                validation = False
            elif slug == "Passed_Report":
                post_list = models.UnitedJudge.objects.filter(status = '已審核')
                validation = False        
    else:
        return redirect('/login')
    return render(request, 'Report_List.html', locals())

def delete_post(request, judge , slug, id):
    if request.session.get('is_login',None):
        if judge == "EX":
            models.ExploitReport.objects.get(id = id).delete()  #根據收到的ID從資料庫中刪除
        elif judge == "UN": 
            models.UnitedJudge.objects.get(id = id).delete()  #根據收到的ID從資料庫中刪除
        url = '/Report_List/' + judge + '/' + slug    
        return redirect(url)
    else:
        return redirect('/login')

def judge_post(request, judge, slug, success, id): #審核報告
    if request.session.get('is_login',None):
        if judge == "EX":
            if success == "success":    #審核成功
                new_report = models.ExploitReport.objects.get(id = id)
                new_report.status = '已審核'
            elif  success == "return":  #退回
                new_report = models.ExploitReport.objects.get(id = id)
                new_report.status = '待審核'
        elif judge == "UN": 
            if success == "success":    #審核成功
                new_report = models.UnitedJudge.objects.get(id = id)
                new_report.status = '已審核'
            elif  success == "return":  #退回
                new_report = models.UnitedJudge.objects.get(id = id)
                new_report.status = '待審核'        
        new_report.save()
        url = '/Report_List/' + judge + '/' + slug
        return redirect(url)
    else:
        return redirect('/login')

def generate_word(request, judge, id):
    relate_imgs,summary_imgs,exploit_imgs,relate_imgText,summary_imgText,exploit_imgText =[],[],[],[],[],[]
    if judge == "EX":
        report = models.ExploitReport.objects.get(id = id)  #依據ID尋找報告
        doc = DocxTemplate('media/word_template/成功記錄卡.docx')   #模板
        file_location=u'media/word/成功記錄卡(%s).docx'%report.target_name   #輸出檔案
        da1 = report.excute_date.split('-') #處理日期格式
        da2 = report.search_time.split('-')
        excute_date = '%d年%s月%s日'%(int(da1[0])-1911,da1[1],da1[2])  #西元轉換民國
        search_time = '%d%s%s'%(int(da2[0])-1911,da2[1],da2[2])
    elif judge == "UN":
        report = models.UnitedJudge.objects.get(id = id)
        doc = DocxTemplate('media/word_template/聯審資料.docx')   #模板
        file_location=u'media/word/聯審資料(%s).docx'%report.target_name   #輸出檔案
    list123 = report.content    #處理資料格式 轉換LIST
    string = ast.literal_eval(list123)
    relate_content = string[1]
    summary_content = string[3]
    exploit_content = string[5]
    
    for x in content_title: #處理資料
        locals()[ x + '_count'] = range(len(locals()[ x + '_content'])) #創造for迴圈需要的range
        try:
            if judge == "EX":
                locals()[ x + '_img'] = models.Images.objects.filter(ex_post_id = id,content= (x + '_image'))   #將報告圖片出來
            elif judge == "UN":
                locals()[ x + '_img'] = models.Images.objects.filter(uni_judge_id = id,content= (x + '_image'))   #將報告圖片出來
            for i in locals()[ x + '_img']:
                imgdata = InlineImage(doc,i.image.url.lstrip('/'), width=Mm(130), height=Mm(75))    #處理成doxctpl可讀取圖片格式
                locals()[ x + '_imgs'].append(imgdata)
                locals()[ x + '_imgText'].append(i.description)
        except:
            pass
        
    doc.render(locals())    #渲染至word
    doc.save(file_location) #存檔

    if os.path.exists(file_location): #檔案下載
        with open(file_location, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
            response['Content-Disposition'] = 'inline; filename={0}'.format(urlquote(os.path.basename(file_location)))
            return response
    raise Http404

    url = '/Report_List/' + judge + '/My_Report' 
    return redirect(url) #返回我的報告

def log_out(request):
    request.session.flush() #一次性將session內容全部清除
    return redirect('/login') 

