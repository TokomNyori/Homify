//User Credential
const user = document.querySelectorAll('.credentialUser');
user.forEach((e) => {
    e.addEventListener('click', function() {
        document.querySelector('.modals').style.display = 'flex';
        let myAudio = document.querySelector('#popup_audio');
        myAudio.play();
    });
});
//User Credential End


//Partner Credential
/*
const partner = document.querySelectorAll('.credentialPartner');
partner.forEach((e) => {
    e.addEventListener('click', function() {
        document.querySelector('.modals1').style.display = 'flex';
        let myAudio = document.querySelector('#popup_audio');
        myAudio.play();
    });
});
*/

//Close Modals
const closemodals = document.querySelectorAll('#closeBtn');
closemodals.forEach((f) => {
    f.addEventListener('click', function() {
        document.querySelector('.modals').style.display = 'none';
        document.querySelector('.modals1').style.display = 'none';
        let myAudio2 = document.querySelector('#popup_audio2');
        myAudio2.play();
    });
});
/*
document.querySelector('#modal-signup').addEventListener('click', function(){
    var xhr = new XMLHttpRequest();
    xhr.open('GET', "static/signup.html", true)
    xhr.onload = function () {
        if (this.status == 200){
            document.querySelector('.modals').innerHTML = this.responseText;
            document.querySelector("#typeP").value =  document.querySelector("#changeType").innerHTML;
            document.querySelector("#building_nameP").value =  document.querySelector("#building_name").innerHTML;
            document.querySelector('.modals-closeBtn').addEventListener('click', function(){
                document.querySelector('.modals').style.display = 'none';
                document.location.reload(true);
            });
        }
    }
    xhr.send();
});
*/


const signupPop = document.querySelectorAll('#modal-signup');
signupPop.forEach((e) => {
    e.addEventListener('click', function() {
        document.querySelector('.spinner0').style.display = 'flex';
        var xhr = new XMLHttpRequest();
        xhr.open('GET', "static/signup.html", true);
        xhr.onload = function () {
            if (this.status == 200){
                document.querySelector('.spinner0').style.display = 'none';
                var chgModals = document.querySelectorAll('.modals');
                chgModals.forEach((f) => {
                    console.log('Changing...');
                    f.innerHTML = xhr.responseText;
                    console.log('Changed!');
                    //document.querySelector("#typeP").value =  document.querySelector("#changeType").innerHTML;
                    //document.querySelector("#building_nameP").value =  document.querySelector("#building_name").innerHTML;
                });

                var chgModals1 = document.querySelectorAll('.modals1');
                chgModals1.forEach((g) => {
                    console.log('Changing...');
                    g.innerHTML = xhr.responseText;
                    console.log('Changed!');
                    //document.querySelector("#typeP").value =  document.querySelector("#changeType").innerHTML;
                    //document.querySelector("#building_nameP").value =  document.querySelector("#building_name").innerHTML;
                });
                //document.querySelector('.modals', '.modals1').innerHTML = this.responseText;
                const closemodals1 = document.querySelectorAll('#closeBtn');
                closemodals1.forEach((h) => {
                    h.addEventListener('click', function() {
                        console.log('Closing...');
                        document.querySelector('.modals').style.display = 'none';
                        document.querySelector('.modals1').style.display = 'none';
                        document.location.reload(true);
                        console.log('Closed...');
                        let myAudio2 = document.querySelector('#popup_audio2');
                        myAudio2.play();
                    });
                });
            }
        }
        xhr.send();
    });
});


/*
const soundBtn2 = document.querySelector('#closeBtn');
let myAudio2 = document.querySelector('#popup_audio2');
soundBtn2.addEventListener('click', ()=> {
    myAudio2.play();
});



document.querySelector('.credential').addEventListener('click', function(){
    document.querySelector('.modals').style.display = 'flex';
});

document.querySelector('#poppins').addEventListener('click', function(){
    document.querySelector('.modals').style.display = 'flex';
});
*/
