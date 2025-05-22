import json, time, requests, pyttsx3, pyaudio, vosk


class Speech:
    def __init__(self):
        self.tts = pyttsx3.init()

    def set_voice(self, speaker):
        self.voices = self.tts.getProperty("voices")
        for voice in self.voices:
            if "ru" in voice.languages:
                self.tts.setProperty("voice", voice.id)
                break
        return id

    def text2voice(self, speaker=0, text="Готов"):
        self.tts.setProperty("voice", self.set_voice(speaker))
        self.tts.say(text)
        self.tts.runAndWait()


class Recognize:
    def __init__(self, path)
        model = vosk.Model('C:/Users/User/PycharmProjects/Lab-10/vosk-model-small-ru-0.22')
        self.record = vosk.KaldiRecognizer(model, 16000)
        self.stream()

    def stream(self):
        pa = pyaudio.PyAudio()
        self.stream = pa.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=16000,
            input=True,
            frames_per_buffer=8000,
        )

    def listen(self):
        while True:
            data = self.stream.read(4000, exception_on_overflow=False)
            if self.record.AcceptWaveform(data) and len(data) > 0:
                answer = json.loads(self.record.Result())
                if answer["text"]:
                    yield answer["text"]


def get_fact():
    try:
        response = requests.get("http://numbersapi.com/random/math")
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        return f"Ошибка запроса: {e}"


def write_fact(fact):
    with open("facts.txt", "a") as file:
        file.write(fact + "\n")


def delete_fact():
    try:
        with open("facts.txt", "r") as file:
            lines = file.readlines()
        if lines:
            with open("facts.txt", "w") as file:
                file.writelines(lines[:-1])
            return "Последний факт удалён."
        else:
            return "Файл пуст. Нечего удалять."
    except Exception as e:
        return f"Ошибка: {e}"


def speak(text):
    speech = Speech()
    speech.text2voice(speaker=1, text=text)


if __name__ == "__main__":
    rec = Recognize("C:/Users/User/PycharmProjects/Lab-10/vosk-model-small-ru-0.22")
    text_gen = rec.listen()
    rec.stream.stop_stream()
    speak(
        "Голосовой ассистент активирован. Команды: факт, следующий, прочитать, записать, удалить, прощаюсь"
    )
    time.sleep(0.5)
    rec.stream.start_stream()

    for text in text_gen:
        print(f"Распознано: {text}")

        if "прощаюсь" in text:
            speak("До скорых встреч!")
            quit()

        elif "факт" in text:
            fact = get_fact()
            speak(f"Ваш факт: {fact}")

        elif "следующий" in text:
            fact = get_fact()
            speak(f"Ваш новый факт: {fact}")

        elif "прочитать" in text:
            try:
                with open("facts.txt", "r") as file:
                    last_fact = file.readlines()[-1]
                speak(f"Ваш последний факт: {last_fact.strip()}")
            except IndexError:
                speak("Факт отсутствует. Сначала получите факт.")

        elif "записать" in text:
            if fact:
                write_fact(fact)
                speak("Факт записан.")
            else:
                speak("Факта нет, ничего не записано.")

        elif "удалить" in text:
            result = delete_fact()
            speak(result)
        else:
            speak("Команда не распознана. Пожалуйста, попробуйте снова.")