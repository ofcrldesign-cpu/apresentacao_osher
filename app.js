/**
 * OSHER AÇAÍ SHOP — Interactive Presentation Logic
 * Handles Scroll Animations, Color Copy, Typography Sandbox, 
 * Interactive Stories Video Player, Delivery App Simulator, Lightbox Modal
 */

document.addEventListener('DOMContentLoaded', () => {
  initHeroInteractiveCover();
  initParallax();
  initScrollAnimations();
  initScrollProgressBar();
  initActiveNav();
  initColorCopy();
  initTypographyTester();
  initLightbox();
  initStoriesPlayer();
  initMockupFilters();
  initAppTabs();
  initMobileMenu();
});

/* --------------------------------------------------------------------------
   0. Parallax Scrolling Engine (3D Depth & Differential Speed)
   -------------------------------------------------------------------------- */
function initParallax() {
  const parallaxItems = document.querySelectorAll('[data-parallax-speed]');
  const parallaxOrbs = document.querySelectorAll('.parallax-orb');

  let latestScrollY = window.scrollY;
  let ticking = false;

  function updateParallax() {
    const scrollY = latestScrollY;

    // Animate custom elements with data-parallax-speed
    parallaxItems.forEach(item => {
      const speed = parseFloat(item.dataset.parallaxSpeed) || 0.15;
      const rect = item.parentElement.getBoundingClientRect();
      const offset = (window.innerHeight - rect.top) * speed * 0.4;
      item.style.transform = `translate3d(0, ${-offset}px, 0)`;
    });

    // Animate background ambient orbs
    parallaxOrbs.forEach((orb, index) => {
      const speed = (index + 1) * 0.08;
      const yPos = scrollY * speed;
      orb.style.transform = `translate3d(0, ${yPos}px, 0)`;
    });

    ticking = false;
  }

  window.addEventListener('scroll', () => {
    latestScrollY = window.scrollY;
    if (!ticking) {
      window.requestAnimationFrame(updateParallax);
      ticking = true;
    }
  }, { passive: true });

  updateParallax();
}

/* --------------------------------------------------------------------------
   0.1 Capa Interativa da Logo (3D Perspective Tilt & Golden Shine)
   -------------------------------------------------------------------------- */
function initHeroInteractiveCover() {
  const cover = document.getElementById('heroCoverInteractive');
  const showcase = document.getElementById('heroLogoShowcase');
  const shineBtn = document.getElementById('btnShineTrigger');
  if (!cover || !showcase) return;

  cover.addEventListener('mousemove', (e) => {
    const rect = cover.getBoundingClientRect();
    const x = e.clientX - rect.left - rect.width / 2;
    const y = e.clientY - rect.top - rect.height / 2;
    const rotX = -(y / (rect.height / 2)) * 12;
    const rotY = (x / (rect.width / 2)) * 12;
    showcase.style.transform = `perspective(1000px) rotateX(${rotX.toFixed(2)}deg) rotateY(${rotY.toFixed(2)}deg) scale3d(1.03, 1.03, 1.03)`;
  });

  cover.addEventListener('mouseleave', () => {
    showcase.style.transform = 'perspective(1000px) rotateX(0deg) rotateY(0deg) scale3d(1, 1, 1)';
  });

  function triggerShine() {
    showcase.style.transition = 'filter 0.3s ease, transform 0.3s ease';
    showcase.style.filter = 'drop-shadow(0 25px 50px rgba(0,0,0,0.95)) drop-shadow(0 0 75px rgba(255,215,120,0.9)) brightness(1.25)';
    showcase.style.transform = 'perspective(1000px) scale3d(1.06, 1.06, 1.06)';
    playClickSound();
    showToast('✨ Identidade Oficial OSHER: Açaí + Sorvete. Do seu jeito.');

    setTimeout(() => {
      showcase.style.transition = 'transform 0.18s ease-out, filter 0.35s ease';
      showcase.style.filter = '';
      showcase.style.transform = '';
    }, 800);
  }

  if (shineBtn) {
    shineBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      triggerShine();
    });
  }

  cover.addEventListener('click', () => {
    triggerShine();
  });
}

