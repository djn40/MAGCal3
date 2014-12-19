import os, re, types


PAGES = {
	"Splash": {
						'TITLE' : "Introducing the SoundPost from Povidi", 'TEMPLATE': "fptemp.html", 'NEXT': "Slide1", 'PREV': "Splash", 'HOME':"Splash", 'OUTDIR': "./",  'CHUNKDIR':"", 'CONDIR': ""}
	}



Defaults = { 'TEMPLATE': 'template.html', 'CHUNKDIR': './',  'OUTDIR': './site/', 'CONDIR': './'
}
# Module also uses OUTFNAME which cannot have a default and is the override for saving.



#fTag = re.compile ( "%TAG_DMS.*?%" )
#fTag = re.compile ( "(%TAG_DMS_.*?%|%dz_.*?%)")
fTag = re.compile ( "(%TAG_DMS_.*?%|%dz_.*?%)")

gblCondCnt = 0
gblInCondCnt = 0
SubContentDicElement = "__subdic__"


def GetNav(  nav, dic):
	i=dic[nav]
	if i.find('.') < 0:
		i+='.html'
	return i

def GetNextPage ( arg2, dic ):
	return GetNav( 'NEXT', dic )

def GetPrevPage( arg2, dic ):
	return GetNav( 'PREV', dic )

def GetHomePage ( arg2,  dic ):
	return GetNav( 'HOME', dic )

def GetInclude ( arg2, dic ):
	if gblCondCnt != gblInCondCnt:
		return ""
	if arg2.find(".") < 0:
		arg2 += '.unk'
	ChunkDir = dic.setdefault('CHUNKDIR', Defaults['CHUNKDIR'] )
	return open( ChunkDir + arg2 ).read ()

def GetMainContent( arg2, dic ):
	if gblCondCnt != gblInCondCnt:
		return ""
	MainContentDir = dic.setdefault('CONDIR', Defaults['CONDIR'])
	return open( MainContentDir + dic['CONNAME'] ).read()


def GetTitle ( arg2, dic ):
	return dic.setdefault( 'TITLE', '' )


def DeriveDicAndEle( arg2, dic):
	if dic.has_key(SubContentDicElement):
		d = dic[SubContentDicElement].split(".")
		for sd in d:
			dic = dic[sd]
	if ('.' in arg2) == False:
		return (arg2, dic)
	else:
		es = arg2.split('.')
		cd = dic
		for x in range(0, len(es)-1):
			cd = cd[es[x]]
		return (es[-1], cd)



def GetFieldValue ( arg2, dic ):
	try:
		a = DeriveDicAndEle( arg2, dic )
		if a[1].has_key(a[0]) == False:
			return ""
		if isinstance( a[1][ a[0] ], types.FunctionType ):
			return str( a[1][ a[0] ]( arg2 ) )  #Still need thoughts on argument pass
		else:
			return str( a[1][ a[0] ] )
	except:
		return ""
def UnSetFieldValue( arg2, dic ):
	fld = DeriveDicAndEle(arg2, dic)
	if fld[1].has_key(fld[0]):
		del fld[1][fld[0]]
	return ""


def SetFieldValue( arg2, dic ):
	"""Still a design call to check if field exists before replace. """
	parms=arg2.split(",")
	fld = DeriveDicAndEle( parms[0], dic )
	if fld[1].has_key(fld[0]) == False:
		fld[1][fld[0]] = ",".join(parms[1:]).replace("&pct", "%")

	return ""	

def DecField( arg2, dic ):
	fld = DeriveDicAndEle( arg2, dic )
	fld[1][ fld[0] ] = int(fld[1][ fld[0] ]) - 1

	return ""

def IncField( arg2, dic ):
	fld = DeriveDicAndEle( arg2, dic )
	fld[1][ fld[0] ] = str(int(fld[1][ fld[0] ])+1)


def GetCallbackData ( arg2, dic ):
	if gblCondCnt != gblInCondCnt:
		return ""
	try:
		fld = DerviveDataAndEle( arg2, dic)
		return str( fld[1][fld[0]]( dic ) )
	except:
		return ""

def _DoMulti(render_str, listdic):
	ret = ""
	for Entry in listdic:
		ret += RenderText(  render_str, Entry)
	return ret



