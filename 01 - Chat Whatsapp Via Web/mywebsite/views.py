from django.shortcuts import render
from django.http import HttpResponseRedirect

def index(request):
    no = ''
    text = ''
    context = {
        'page_title': 'Home',
        'heading': 'Chat Whatsapp Via Web',
    }

    if request.method == 'POST':
        no = request.POST['noWhatsapp']
        text = request.POST['textInput']
        if no[:2] == '08':
            no = no.replace(no[:2], '628')
        elif no[:3] == '628':
            no = no

        # untuk membagi kata menjadi list
        text = text.split('\n')
        lol = []
        for perKata in text:
            if '\r' in perKata:  # scan for new line
                perKata = perKata.replace('\r', '%0A')

            if ' ' in perKata:  # scan for space
                perKata = perKata.replace(' ', '%20')
            lol.append(perKata)

        text = ''.join(lol)

        url = 'https://web.whatsapp.com/send?phone={}&text={}'.format(no, text)
        return HttpResponseRedirect(url)

    return render(request, 'index.html', context)

