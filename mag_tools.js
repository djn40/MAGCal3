function addZero(n){
	n=Math.floor(n);
	if (n<10){
	if (n<0)
		n="-0"+Math.abs(n);
	else
		n="0"+n;}
	return ""+n;}



function selectVal(options,val){
	//alert("called with "+val);
	for  (i=0; i<options.length; i++){
		if (options[i].value==val){
			options[i].selected=true;
			//alert("found "+options[i].selected);
			break;}}}

function setToday(){
var date=new Date();
	month=addZero((date.getMonth()+1));
	day=addZero(date.getDate());
	year=date.getFullYear();
	dateString=year+"-"+month+"-"+day;
selectDate(day,month,year,day,month,year);}
	
function selectDate(sday,smonth,syear,eday,emonth,eyear){
startDayVal=document.getElementById("SDay").options;
	selectVal(startDayVal,sday);
	startMonthVal=document.getElementById("SMonth").options;
	selectVal(startMonthVal,smonth);
	startYearVal=document.getElementById("SYear").options;
	selectVal(startYearVal,syear);

	endDayVal=document.getElementById("EDay").options;
	selectVal(endDayVal,eday);
	endMonthVal=document.getElementById("EMonth").options;
	selectVal(endMonthVal,smonth);
endYearVal=document.getElementById("EYear").options;
	selectVal(endYearVal,eyear);}




function test(){
	qp=document.getElementById("QuickPick").options[document.getElementById("QuickPick").selectedIndex].value;
	alert(qp);}
function setCookieInfo(key,val){

	var date = new Date();
	date.setTime(date.getTime()+(30*24*60*60*1000));
	var expires = "; expires="+date.toGMTString();
	document.cookie=key+"="+val+expires;}

/* 
 * Original script by Josh Fraser (http://www.onlineaspect.com)
 * Continued by Jon Nylander, (jon at pageloom dot com)
 * According to both of us, you are absolutely free to do whatever 
 * you want with this code.
 * 
 * This code is  maintained at bitbucket.org as jsTimezoneDetect.
 */

/**
 * Namespace to hold all the code for timezone detection.
 */
var jzTimezoneDetector = new Object();

jzTimezoneDetector.HEMISPHERE_SOUTH = 'SOUTH';
jzTimezoneDetector.HEMISPHERE_NORTH = 'NORTH';
jzTimezoneDetector.HEMISPHERE_UNKNOWN = 'N/A';


jzTimezoneDetector.get_date_offset = function (date) {
	return -date.getTimezoneOffset();}

jzTimezoneDetector.get_timezone_info = function () {
	var january_offset = jzTimezoneDetector.get_january_offset();
	
	var june_offset = jzTimezoneDetector.get_june_offset();
	
	var diff = january_offset - june_offset;

	if (diff < 0) {
	    return {'utc_offset' : january_offset,
	    		'dst':	1,
	    		'hemisphere' : jzTimezoneDetector.HEMISPHERE_NORTH}
	}
	else if (diff > 0) {
        return {'utc_offset' : june_offset,
        		'dst' : 1,
        		'hemisphere' : jzTimezoneDetector.HEMISPHERE_SOUTH}
	}

    return {'utc_offset' : january_offset, 
    		'dst': 0, 
    		'hemisphere' : jzTimezoneDetector.HEMISPHERE_UNKNOWN}
}

jzTimezoneDetector.get_january_offset = function () {
	return jzTimezoneDetector.get_date_offset(new Date(2011, 0, 1, 0, 0, 0, 0));
}

jzTimezoneDetector.get_june_offset = function () {
	return jzTimezoneDetector.get_date_offset(new Date(2011, 5, 1, 0, 0, 0, 0));
}
/*
End of script by Josh Fraser
*/

function getTz(){
	offset=jzTimezoneDetector.get_timezone_info()['utc_offset'];
	hours=addZero(offset/60);
	minutes=addZero(offset%60);
	return hours+":"+minutes;}

function setTzCookie(){
	tz=getTz();
	setCookieInfo("CTZ",tz);}

function onLoad (){
	setTzCookie();
	setToday();}

