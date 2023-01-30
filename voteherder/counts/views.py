# Create your views here.

from django.contrib.auth.models import User, Group
from django.views.generic import ListView, DetailView


from .models import Election, Candidate, Stage, StageCell, Ballot


### Entity List Views
class ElectionListView(ListView):
    model = Election
    template_name = "table_view.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Elections"
        return context

class BallotListView(ListView):
    model = Ballot
    template_name = "table_view.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Ballots"
        return context

class CandidateListView(ListView):
    model = Candidate
    template_name = "table_view.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Candidates"
        return context


### Entity Detail Views


class ElectionDetailView(DetailView):
    model = Election
    template_name = "election_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["ballots"] = Ballot.objects.filter(parent=self.object)
        return context

class BallotDetailView(DetailView):
    model = Ballot
    template_name = "ballot_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["stages"] = Stage.objects.filter(ballot=self.object)
        return context


class CandidateDetailView(DetailView):
    model = Candidate
    template_name = "candidate_detail.html"


class StageDetailView(DetailView):
    model = Stage
    template_name = "stage_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["stagecells"] = StageCell.objects.filter(stage=self.object)
        return context
