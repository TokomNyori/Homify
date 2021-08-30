const navbar1 = document.querySelector("nav");
const navbarAnchs = document.querySelector("nav a");
const navColps0 = document.querySelector("#navColps0 i");
const navColps1 = document.querySelector("#navColps1 i");
const navColps2 = document.querySelector("#navColps2 i");
const navColps2_btn = document.querySelector(".user_nav_profileBtn");
const navColps2_0 = document.querySelector(".userProfileNav");
const navHamIcon = document.querySelector("#hamIcon");
const navTogglers = document.querySelector("#navColBtn");
const hideLists0 = document.querySelector(".hideLists0");
const hideLists1 = document.querySelector(".hideLists1");
const hideLists2 = document.querySelector(".hideLists2");
const heroText = document.querySelector('#herotext');


const search_bar = document.querySelector(".identifyObserver");
//const heroText = document.querySelector("#heroh1");

const options1 = {
    rootMargin: "-150px 0px 0px 0px"
};

const observer1 = new IntersectionObserver(function(entries, observer1) {
    entries.forEach(entry => {
        if (!entry.isIntersecting) {
           navbar1.classList.add("addNav");
           navTogglers.classList.add("navToggler");
           navHamIcon.classList.add("navTogglerIcon");  
           navColps0.classList.add("addNavAnchs");
           navColps1.classList.add("addNavAnchs");
           navColps2.classList.add("addNavAnchs");
           navColps2_btn.classList.add("addNavAnchsBG");
           navColps2_0.classList.add("addNavAnchs");
           hideLists0.classList.add("hideListsADD");
           hideLists1.classList.add("hideListsADD");
           hideLists2.classList.add("hideListsADD");
        }
        else
        {
           navbar1.classList.remove("addNav");
           navTogglers.classList.remove("navToggler");
           navHamIcon.classList.remove("navTogglerIcon");
           navColps0.classList.remove("addNavAnchs");
           navColps1.classList.remove("addNavAnchs");
           navColps2.classList.remove("addNavAnchs");
           navColps2_btn.classList.remove("addNavAnchsBG");
           navColps2_0.classList.remove("addNavAnchs");
           hideLists0.classList.remove("hideListsADD");
           hideLists1.classList.remove("hideListsADD");
           hideLists2.classList.remove("hideListsADD");
        };
    });
} , options1);

observer1.observe(search_bar);
observer1.observe(heroText);