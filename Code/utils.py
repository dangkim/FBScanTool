import os


# Create Original URL to crawl Data
def create_original_link(url):
    if url.find(".php") != -1:
        original_link = "https://en-gb.facebook.com/profile.php?id=" + ((url.split("="))[1])
    else:
        original_link = url
    return original_link


# Get Section Route
def get_friend_section_route(url):
    section = ["/friends",
               "/friends_mutual",
               "/following",
               "/followers",
               "/friends_work",
               "/friends_college",
               "/friends_current_city",
               "/friends_hometown"]
    if url.find(".php") != -1:
        section = ["&sk=friends",
                   "&sk=friends_mutual",
                   "&sk=following",
                   "&sk=followers",
                   "&sk=friends_work",
                   "&sk=friends_college",
                   "&sk=friends_current_city",
                   "&sk=friends_hometown"]
    return section


# Get Photos Section Route
def get_photos_section_route(url):
    section = ["/photos_by",
               "/photos_of"]
    if url.find(".php") != -1:
        section = ["&sk=photos_by",
                   "&sk=photos_of"]
    return section


# Get Video Section Route
def get_video_section_route(url):
    section = ["/videos",
               "/videos_of"]
    if url.find(".php") != -1:
        section = ["&sk=videos",
                   "&sk=videos_of"]
    return section


# Get Video Section Route
def get_about_section_route(url):
    section = ["/about_overview",
               "/about_work_and_education",
               "/about_places",
               "/about_contact_and_basic_info",
               "/about_family_and_relationships",
               "/about_details",
               "/about_life_events"]
    if url.find(".php") != -1:
        section = ["&sk=about_overview", "&sk=about_work_and_education", "&sk=about_places",
                   "&sk=about_contact_and_basic_info", "&sk=about_family_and_relationships", "&sk=about_details",
                   "&sk=about_life_events"]
    return section


# Get Profile Folder
def get_profile_folder(folder, url):
    if url.find(".php") != -1:
        target_dir = os.path.join(folder, url.split('/')[-1].replace('profile.php?id=', ''))
    else:
        target_dir = os.path.join(folder, url.split('/')[-1])
    return target_dir
