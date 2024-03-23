import streamlit as st
import requests
import plotly.express as px

def getDataPokemon(pokemonName):
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemonName.lower()}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None
    
def statsChart(pokemonData):
    stats = pokemonData['stats']
    df = {'Stat': [stat['stat']['name'].capitalize() for stat in stats],
          'Base Value': [stat['base_stat'] for stat in stats]}
    fig = px.bar(df, x='Stat', y='Base Value', title='Base Stats',
                 labels={'Base Value': 'Base Stat Value'}, color='Stat',
                 template='plotly_dark')
    st.plotly_chart(fig) #NEW

def get_type_background_color(pokemon_type):
    type_colors = {
        'normal': '#A8A77A', 'fighting': '#C22E28', 'flying': '#A98FF3', 'poison': '#A33EA1',
        'ground': '#E2BF65', 'rock': '#B6A136', 'bug': '#A6B91A', 'ghost': '#735797',
        'steel': '#B7B7CE', 'fire': '#EE8130', 'water': '#6390F0', 'grass': '#7AC74C',
        'electric': '#F7D02C', 'psychic': '#F95587', 'ice': '#96D9D6', 'dragon': '#6F35FC',
        'dark': '#705746', 'fairy': '#D685AD'
    }
    return type_colors.get(pokemon_type, '#68A090')

def randomPokemon():
    import random
    total_pokemon = 807
    return str(random.randint(1, total_pokemon))

def pokemonByType(pokemon_type):
    url = f"https://pokeapi.co/api/v2/type/{pokemon_type.lower()}"
    response = requests.get(url)
    if response.status_code == 200:
        type_data = response.json()
        return [pokemon['pokemon']['name'] for pokemon in type_data['pokemon']]
    else:
        return None

def main():
    st.title("Pokémon Explorer App")
    tabSelection = st.sidebar.selectbox("Select View", ["Enter Pokémon Name", "Random Pokémon", "Search by Type"])
    if tabSelection == "Enter Pokémon Name":
        pokemon_name = st.text_input("Enter Pokémon Name:", "pikachu") #NEW
        pokemonData = getDataPokemon(pokemon_name)
        if pokemonData:
            backgroundColor = get_type_background_color(pokemonData['types'][0]['type']['name'])
            st.markdown(
                f'<div style="background-color:{backgroundColor};padding:10px;border-radius:10px;">'
                f'<h3 style="color:white;">Information about {pokemon_name.capitalize()}</h3></div>',
                unsafe_allow_html=True
            ) 
            st.write(f"**ID:** {pokemonData['id']}")
            st.write(f"**Height:** {pokemonData['height']} decimetres")
            st.write(f"**Weight:** {pokemonData['weight']} hectograms")
            st.write(f"**Type(s):** {', '.join([t['type']['name'] for t in pokemonData['types']])}")
            image_url = pokemonData['sprites']['front_default']
            st.image(image_url, caption=f"{pokemon_name.capitalize()} Image", use_column_width=True)
            statsChart(pokemonData)
        else:
            st.warning("Pokémon not found. Please enter a valid Pokémon name.") #NEW
    
    elif tabSelection == "Random Pokémon":
        numPokemon = st.slider("Select the number of Pokémon to display:", 1, 10, 5)
        st.subheader(f"**Top {numPokemon} Random Pokémon**")
        for _ in range(1, numPokemon + 1):
            randomPokemon1 = randomPokemon()
            pokemonInfo = getDataPokemon(randomPokemon1)
            if pokemonInfo:
                st.markdown(f"**{randomPokemon1.capitalize()}. {pokemonInfo['name'].capitalize()}**")
                st.write(f"**ID:** {pokemonInfo['id']}")
                st.write(f"**Height:** {pokemonInfo['height']} decimetres")
                st.write(f"**Weight:** {pokemonInfo['weight']} hectograms")
                types = [t['type']['name'] for t in pokemonInfo['types']]
                st.write(f"**Type(s):** {', '.join(types)}")
                image_url = pokemonInfo['sprites']['front_default']
                st.image(image_url, caption=f"{pokemonInfo['name'].capitalize()} Image", use_column_width=True)
                st.write("---")
            else:
                st.warning(f"Failed to fetch data for {pokemonInfo}")

    elif tabSelection == "Search by Type":
        selected_type = st.selectbox("Select Pokémon Type:", ["normal", "fighting", "flying", "poison", "ground","rock", "bug", "ghost", "steel", "fire", "water","grass", "electric", "psychic", "ice", "dragon","dark", "fairy"])
        pokemoneType = pokemonByType(selected_type)
        if pokemoneType:
            st.subheader(f"**Pokémon with Type: {selected_type.capitalize()}**")
            for pokemon_name in pokemoneType:
                st.write(f"- {pokemon_name.capitalize()}")
        else:
            st.warning("No Pokémon found for the selected type.")
main()
