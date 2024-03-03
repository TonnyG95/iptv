from .models import PostavkePlatforme

class PostavkeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        postavke = PostavkePlatforme.objects.first()
        linkovi = postavke.linkovi.all() if postavke else []
        drustvene_mreze = postavke.drustvene_mreze.all() if postavke else []
        white_logo = postavke.white_logo.url if postavke and postavke.white_logo else None

        request.postavke = postavke
        request.linkovi = linkovi
        request.drustvene_mreze = drustvene_mreze
        request.white_logo = white_logo

        response = self.get_response(request)
        return response