/* --------------------------------------------------------------------------
   1. Reveal on Scroll (Intersection Observer for Fade-in & Slide-in)
   -------------------------------------------------------------------------- */
function initScrollAnimations() {
  const revealElements = document.querySelectorAll('.reveal, .reveal-fade, .reveal-left, .reveal-right, .reveal-zoom');
  
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('active');
      }
    });
  }, {
    root: null,
    threshold: 0.08,
    rootMargin: '0px 0px -50px 0px'
  });

  revealElements.forEach(el => observer.observe(el));
}

/* --------------------------------------------------------------------------
   2. Scroll Progress Bar
   -------------------------------------------------------------------------- */
function initScrollProgressBar() {
  const progressBar = document.getElementById('scroll-progress');
  if (!progressBar) return;

  window.addEventListener('scroll', () => {
    const totalHeight = document.documentElement.scrollHeight - window.innerHeight;
    const progress = (window.scrollY / totalHeight) * 100;
    progressBar.style.width = `${progress}%`;
  }, { passive: true });
}

/* --------------------------------------------------------------------------
   3. Active Navigation on Scroll
   -------------------------------------------------------------------------- */
function initActiveNav() {
  const sections = document.querySelectorAll('section[id]');
  const navLinks = document.querySelectorAll('.nav-links a');

  window.addEventListener('scroll', () => {
    let current = '';
    const scrollPosition = window.scrollY + 200;

    sections.forEach(section => {
      const sectionTop = section.offsetTop;
      const sectionHeight = section.offsetHeight;
      if (scrollPosition >= sectionTop && scrollPosition < sectionTop + sectionHeight) {
        current = section.getAttribute('id');
      }
    });

    navLinks.forEach(link => {
      link.classList.remove('active');
      if (link.getAttribute('href') === `#${current}`) {
        link.classList.add('active');
      }
    });
  }, { passive: true });
}

/* --------------------------------------------------------------------------
   4. Color Swatches Copy to Clipboard
   -------------------------------------------------------------------------- */
function initColorCopy() {
  const colorCards = document.querySelectorAll('.color-card');
  
  colorCards.forEach(card => {
    card.addEventListener('click', () => {
      const hex = card.dataset.hex;
      if (!hex) return;

      navigator.clipboard.writeText(hex).then(() => {
        showToast(`Cor ${hex} copiada para a área de transferência!`);
        playClickSound();
      }).catch(err => {
        showToast(`Código: ${hex}`);
      });
    });
  });
}

function showToast(message) {
  let toast = document.getElementById('toast');
  if (!toast) {
    toast = document.createElement('div');
    toast.id = 'toast';
    document.body.appendChild(toast);
  }
  toast.innerHTML = `<span>✨</span> <span>${message}</span>`;
  toast.classList.add('show');

  setTimeout(() => {
    toast.classList.remove('show');
  }, 2800);
}

/* --------------------------------------------------------------------------
   5. Typography Live Sandbox Tester
   -------------------------------------------------------------------------- */
function initTypographyTester() {
  const input = document.getElementById('tester-text');
  const slider = document.getElementById('tester-size');
  const sizeValue = document.getElementById('tester-size-val');
  const serifPreview = document.querySelector('.preview-serif');
  const sansPreview = document.querySelector('.preview-sans');

  if (!input || !slider || !serifPreview || !sansPreview) return;

  input.addEventListener('input', (e) => {
    const text = e.target.value.trim() || 'Açaí + Sorvete. Do seu jeito.';
    serifPreview.textContent = text;
    sansPreview.textContent = text;
  });

  slider.addEventListener('input', (e) => {
    const size = e.target.value;
    sizeValue.textContent = `${size}px`;
    serifPreview.style.fontSize = `${size}px`;
    sansPreview.style.fontSize = `${Math.max(14, Math.round(size * 0.5))}px`;
  });
}

