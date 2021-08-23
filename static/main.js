function cc(name) {
  document.querySelector("#changeType").innerHTML = 'Type: ' + name;
}


var swiper = new Swiper('.swiper-container', {
  effect: 'coverflow',
  grabCursor: true,
  centeredSlides: true,
  slidesPerView: 'auto',
  coverflowEffect: {
    rotate: 20,
    stretch: 0,
    depth: 200,
    modifier: 1,
    slideShadows: true,
  },
  loop: true,
  autoplay: {
      delay: 2000,
      disableOnInteraction: false,
  },
});
