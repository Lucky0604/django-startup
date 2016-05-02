from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
# Create your views here.
from .models import Question, Choice


''' remove old index, detail, and results views and use Django's generic views instead
def index(request):
    # return HttpResponse("Hello world, You're at the polls index")
    
    # write views that actrully do something
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {
    	'latest_question_list': latest_question_list
    }
    # render() shortcut
    # The render() function takes the request object as its first argument, 
    # a template name as its second argument 
    # and a dictionary as its optional third argument. 
    # It returns an HttpResponse object of the given template 
    # rendered with the given context.
    return render(request, 'polls/index.html', context)

def detail(request, question_id):
	# handle 404

	# try:
	# 	question = Question.objects.get(pk = question_id)
	# except Question.DoesNotExist:
	#	raise Http404('Question does not exist')
	# return render(request, 'polls/detail.html', {'question': question})

    # shortcut : get_object_or_404()
    question = get_object_or_404(Question, pk = question_id)
    return render(request, 'polls/detail.html', {'question': question})

def results(request, question_id):
	question = get_object_or_404(Question, pk = question_id)
	return render(request, 'polls/results.html', {'question': question})
'''

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        # Return the last five published questions
        return Question.objects.order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'



# the same, no changes needed
def vote(request, question_id):
    question = get_object_or_404(Question, pk = question_id)
    # implemention of the vote() real version 
    try:
        selected_choice = question.choice_set.get(pk = request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form
        return render(request, 'polls/detail.html', {
                'question': question,
                'error_message': 'You did not select a choice'
            })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a 
        # user hits the Back button
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))