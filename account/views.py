from django.http import JsonResponse
from django.shortcuts import render
import string,random
from account.decorators import if_email_verified, verified_email_required
from django.views import View
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView
from account.forms import TbmUserSignupForm
from django.contrib import messages
from account.models import Company, DefaultCompany, EmailOTP,CustomUser
from common.common_function import send_message
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password, check_password

from tbm.tasks import send_mail
# Create your views here.

class LoginView(TemplateView):
    template_name = 'login.html'

    @method_decorator(verified_email_required)
    def get(self, request):
        return render(request, self.template_name, {})

    @method_decorator(verified_email_required)
    def post(self, request, *args, **kwargs):
            # Get username and password from request.POST
            username = request.POST.get('email')
            password = request.POST.get('password')
            # User logi
            authenticated_user = authenticate(username=username, password=password)
            if authenticated_user:
                login(request, authenticated_user)
                messages.success(request,"Login Successful")
                return redirect('tbm:index')
            else:
                messages.error(request,'Invalid username or password')
                return redirect('accounts:login')
            
class Profile(LoginRequiredMixin,View):
    template_name = 'my-profile.html'
    def get(self, request):
        return render(request, self.template_name, {'companies':request.user.company.all()})
    def post(self, request):
        if 'changeCompany' in request.POST:
            id = request.POST.get('id')
            company = request.POST.get('company')
            if Company.objects.filter(name = company).exists() is False:
                Company.objects.filter(id=id).update(name=company)
                messages.success(request,'Change successfull')
            else:
                messages.error(request,'Already Exists')
        if 'addCompany' in request.POST:
            company = request.POST.get('companyName')
            if Company.objects.filter(name = company).exists() is False:
                coupon = ''.join(random.choice(string.digits + string.ascii_letters) for _ in range(15))
                NewCompany = Company.objects.create(name=company,coupon=coupon)  
                request.user.company.add(NewCompany)
                messages.success(request,'Create Successfully')
            else:
                messages.error(request,'Already Exists')
        if  'activeCompany' in request.POST:
            domainName = request.POST.get('domainName')
            companyID = request.POST.get('companyID')
            company = Company.objects.get(id = int(companyID))
            if company.domain == None or company.domain == '':
                company.domain = domainName
            else: 
                domainName = company.domain+' , '+domainName
                company.domain = domainName
            company.save()

        if 'disableCompany' in request.POST:
            disableCompanyID = request.POST.get('disableID')
            Company.objects.filter(id = int(disableCompanyID)).update(domain = '')

        return redirect('accounts:profile')

class SignupView(View):
    template_name = 'signup.html'

    @method_decorator(verified_email_required)
    def get(self, request):
        form = TbmUserSignupForm()
        return render(request, self.template_name, {'form': form})

    @method_decorator(verified_email_required)
    def post(self, request):
        form = TbmUserSignupForm(request.POST)
        if form.is_valid():
            password1 = request.POST.get('password')
            password2 = request.POST.get('repassword')
            user_email = request.POST.get('email')
            
            if password1 == password2:
                user = form.save(commit=False)
                user.type = 'user'
                user.username = form.cleaned_data['email']
                user.set_password(password1)
                if CustomUser.objects.filter(email=user.email).exists() is False:
                    user.save()
                else:
                    messages.error(request,"Already exists!")
                    return redirect('accounts:login')
                company_name = DefaultCompany.objects.order_by('?').first()
                coupon = ''.join(random.choice(string.digits + string.ascii_letters) for _ in range(15))
                company = Company.objects.create(name=company_name.name,coupon=coupon)
                user.company.add(company)
                messages.success(request,"Create Account Successful")
                
                # Process OTP generation and email sending
                otp = EmailOTP.generate_otp(user)
                send_mail(subject='OTP for Email Verification', message=f'Your OTP is: {otp}', recipient=user.email)

                authenticated_user = authenticate(username=user_email, password=password1)

                if authenticated_user:
                    login(request, authenticated_user)
                    return redirect('accounts:VerifyOTP')
            else:
                messages.error(request,'Password not match')
           
        return redirect('accounts:signup')
    
