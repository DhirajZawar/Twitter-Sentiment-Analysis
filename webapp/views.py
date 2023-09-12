from django.shortcuts import render, redirect
from django.contrib import messages

from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from webapp.tweet import fetch_tweets_for_query, save_query_and_result
from webapp.models import SearchQuery, SearchResult

import matplotlib.pyplot as plt
import io, urllib, base64


# Create your views here.

@login_required
def Home(request):
	query = request.GET.get('query', '')
	tweet_list = []
	uri = ""

	if query:
		if not SearchQuery.objects.filter(user = request.user.id, query = query).exists():
			tweets = fetch_tweets_for_query(query)
			if tweets:
				tweet_list = save_query_and_result(request.user.id, query, tweets)
			else:
				messages.warning(request, 'Tweet result not found for query search %s' % query )
		else:
			tweet_list = SearchResult.objects.filter(query_id__user = request.user.id, query_id__query = query)

		if tweet_list:
			positive = 0
			netural = 0
			negative = 0
			for i in tweet_list:
				positive += 1 if float(i.polarity) > 0 else 0
				netural += 1 if float(i.polarity) == 0 else 0
				negative += 1 if float(i.polarity) < 0 else 0

			labels=['Positive Tweets','Neutral Tweets','Negative Tweets']
			colors=['green','blue','red']
			exp=(0.07,0,0)
			result = [positive, netural, negative]

			plt.pie(result,colors=colors,labels=labels,shadow=True,explode=exp,autopct='%1.1f%%')
			plt.title('Sentiment Analysis')
			figure = plt.gcf()

			buff = io.BytesIO()
			figure.savefig(buff, format="png")
			buff.seek(0)
			string = base64.b64encode(buff.read())
			uri = urllib.parse.quote(string)

	recent_search = SearchQuery.objects.filter(user = request.user.id)
	return render(request, "webapp/index.html", {'recent_search': recent_search, 'tweets': tweet_list, 'uri':uri})


def Signup(request):

	if request.user.is_authenticated:
		return redirect('webapp:home')

	if request.method == 'POST':
		form = UserCreationForm(request.POST)

		if form.is_valid():
			form.save()
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			user = authenticate(username = username,password = password)
			login(request, user)
			return redirect('webapp:home')

		else:
			return render(request,'webapp/registration.html',{'form':form})

	else:
		form = UserCreationForm()
		return render(request,'webapp/registration.html',{'form':form})



def Signin(request):
    if request.user.is_authenticated:
        return redirect('/')
     
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username = username, password = password)
 
        if user is not None:
            login(request,user)
            return redirect('webapp:home')
        else:
        	messages.warning(request, "Incorrect username or password")
        	return render(request,'webapp/login.html')
    else:
        return render(request, 'webapp/login.html')


@login_required
def Signout(request):
    logout(request)
    return redirect('webapp:signin')