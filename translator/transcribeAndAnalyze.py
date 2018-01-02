def transcribe_and_analyze():

    import io
    import os

    from google.cloud import speech
    from google.cloud.speech import enums
    from google.cloud.speech import types

    client = speech.SpeechClient()

    file_name = os.path.join(
        os.path.dirname(__file__),
        'resources',
        'verymuch.flac')

    with io.open(file_name, 'rb') as audio_file:
        content = audio_file.read()
        audio = types.RecognitionAudio(content=content)

    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.FLAC,
        sample_rate_hertz=44100,
        language_code='en-US',
        profanity_filter=False)
    print('--- SPEECH TO TEXT ---')
    print('transcription started')
    print('...')

    response = client.recognize(config, audio)

    best_result=''

    for result in response.results:
        print('Confidence: {}'.format(result.alternatives[0].confidence))
        print('Transcript: {}'.format(result.alternatives[0].transcript))
        best_result = result.alternatives[0].transcript

    if (best_result!=''):
        from google.cloud import language
        from google.cloud.language import enums
        from google.cloud.language import types

        client = language.LanguageServiceClient()

        print('\n--- TEXT TO SENTIMENT ---')
        print('starting sentiment analysis on: {}'.format(best_result))

        document = types.Document(
            content=best_result,
            type=enums.Document.Type.PLAIN_TEXT)

        print('...')

        annotations = client.analyze_sentiment(document=document)

        print_result(annotations)
    else:
        print('Empty transpcription')


def print_result(annotations):
    score = annotations.document_sentiment.score
    magnitude = annotations.document_sentiment.magnitude

    for index, sentence in enumerate(annotations.sentences):
        sentence_sentiment = sentence.sentiment.score

    print('Overall Sentiment: score of {} with magnitude of {}'.format(
        score, magnitude))
    evaluate(score)
    return 0

def evaluate(score):
    print('\nFinal evaluation: ')

    if (score<-0.5):
        print('clearly negative sentiment')
    elif (score<-0.25):
        print('negative sentiment')
    elif (score<-0.1):
        print('somewhat negative sentiment')
    elif (score>0.1):
        print('somewhat positive sentiment')
    elif (score>0.25):
        print('positive sentiment')
    elif (score>0.5):
        print('clearly positive sentiment')
    else :
        print('mixed or neutral sentiment, not clearly defined')



if __name__ == '__main__':
    transcribe_and_analyze()