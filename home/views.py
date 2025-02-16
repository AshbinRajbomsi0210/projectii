from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Count
from datetime import date
from django.contrib import messages
from django.db.models import Q
from .models import RequestBlood 
from .models import BloodBank



# Check if user is admin
def is_admin(user):
    return user.is_staff  # Check if user has admin (staff) privileges

# Home page
def index(request):
    all_group = BloodGroup.objects.annotate(total=Count('donor'))
    return render(request, "index.html", {'all_group': all_group})

# Donor list page
def donors_list(request, myid):
    blood_groups = BloodGroup.objects.filter(id=myid).first()
    donor = Donor.objects.filter(blood_group=blood_groups, is_approved=True).order_by("date_of_birth")
    return render(request, "donors_list.html", {'donor': donor})

# Donor details page
def donors_details(request, myid):
    details = Donor.objects.filter(id=myid)[0]
    return render(request, "donors_details.html", {'details': details})

# Request blood page
def request_blood(request):
    if request.method == "POST":
        name = request.POST['name']
        phone = request.POST['phone']
        state = request.POST['state'].capitalize()
        city = request.POST['city'].capitalize()
        address = request.POST['address']
        blood_group = request.POST['blood_group']
        date = request.POST['date']
        
        # Save the request to the database
        blood_requests = RequestBlood.objects.create(
            name=name,
            phone=phone,
            state=state,
            city=city,
            address=address,
            blood_group=BloodGroup.objects.get(name=blood_group),
            date=date,
        )
        blood_requests.save()

        # Add a success message
        messages.success(request, "Your blood request has been submitted successfully!")

        # Redirect to prevent form resubmission
        return redirect("request_blood")  # Replace "index" with your desired view name or URL pattern

    return render(request, "request_blood.html")
# See all blood requests
def see_all_request(request):
    unfulfilled_requests = RequestBlood.objects.filter(is_fulfilled=False).order_by('date')
    fulfilled_requests = RequestBlood.objects.filter(is_fulfilled=True).order_by('date')
    return render(request, "see_all_request.html", {
        'unfulfilled_requests': unfulfilled_requests,
        'fulfilled_requests': fulfilled_requests,
    })

# Become a donor page
def become_donor(request):
    if request.method == "POST":   
        username = request.POST['username']
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken. Please choose another one.")
            return redirect("become_donor")  # Redirect back to the form
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        phone = request.POST['phone']
        state = request.POST['state']
        city = request.POST['city']
        address = request.POST['address']
        gender = request.POST['gender']
        blood_group = request.POST['blood_group']
        date = request.POST['date']
        image = request.FILES['image']
        report =request.FILES['report']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('/signup')
            

        # Create the user
        user = User.objects.create_user(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password
        )
        # Create the donor, with is_approved=False
        Donor.objects.create(
            donor=user,
            phone=phone,
            state=state,
            city=city,
            address=address,
            gender=gender,
            blood_group=BloodGroup.objects.get(name=blood_group),
            date_of_birth=date,
            image=image,
            report=report,
            # is_approved=False  # Donor approval is False by default
        )
        user.save()
        messages.success(request, "Donor Registration successful!")
        return redirect('/login')
    return render(request, "become_donor.html")
# Login page
def Login(request):
    if request.user.is_authenticated:
        return redirect("/")
    else:
        if request.method == "POST":
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect("/")
            else:
                thank = True
                return render(request, "user_login.html", {"thank": thank})
    return render(request, "login.html")

# Logout
def Logout(request):
    messages.success(request, "You have successfully logged out.")
    logout(request)
    return redirect('/')

# User profile page
@login_required(login_url='/login')
def profile(request):
    donor_profile = Donor.objects.get(donor=request.user)
    return render(request, "profile.html", {'donor_profile': donor_profile})

# Edit profile page
@login_required(login_url='/login')
def edit_profile(request):
    donor_profile = Donor.objects.get(donor=request.user)
    if request.method == "POST":
        email = request.POST['email']
        phone = request.POST['phone']
        state = request.POST['state']
        city = request.POST['city']
        address = request.POST['address']

        donor_profile.donor.email = email
        donor_profile.phone = phone
        donor_profile.state = state
        donor_profile.city = city
        donor_profile.address = address
        donor_profile.save()
        donor_profile.donor.save()

        try:
            image = request.FILES['image']
            donor_profile.image = image
            donor_profile.save()
            report = request.FILES['report']
            donor_profile.report = report
            donor_profile.save()

        except:
            pass
        alert = True
        return render(request, "edit_profile.html", {'alert': alert})
    return render(request, "edit_profile.html", {'donor_profile': donor_profile})

