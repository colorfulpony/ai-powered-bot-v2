import re

class TextCleaner:
    @staticmethod
    def remove_repeating_text(original_text):
        if not original_text:
            raise ValueError("Text argument cannot be empty")

        if not isinstance(original_text, str):
            raise TypeError("Text argument must be a string")

        # Remove newline characters
        original_text = original_text.replace('\n', '')

        # Split the text into sentences
        sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', original_text)
        sentences = [s.strip() for s in sentences]

        # Remove duplicate sentences
        unique_sentences = list(set(sentences))

        # Join the unique sentences into a single string
        unique_text = ". ".join(unique_sentences)

        return unique_text


def clean_text(text):
    cleaned_text = TextCleaner.remove_repeating_text(text)
    return cleaned_text
