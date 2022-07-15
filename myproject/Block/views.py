from typing import final
from django.shortcuts import render,redirect
from Block.models import *
from django.http import HttpResponse, HttpResponseRedirect
# Create your views here.

def demo(request):
    block_data = BlockTranslation.objects.raw("select * from block_block as b inner join block_blocktranslation as bt on b.blockid = bt.block_id where b.status = 'Enabled'")
    for bd in block_data:
        title = bd.title
        content = bd.content
    
    block = Block.objects.all()
    for b in block:
        blockt = BlockTranslation.objects.filter(block = b.blockid)
        for bt in blockt:
            print(bt)
    return render(request, 'demo.html',{"content":content,"title":title,"block":block,"blockt":blockt})