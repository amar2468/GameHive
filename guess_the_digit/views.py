from django.shortcuts import render

# Create your views here.

def check_if_works(request):
    if request.method == "POST":

        user_guess = int(request.POST.get('guess_number_input_field', ''))

        context = {
            'result': 'You guessed ' + str(user_guess) + '! Congratulations!'
        }

        return render(request, 'home.html', context)
    return render(request, 'home.html')