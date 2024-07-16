import 'vite/modulepreload-polyfill';

// Import our custom CSS
import '../scss/styles.scss';

import 'unpoly';
import 'unpoly/unpoly-bootstrap5.js';

// Import all of Bootstrap's JS
import 'bootstrap';
import Lightbox from 'bs5-lightbox';

function getCurrentSection(sections) {
  const viewportTop = window.scrollY;
  let closestSection = null;
  let minDistance = Infinity;

  sections.forEach(function (section) {
    const rect = section.getBoundingClientRect();
    const distance = Math.abs(rect.top - viewportTop);

    if (distance < minDistance) {
      minDistance = distance;
      closestSection = section;
    }
  });

  return closestSection;
}

function isMobile() {
  const regex = /Mobi|Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i;
  return regex.test(navigator.userAgent);
}

up.on('click', '.next-section', function (event, element) {
  var sections = document.querySelectorAll('section');
  var currentSection = getCurrentSection(sections);
  if (currentSection !== null) {
    const nextSection = currentSection.nextElementSibling;

    if (nextSection) {
      nextSection.scrollIntoView({ behavior: 'smooth', block: 'start', inline: 'nearest' });
    }
  }
});

up.compiler('.pt-navbar .nav-item.dropdown', async function (element) {
  element.addEventListener('click', function (e) {
    if (window.innerWidth > 992) {
      let el_link = element.querySelector('a[data-bs-toggle]');
      if (el_link != null) {
        location.href = el_link.href;
      }
    }
  });
});

up.compiler('div#solutions__swiper', async function (element) {
  const { Swiper } = await import("swiper");
  const { Navigation } = await import("swiper/modules");
  Swiper.use([Navigation])

  const swiper_element = element.querySelector('.swiper');

  const swiper = new Swiper(swiper_element, {
    modules: [Navigation],
    breakpoints: {
      300: {
        slidesPerView: 1,
        spaceBetween: 10,
      },
      370: {
        slidesPerView: 1.5,
        spaceBetween: 10,
      },
      768: {
        slidesPerView: 2.5,
        spaceBetween: 20,
      },
      1300: {
        slidesPerView: 4,
        spaceBetween: 20,
        slidesOffsetBefore: 130,
        centeredSlidesBounds: true,
      }
    },
    slidesPerView: 1,
    slidesOffsetBefore: 0,
    spaceBetween: 20,
    loop: true,
    loopFillGroupWithBlank: true,
    navigation: {
      nextEl: "#solutions__swiper .swiper-button-next",
      prevEl: "#solutions__swiper .swiper-button-prev",
    },
  });
});

up.compiler('.image-slider .image-slider--wrapper', async function (element) {
  const { Swiper } = await import("swiper");
  const { Navigation } = await import("swiper/modules");
  Swiper.use([Navigation])

  const swiper = new Swiper(element, {
    modules: [Navigation],
    breakpoints: {
      300: {
        slidesPerView: 1.5,
        spaceBetween: 10,
      },
      370: {
        slidesPerView: 1.5,
        spaceBetween: 10,
      },
      768: {
        slidesPerView: 2.5,
        spaceBetween: 20,
        slidesOffsetAfter: 100,
        slidesOffsetBefore: 150,
      },
    },
    centeredSlidesBounds: true,
    slidesPerView: 1.5,
    spaceBetween: 20,
    loop: true,
    loopFillGroupWithBlank: true,
    navigation: {
      nextEl: ".swiper-button-next",
      prevEl: ".swiper-button-prev",
    },
  });
});

