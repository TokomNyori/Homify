var swiper = new Swiper('.swiper-container1', {
    effect: 'coverflow',
    grabCursor: true,
    centeredSlides: false,
    slidesPerView: 'auto',
    coverflowEffect: {
        rotate: 0,
        stretch: 0,
        depth: 0,
        modifier: 1,
        slideShadows: true,
    },
    loop: true,
    freeMode: true,
});