def GetIncludeMulti( arg2, dic ):
	ChunkDir = dic.setdefault('CHUNKDIR', Defaults['CHUNKDIR'] )
	if gblCondCnt != gblInCondCnt:
		return ""
	params = arg2.split(",")
	html_data = open( ChunkDir + params[0]).read()
	fld = DeriveDicAndEle( params[1], dic )
	return _DoMulti(html_data, fld[1][fld[0]])

def GetMultiHash( arg2, dic ):
	ChunkDir = dic.setdefault( 'CHUNKDIR', Defaults['CHUNKDIR'] )
	if gblCondCnt != gblInCondCnt:
		return ""
	params = arg2.split(",")
	rend_str = DeriveDicAndEle( params[0], dic )
	rend_data = DeriveDicAndEle( params[1], dic )
	return _DoMulti( rend_str[1][rend_str[0]], rend_data[1][rend_data[0]] )

def GetRepeat(arg2, dic):
	""" first part of arg2 is the hash unlike other calls due to potential length of rendering str
	"""
	if gblCondCnt != gblInCondCnt:
		return ""
	params = arg2.split(",")
	rend_data = DeriveDicAndele( params[0], dic )
	return DoMulti( ",".join(params[1:]), rend_data[1][rend_data[0]] )

def IfHash( arg2, dic ):
	global gblCondCnt
	global gblInCondCnt
	gblCondCnt += 1
	fld = DeriveDicAndEle( arg2, dic )
	if fld[1].has_key( fld[0] ):
		gblInCondCnt += 1
	return ""

def IfNotHash( arg2, dic ):
	global gblCondCnt
	global gblInCondCnt
	gblCondCnt += 1
	fld = DeriveDicAndEle( arg2, dic )
	if fld[1].has_key( fld[0] ) == False:
		gblInCondCnt += 1
	return ""


def IfHashEq( arg2, dic ):
	global gblInCondCnt
	global gblCondCnt

	vals = arg2.split(",")
	ret_str=RenderText( ",".join( vals[1:]), dic )
	gblCondCnt += 1
	fld = DeriveDicAndEle( vals[0], dic )
	if fld[1].has_key( fld[0] ):
		if str(fld[1][ fld[0] ]) == ret_str:
			gblInCondCnt += 1
	return ""


def EndIf( arg2, dic ):
	global gblCondCnt
	global gblInCondCnt
	#print "EndIf : %s:%s" % (gblCondCnt, gblInCondCnt )
	if gblInCondCnt == gblCondCnt:
		gblInCondCnt -= 1
	gblCondCnt -= 1
	if gblInCondCnt < 0:
		raise Exception("malformed conditional in template whilst rendering")
	if gblCondCnt < 0:
		raise Exception("malformed conditional in template whilst rendering")
	return ""
def SetSubDic( arg2, dic):
	if dic.has_key(SubContentDicElement ) == False:
		dic[SubContentDicElement ] = arg2
	return ""

def UnSetSubDic(arg2, dic):
	del dic[SubContentDicElement]
	return ""

def DebugPrintDic( arg2, dic):
	return "%s : %s" % (arg2, str(dic) )

def DebugPrintIfState(arg2, dic):
	return "InCnt : %s Cnt : %s" % (gblInCondCnt, gblCondCnt)

tag_actions = {
	"TAG_DMS_INCLUDE" : GetInclude,
	"dz_inc" : GetInclude,
	"TAG_DMS_SUB_MAIN_CONTENT" : GetMainContent,
	"dz_mc" : GetMainContent,
	"TAG_DMS_SB_META_TITLE" : GetTitle,
	"TAG_DMS_NAV_NEXT": GetNextPage,
	"TAG_DMS_NAV_PREV": GetPrevPage,
	"TAG_DMS_NAV_HOME": GetHomePage,
	"TAG_DMS_GET_FIELD" : GetFieldValue,
	"dz_gfv" : GetFieldValue,
	"TAG_DMS_CALLBACK" : GetCallbackData,
	"dz_callb" : GetCallbackData,
	"TAG_DMS_INCLUDEMULTI" : GetIncludeMulti,
	"dz_imult" : GetIncludeMulti,
	"dz_multi" : GetMultiHash,
	"dz_repeat" : GetRepeat,
	"dz_if" : IfHash,
	"dz_nif" : IfNotHash,
	"dz_ifeq" : IfHashEq,
	"dz_endif" : EndIf,
	"dz_sfv" : SetFieldValue,
	"dz_unsfv" : UnSetFieldValue,
	"dz_--" : DecField,
	"dz_++" : IncField,
	"dz_subdic": SetSubDic,
	"dz_unsubdic": UnSetSubDic,
	"dz_printdic": DebugPrintDic,
	'dz_globalifstate': DebugPrintIfState
	}



