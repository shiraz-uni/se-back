

# Create your views here.
def test(request):
	#return HttpResponse(len(request.read()))
	#return JsonResponse({'foo': 'bar'})
	#return HttpResponse(request.META['HTTP_USER_AGENT'])
	#return HttpResponse(request.META['REMOTE_ADDR']) # for getting the ip
	if request.method == 'POST':
		return HttpResponse('Your Ip is ' + request.META['REMOTE_ADDR'] + ' and Your post body is ' + request.read())
	return HttpResponse('Your Ip is ' + request.META['REMOTE_ADDR'] + '''

<head>
<style> 
div {
  width: 100px;
  height: 100px;
  background-color: red;
  position: relative;
  -webkit-animation-name: example; /* Safari 4.0 - 8.0 */
  -webkit-animation-duration: 4s; /* Safari 4.0 - 8.0 */
  animation-name: example;
  animation-duration: 1s;
  animation-iteration-count: 10000;
}

/* Safari 4.0 - 8.0 */
@-webkit-keyframes example {
  0%   {background-color:red; left:0px; top:0px;}
  25%  {background-color:yellow; left:200px; top:0px;}
  50%  {background-color:blue; left:200px; top:200px;}
  75%  {background-color:green; left:0px; top:200px;}
  100% {background-color:red; left:0px; top:0px;}
}

/* Standard syntax */
@keyframes example {
  0%   {background-color:red; left:0px; top:0px;}
  25%  {background-color:yellow; left:200px; top:0px;}
  50%  {background-color:blue; left:200px; top:200px;}
  75%  {background-color:green; left:0px; top:200px;}
  100% {background-color:red; left:0px; top:0px;}
}
</style>
</head>
<body>

<p><b>Note:</b> This example does not work in Internet Explorer 9 and earlier versions.</p>

<div></div>

</body>


		''')