import requests
import re

def extract_posts(url):
    # Sending an HTTP GET request to the URL
    response = requests.get(url)
    html_content = response.text

    # Regex pattern to capture all content inside the div with class "content"
    # We stop reading at the div with class "signature" to avoid issues with nested divs.
    # If we stopped reading at the closing </div> tag, we could miss part of the content 
    # due to nested divs in some posts. Stopping at the "signature" div ensures we capture 
    # the entire content section without being interrupted by nested divs.
    post_pattern = re.compile(r'<div class="content">(.*?)<div[^>]*class="signature"', re.DOTALL)
    posts = post_pattern.findall(html_content)
    cleaned_posts = []

    for i, post in enumerate(posts):
        # Remove any remaining HTML tags using a regex pattern
        post = re.sub('<.*?>', '', post).strip()

        # Remove leading/trailing quotes
        post = post.replace('"', '').strip()

        # Append the cleaned post to the list
        cleaned_posts.append(post)

    # Writing the extracted posts to the output file
    with open("url1_output.txt", "w") as file:
        # Write the extracted posts with numbering
        for i, post in enumerate(cleaned_posts, start=1):
            file.write(f"\n{i}. [{post}]\n")

# URL to extract posts from
url = "http://www.phpbb.com/community/viewtopic.php?f=46&t=2159437"

# Extracting and saving posts to the file
extract_posts(url)