class VerifyOTPView(LoginRequiredMixin,View):
    template_name = 'verify_otp.html'
    @method_decorator(if_email_verified)
    def get(self, request, **kwargs):
        return render(request, self.template_name, {})
    
    def post(self, request):
        user = request.user
        if 'verify_email' in request.POST:
            # Get the OTP from the POST request
            otp = request.POST.get('otp')
            # Check if the OTP is valid
            try:
                email_otp = EmailOTP.objects.get(user=user,otp=otp)
            except EmailOTP.DoesNotExist:
                # Invalid OTP
                messages.error(request,'Invalid OTP')
                return render(request, self.template_name, {})

            # Verify email account
            user.is_staff = True
            user.email_verified = True
            user.save()
            email_otp.delete()

            # Send email that the user has been verified
            send_mail(subject='Email Verification', message=f'Your email has been verified', recipient=user.email)
            # redirect to the index page after email verification
            messages.success(request,"Account verified successful")
            return redirect('tbm:index')

        elif 'resend_otp' in request.POST:
            # Process OTP generation and email sending
            otp = EmailOTP.generate_otp(user)
            send_mail(subject='OTP for Email Verification', message=f'Your OTP is: {otp}', recipient=user.email)
            messages.success(request,"OTP Resend successfully!")
            return redirect('accounts:VerifyOTP')

# Logout view
class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('accounts:login')
    
class ForgotPasswordView(View):
    template_name = 'forget_password.html'

    def get(self, request, **kwargs):
        return render(request, self.template_name, {})
    
    def post(self, request, **kwargs):
        if request.method == 'POST':
            email = request.POST.get('email')
            try:
                user = CustomUser.objects.get(email=email)
                otp = EmailOTP.generate_otp(user)
                send_mail(subject='OTP for Email Verification', message=f'Your OTP is: {otp}', recipient=email)
                messages.warning(request,'Please check OTP to your email')
                return redirect('accounts:new_set_password',user_id=user.id)
            except:
                messages.error(request,'No account find!')
                return redirect('accounts:forgot_password')
    
def new_set_password(request,user_id):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        try:
            user = CustomUser.objects.get(id=user_id)
            otp = EmailOTP.objects.get(user=user_id,otp=otp)
            if password1 == password2:
                user.password = make_password(password1)
                user.save()
                otp.delete()
                messages.success(request,"Password set successfully")
                return redirect("accounts:login")
            else:
                messages.error(request,"Password not match.")
        except EmailOTP.DoesNotExist:
            # Invalid OTP
            messages.error(request,'Invalid OTP')
            return redirect("accounts:new_set_password",user_id=user_id)
    return render(request,"set_new_password.html")

@login_required
def social_login(request):
    user=request.user
    if user.is_staff == False:
        request.user.delete()
        logout(request)
        messages.warning(request, "No account found link with this account, Please Sign up first")
        return redirect('accounts:login')
    if user.email_verified:
        if request.session.get('next_url'):
            redirect_url = request.session['next_url']
            del request.session['next_url']
            return redirect(redirect_url)
        return redirect('tbm:index')
    else:
        otp = EmailOTP.generate_otp(request.user)
        send_mail(subject='OTP for Email Verification', message=f'Your OTP is: {otp}', recipient=request.user.email)
        return redirect('VerifyOTP')

@login_required    
def social_signup(request):
    user=request.user
    if user.is_staff == False and user.email_verified == False:
        company_name = DefaultCompany.objects.order_by('?').first()
        coupon = ''.join(random.choice(string.digits + string.ascii_letters) for _ in range(15))
        company = Company.objects.create(name=company_name.name,coupon=coupon)        
        user.company.add(company)
        otp = EmailOTP.generate_otp(user)
        send_mail(subject='OTP for Email Verification', message=f'Your OTP is: {otp}', recipient=request.user.email)
        return redirect('accounts:VerifyOTP')
    elif user.is_staff == True and user.email_verified == True:
        return redirect('tbm:index')
    else:
        return redirect('accounts:signup')
    