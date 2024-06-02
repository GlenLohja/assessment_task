import requests
import re

def extract_posts(url):
    # Sending an HTTP GET request to the URL
    response = requests.get(url)
    html_content = response.text

    # Regex pattern to extract content within the "js-post__content-text restore h-wordwrap" div
    # This pattern captures the entire content, including nested divs, until it reaches the closing </div>,
    # either followed by another <div> or the end of the signature section.
    # This modification accounts for posts with quotes, as they may not have the signature section, requiring different closing logic.
    post_pattern = re.compile(r'<div class="js-post__content-text restore h-wordwrap" itemprop="text">(.*?)</div>\s*</div>\s*<div|<div class="post-signature restore">', re.DOTALL)
    posts = post_pattern.findall(html_content)
    cleaned_posts = []

    for i, post in enumerate(posts):

        # Remove <a> tags
        post = re.sub(r'<a[^>]*>.*?</a>', '', post, flags=re.DOTALL)

        # Replace <br> tags with newlines
        post = post.replace('<br>', '\n')

        # Remove any remaining HTML tags using a regex pattern
        post = re.sub('<.*?>', '', post).strip()

        # Replace HTML entities with their plain text equivalents
        post = re.sub(r'&quot;', '"', post)
        post = re.sub(r'&#91;', '[', post)
        post = re.sub(r'&#93;', ']', post)

        # Replace multiple newlines with a single newline
        post = re.sub(r'\n\s*\n', '\n\n', post)
        
        # Remove tabs
        post = post.replace('\t', '')

        # Remove leading/trailing quotes
        post = post.replace('"', '').strip()

        # Append the cleaned post to the list
        cleaned_posts.append(post)


    # Writing the extracted posts to the output file
    with open("url2_output.txt", "w") as file:
        # Write the extracted posts with numbering
        for i, post in enumerate(cleaned_posts, start=1):
            file.write(f"\n{i}. [{post}]\n")

# URL to extract posts from
url = "https://forum.vbulletin.com/forum/vbulletin-3-8/vbulletin-3-8-questions-problems-and-troubleshooting/414325-www-vs-non-www-url-causing-site-not-to-login"

# Extracting and saving posts to the file
extract_posts(url)
