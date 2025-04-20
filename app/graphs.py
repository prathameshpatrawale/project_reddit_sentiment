import os
import matplotlib
import seaborn as sns
from wordcloud import WordCloud
import base64
from io import BytesIO
from collections import Counter
import re

# Use Agg backend for headless environments like servers
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def create_directory(path):
    """Ensure the directory exists."""
    if not os.path.exists(path):
        os.makedirs(path)


def generate_graphs(sentiment_results, topic):
    # Extract sentiment labels and scores
    sentiments = [result['sentiment'] for result in sentiment_results]
    scores = [result['score'] for result in sentiment_results]

    # Create the directory for saving images if it doesn't exist
    images_dir = os.path.join('static', 'images')
    create_directory(images_dir)

    # Define the paths for saving the bar chart and word cloud images
    bar_chart_path = os.path.join(images_dir, 'sentiment_bar_chart.png')
    word_cloud_path = os.path.join(images_dir, 'word_cloud.png')

    # Create a barplot for sentiment scores
    plt.figure(figsize=(10, 6))
    ax = sns.barplot(x=sentiments, y=scores, hue=sentiments, palette="coolwarm", legend=False)
    plt.title(f'Sentiment Scores for Reddit Posts on "{topic}"', fontsize=16)
    plt.xlabel('Sentiment', fontsize=12)
    plt.ylabel('Score', fontsize=12)
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()

    # Add data labels on top of the bars
    for p in ax.patches:
        ax.annotate(f'{p.get_height():.2f}',
                    (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha='center', va='center',
                    fontsize=12, color='black',
                    xytext=(0, 5), textcoords='offset points')

    # Add gridlines
    plt.grid(True, linestyle='--', alpha=0.7)

    # Save the bar plot
    plt.savefig(bar_chart_path)
    plt.close()

    # Convert the bar chart to base64
    bar_img_b64 = encode_image_to_base64(bar_chart_path)

    # Generate word cloud from most frequent words in content
    text = ' '.join([result['content'] for result in sentiment_results])
    text = re.sub(r'[^A-Za-z\s]', '', text.lower())  # Clean text

    words = text.split()
    word_counts = Counter(words)

    wordcloud = WordCloud(width=800, height=400, background_color="white",
                          max_words=200, colormap='viridis').generate_from_frequencies(word_counts)

    wordcloud.to_file(word_cloud_path)
    word_cloud_b64 = encode_image_to_base64(word_cloud_path)

    return bar_img_b64, word_cloud_b64


def encode_image_to_base64(image_path):
    """Helper function to encode image file to base64."""
    with open(image_path, "rb") as img_file:
        img_b64 = base64.b64encode(img_file.read()).decode('utf-8')
    return img_b64
