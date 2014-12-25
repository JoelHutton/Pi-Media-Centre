var pinging = false;
var toGo = 0;
function sendCommand(command)
{
	if (command!="")
	{
            if(command.indexOf("relay")>-1){
                pinging = true;
            }
		$.ajax(
		{
			type: "POST",
			url: "toPort.py",
			data: 'command=' + command, // data to send to above script page if any
			cache: false,
			success: function(response)
			{
                            handleResponse(response);
				// update code for your page
			}
		});
	}
} 
function handleResponse(response){
    var a = response.trim().slice(1,response.trim().length-1);
    a = a.split(",");
    for(var i=0;i<a.length;i++){
        var cur = a[i];    
        var split = cur.split(':');
        var relayName = split[0].trim();
        var relayState = split[1].trim();
        if(relayState =="1"){
            //alert(relayName + " is on");
            $('#'+relayName+'Relay').css("background-color","green");
            $('#'+relayName+'Relay').attr("onclick","sendCommand('{commandType: \\\'relay\\\',device: \\\'"+ relayName + "\\\', state: \\\'off\\\'}')");
        }
        else{
            //alert(relayName + " is off");
            $('#'+relayName+'Relay').css("background-color","grey");
            $('#'+relayName+'Relay').attr("onclick","sendCommand('{commandType: \\\'relay\\\',device: \\\'"+ relayName + "\\\', state: \\\'on\\\'}')");
        }
    }
}
function showSection(option)
{
	document.getElementById('sonyav').style.display = "none";
	document.getElementById('skyTimeButtons').style.display = "none";
	document.getElementById('skyColors').style.display = "none";
	document.getElementById('projector').style.display = "none";
	document.getElementById('relays').style.display = "none";
	document.getElementById('samsung').style.display = "none";
 	if(option!='default')
 	{
		document.getElementById(option).style.display = "block";
	}		
 	
}
function ping(){
	if (pinging == true){
            setTimeout("ping();",5000);
	}
        sendCommand("{commandType: 'request'}");
}
function fadeout(){
	$('.opt').slideUp('slow', function() {
	// Animation complete
	});

}
function selectDevice(action){
	if (action == "hide"){
		$('#dropdownDevice').slideUp('slow', function(){});
	}
	else{
		$('#dropdownDevice').slideDown('slow', function(){});
	}
}
function selectScreen(action){
	if (action == "hide"){
		$('#dropdownScreen').slideUp('slow', function(){});
	}
	else{
		$('#dropdownScreen').slideDown('slow', function(){});
	}
}
function selectExtra(extra){
	$('.opt').slideUp('slow', function(){});
	$("#"+extra).slideDown('slow', function(){});
}
ping();
