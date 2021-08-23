//User Credential
const userPy = document.querySelectorAll('.credentialUser1');
userPy.forEach((e) => {
    e.addEventListener('click', function() {
        document.querySelector('#modals_users_payment').style.display = 'flex';
        let myAudio = document.querySelector('#popup_audio');
        myAudio.play();
    });
});
//User Credential End

//User Credential | survey modal
const userSv = document.querySelectorAll('#credentialUser2');
userSv.forEach((e) => {
    e.addEventListener('click', function() {
        document.querySelector('#modals_users_survey').style.display = 'flex';
        let myAudio = document.querySelector('#popup_audio');
        myAudio.play();
    });
});
//User Credential End


//Close Modals
const closemodals = document.querySelectorAll('#closeBtnUsers');
closemodals.forEach((e) => {
    e.addEventListener('click', function() {
        document.querySelector('#modals_users_payment').style.display = 'none';
        document.querySelector('#modals_users_survey').style.display = 'none';
        let myAudio2 = document.querySelector('#popup_audio2');
        myAudio2.play();
    })    
});


/*
document.querySelector('#modal-signup-users').addEventListener('click', function(){
    var xhr = new XMLHttpRequest();
    xhr.open('GET', "static/signupPopupUsers.html", true)
    xhr.onload = function () {
        if (this.status == 200) {
            document.querySelector('#modals_users').innerHTML = this.responseText;
            document.querySelector("#typeP").value =  document.querySelector("#changeType").innerHTML;
            document.querySelector("#building_nameP").value =  document.querySelector("#building_name").innerHTML;
            //const closemodalsUsers = document.querySelectorAll('.closeBtnUsers');
            const closemodals_signUP = document.querySelector('#closeBtnUsers');
            closemodals_signUP.addEventListener('click', function() {
                document.querySelector('#modals_users').style.display = 'none';
                let myAudio2 = document.querySelector('#popup_audio2');
                myAudio2.play();
                document.location.reload(true);
            });
        }
    }
    xhr.send();
});
*/

//Handles siugnup via payment
const userSignupPop_py = document.querySelectorAll('#modal-signup-usersPy');
userSignupPop_py.forEach((e) => {
    e.addEventListener('click', function() {
        document.querySelector('.spinner0').style.display = 'flex';
        var xhr = new XMLHttpRequest();
        xhr.open('GET', "static/signupPopupUsers_payment.html", true);
        xhr.onload = function () {
            if (this.status == 200){
                document.querySelector('.spinner0').style.display = 'none';
                var chgModals = document.querySelectorAll('#modals_users_payment');
                chgModals.forEach((f) => {
                    console.log('Changing...');
                    f.innerHTML = xhr.responseText;
                    console.log('Paymenet POP!');
                    document.querySelector("#home_type_SignUp").value = document.querySelector("#h_type_value").value;
                    document.querySelector("#home_id_SignUp").value = document.querySelector("#h_id_value").value;
                    document.querySelector("#home_name_SignUp").value = document.querySelector("#h_name_value").value;
                    document.querySelector("#price_SignUp").value = document.querySelector("#price").value;
                    document.querySelector("#mode_signUp").value = 'payment';
                    //document.querySelector("#building_nameP").value =  document.querySelector("#building_name").innerHTML;
                });

                const closemodalsUsers = document.querySelectorAll('#closeBtnUsers');
                closemodalsUsers.forEach((h) => {
                    h.addEventListener('click', function() {
                        document.querySelector('#modals_users_payment').style.display = 'none';
                        let myAudio2 = document.querySelector('#popup_audio2');
                        myAudio2.play();
                        document.location.reload(true);
                    });
                });
            }
        }
        xhr.send();
    });
});


//Handles siugnup via survey
const userSignupPop_sv = document.querySelectorAll('#modal-signup-usersSv');
userSignupPop_sv.forEach((e) => {
    e.addEventListener('click', function() {
        document.querySelector('.spinner0').style.display = 'flex';
        var xhr = new XMLHttpRequest();
        xhr.open('GET', "static/signupPopupUsers_payment.html", true);
        xhr.onload = function () {
            if (this.status == 200){
                document.querySelector('.spinner0').style.display = 'none';
                var chgModals = document.querySelectorAll('#modals_users_survey');
                chgModals.forEach((f) => {
                    console.log('Suyrvey POP...');
                    f.innerHTML = xhr.responseText;
                    console.log('Changed!');
                    document.querySelector("#home_type_SignUp").value = document.querySelector("#h_type_value").value;
                    document.querySelector("#home_id_SignUp").value = document.querySelector("#h_id_value").value;
                    document.querySelector("#home_name_SignUp").value = document.querySelector("#h_name_value").value;
                    document.querySelector("#price_SignUp").value = document.querySelector("#price").value;
                    document.querySelector("#mode_signUp").value = 'survey';
                    //document.querySelector("#building_nameP").value =  document.querySelector("#building_name").innerHTML;
                });

                const closemodalsUsers = document.querySelectorAll('#closeBtnUsers');
                closemodalsUsers.forEach((h) => {
                    h.addEventListener('click', function() {
                        document.querySelector('#modals_users_survey').style.display = 'none';
                        let myAudio2 = document.querySelector('#popup_audio2');
                        myAudio2.play();
                        document.location.reload(true);
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