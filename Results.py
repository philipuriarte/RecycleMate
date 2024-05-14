import streamlit as st
import requests
from bs4 import BeautifulSoup
import itertools

websites = [
    "https://craftbits.com/recycled-crafts/",
    "https://craftgossip.com/about-craftgossip/notes",
    "https://upcyclethat.com/organizational-hacks-for-students/",
    "https://www.weareteachers.com/earth-day-crafts-classroom-activities/"
    "https://earth911.com/recycling-center-search-guides/?utm_source=earth911-header"
    "https://howtodispose.info/recycle-aluminum-foil/"
    "https://energytheory.com/how-to-recycle-plastic-at-home/#:~:text=How%20to%20Recycle%20Plastic%20Properly%20at%20Home%201,Garden%20Using%20Old%20Plastic%20Pipes%20...%20More%20items"
    "https://www.instructables.com/projects"
    "https://www.diycraftsy.com/recycling-ideas/"
    "https://www.diybunker.com/68-diy-recycle-project-ideas-thatre-totally-genius/"
    "https://petticoatjunktion.com/crafts/upcycled-aluminum-can-decor/"
    "https://www.familyholiday.net/55-creative-bottle-cap-craft-ideas-diy-recycle-projects/#google_vignette"
    "https://www.hellowonderful.co/post/10-creative-ways-to-recycle-cardboard-into-kids-crafts/"
    "https://www.diyncrafts.com/27010/repurpose/35-brilliant-diy-repurposing-ideas-cardboard-boxes"
    "https://www.diyncrafts.com/110523/decor/old-book-crafts-and-decorations"
]

def fetch_links_from_website(url, query):
    try:
        response = requests.get(url)
        response.raise_for_status()  
        soup = BeautifulSoup(response.content, 'html.parser')
        links = []
        for a_tag in soup.find_all('a', href=True):
            link_text = a_tag.text.strip().lower()
            link_url = a_tag['href']
            if query.lower() in link_text:
                linked_page_content = get_linked_page_content(link_url)
                if is_relevant_content(linked_page_content):
                    links.append({
                        'title': link_text,
                        'link': link_url
                    })
        return links
    except requests.exceptions.RequestException as e:
        print(f"Error fetching links from {url}: {e}")
        return []

def get_linked_page_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # HTTP errors
        return response.text.lower()  
    except requests.exceptions.RequestException as e:
        print(f"Error fetching content from {url}: {e}")
        return ""

def is_relevant_content(content):
    content_lower = content.lower()
    relevant_keywords = ["recycle", "upcycle", "crafts", "artcrafts"]
    for keyword in relevant_keywords:
        if keyword in content_lower:
            return True
    return False

def query_websites(materials):
    found_projects = False
    results = {material: [] for material in materials}

    for material in materials:
        for website in websites:
            links = fetch_links_from_website(website, material)
            if links:
                found_projects = True
                results[material].extend(links)

    for i in range(2, len(materials) + 1):
        for combo in itertools.combinations(materials, i):
            combo_key = ", ".join(combo)
            for website in websites:
                links = fetch_links_from_website(website, combo_key)
                if links:
                    found_projects = True
                    results[combo_key] = links
    
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
            st.experimental_rerun()
        return

    st.image(image="https://developers.elementor.com/docs/assets/img/elementor-placeholder-image.png")
     
    st.header("Detected objects:")
    st.write(", ".join(st.session_state.recommendations))
    
    st.header("Recommended Projects:")
    display_recycling_projects(st.session_state.recommendations)

    if st.button("Back to Home"):
        st.session_state.page = 'home'
        st.experimental_rerun()

if __name__ == "__main__":
    main()
