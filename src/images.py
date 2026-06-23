from dotenv import load_dotenv
from imagekitio import ImageKit
import os

load_dotenv()

# Check what os.getenv is actually returning
print("Private:", os.getenv("IMAGEKIT_PRIVATE_KEY"))
print("Public:", os.getenv("IMAGEKIT_PUBLIC_KEY"))
print("URL:", os.getenv("IMAGEKIT_URL"))

# If any of the above print "None", ImageKit will crash here:
imagekit = ImageKit(
    private_key=os.getenv("IMAGEKIT_PRIVATE_KEY"),
    public_key=os.getenv("IMAGEKIT_PUBLIC_KEY"),
    url_endpoint=os.getenv("IMAGEKIT_URL"),
)