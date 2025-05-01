// 登入彈窗開啟
const loginBtn = document.querySelector('.login');
const startBtn = document.querySelector('.start-btn');
const heroContent = document.querySelector('.hero-content');
const loginModal = document.createElement('div');

loginModal.id = 'login-modal';
loginModal.className = 'modal-overlay';
loginModal.style.display = 'none';

toggleLoginForm(); // 預設載入登入表單

document.body.appendChild(loginModal);

if (startBtn) {
  startBtn.onclick = function(e) {
    e.preventDefault();
    toggleLoginForm();
  };
}

function toggleLoginForm() {
  loginModal.innerHTML = `
    <div class="modal-content">
      <h2>登入</h2>
      <form id="login-form">
        <input type="text" class="modal-input" placeholder="輸入帳號" required style="margin-bottom:14px;">
        <input type="password" class="modal-input" placeholder="輸入密碼" required style="margin-bottom:18px;">
        <button type="submit" class="login-btn">登入</button>
      </form>
      <div class="modal-footer">
        尚未註冊？<a href="#" id="to-register">註冊</a>
      </div>
      <span class="modal-close">&times;</span>
    </div>
  `;
  bindModalEvents();
  // 新增：登入表單送出時導向home.html
  const loginForm = loginModal.querySelector('#login-form');
  if (loginForm) {
    loginForm.onsubmit = function(e) {
      e.preventDefault();
      window.location.href = '/homepage';
    };
  }
}

function toggleRegisterForm() {
  loginModal.innerHTML = `
    <div class="modal-content">
      <h2>註冊</h2>
      <form>
        <div class="input-group">
          <input type="email" class="modal-input" placeholder="輸入電子郵件" required>
          <button type="button" class="get-code-btn">取得驗證碼</button>
        </div>
        <input type="text" class="modal-input" placeholder="輸入驗證碼" required style="margin-bottom:14px;">
        <input type="password" class="modal-input" placeholder="設定密碼" required style="margin-bottom:14px;">
        <input type="password" class="modal-input" placeholder="再次輸入密碼" required style="margin-bottom:18px;">
        <button type="submit" class="login-btn">註冊</button>
      </form>
      <div class="modal-footer">
        已有帳號？<a href="#" id="to-login">返回登入</a>
      </div>
      <span class="modal-close">&times;</span>
    </div>
  `;
  bindModalEvents();
}

function bindModalEvents() {
  const toRegister = loginModal.querySelector('#to-register');
  if (toRegister) toRegister.onclick = (e) => { e.preventDefault(); toggleRegisterForm(); };
  const toLogin = loginModal.querySelector('#to-login');
  if (toLogin) toLogin.onclick = (e) => { e.preventDefault(); toggleLoginForm(); };
  const closeBtn = loginModal.querySelector('.modal-close');
  if (closeBtn) closeBtn.onclick = () => closeLoginModal();
  loginModal.onclick = function(e) {
    if (e.target === this) closeLoginModal();
  };
}

function openLoginModal(e) {
  if (e) e.preventDefault();
  loginModal.style.display = 'flex';
  if (heroContent) heroContent.style.display = 'none';
}

function closeLoginModal() {
  loginModal.style.display = 'none';
  if (heroContent) heroContent.style.display = '';
}

loginBtn.addEventListener('click', openLoginModal);
if (startBtn) startBtn.addEventListener('click', openLoginModal); 