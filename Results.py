import streamlit as st
import requests
from bs4 import BeautifulSoup
import itertools

# List of crafts websites
websites = [
    "https://craftprojectideas.com/diy-terrarium-with-recycled-cups/",
    "https://craftbits.com/recycled-crafts/",
    "https://craftgossip.com/about-craftgossip/notes",
    "https://upcyclethat.com/organizational-hacks-for-students/",
    "https://www.weareteachers.com/earth-day-crafts-classroom-activities/",
    "https://earth911.com/recycling-center-search-guides/?utm_source=earth911-header",
    "https://howtodispose.info/recycle-aluminum-foil/",
    "https://energytheory.com/how-to-recycle-plastic-at-home/#:~:text=How%20to%20Recycle%20Plastic%20Properly%20at%20Home%201,Garden%20Using%20Old%20Plastic%20Pipes%20...%20More%20items",
    "https://www.instructables.com/projects",
    "https://www.diycraftsy.com/recycling-ideas/",
    "https://www.diybunker.com/68-diy-recycle-project-ideas-thatre-totally-genius/",
    "https://petticoatjunktion.com/crafts/upcycled-aluminum-can-decor/",
    "https://www.familyholiday.net/55-creative-bottle-cap-craft-ideas-diy-recycle-projects/#google_vignette",
    "https://www.diytomake.com/37-diy-ways-to-recycle-bottle-caps/#:~:text=20%20Smart%20Ways%20To%20Recycle%20Bottle%20Caps%20And,8.%20DIY%20Bottle%20Cap%20Basket%20...%20More%20items",
    "https://www.diyncrafts.com/17424/repurpose/50-jaw-dropping-ideas-for-upcycling-tin-cans-into-beautiful-household-items",
    "https://singlegirlsdiy.com/candy-wrapper-crafts/",
    "https://www.hellowonderful.co/post/10-creative-ways-to-recycle-cardboard-into-kids-crafts/",
    "https://www.diyncrafts.com/27010/repurpose/35-brilliant-diy-repurposing-ideas-cardboard-boxes",
    "https://veryinformed.com/can-you-recycle-chip-bags/#:~:text=How%20Can%20I%20Reuse%20and%20Repurpose%20My%20Old,Baby%20Toys%20...%205%205.%20Party%20Decorations%20",
    "https://www.diyncrafts.com/16784/repurpose/35-impossibly-creative-projects-you-can-make-with-recycled-egg-cartons",
    "https://organisemyhouse.com/egg-carton-reuse/",
    "https://organisemyhouse.com/egg-carton-reuse/",
    "https://www.upcycleart.info/crafts/glass-jars-recycled-decor-crafts/",
    "https://wonderfuldiy.com/recycled-mason-jar-lids/",
    "https://craftinvaders.co.uk/recycled-magazine-basket/",
    "https://www.diyncrafts.com/110523/decor/old-book-crafts-and-decorations",
    "https://energytheory.com/how-to-recycle-plastic-at-home/#:~:text=How%20to%20Recycle%20Plastic%20Properly%20at%20Home%201,Garden%20Using%20Old%20Plastic%20Pipes%20...%20More%20items",
    "https://digginginthegarden.com/diy-recycled-plastic-bottle-gardens/",
    "https://www.ecomasteryproject.com/reuse-plastic-cups/#:~:text=40%20Brilliant%20Ways%20to%20Reuse%20Plastic%20Cups%20for,8%208.%20Greenhouse%20for%20Seedlings%20...%20More%20items",
    "https://www.familyhandyman.com/list/21-nifty-ways-to-reuse-plastic-jugs-and-bottles-at-home/",
    "https://www.boredart.com/2019/08/repurposing-plastic-straw-crafts-ideas.html",
    "https://www.ecomasteryproject.com/shampoo-bottles-reuse-ideas/#:~:text=Easy%20Shampoo%20Bottles%20Reuse%20Ideas%20For%20Minimum%20Waste,hanging%20garden%20...%208%20Sprinkler%20...%20More%20items",
    "https://get-green-now.com/reuse-styrofoam/",
    "https://simplelifeofalady.com/recycle-tires/#:~:text=20%20Amazing%20Ideas%20to%20Recycle%20Tires%201%201.,...%208%208.%20Toy%20storage%20...%20More%20items",
    "https://www.creativejewishmom.com/recycled-plastic-cup-crafts/"
]

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

