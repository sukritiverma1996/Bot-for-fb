from django.shortcuts import render
from django.http import HttpResponse

from django.views import generic
from django.http.response import HttpResponse

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

quotes_string = '''
There is no charge for awesomeness... or attractiveness.;Kung Fu Panda;http://www.google.co.in/search?ie=UTF-8&q=kung+fu+panda+awesomeness
Any fool can write code that a computer can understand. Good programmers write code that humans can understand.;Martin Fowle;http://thc.org/root/phun/unmaintain.html
He was so deadly, in fact, that his enemies would go blind from over-exposure to pure awesomeness!;Kung Fu Panda;
One often meets his destiny on the road he takes to avoid it.;Kung Fu Panda;
The world is moved along, not only by the mighty shoves of its heroes, but also by the aggregate of the tiny pushes of each honest worker.;Helen Keller;
'''

quotes_arr = quotes_string.split('\n')

PAGE_ACCESS_TOKEN ='EAATD9Q2WbQgBAMyb3chgCdZAokOx0Wn4iV3mgPQoN4uLF7CwYJg2HfNHNUyhvpQKNf0r6kQClgL2NRnPPAxl5db1n6ZBeZA1FyZBcks5zGUDaVZBlDQsasTZBKV1it9sOB3t2xxbtODr3mPNuAIAdsmltk3WdAg87Y1TC0AK5H5AZDZD'

def post_facebook_message(fbid, recevied_message):
    # Remove all punctuations, lower case the text and split it based on space
    #clean_message = re.sub(r"[^a-zA-Z0-9\s]",' ',recevied_message)

    reply_text = ''
    

    if not reply_text:
        reply_text = recevied_message

    user_details_url = "https://graph.facebook.com/v2.6/%s"%fbid 
    user_details_params = {'fields':'first_name,last_name,profile_pic', 'access_token':PAGE_ACCESS_TOKEN} 
    user_details = requests.get(user_details_url, user_details_params).json() 
    joke_text = 'Yo '+user_details['first_name']+'..! ' + reply_text
                   
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s'%PAGE_ACCESS_TOKEN
    response_msg = json.dumps({"recipient":{"id":fbid}, "message":{"text":joke_text}})
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)
    pprint(status.json())

# Create your views here.

class MyQuoteBotView(generic.View):
    def get(self, request, *args, **kwargs):
        try:
            # that number is your webhook token which youll set up in a bit
            if self.request.GET['hub.verify_token'] == '8447789934':
                return HttpResponse(self.request.GET['hub.challenge'])
            else:
                return HttpResponse('Error, invalid token')
        except:
            return HttpResponse('Error, invalid token')

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return generic.View.dispatch(self, request, *args, **kwargs)

    # Post function to handle Facebook messages
    def post(self, request, *args, **kwargs):
        # Converts the text payload into a python dictionary
        incoming_message = json.loads(self.request.body.decode('utf-8'))
        # Facebook recommends going through every entry since they might send
        # multiple messages in a single call during high load
        for entry in incoming_message['entry']:
            for message in entry['messaging']:
                # Check to make sure the received call is a message call
                # This might be delivery, optin, postback for other events 
                if 'message' in message:
                    # Print the message to the terminal
                    pprint(message)    
                    # Assuming the sender only sends text. Non-text messages like stickers, audio, pictures
                    # are sent as attachments and must be handled accordingly. 
                    post_facebook_message(message['sender']['id'], message['message']['text'])    
        return HttpResponse()    



# Create your views here.

def hello_world(request):
    return HttpResponse("<b><i>Hello World</i></b>")

def hello(request):
    return HttpResponse("Hey Hey!")