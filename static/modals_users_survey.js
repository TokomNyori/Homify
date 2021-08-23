//User Credential

const user = document.querySelectorAll('#credentialUser2');
user.forEach((e) => {
    e.addEventListener('click', function() {
        document.querySelector('#modals_users_payment').style.display = 'flex';
        let myAudio = document.querySelector('#popup_audio');
        myAudio.play();
    });
});
//User Credential End


//Close Modals
const closemodals = document.querySelector('#closeBtnUsers');
closemodals.addEventListener('click', function() {
        document.querySelector('#modals_users_payment').style.display = 'none';
        let myAudio2 = document.querySelector('#popup_audio2');
        myAudio2.play();
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


const userSignupPop = document.querySelectorAll('#modal-signup-users');
userSignupPop.forEach((e) => {
    e.addEventListener('click', function() {
        document.querySelector('.spinner0').style.display = 'flex';
        var xhr = new XMLHttpRequest();
        xhr.open('GET', "static/signupPopupUsers.html", true);
        xhr.onload = function () {
            if (this.status == 200){
                document.querySelector('.spinner0').style.display = 'none';
                var chgModals = document.querySelectorAll('#modals_users');
                chgModals.forEach((f) => {
                    console.log('Changing...');
                    f.innerHTML = xhr.responseText;
                    console.log('Changed!');
                    //document.querySelector("#typeP").value =  document.querySelector("#changeType").innerHTML;
                    //document.querySelector("#building_nameP").value =  document.querySelector("#building_name").innerHTML;
                });

                const closemodalsUsers = document.querySelectorAll('#closeBtnUsers');
                closemodalsUsers.forEach((h) => {
                    h.addEventListener('click', function() {
                        document.querySelector('#modals_users').style.display = 'none';
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