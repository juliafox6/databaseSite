const ad = document.querySelector(".ad");
const footer=document.querySelector(".footer");

function hideAd() {
  ad.style.display = "none";
}

const register = {
  addits_artist: document.querySelector('.addits_artist'),
  addits_customer: document.querySelector('.addits_customer'),
  show(el) {
    el.classList.remove('up_hide');
  },
  hide(el) {
    el.classList.add('up_hide');
  },
  addEventListener() {
    document.querySelector('.artist').onclick = () => {
      this.show(this.addits_artist);
      this.hide(this.addits_customer);
    }
    document.querySelector('.customer').onclick = () => {
      this.show(this.addits_customer);
      this.hide(this.addits_artist);
    }
  }
}

register.addEventListener();

function checkPassword() {
  let value1 = document.getElementById('password').value;
  let value2 = document.getElementById('repeat').value;
  let but = document.querySelector('.button_login')
  let el = document.querySelector('.error');
  if (value1 !== value2) {
    el.classList.remove('up_hide');
    but.setAttribute('disabled', 'disabled');
  }
    else {
      el.classList.add('up_hide');
      but.removeAttribute('disabled');
    }
}

function checkFields() {
  let field1 = document.getElementById('surname').value;
  let field2 = document.getElementById('name').value;
  let field3 = document.getElementById('email').value;
  let field4 = document.getElementById('password').value;
  let field5 = document.getElementById('phone').value;
  let field6 = document.getElementById('artist').value;
  let field7 = document.getElementById('customer').value;
  let field8 = document.getElementById('about').value;
  let but = document.querySelector('.button_login');
  let el = document.querySelector('.notification1')
  if (field1 === '' || field2 === '' || field3 === '' || field4 === '' || field5 === '' || (field6 === '' || field7 === '') || field8 === '') {
    el.classList.remove('up_hide');
    but.setAttribute('disabled', 'disabled');
  }
  else {
    el.classList.add('up_hide');
    but.removeAttribute('disabled');
  }
}

const btnUp = {
  el: document.querySelector('.up'),
  show() {
    this.el.classList.remove('up_hide');
    },
  hide() {
    this.el.classList.add('up_hide');
    },
  addEventListener() {
    window.addEventListener('scroll', () => {
      const scrollY = window.scrollY || document.documentElement.scrollTop;
      scrollY > 200 ? this.show() : this.hide();
    });
    document.querySelector('.up').onclick = () => {
      window.scrollTo({
        top: 0,
        left: 0,
        behavior: 'smooth'
      });
    }
  }
}

btnUp.addEventListener();

const avoidFooter = {
  ad: document.querySelector('.ad'),
  main: document.querySelector('main'),
  footer: document.querySelector('.footer'),
  body: document.querySelector('body'),
  avoid() {
    let mainAdPosition = this.main.getBoundingClientRect().bottom + window.scrollY - this.ad.getBoundingClientRect().height;
    this.ad.style.position = 'absolute';
    this.ad.style.top = String(mainAdPosition) + 'px';
  },
  returnBack() {
    this.ad.style.position = 'fixed';
    this.ad.style.top = '18.5rem';
  },
  checkOffset() {
    window.addEventListener("scroll", () => {
      let adAbsPosition = this.ad.getBoundingClientRect().bottom + window.scrollY;
      let mainAbsPosition = this.main.getBoundingClientRect().bottom + window.scrollY;
      let breakPoint = window.innerHeight - this.footer.getBoundingClientRect().height;
      let mainBottomPosition = this.body.getBoundingClientRect().bottom - 60;
      if (adAbsPosition >= (mainAbsPosition)) {
        this.avoid();
      }
      if (mainBottomPosition > breakPoint) {
        this.returnBack();
      }
    })      
    },
};

avoidFooter.checkOffset();