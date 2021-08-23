const nav = document.querySelector('nav');
const expandableSearch = document.querySelector('.cont');
const heroHeraLal = document.querySelector(".identify1Observer");
const searchBar = document.querySelector(".searchbar");

const options = {
    rootMargin: "-70px 0px 0px 0px"
};

const observer = new IntersectionObserver(function(entries, observer) {
    entries.forEach(entry => {
        if (!entry.isIntersecting) {
            expandableSearch.style.display = 'flex';
            searchBar.style.visibility = 'hidden';
        }
        else {
            expandableSearch.style.display = 'none';
            //searchBar.style.display = 'flex';
            searchBar.style.visibility = 'visible';
        }
    });
}, options);

observer.observe(heroHeraLal);



/*
const navbar = document.querySelector("nav");
const stickyId = document.querySelector(".sticky");
const options = {};
const observer = new IntersectionObserver(function(entries, observer) {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            stickyId.classList.add("add", "colors");
        }
        else{
            stickyId.classList.remove("add", "colors");
        }
    });
} , options);

observer.observe(stickyId);

*/

/*
const observerOne = new IntersectionObserver(function(entries, observerOne) {
    entries.forEach(entry => {
        if (!entry.isIntersecting) {
            stickyId.classList.add("colors");
        }
        else{
            stickyId.classList.remove("colors");
        };
    });
} , options);

observerOne.observe(stickyId);
*/