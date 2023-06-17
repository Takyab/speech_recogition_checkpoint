# This is a sample Python script.


# Press Maj+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


async def transcribe_speech(api, language, paused):
    # Initialize recognizer class
    r = sr.Recognizer()
    # Initialize microphone source
    mic = sr.Microphone()

    # Initialize the Deepgram client outside the while loop
    dg_client = None
    if api == "deepgram":
        # Initialize the Deepgram client here or use your existing initialization code
        dg_client = Deepgram('1ed922757401dbb61ea9900d64ee4c4136a6ee54')

    # Read input from microphone
    async def read_audio():
        with mic as source:
            audio_text = r.listen(source)
        return audio_text

    while True:
        # Check if the process should be paused
        while paused[0]:
            await asyncio.sleep(0.1)  # Use await inside an async function

        # Read audio input
        audio_text = await read_audio()
        text = ''

        try:
            # Perform speech recognition
            if api == "google":
                text = r.recognize_google(audio_text, language=language)
            elif api == "deepgram":
                audio_data = audio_text.get_wav_data()
                response = await dg_client.transcription.prerecorded({'buffer': audio_data, 'mimetype': 'audio/wav'},
                                                                     {'punctuate': True})

                if 'channel' in response and 'alternatives' in response['channel']:
                    alternatives = response['channel']['alternatives']
                    if alternatives:
                        transcript = alternatives[0].get('transcript')
                        if transcript:
                            text = transcript
                        else:
                            text = "Transcription not available"
                    else:
                        text = "Transcription not available"
                else:
                    text = "Transcription not available"

            return text
        except sr.UnknownValueError:
            return "Sorry, I did not understand what you said."


def save_text_to_file(text):
    file_path = "transcription.txt"  # Define the file path where you want to save the text
    with open(file_path, 'w') as file:
        file.write(text)
    return file_path


async def main():
    st.title("Speech Recognition App")
    st.write("Click on the microphone to start speaking:")

    # add a select box to choose the speech recognition API
    api = st.selectbox("Select API", ("google", "deepgram"))

    # add a select box to choose the language
    language = st.selectbox("Select Language", ("en-US", "es-ES", "fr-FR"))

    text = ""  # Initialize the 'text' variable
    paused = [False]  # Initialize the 'paused' flag as a list

    # add a button to trigger speech recognition
    if st.button("Start Recording"):
        text = await transcribe_speech(api, language, paused)
        st.write("Transcription: ", text)

    # add a button to pause and resume speech recognition
    if st.checkbox("Pause/Resume"):
        paused[0] = not paused[0]
        if paused[0]:
            st.write("Speech recognition paused.")
        else:
            st.write("Speech recognition resumed.")

    # add a button to save the transcribed text
    if text:  # Check if 'text' is not empty
        if st.button("Save Transcription"):
            file_path = save_text_to_file(text)
            st.write(f"Transcription saved to file: {file_path}")


if __name__ == "__main__":
    import streamlit as st
    import speech_recognition as sr
    import asyncio
    from deepgram import Deepgram
    asyncio.run(main())


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