/* --------------------------------------------------------------------------
   6. Lightbox Modal
   -------------------------------------------------------------------------- */
function initLightbox() {
  const modal = document.getElementById('lightbox-modal');
  const modalImg = document.getElementById('lightbox-img');
  const modalCaption = document.getElementById('lightbox-caption');
  const closeBtn = document.querySelector('.lightbox-close');

  if (!modal || !modalImg) return;

  const triggerElements = document.querySelectorAll('[data-lightbox-src]');

  triggerElements.forEach(el => {
    el.addEventListener('click', (e) => {
      e.preventDefault();
      const src = el.dataset.lightboxSrc;
      const caption = el.dataset.lightboxCaption || '';

      modalImg.src = src;
      modalCaption.textContent = caption;
      modal.classList.add('active');
      document.body.style.overflow = 'hidden';
    });
  });

  const closeModal = () => {
    modal.classList.remove('active');
    document.body.style.overflow = '';
  };

  if (closeBtn) closeBtn.addEventListener('click', closeModal);
  modal.addEventListener('click', (e) => {
    if (e.target === modal) closeModal();
  });

  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && modal.classList.contains('active')) {
      closeModal();
    }
  });
}

/* --------------------------------------------------------------------------
   7. Interactive Stories Video Simulator
   -------------------------------------------------------------------------- */
let storyCurrentIndex = 0;
let storyTimer = null;
let storyProgress = 0;
let isStoryPlaying = true;
let isAudioMuted = true;
const STORY_DURATION = 5000; // 5 seconds per story
const TICK_INTERVAL = 50;

function initStoriesPlayer() {
  const slides = document.querySelectorAll('.video-slide');
  const segs = document.querySelectorAll('.story-prog-track');
  const playBtn = document.getElementById('btn-story-play');
  const soundBtn = document.getElementById('btn-story-sound');
  const tapLeft = document.querySelector('.tap-zone.left');
  const tapRight = document.querySelector('.tap-zone.right');

  if (slides.length === 0) return;

  function updateStoryUI() {
    slides.forEach((slide, idx) => {
      slide.classList.toggle('active', idx === storyCurrentIndex);
    });

    segs.forEach((seg, idx) => {
      const fill = seg.querySelector('.story-fill');
      if (idx < storyCurrentIndex) {
        fill.style.width = '100%';
      } else if (idx === storyCurrentIndex) {
        fill.style.width = `${(storyProgress / STORY_DURATION) * 100}%`;
      } else {
        fill.style.width = '0%';
      }
    });
  }

  function nextStory() {
    storyProgress = 0;
    if (storyCurrentIndex < slides.length - 1) {
      storyCurrentIndex++;
    } else {
      storyCurrentIndex = 0; // loop back
    }
    updateStoryUI();
    playStoryBeep();
  }

  function prevStory() {
    storyProgress = 0;
    if (storyCurrentIndex > 0) {
      storyCurrentIndex--;
    } else {
      storyCurrentIndex = slides.length - 1;
    }
    updateStoryUI();
    playStoryBeep();
  }

  function startStoryTimer() {
    clearInterval(storyTimer);
    storyTimer = setInterval(() => {
      if (!isStoryPlaying) return;
      storyProgress += TICK_INTERVAL;
      if (storyProgress >= STORY_DURATION) {
        nextStory();
      } else {
        updateStoryUI();
      }
    }, TICK_INTERVAL);
  }

  startStoryTimer();

  // Navigation taps
  if (tapLeft) {
    tapLeft.addEventListener('click', () => {
      prevStory();
    });
  }
  if (tapRight) {
    tapRight.addEventListener('click', () => {
      nextStory();
    });
  }

  // Play / Pause Toggle
  if (playBtn) {
    playBtn.addEventListener('click', () => {
      isStoryPlaying = !isStoryPlaying;
      playBtn.innerHTML = isStoryPlaying 
        ? '<span>⏸</span> Pausar Story' 
        : '<span>▶</span> Reproduzir';
      playBtn.classList.toggle('active', isStoryPlaying);
    });
  }

  // Audio Toggle
  if (soundBtn) {
    soundBtn.addEventListener('click', () => {
      isAudioMuted = !isAudioMuted;
      soundBtn.innerHTML = isAudioMuted 
        ? '<span>🔇</span> Ativar Som' 
        : '<span>🔊</span> Som Ativo';
      soundBtn.classList.toggle('active', !isAudioMuted);
      if (!isAudioMuted) {
        playWelcomeChime();
        showToast('Áudio imersivo ativado para o Stories');
      }
    });
  }

  // Interactive Poll Voting
  const pollBtns = document.querySelectorAll('.poll-opt-btn');
  pollBtns.forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.stopPropagation();
      pollBtns.forEach(b => b.classList.remove('voted'));
      btn.classList.add('voted');
      showToast('Seu voto foi registrado no Story!');
      playClickSound();
    });
  });
}