#==========
def RenderText (pagedata, pagedic ):
	""" creates html string based on dic template etc. Function does NO setup of directories for chunk data, content etc. This needs to be setup prior to call
	Reason: speed hit due to recursive nature of routine and also to allow setup file directories to be within templates and chunks and not reliant on globals.
	"""
	if pagedata == "" or pagedata == None:
		return ""
	Tags = fTag.findall ( pagedata )
	lData = fTag.split ( pagedata )	
	ToRemove = []
	for x in range(0, len(lData)-1):
		if lData[x] in Tags:
			ToRemove.append(x)
		ToRemove.reverse()
	for x in ToRemove:
		del lData[x]
	out = ""
	for seg in range (0, len(lData)):
		if gblCondCnt == gblInCondCnt:
			out += lData[seg]
		if seg < len(Tags): 
			if Tags[seg].find('=' ) == -1: 
				cTag = Tags[seg][1:-1]
				arg2 = None
			else:
				
				tmp = (Tags[seg][1:-1]).split('=')
				cTag=tmp[0]
				arg2 = "=".join(tmp[1:])
			act =  tag_actions[cTag](arg2, pagedic) 
			if gblCondCnt == gblInCondCnt:
				out += RenderText (act, pagedic)
	if gblCondCnt == 0 and gblInCondCnt > 0:
		raise Exception("malformed conditional in template whilst rendering")	
	return out

def DoPage ( pagename, pagedata, dic=PAGES ):
	dic[pagename].setdefault('CONNAME', pagename+'.con' )
	return RenderText(pagedata, dic[pagename])


def DoSinglePage( PageDic, cPage, SaveAsHTML = True):
	ChunkDir = PageDic[cPage].setdefault( 'CHUNKDIR', Defaults['CHUNKDIR'] )
	MainContentDir = PageDic[cPage].setdefault( 'CONDIR', Defaults['CONDIR'] )
	OutputDir = PageDic[cPage].setdefault( 'OUTDIR', Defaults['OUTDIR'] )
	Template = PageDic[cPage].setdefault( 'TEMPLATE', Defaults['TEMPLATE'] )

	data  = open( ChunkDir+PageDic[cPage]['TEMPLATE'] ).read ()
	data = DoPage( cPage, data, PageDic )
	if SaveAsHTML == True:
		if len(cPage.split(".")) < 2:
			sPage=cPage+".html"
		else:
			sPage = cPage
		sPage = PageDic[cPage].setdefault( 'OUTFNAME', sPage )
		open (OutputDir+sPage,"wt").write(data)
	else:
		return data

def RenderDic( dic, Save=False ):
	""" dic must have minimum of TEMPLATE argument in order to find initial text data
	Also ensure directories are setup correctly, CHUNKDIR etc. CONNAME shoud exist as well if including main content
	"""
	foo = {}
	foo['bar']=dic
	return DoSinglePage(foo, 'bar', Save)


def DoAllPages ( pgs = None):
	global PAGES
	if pgs != None:
		PAGES=pgs
	for cPage in PAGES:
		#print cPage + "..."
		data = DoSinglePage (  PAGES, cPage)




if __name__ == '__main__':

	#DoAllPages ()
	#print "hello"
	a= {'zzz' : "world", 'if_test': True}
	b = "hello, %dz_sfv=dta,&pct_gfv=zzz&pct.% End"
	test = "dz_gfv=zzz% %dz_if=zzz%World\n %dz_nif=zzz%Again%dz_endif% "
	print RenderText(test, a)
