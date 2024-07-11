import os
import base64
import yake
from together import Together

os.environ["TOGETHER_API_KEY"] = "d5da5a58304a1f224c271d51c39fc90e042471a9bb4b7d5dbddd2193d237bf8a"
client = Together(api_key=os.environ.get("TOGETHER_API_KEY"))

def generate_content(topic):
    # Generate keywords
    response_keywords = client.completions.create(
        model="togethercomputer/llama-2-70b-chat",
        prompt=f"Give me 3 keywords related to {topic}",
    )
    kw_extractor = yake.KeywordExtractor()
    keywords = kw_extractor.extract_keywords(response_keywords.choices[0].text)
    kwrds = [kw for kw, _ in keywords[:3]]  # Get first 3 keywords

    # Generate blog post
    response_blog_post = client.completions.create(
        model="togethercomputer/llama-2-70b-chat",
        prompt=f"Write a blog on the topic: {topic}. it should include the following parts answering the questions of what, why, how, where and when we use {topic}. Give a good description and grammar.",
    )
    blog_post_text = response_blog_post.choices[0].text

    # Write blog post text to a file
    with open('text.txt', 'w', encoding='utf-8') as text_file:
        text_file.write(blog_post_text)

    # Generate images
    images = []
    for i in range(2):  # Generate 2 images
        response_image = client.images.generate(
            prompt=topic,
            model="stabilityai/stable-diffusion-xl-base-1.0",
            steps=10,
            n=4,
        )
        img_data = response_image.data[i].b64_json
        img_decode = base64.b64decode(img_data)
        image_filename = f'static/img{i + 1}.jpg'
        with open(image_filename, 'wb') as image_file:
            image_file.write(img_decode)
        images.append(image_filename)

    return kwrds, images, blog_post_text  # Return keywords, image filenames, and blog post text