def fetch_links_from_website(url, query):
    """
    Fetches links from a website that contain a specific query in their text.
    
    Args:
        url (str): The URL of the website to fetch links from.
        query (str): The query to search for in the link text.
    
    Returns:
        list: A list of dictionaries containing the title and URL of the relevant links.
    """
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        links = []
        for a_tag in soup.find_all('a', href=True):
            link_text = a_tag.text.strip().lower()
            link_url = a_tag['href']
            # filter out local/anchor links
            if not link_url.startswith(('#', '/')):
                if not link_url.startswith(('http://', 'https://')):
                    link_url = construct_full_url(url, link_url)
                if query.lower() in link_text:
                    links.append({
                        'title': link_text,
                        'link': link_url
                    })
        return links
    except requests.exceptions.RequestException as e:
        print(f"Error fetching links from {url}: {e}")
        return [] 

def construct_full_url(base_url, url):
    """
    Constructs the full URL from a base URL and a possibly relative URL.
    
    Args:
        base_url (str): The base URL.
        url (str): The possibly relative URL.
    
    Returns:
        str: The full URL.
    """
    return requests.compat.urljoin(base_url, url)

def query_websites(materials):
    # Initialize results dictionary with empty lists for each material
    results = {material: [] for material in materials}
    found_projects = False

    # Combine materials and their synonyms
    synonyms = {
        "plastic cup": ["plastic cup", "disposable cup", "plastic container", "plastic drinkware", "recycled cups"]
        # add more synonyms or materials if needed
    }
    material_terms = {material: synonyms.get(material, []) + [material] for material in materials}

    for material, terms in material_terms.items():
        for term in terms:
            for website in websites:
                links = fetch_links_from_website(website, term)
                if links:
                    found_projects = True
                    results[material].extend(links)

    # remove duplicate links and makes sure all materials have fetched links
    for material in results:
        unique_links = {link['link']: link for link in results[material]}.values()
        results[material] = list(unique_links)
        if not results[material]:
            print(f"No links fetched for material: {material}")
    
    return results, found_projects

def display_recycling_projects(materials):
    results, found_projects = query_websites(materials)
    
    for material in materials:
        st.subheader(f"Projects for {material}:")
        if results[material]:
            for result in results[material]:
                st.markdown(
                    f'<a href="{result["link"]}" target="_blank"><button>{result["title"]}</button></a>',
                    unsafe_allow_html=True
                )
        else:
            st.warning(f"No recycling projects found for {material}")
    
    combo_results = {k: v for k, v in results.items() if k not in materials}
    if combo_results:
        st.subheader("Projects for combinations of materials:")
        for combo, links in combo_results.items():
            if links:
                st.markdown(f"### {combo}")
                for link in links:
                    st.markdown(
                        f'<a href="{link["link"]}" target="_blank"><button>{link["title"]}</button></a>',
                        unsafe_allow_html=True
                    )

def main():
    st.title("Results")
    
    if 'recommendations' not in st.session_state:
        st.write("No recommendations to display. Please go back to the home page and try again.")
        if st.button("Back to Home"):
            st.session_state.page = 'home'
            st.rerun()
        return
     
    st.header("Detected objects:")
    st.write(", ".join(st.session_state.recommendations))
    
    st.header("Recommended Projects:")
    display_recycling_projects(st.session_state.recommendations)

    if st.button("Back to Home"):
        st.session_state.page = 'home'
        st.rerun()

if __name__ == "__main__":
    main()
