const search = document.querySelector('.searchCstm');
const conto = document.querySelector('.cont');
const icon = document.querySelector('.iconCstm');
const body = document.querySelector('body');
const close = document.querySelector('#customSearchClose');
const divy = document.querySelector('div');  
const def0 = document.querySelector('#cstmSelect1');
const def1 = document.querySelector('#cstmSelect2');

icon.onclick = function() {
    search.classList.add('expand');
}

close.onclick = function() {
    search.classList.remove('expand');
    def0.getElementsByTagName('option')[0].selected = 'selected'
    def1.getElementsByTagName('option')[0].selected = 'selected'
}

/*
window.addEventListener('click', outsideclick);

function outsideclick (e) {
    if (e.target != search) {
        console.log('BODY')
        search.classList.remove('expand');
    }
}
*/

