import openai
import os
import sys
# TODO: Import your libaries

# TODO: Maybe you need a key?
client = OpenAI()
script_openAI_dir = os.path.dirname(os.path.abspath(__file__))
audio_file_loc = filename = os.path.join(script_openAI_dir, "../frontend/src/audio_discription.mp3") 


# Image encoding, code provided
def encode_image(image_path):
    global img_path
    img_path = image_path
    with open(image_path, "rb") as image_F:
        return base64.b64encode(image_F.read()).decode('utf-8')


# TODO: Sending a request and getting a response
def make_response(image_path):
    response = client.responses.create(
        model="gpt-4.1 mini",
        input=[
            {
                "role": "user",
                "content": [
                    { "type": "input_text",
                         "text": "Briefly discribe this image(At most 1 sentences" },
                    {
                        "type": "input_image",
                        "image_url": f"data:image/jpeg;base64,{encode_image(image_path)}",
                    },
                ],
            }
        ],
    )
    return response.choices[0].message.content


# TODO: How do we make things audible?
def make_audible(text):
    with client.audio.speech.with_streaming_response.create(
        model="gpt-4o-mini-tts",
        voice="coral",
        input="Today is a wonderful day to build something people love!",
        instructions="Speak in a cheerful and positive tone.",
    ) as response:
        response.stream_to_file(audio_file_loc)

# TODO: Can we put everything together?

