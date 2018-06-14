import dialogflow
import os

def detect_intent_texts(project_id, session_id, texts, language_code):
    """Returns the result of detect intent with texts as inputs.
    Using the same `session_id` between requests allows to continue
    into the conversaion."""
    ruta = "../DATA/TransferenciaAutomatica2-9c525654a2fb_admin.json"
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = ruta
    session_client = dialogflow.SessionsClient() # Implícita

    # print(dir(session_client))

    session = session_client.session_path(project_id, session_id)
    print('Session path: {}\n'.format(session))
    for text in texts:
        text_input = dialogflow.types.TextInput(
            text=text, language_code=language_code)

        query_input = dialogflow.types.QueryInput(text=text_input)

        response = session_client.detect_intent(
            session=session, query_input=query_input)

        print('=' * 20)
        print('Query text: {}'.format(response.query_result.query_text))
        print('Detected intent: {} (confidence: {})\n'.format(
            response.query_result.intent.display_name,
            response.query_result.intent_detection_confidence))
        print('Fulfillment text: {}\n'.format(
            response.query_result.fulfillment_text))

if __name__ == "__main__":
    detect_intent_texts("transferenciaautomatica2", "089ca6d2-c6dc-9772-861b-ab98ba0ab24f",
                        ["quiero hablar con Javier", "Javier Escalante"], "es")
