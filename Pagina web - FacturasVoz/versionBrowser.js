'use strict'
 
function getBrowserInfo() {
    var ua= navigator.userAgent, tem, 
    M= ua.match(/(opera|chrome|safari|firefox|msie|trident(?=\/))\/?\s*(\d+)/i) || [];
    if(/trident/i.test(M[1])){
        tem=  /\brv[ :]+(\d+)/g.exec(ua) || [];
        return 'IE '+(tem[1] || '');
    }
    if(M[1]=== 'Chrome'){
        tem= ua.match(/\b(OPR|Edge)\/(\d+)/);
        if(tem!= null) {
        	//return tem.slice(1).join(' ').replace('OPR', 'Opera');
        	tem[1] = tem[1].replace('OPR', 'Opera');
        	return tem.slice(1);
        }
    }
    M= M[2]? [M[1], M[2]]: [navigator.appName, navigator.appVersion, '-?'];
    if((tem= ua.match(/version\/(\d+)/i))!= null) M.splice(1, 1, tem[1]);
    //return M.join(' ');
    return M;
};

function validateVersion(version) {
	switch(version[0]) {
		case "Chrome":
			if (version[1] < 55){
				upgradeBrowser();
			}
			break;
		case "Opera":
			if (version[1] < 42){
				upgradeBrowser();
			}
			break;
		case "Firefox":
			if (version[1] < 44){
				upgradeBrowser();
			}
			break;
		case "Edge":
			if (version[1] < 12){
				upgradeBrowser();
			}
			break;
		default:
			upgradeBrowser();
	}

	console.log(version);
}

function upgradeBrowser(){
	alert("Es posible que en su navegador no funcione correctamente la función de voz. Le recomendamos actualizarlo.");
}

validateVersion(getBrowserInfo());