/* --------------------------------------------------------------------------
   8. Mockup Filters
   -------------------------------------------------------------------------- */
function initMockupFilters() {
  const filterBtns = document.querySelectorAll('.filter-btn');
  const mockupCards = document.querySelectorAll('.mockup-card');

  if (filterBtns.length === 0) return;

  filterBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      filterBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');

      const filter = btn.dataset.filter;

      mockupCards.forEach(card => {
        const cat = card.dataset.category;
        if (filter === 'all' || cat === filter) {
          card.style.display = 'flex';
          setTimeout(() => {
            card.classList.add('active');
          }, 50);
        } else {
          card.style.display = 'none';
        }
      });
    });
  });
}

/* --------------------------------------------------------------------------
   9. Delivery App Switcher (iFood, Keeta, 99 Food)
   -------------------------------------------------------------------------- */
const appConfigurations = {
  ifood: {
    brandName: 'OSHER Açaí Shop — iFood Store',
    rating: '4.9',
    reviews: '(520+ avaliações no iFood)',
    time: '🛵 25-35 min • Entrega iFood',
    fee: 'Entrega Grátis acima de R$ 45',
    themeColor: '#EA1D2C',
    badge: 'Super Restaurante iFood',
    badgeBg: 'rgba(234, 29, 44, 0.25)',
    badgeColor: '#ff6b78',
    floatingPill: 'Super Restaurante iFood',
    searchText: 'Buscar no cardápio iFood de OSHER...',
    promoText: '🏷️ Cupom de R$ 10 OFF disponível no Clube iFood para pedidos acima de R$ 40',
    headerBanner: 'assets/osher_delivery_header.jpg',
    category: '⭐ Destaques & Mais Pedidos do iFood',
    cartColor: '#EA1D2C',
    buttonText: '+ Adicionar',
    products: [
      {
        title: 'Copo OSHER 500ml (Monte do Seu Jeito)',
        desc: 'Açaí artesanal cremoso + Sorvete artesanal + 2 Caldas especiais + 3 Complementos à sua escolha.',
        price: 'R$ 17,00',
        img: 'assets/cardapio1.jpg'
      },
      {
        title: 'Shake dos Artists 500ml',
        desc: 'Exclusividade OSHER com textura aveludada, toppings em pó e frutas frescas selecionadas.',
        price: 'R$ 25,00',
        img: 'assets/feed1.jpg'
      },
      {
        title: 'Combo Casal OSHER (2 Copos 400ml)',
        desc: '2 copos de 400ml montados do seu jeito com adicionais gourmet inclusos.',
        price: 'R$ 30,00',
        img: 'assets/feed2.jpg'
      },
      {
        title: 'Mega Pote OSHER 1000ml Família',
        desc: '1 Litro de puro sabor para compartilhar com família e amigos.',
        price: 'R$ 36,00',
        img: 'assets/cardapio2.jpg'
      }
    ]
  },
  keeta: {
    brandName: 'OSHER Açaí Shop — KeeTa Express',
    rating: '4.95',
    reviews: '(380+ pedidos KeeTa)',
    time: '⚡ 15-25 min • KeeTa Express',
    fee: 'Frete Promocional KeeTa R$ 0,99',
    themeColor: '#FFD100',
    badge: '⚡ KeeTa On-Time Guarantee',
    badgeBg: 'rgba(255, 209, 0, 0.2)',
    badgeColor: '#FFD100',
    floatingPill: '⚡ KeeTa On-Time Guarantee',
    searchText: 'Buscar no cardápio KeeTa de OSHER...',
    promoText: '⚡ KeeTa On-Time: Entrega no prazo garantida ou cupom de R$ 15 de volta',
    headerBanner: 'assets/osher_delivery_packaging.jpg',
    category: '⚡ Entrega Rápida & Combos de Outono KeeTa',
    cartColor: '#1D1D1F',
    buttonText: '+ Pedir KeeTa',
    products: [
      {
        title: 'Bowl Gourmet OSHER + Frutas Vermelhas',
        desc: 'Açaí premium servido com morangos, mirtilos frescos e colher de bambu.',
        price: 'R$ 22,90',
        img: 'assets/osher_bowls_mockup.jpg'
      },
      {
        title: 'Copo OSHER 400ml + Calda Manuka Gold',
        desc: 'Açaí com sorvete e toque especial de calda de mel.',
        price: 'R$ 15,00',
        img: 'assets/stories2.jpg'
      },
      {
        title: 'Pote de Sorvete Artesanal 500ml',
        desc: 'Embalagem kraft térmica com lacre hot stamping seguro.',
        price: 'R$ 17,00',
        img: 'assets/materiais.jpg'
      },
      {
        title: 'Combo Individual Rápido 300ml + Topping',
        desc: 'Perfeito para a pausa no trabalho ou lanche da tarde.',
        price: 'R$ 13,00',
        img: 'assets/stories3.jpg'
      }
    ]
  },
  food99: {
    brandName: 'OSHER Açaí Shop — 99 Food',
    rating: '4.88',
    reviews: '(440+ notas 99Food)',
    time: '🛵 20-30 min • 99Food Direta',
    fee: 'Cupom 99FOOD: R$ 12 OFF no 1º Pedido',
    themeColor: '#FF7D00',
    badge: '★ 99Food Seleção Ouro',
    badgeBg: 'rgba(255, 125, 0, 0.2)',
    badgeColor: '#FF7D00',
    floatingPill: '★ 99Food Seleção Ouro',
    searchText: 'Buscar no cardápio 99 Food de OSHER...',
    promoText: '🎁 10% de Cashback no 99Pay + Taxa de Entrega Zero no primeiro pedido',
    headerBanner: 'assets/osher_delivery_header.jpg',
    category: '🔥 Promoções Exclusivas 99 Food',
    cartColor: '#FF7D00',
    buttonText: '+ Adicionar',
    products: [
      {
        title: 'PAGUE 2 LEVE 3 — 3 Copos de 200ml',
        desc: 'Super oferta de 3 copos individuais montados do seu jeito.',
        price: 'R$ 21,99',
        img: 'assets/stories1.jpg'
      },
      {
        title: 'Copo OSHER 700ml Turbinado',
        desc: 'Grande formato com 4 caldas e 5 acompanhamentos inclusos.',
        price: 'R$ 25,00',
        img: 'assets/cardapio1.jpg'
      },
      {
        title: 'Taça OSHER Sobremesa Especial',
        desc: 'Açaí swirl com frutas frescas em embalagem lacrada.',
        price: 'R$ 19,90',
        img: 'assets/feed3.jpg'
      },
      {
        title: 'Copo OSHER 300ml Clássico',
        desc: 'Sabor puro de açaí brasileiro equilibrado.',
        price: 'R$ 13,00',
        img: 'assets/feed1.jpg'
      }
    ]
  },
  proprio: {
    brandName: 'App OSHER Oficial • Clube VIP',
    rating: '5.0',
    reviews: '(1.200+ membros VIP)',
    time: '🚀 20-30 min • Logística Própria',
    fee: 'Frete 100% Grátis • 15% OFF Direto',
    themeColor: '#DD8901',
    badge: '👑 Clube VIP OSHER • 0% Taxas',
    badgeBg: 'rgba(221, 137, 1, 0.25)',
    badgeColor: '#FFDC8C',
    floatingPill: '👑 Canal Oficial OSHER',
    searchText: 'Buscar no App Oficial OSHER VIP...',
    promoText: '👑 Clube VIP: Sem taxas de intermediários + Pontos OSHER Ouro em dobro',
    headerBanner: 'assets/osher_store_ambiance.jpg',
    category: '👑 Experiência VIP Oficial • Monte do Seu Jeito',
    cartColor: '#DD8901',
    buttonText: '+ Pedir VIP',
    products: [
      {
        title: 'Copo OSHER 500ml VIP + Calda Manuka Gold',
        desc: 'Exclusividade do App Próprio: Ganhe pontos OSHER Ouro em dobro e monte com caldas e toppings à vontade.',
        price: 'R$ 17,00 (15% OFF)',
        img: 'assets/osher_bowls_mockup.jpg'
      },
      {
        title: 'Bowl Cerâmico Gourmet OSHER',
        desc: 'Açaí artesanal cremoso servido com frutas frescas do dia, pó dourado comestível e colher de bambu sustentável.',
        price: 'R$ 24,90',
        img: 'assets/cardapio1.jpg'
      },
      {
        title: 'Combo Fidelidade 2 Copos 500ml + Sacola Luxo',
        desc: 'Pedido oficial embalado com lacre de segurança hot stamping e brinde surpresa do Clube OSHER.',
        price: 'R$ 32,00',
        img: 'assets/osher_delivery_packaging.jpg'
      },
      {
        title: 'Mega Pote 1000ml Família Reserva Especial',
        desc: '1 Litro de pura densidade e cremosidade direto da fábrica para sua casa com 0% taxas de intermediação.',
        price: 'R$ 34,90',
        img: 'assets/cardapio2.jpg'
      }
    ]
  }
};