# Change donation status
@login_required(login_url='/login')
def change_status(request):
    donor_profile = Donor.objects.get(donor=request.user)
    donor_profile.ready_to_donate = not donor_profile.ready_to_donate
    donor_profile.save()
    return redirect('/profile')

# About Us page
def about_us(request):
    return render(request, 'about_us.html')

# Contact Us page
def contact_us(request):
    return render(request, 'contact_us.html')

# Campaigns page
def campaigns(request):
    return render(request, 'blood_banks.html')

# Admin Panel Views

@login_required(login_url='/login')
@user_passes_test(is_admin)
def admin_dashboard(request):
    total_donors = Donor.objects.count()
    total_requests = RequestBlood.objects.count()
    unfulfilled_requests = RequestBlood.objects.filter(is_fulfilled=False).count()
    fulfilled_requests = RequestBlood.objects.filter(is_fulfilled=True).count()

    # Search functionality for donors
    donor_search_query = request.GET.get('donor_search', '')
    if donor_search_query:
        donors = Donor.objects.filter(donor__username__icontains=donor_search_query)
    else:
        donors = Donor.objects.all()

    # Search functionality for requests
    request_search_query = request.GET.get('request_search', '')
    if request_search_query:
        filtered_requests = RequestBlood.objects.filter(name__icontains=request_search_query)
    else:
        filtered_requests = RequestBlood.objects.all()

    context = {
        'total_donors': total_donors,
        'total_requests': total_requests,
        'unfulfilled_requests': unfulfilled_requests,
        'fulfilled_requests': fulfilled_requests,
        'donors': donors,
        'requests': filtered_requests,
    }

    return render(request, 'admin_panel/dashboard.html', context)

@login_required(login_url='/login')
@user_passes_test(is_admin)
def manage_donors(request):
    donors = Donor.objects.all()
    return render(request, 'admin_panel/dashboard.html', {'donors': donors})

@login_required(login_url='/login')
@user_passes_test(is_admin)
def manage_requests(request):
    requests = RequestBlood.objects.all()
    return render(request, 'admin_panel/dashboard.html', {'requests': requests})



@login_required(login_url='/login')
@user_passes_test(is_admin)
def delete_donor(request, donor_id):
    donor = get_object_or_404(Donor, id=donor_id)
    donor.delete()
    messages.success(request, f"{donor.donor.username} has been deleted successfully.")
    return redirect('manage_donors')

@login_required(login_url='/login')
@user_passes_test(is_admin)
def fulfill_request(request, request_id):
    blood_request = get_object_or_404(RequestBlood, id=request_id)
    blood_request.is_fulfilled = not blood_request.is_fulfilled  # Toggle status
    blood_request.save()
    
    status_message = "fulfilled" if blood_request.is_fulfilled else "not fulfilled"
    messages.success(request, f"Request from {blood_request.name} has been marked as {status_message}.")
    
    return redirect('manage_requests')

@login_required(login_url='/login')
@user_passes_test(is_admin)
def delete_request(request, request_id):
    blood_request = get_object_or_404(RequestBlood, id=request_id)
    blood_request.delete()
    messages.success(request, f"Request from {blood_request.name} has been deleted.")
    return redirect('manage_requests')

def blood_banks(request):
    banks = BloodBank.objects.all()  # Fetch all blood banks from DB
    return render(request, 'blood_banks.html', {'banks': banks})

@login_required
def approve_donor(request, donor_id):
    donor = get_object_or_404(Donor, id=donor_id)
    donor.is_approved = True
    donor.save()
    messages.success(request, "Donor approved successfully!")
    return redirect('admin_dashboard')

@login_required
def unapprove_donor(request, donor_id):
    donor = get_object_or_404(Donor, id=donor_id)
    donor.is_approved = False
    donor.save()
    messages.success(request, "Donor unapproved successfully!")
    return redirect('admin_dashboard')

@login_required
def approve_request(request, request_id):
    req = get_object_or_404(RequestBlood, id=request_id)
    req.is_approved = True
    req.save()
    messages.success(request, "Request approved successfully!")
    return redirect('admin_dashboard')

@login_required
def unapprove_request(request, request_id):
    req = get_object_or_404(RequestBlood, id=request_id)
    req.is_approved = False
    req.save()
    messages.success(request, "Request unapproved successfully!")
    return redirect('admin_dashboard')