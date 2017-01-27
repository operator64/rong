from django.shortcuts import get_object_or_404, render
from django.template import loader
from .models import Node, Trait, NodeTrait
# Create your views here.

def home(request):
    return render(request, 'core/home.html')

def entry_full(request):
	entrytraits = {}
	entry = get_object_or_404(Node, pk=1)
	for nt in entry.nodetrait_set.all():
		entrytraits[nt.trait.name]=nt.value
	
	print(entrytraits)

	#print(entry.nodetrait_set.all().__dict__)
	#template = loader.get_template('core/entry_full.html')
	return render(request, 'core/entry_full.html', {'entry': entry, 'traits':entrytraits})
#filter(node=entry)