let cartItemsCount = 1;

function initAppTabs() {
  const tabs = document.querySelectorAll('.app-tab-btn');
  const claimBtn = document.getElementById('btnClaimCoupon');
  const cartBar = document.getElementById('appBottomCartBar');
  if (tabs.length === 0) return;

  tabs.forEach(tab => {
    tab.addEventListener('click', () => {
      const appKey = tab.dataset.app;
      tabs.forEach(t => t.classList.remove('active'));
      tab.classList.add('active');

      renderAppView(appKey);
      playClickSound();
    });
  });

  if (claimBtn) {
    claimBtn.addEventListener('click', () => {
      showToast('🎟️ Cupom de desconto ativado com sucesso para este app!');
      playClickSound();
    });
  }

  if (cartBar) {
    cartBar.addEventListener('click', () => {
      showToast(`🛒 Sacola: ${cartItemsCount} item(s) selecionado(s). Pedido pronto para envio!`);
      playClickSound();
    });
  }
}

function renderAppView(appKey) {
  const config = appConfigurations[appKey];
  if (!config) return;

  const container = document.getElementById('appMockupContainer');
  const titleEl = document.getElementById('app-store-title');
  const ratingEl = document.getElementById('app-rating-val');
  const reviewsEl = document.getElementById('app-reviews-val');
  const timeEl = document.getElementById('app-time-val');
  const feeEl = document.getElementById('app-fee-val');
  const badgeEl = document.getElementById('app-badge-val');
  const bannerImg = document.getElementById('app-header-img');
  const catTitleEl = document.getElementById('app-category-name');
  const productsContainer = document.getElementById('app-products-list');
  const floatingPillText = document.getElementById('appFloatingPillText');
  const searchPlaceholder = document.getElementById('appNavSearchText');
  const promoText = document.getElementById('appPromoText');
  const promoRibbon = document.getElementById('appPromoRibbon');
  const claimBtn = document.getElementById('btnClaimCoupon');
  const verifiedTick = document.getElementById('appVerifiedTick');
  const bottomCartBar = document.getElementById('appBottomCartBar');

  if (container) {
    container.style.borderColor = config.themeColor;
    container.style.boxShadow = `0 35px 90px rgba(0, 0, 0, 0.85), 0 0 40px ${config.themeColor}33`;
  }
  if (titleEl) titleEl.textContent = config.brandName;
  if (ratingEl) ratingEl.textContent = config.rating;
  if (reviewsEl) reviewsEl.textContent = config.reviews;
  if (timeEl) timeEl.textContent = config.time;
  if (feeEl) feeEl.textContent = config.fee;
  
  if (badgeEl) {
    badgeEl.textContent = config.badge;
    badgeEl.style.background = config.badgeBg;
    badgeEl.style.color = config.badgeColor;
  }
  if (bannerImg) bannerImg.src = config.headerBanner;
  if (catTitleEl) catTitleEl.textContent = config.category;
  if (floatingPillText) floatingPillText.textContent = config.floatingPill;
  if (searchPlaceholder) searchPlaceholder.textContent = config.searchText;
  if (promoText) promoText.textContent = config.promoText;

  if (promoRibbon) {
    promoRibbon.style.borderColor = `${config.themeColor}66`;
    promoRibbon.style.background = `${config.themeColor}1a`;
  }
  if (claimBtn) {
    claimBtn.style.backgroundColor = config.themeColor;
    if (appKey === 'keeta') claimBtn.style.color = '#000';
    else claimBtn.style.color = '#fff';
  }
  if (verifiedTick) {
    verifiedTick.style.backgroundColor = config.themeColor;
    if (appKey === 'keeta') verifiedTick.style.color = '#000';
    else verifiedTick.style.color = '#fff';
  }
  if (bottomCartBar) {
    bottomCartBar.style.backgroundColor = config.cartColor;
    if (appKey === 'keeta') {
      bottomCartBar.style.color = '#FFD100';
      bottomCartBar.style.border = '2px solid #FFD100';
    } else {
      bottomCartBar.style.color = '#fff';
      bottomCartBar.style.border = 'none';
    }
  }

  if (productsContainer) {
    productsContainer.innerHTML = '';
    config.products.forEach(p => {
      const card = document.createElement('div');
      card.className = 'app-product-card';
      card.innerHTML = `
        <div class="app-prod-details">
          <h4 class="app-prod-title">${p.title}</h4>
          <p class="app-prod-desc">${p.desc}</p>
          <div class="app-prod-action-row">
            <span class="app-prod-price">${p.price}</span>
            <button type="button" class="btn-add-item">${config.buttonText}</button>
          </div>
        </div>
        <img class="app-prod-img" src="${p.img}" alt="${p.title}" />
      `;

      const addBtn = card.querySelector('.btn-add-item');
      if (addBtn && appKey === 'keeta') {
        addBtn.style.borderColor = '#FFD100';
        addBtn.style.color = '#FFD100';
      } else if (addBtn) {
        addBtn.style.borderColor = config.themeColor;
        addBtn.style.color = config.themeColor;
      }

      card.addEventListener('click', () => {
        cartItemsCount++;
        const badge = document.querySelector('.cart-count-badge');
        if (badge) badge.textContent = cartItemsCount;
        showToast(`Item adicionado à sacola: ${p.title} (${p.price})`);
        playClickSound();
      });
      productsContainer.appendChild(card);
    });
  }
}

