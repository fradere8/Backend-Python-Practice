import requests
from django.shortcuts import render, redirect


POKEMON_TEAM = {}

def get_first_20_pokemons():
    try:
        response = requests.get('https://pokeapi.co', timeout=5)
        if response.status_code == 200 and response.text:
            return [p['name'] for p in response.json().get('results', [])]
    except (requests.RequestException, ValueError):
        pass
    return []

def fetch_pokemon_data(name):
    url = f'https://pokeapi.co{name.strip().lower()}'
    try:
        response = requests.get(url, timeout=5)
        if response.status_code != 200 or not response.text:
            return None
        data = response.json()
        stats = {s['stat']['name']: s['base_stat'] for s in data['stats']}
        return {
            'name': data['name'],
            'image': data['sprites']['front_default'],
            'types': [t['type']['name'] for t in data['types']],
            'weight': data['weight'],
            'height': data['height'],
            'abilities': [a['ability']['name'] for a in data['abilities']],
            'hp': stats.get('hp', 0),
            'attack': stats.get('attack', 0),
        }
    except (requests.RequestException, ValueError):
        return None

def pokemon_view(request):
    first_20 = get_first_20_pokemons()
    message = ''
    found_pokemon = None
    battle_result = ''

    if 'add_name' in request.GET:
        name = request.GET.get('add_name', '').strip().lower()
        if not name:
            message = 'Введите имя покемона.'
        elif name in POKEMON_TEAM:
            message = f'Покемон {name.title()} уже есть в вашей команде!'
        else:
            data = fetch_pokemon_data(name)
            if data:
                POKEMON_TEAM[name] = data
                message = f'Покемон {name.title()} добавлен в команду!'
            else:
                message = f'Покемон "{name}" не найден.'

    if 'search_name' in request.GET:
        name = request.GET.get('search_name', '').strip().lower()
        if name in POKEMON_TEAM:
            found_pokemon = POKEMON_TEAM[name]
            message = f'Данные покемона {name.title()} (уже в команде):'
        elif name:
            found_pokemon = fetch_pokemon_data(name)
            if found_pokemon:
                message = f'Данные покемона {name.title()}:'
            else:
                message = f'Покемон "{name}" не найден.'

    if 'fighter1' in request.GET and 'fighter2' in request.GET:
        f1 = request.GET.get('fighter1')
        f2 = request.GET.get('fighter2')
        if f1 in POKEMON_TEAM and f2 in POKEMON_TEAM:
            if f1 == f2:
                battle_result = 'Покемон не может сражаться сам с собой!'
            else:
                p1, p2 = POKEMON_TEAM[f1], POKEMON_TEAM[f2]
                power1 = p1['hp'] + p1['attack']
                power2 = p2['hp'] + p2['attack']
                if power1 > power2:
                    battle_result = f"Победил {p1['name'].title()} (сила {power1}) против {p2['name'].title()} (сила {power2})!"
                elif power2 > power1:
                    battle_result = f"Победил {p2['name'].title()} (сила {power2}) против {p1['name'].title()} (сила {power1})!"
                else:
                    battle_result = f"Ничья! Оба бойца набрали по {power1} очков силы."

    return render(request, 'services/pokemon.html', {
        'active_tab': 'pokemon',
        'first_20': first_20,
        'team': POKEMON_TEAM.values(),
        'message': message,
        'found_pokemon': found_pokemon,
        'battle_result': battle_result,
    })

def remove_pokemon(request, pokemon_name):
    if pokemon_name in POKEMON_TEAM:
        del POKEMON_TEAM[pokemon_name]
    return redirect('services:pokemon')

def get_all_breeds():
    response = requests.get('https://dog.ceo')
    if response.status_code == 200:
        return list(response.json()['message'].keys())
    return []

def get_breed_images(breeds_list):
    images = {}
    for breed in breeds_list:
        clean_breed = breed.strip().lower()
        if clean_breed:
            response = requests.get(f'https://dog.ceo{clean_breed}/images/random')
            if response.status_code == 200:
                images[clean_breed] = response.json()['message']
    return images

def dogs_view(request):
    all_breeds = get_all_breeds()
    user_input = request.GET.get('breeds', '')
    images = {}

    if user_input:
        selected_breeds = user_input.split(',')
        images = get_breed_images(selected_breeds)

    return render(request, 'services/dogs.html', {
        'active_tab': 'dogs',
        'all_breeds': all_breeds,
        'images': images,
        'user_input': user_input,
    })
    