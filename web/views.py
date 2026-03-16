from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .gemini_service import identify_plant_from_image, get_growth_tips, chat_with_bot
import base64
import markdown

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'auth/register.html', {'form': form})

def index_view(request):
    return render(request, 'index.html')

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

@login_required
def identify_view(request):
    context = {}
    if request.method == 'POST':
        image_data = None
        
        # Check for uploaded file
        if 'image_upload' in request.FILES:
            image_file = request.FILES['image_upload']
            image_data = image_file.read()
            context['image_url'] = "data:image/jpeg;base64," + base64.b64encode(image_data).decode('utf-8')
            
        # Check for captured camera image (base64 string)
        elif 'camera_image' in request.POST and request.POST['camera_image']:
            data_url = request.POST['camera_image']
            # Remove "data:image/png;base64," header
            image_data = base64.b64decode(data_url.split(',')[1])
            context['image_url'] = data_url

        if image_data:
            result = identify_plant_from_image(image_data)
            context['result'] = markdown.markdown(result)
            
    return render(request, 'identify.html', context)

@login_required
def growth_tips_view(request):
    context = {}
    if request.method == 'POST':
        plant_name = request.POST.get('plant_name')
        if plant_name:
            context['plant_name'] = plant_name
            tips = get_growth_tips(plant_name)
            context['tips'] = markdown.markdown(tips)
    return render(request, 'growth_tips.html', context)

@login_required
def chatbot_view(request):
    # Initialize chat history in session if not exists
    if 'chat_history' not in request.session:
        request.session['chat_history'] = []
    
    context = {'chat_history': request.session['chat_history']}
    
    if request.method == 'POST':
        user_message = request.POST.get('message')
        if user_message:
            # Transform session history to Gemini format if needed, 
            # for now passing empty list as we want single turn or simple history
            # To properly implement history with Gemini SDK, we need to map roles.
            # Here we simplify and just send context if needed or just message.
            
            bot_response = chat_with_bot(user_message)
            
            # Update session history
            request.session['chat_history'].append({'role': 'user', 'content': user_message})
            request.session['chat_history'].append({'role': 'bot', 'content': markdown.markdown(bot_response)})
            request.session.modified = True
            
    return render(request, 'chatbot.html', context)

@login_required
def marketplace_view(request):
    products = [
        {"name": "Organic Tulsi Seeds", "image": "images/marketplace/tulsi.png", "shop": "Green Earth Nursery", "desc": "Premium quality holy basil seeds for home gardening."},
        {"name": "Aloe Vera Sapling", "image": "images/marketplace/aloe.png", "shop": "NGL Organics", "desc": "Healthy 6-month old medicinal Aloe Vera sapling."},
        {"name": "Neem Oil (500ml)", "image": "images/marketplace/neem.png", "shop": "Herbal Haven", "desc": "100% natural cold-pressed neem oil."},
        {"name": "Hibiscus Plant", "image": "images/marketplace/hibiscus.png", "shop": "Flower Power", "desc": "Vibrant red hibiscus plant, medicinal variety."},
        {"name": "Ashwagandha Root Powder", "image": "images/marketplace/ashwagandha.png", "shop": "AyurVeda Pro", "desc": "Pure organic ashwagandha root powder."},
        {"name": "Tulsi Plant (Krishna)", "image": "images/marketplace/tulsi.png", "shop": "Sacred Groves", "desc": "Dark purple Krishna Tulsi variety."},
        {"name": "Aloe Vera Gel (Pure)", "image": "images/marketplace/aloe.png", "shop": "NGL Organics", "desc": "Freshly extracted pure aloe vera gel."},
        {"name": "Neem Cake Fertilizer", "image": "images/marketplace/neem.png", "shop": "Organic Farmers", "desc": "Organic neem cake for soil enrichment."},
        {"name": "Hibiscus Tea (Dried)", "image": "images/marketplace/hibiscus.png", "shop": "Tea Gardens", "desc": "Dried hibiscus petals for herbal tea."},
        {"name": "Ashwagandha Capsules", "image": "images/marketplace/ashwagandha.png", "shop": "Wellness World", "desc": "High potency ashwagandha extract capsules."},
        {"name": "Lemon Tulsi Seeds", "image": "images/marketplace/tulsi.png", "shop": "Green Earth Nursery", "desc": "Rare lemon-scented basil seeds."},
        {"name": "Aloe Baby Pups", "image": "images/marketplace/aloe.png", "shop": "Succulent City", "desc": "Pack of 3 small aloe vera pups."},
        {"name": "Neem Soap (Handmade)", "image": "images/marketplace/neem.png", "shop": "Village Crafts", "desc": "Handmade soap with neem oil and turmeric."},
        {"name": "White Hibiscus Sapling", "image": "images/marketplace/hibiscus.png", "shop": "Flower Power", "desc": "Rare white medicinal hibiscus variety."},
        {"name": "Ashwagandha Roots (Raw)", "image": "images/marketplace/ashwagandha.png", "shop": "Roots & Herbs", "desc": "Dried raw ashwagandha roots for decoration or use."}
    ]
    return render(request, 'marketplace.html', {'products': products})
