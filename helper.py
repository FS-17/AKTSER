import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
import os
import time
from numpy import std, concatenate
import librosa
from soundfile import write as sf_write
from dotenv import load_dotenv

load_dotenv()


genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-pro-latest')


extraxtText = "I want you to act as translator for me. just Extract the text content from voice message in the same language as the voice message."
summarizeText = "Summarize the voice message in markdown to cleanly format your output. Example: Bold key subject matter and potential areas that may need expanded information. Use bullet points to list key points. Use italics to emphasize important information. Use headers to separate sections of the summary. Use numbered lists to list steps or key points in a process. and translate it to the same language as the voice message."

safety_setting = {
    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
    # HarmCategory.HARM_CATEGORY_DANGEROUS: HarmBlockThreshold.BLOCK_NONE,
    # HarmCategory.HARM_CATEGORY_VIOLENCE: HarmBlockThreshold.BLOCK_NONE,
    # HarmCategory.HARM_CATEGORY_MEDICAL: HarmBlockThreshold.BLOCK_NONE,
    # HarmCategory.HARM_CATEGORY_DEROGATORY: HarmBlockThreshold.BLOCK_NONE,
    # HarmCategory.HARM_CATEGORY_SEXUAL: HarmBlockThreshold.BLOCK_NONE,
    # HarmCategory.HARM_CATEGORY_UNSPECIFIED: HarmBlockThreshold.BLOCK_NONE,
    # HarmCategory.HARM_CATEGORY_TOXICITY: HarmBlockThreshold.BLOCK_NONE,
}


def summarize(voicepath: str):
    """
    Summarizes the content of a voice message.

    Args:
        voicepath (str): The path to the voice message file.

    Returns:
        str: The generated content.

    Raises:
        str: If there is an error uploading the voice message.

    """
    # upload the voice message
    UploadedVoice = genai.upload_file(voicepath)
    # verfiy the voice message is uploaded
    while not UploadedVoice.state.name == 'ACTIVE':
        time.sleep(1)
        print(UploadedVoice.state.name)
        if UploadedVoice.state.name == 'FAILED':
            return "Error: Failed to upload the voice message."

    # generate the content
    response = model.generate_content(
        [summarizeText, UploadedVoice], stream=True,
        # block none
        safety_settings=safety_setting)

    # get the response
    return response


def speech_to_text(voicepath: str):
    """
    Converts a voice message to text using a pre-trained model.

    Args:
        voicepath (str): The path to the voice message file.

    Returns:
        str: The generated text content.

    Raises:
        Exception: If there is an error uploading the voice message.

    """
    # upload the voice message
    UploadedVoice = genai.upload_file(voicepath)
    # verfiy the voice message is uploaded
    while not UploadedVoice.state.name == 'ACTIVE':
        time.sleep(1)
        print(UploadedVoice.state.name)
        if UploadedVoice.state.name == 'FAILED':
            return "Error: Failed to upload the voice message."
    # generate the content
    response = model.generate_content(
        [extraxtText, UploadedVoice], stream=True,
        # block none
        safety_settings=safety_setting)

    # get the response
    return response


def cut_silence(file):
    """
    This function is used to crop the silence from the voice message.

    Args:
        file (str): The path of the voice message.

    Returns:
        file (str): The path of the cropped voice message.
        length (int): The length of the cropped voice message.

    """
    data, sampling_rate = librosa.load(file)
    less_data = [max(data[i:i+int(sampling_rate/4)])
                 for i in range(0, len(data), int(sampling_rate/4))]
    SD = std(less_data)

    step = int(sampling_rate/4)

    new_data = []
    for i in range(0, len(data), step):
        if max(abs(data[i:i+step])) < SD-0.1:
            new_data.append(data[i:i+step:7])
        else:
            new_data.append(data[i:i+step])

    new_data = concatenate(new_data)
    new_file = file.split(".")[0] + "_cropped.wav"

    sf_write(new_file, new_data, sampling_rate)

    return new_file, int(len(new_data)/sampling_rate)


def print_models():
    """
    Prints the names of models that support content generation.

    This function iterates over the models returned by `genai.list_models()` and prints the name of each model
    that supports the 'generateContent' generation method.

    """
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(m.name)


if __name__ == "__main__":
    """
    This script is used to test the helper functions.

    """
    # print_models()
    print(summarize("voice.ogg"))
