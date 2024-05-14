import streamlit as st
import requests
from bs4 import BeautifulSoup
import itertools

websites = [
    "https://craftbits.com/recycled-crafts/",
    "https://craftgossip.com/about-craftgossip/notes",
    "https://upcyclethat.com/organizational-hacks-for-students/",
    "https://www.weareteachers.com/earth-day-crafts-classroom-activities/"
]

def fetch_links_from_website(url, query):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    links = []
    for a_tag in soup.find_all('a', href=True):
        if query.lower() in a_tag.text.lower():
            links.append({
                'title': a_tag.text,
                'link': a_tag['href']
            })
    return links

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

def get_site_image(url):
    site_images = {
        "https://craftbits.com/recycled-crafts/": "https://craftbits.com/wp-content/uploads/2020/06/cb-logo-header.png",
        "https://craftgossip.com/about-craftgossip/notes": "https://craftgossip.com/wp-content/uploads/2021/04/logo.svg",
        "https://upcyclethat.com/organizational-hacks-for-students/": "https://upcyclethat.com/wp-content/uploads/2015/04/upcycle-that-logo.png",
        "https://www.weareteachers.com/earth-day-crafts-classroom-activities/": "https://www.weareteachers.com/wp-content/uploads/2020/09/We-Are-Teachers-Logo.png"
    }
    return site_images.get(url, "https://via.placeholder.com/150")  # Default placeholder image

def display_recycling_projects(materials):
    results, found_projects = query_websites(materials)
    
    for material in materials:
        st.subheader(f"Projects for {material}:")
        if results[material]:
            for result in results[material]:
                site_image = get_site_image(result['link'])
                st.image(site_image, width=100)
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
                    site_image = get_site_image(link['link'])
                    st.image(site_image, width=100)
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