/* --------------------------------------------------------------------------
   10. Web Audio API for subtle micro-interactions
   -------------------------------------------------------------------------- */
let audioCtx = null;

function getAudioContext() {
  if (!audioCtx) {
    const AudioContextClass = window.AudioContext || window.webkitAudioContext;
    if (AudioContextClass) {
      audioCtx = new AudioContextClass();
    }
  }
  return audioCtx;
}

function playClickSound() {
  try {
    const ctx = getAudioContext();
    if (!ctx) return;
    if (ctx.state === 'suspended') ctx.resume();

    const osc = ctx.createOscillator();
    const gain = ctx.createGain();

    osc.type = 'sine';
    osc.frequency.setValueAtTime(800, ctx.currentTime);
    osc.frequency.exponentialRampToValueAtTime(400, ctx.currentTime + 0.05);

    gain.gain.setValueAtTime(0.08, ctx.currentTime);
    gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.05);

    osc.connect(gain);
    gain.connect(ctx.destination);

    osc.start();
    osc.stop(ctx.currentTime + 0.05);
  } catch (e) {
    // Audio context not allowed or supported
  }
}

function playStoryBeep() {
  try {
    const ctx = getAudioContext();
    if (!ctx || isAudioMuted) return;
    if (ctx.state === 'suspended') ctx.resume();

    const osc = ctx.createOscillator();
    const gain = ctx.createGain();

    osc.type = 'triangle';
    osc.frequency.setValueAtTime(520, ctx.currentTime);
    osc.frequency.exponentialRampToValueAtTime(660, ctx.currentTime + 0.08);

    gain.gain.setValueAtTime(0.1, ctx.currentTime);
    gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.08);

    osc.connect(gain);
    gain.connect(ctx.destination);

    osc.start();
    osc.stop(ctx.currentTime + 0.08);
  } catch (e) {}
}