up.compiler('.pt-solutionindexpage', async function (element) {
  const { gsap, ScrollTrigger } = await import("gsap/all");
  gsap.registerPlugin(ScrollTrigger);

  const tvb = gsap.utils.toArray('.textvideo-block');
  tvb.forEach((t, index) => {
    const v = t.querySelector('video');
    const textBlock = t.querySelector('.column-hero-text-block');

    const videoSource = v.dataset.video;
    const videoSourceMobile = v.dataset.videoMobile;

    if (isMobile()) {
      var start = "top top+=10px"
      var end = "bottom-=10px"
      if (videoSourceMobile) {
        v.src = videoSourceMobile;
      } else {
        v.src = videoSource;
      }
    } else {
      var start = "top top+=50px";
      var end = "bottom-=50px";
      v.src = videoSource;
    }
    v.load()

    up.on(v, 'loadedmetadata', function (event, video) {
      const scrollSpace = video.dataset.scrollSpace;
      const scrollSpaceMobile = video.dataset.scrollSpaceMobile;
      if (isMobile()) {
        if (scrollSpaceMobile) {
          end = "+=" + scrollSpaceMobile + "px " + end;
        } else {
          end = "+=" + ((video.duration * 600) / 2) + "px " + end;
        }
      } else {
        if (scrollSpace) {
          end = "+=" + scrollSpace + "px " + end;
        } else {
          end = "+=" + (video.duration * 600) + "px " + end;
        }
      }

      ScrollTrigger.create({
        id: "st-" + index,
        trigger: t,
        start: start,
        end: end,
        //markers: true,
        pin: true,
        pinSpacing: true,
        pinnedContainer: t,
        preventOverlaps: true,
        onUpdate: (self) => {
          const progress = self.progress;
          const currentTime = progress * video.duration;
          video.currentTime = currentTime;
        }
      });
    });
  });
});

window.onscroll = function () {
  const arrowIndicator = document.getElementById('arrow_indicator')
  if (arrowIndicator) {
    if ((window.innerHeight + Math.round(window.scrollY)) >= document.body.offsetHeight) {
      document.getElementById('arrow_indicator').style.display = 'none';
    } else {
      document.getElementById('arrow_indicator').style.display = '';
    }
  }
  // Functionality for ".animated-block" elements
  var animatedBlocks = document.querySelectorAll(".animated-block");
  animatedBlocks.forEach(function (element) {
    var position = element.getBoundingClientRect();
    var threshold = window.innerWidth >= 600 ? 0.9 : 1.4;

    if (position.top <= window.innerHeight * threshold) {
      element.classList.add("animate");
    } else {
      element.classList.remove("animate");
    }
  });

  // Functionality for specific elements in section 10
  var specificElements = document.querySelectorAll("section:nth-of-type(10) .image-collage .image-collage--image-wrap:nth-of-type(2), section:nth-of-type(10) .image-collage .image-collage--image-wrap:nth-of-type(3)");
  specificElements.forEach(function (element) {
    var position = element.getBoundingClientRect();
    var threshold = window.innerWidth >= 0.5;

    if (position.top <= window.innerHeight * threshold) {
      element.classList.add("animate-img");
    } else {
      element.classList.remove("animate-img");
    }
  });
};


up.compiler('[data-toggle="lightbox"]', async function (element) {
  element.addEventListener('click', Lightbox.initialize);
});


up.on('up:form:submit', async (event, form) => {
  const targetId = event?.target?.id;
  if (targetId === "captchafox-submit-button") {
    event.preventDefault()
    const [cfCaptchaResponse] = event.params.entries.filter(({ name, value }) => name === "cf-captcha-response" && value)
    if (!cfCaptchaResponse) {
      try {
        const token = await captchafox.execute();
        //const token = await new Promise((resolve, reject) => {
        //  setTimeout(() => { resolve("test") }, 1000)
        //})
        event.params.set("cf-captcha-response", token)
        const contactModal = document.getElementById("contactModal");
        if (contactModal) {
          const [backdrop] = document.getElementsByClassName("modal-backdrop");
          contactModal.style.display = "none";
          contactModal.classList.remove("show")
          backdrop.style.display = "none"
        }
        up.render({ ...event.renderOptions });
      } catch (e) {
        console.error(e);
      }
    }
  }
})
