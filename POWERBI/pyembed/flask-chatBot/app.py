from flask import Flask, render_template, request,g,session
import time
app = Flask(__name__)
app.secret_key = 'nttdata'
import json
import watson_developer_cloud
import numpy
import requests

def setAccessToken():
    url = "https://login.windows.net/common/oauth2/token"

    payload = "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"client_id\"\r\n\r\n3a6d2d72-2e5e-4ff1-890d-ade62db70010\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"grant_type\"\r\n\r\npassword\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"resource\"\r\n\r\nhttps://analysis.windows.net/powerbi/api\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"username\"\r\n\r\npramod@thoughtpro.in\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"password\"\r\n\r\npramK@1234\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW--"
    headers = {
        'content-type': "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW",
        'Cache-Control': "no-cache"
    }

    response = requests.request("POST", url, data=payload, headers=headers)
    accessToken = response.json()
    print(accessToken)
    session['access_token'] = accessToken

@app.route("/")
def home():

    session['context'] = {}
    if 'access_token' not in session:
        setAccessToken()
    return render_template("embed.html")

def call_ibm_conversation(workspace_id,userText,conversation):
    # Send message to Conversation service.
    if session['context'] == {}:
        response = conversation.message(
            workspace_id=workspace_id,
            input={
                'text': ''
            }
        )
    else:
        response = conversation.message(
            workspace_id=workspace_id,
            input={
                'text': userText
            },
            context=session['context'],

        )
    session['context'] = response['context']
    print(response['output'])
    return  str(' '.join(response["output"]["text"])),response['intents']

@app.route("/get")
def get_bot_response():

    workspace_id = 'de96a2cc-177a-4b4f-93f1-7a2e78c6b2aa'  # replace with workspace ID
    # conversation = g.get('conversation', None)
    # Set up Conversation service.
    conversation = watson_developer_cloud.ConversationV1(
        username = '79e0d876-7420-429c-b6f4-fb263288b72b',
        password = 'OFKT46d8fFvT',
        version = '2018-02-16'
    )
    userText = request.args.get('msg')
    responseText, intents = call_ibm_conversation(workspace_id,userText,conversation)
    if intents != []:
        intent = intents[0]['intent']
        if 'vaccination' == intent:
            # User text is defaulted to get reply from IBM
            # responseText,intents = call_ibm_conversation(workspace_id, 'vaccination', conversation)
            responseText += '<div class="message-inner"> Here are some resources that might help you:'
            # Call the discovery service to get the data and links
            discovery = watson_developer_cloud.DiscoveryV1(
                username="7f6617a2-d1c0-49a6-84e6-aae810b370bf",
                password="UeXUAzNZGuYX",
                version="2017-11-07"

            )

            collection_id = '85d3782c-e6b5-46c9-af06-f0c2682bcb9e'
            configuration_id = 'd3f5662a-8dfb-4b37-9367-f9f182370f5a'
            environment_id = 'aa7e356e-31c5-4eb6-8c6b-ed0966b936d5'

            my_query = discovery.query(environment_id=environment_id, collection_id=collection_id, query='vaccination')
            for row in my_query['results']:
                responseText += '<br /><a href="'+row['sourceUrl']+'">'+row['title']+'</a>'

            return responseText + "</div>"
    return responseText

@app.route("/getReportEmbedToken")
def getReportEmbedToken():
    if int(session['access_token']['expires_on']) < time.time():
        setAccessToken()
    url = "https://api.powerbi.com/v1.0/myorg/groups/8c388e98-8950-46aa-9c7f-050724aa7f86/reports/32082fb2-3442-4b45-9073-df49ee34de49/GenerateToken"
    payload = "accessLevel=View&allowSaveAs=false"
    headers = {
        'Content-Type': "application/x-www-form-urlencoded",
        'Accept': "application/json",
        'charset': "utf-8",
        'Authorization': "Bearer %s" % (session['access_token']['access_token']),
        'Cache-Control': "no-cache"
    }
    response = requests.request("POST", url, data=payload, headers=headers)
    embedToken = response.json()
    print(embedToken['token'])
    return embedToken['token']

@app.route("/getDashboardEmbedToken")
def getDashboardEmbedToken():
    if int(session['access_token']['expires_on']) < time.time():
        setAccessToken()
    url = "https://api.powerbi.com/v1.0/myorg/groups/8c388e98-8950-46aa-9c7f-050724aa7f86/dashboards/6b20a481-c2c1-43a6-93a4-6f695daceb92/GenerateToken"

    payload = "accessLevel=View&allowSaveAs=false"
    headers = {
        'Content-Type': "application/x-www-form-urlencoded",
        'Accept': "application/json",
        'charset': "utf-8",
        'Authorization': "Bearer %s" % (session['access_token']['access_token']),
        'Cache-Control': "no-cache"
    }

    response = requests.request("POST", url, data=payload, headers=headers)
    embedToken = response.json()
    print(embedToken['token'])
    return embedToken['token']

@app.route("/getQna")
def getQna():
    if int(session['access_token']['expires_on']) < time.time():
        setAccessToken()

    url = "https://api.powerbi.com/v1.0/myorg/groups/8c388e98-8950-46aa-9c7f-050724aa7f86/datasets/45a8d542-54d3-4b4c-9e75-b3a2c167deff/GenerateToken"

    payload = "accessLevel=View&allowSaveAs=false"
    headers = {
        'Content-Type': "application/x-www-form-urlencoded",
        'Accept': "application/json",
        'charset': "utf-8",
        'Authorization': "Bearer %s" % (session['access_token']['access_token']),
        'Cache-Control': "no-cache"
    }
    response = requests.request("POST", url, data=payload, headers=headers)
    embedToken = response.json()
    print(embedToken['token'])
    return embedToken['token']
if __name__ == "__main__":
    app.run()