function playWelcomeChime() {
  try {
    const ctx = getAudioContext();
    if (!ctx) return;
    if (ctx.state === 'suspended') ctx.resume();

    const notes = [440, 554.37, 659.25, 880];
    notes.forEach((freq, idx) => {
      const osc = ctx.createOscillator();
      const gain = ctx.createGain();

      osc.type = 'sine';
      osc.frequency.value = freq;

      const startTime = ctx.currentTime + idx * 0.08;
      gain.gain.setValueAtTime(0.06, startTime);
      gain.gain.exponentialRampToValueAtTime(0.0001, startTime + 0.35);

      osc.connect(gain);
      gain.connect(ctx.destination);

      osc.start(startTime);
      osc.stop(startTime + 0.35);
    });
  } catch (e) {}
}

/* --------------------------------------------------------------------------
   11. Mobile Menu Toggle
   -------------------------------------------------------------------------- */
function initMobileMenu() {
  const btn = document.querySelector('.mobile-menu-btn');
  const links = document.querySelector('.nav-links');

  if (!btn || !links) return;

  btn.addEventListener('click', () => {
    const isVisible = links.style.display === 'flex';
    links.style.display = isVisible ? 'none' : 'flex';
    links.style.position = isVisible ? '' : 'absolute';
    links.style.top = isVisible ? '' : '60px';
    links.style.left = isVisible ? '' : '0';
    links.style.right = isVisible ? '' : '0';
    links.style.flexDirection = isVisible ? '' : 'column';
    links.style.background = isVisible ? '' : 'rgba(20,20,20,0.96)';
    links.style.padding = isVisible ? '' : '20px';
    links.style.borderRadius = isVisible ? '' : '16px';
    links.style.border = isVisible ? '' : '1px solid rgba(221,137,1,0.3)';
  });
}
