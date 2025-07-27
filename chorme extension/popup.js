// Update the current time
function updateTime() {
  const timeElement = document.getElementById('current-time');
  const now = new Date();
  timeElement.textContent = now.toLocaleTimeString();
}


function decodeJWT(token) {
  if (!token) return null;
  const parts = token.split('.');
  if (parts.length !== 3) return null;
  try {
      const payload = parts[1]
          .replace(/-/g, '+')
          .replace(/_/g, '/');
      const decoded = atob(payload);
      return JSON.parse(decoded);
  } catch (e) {
      return null;
  }
}

function startTokenWatcher(exp) {

  const checkInterval = 30 * 1000; // 30 giây

  const intervalId = setInterval(() => {
    const now = Math.floor(Date.now() / 1000); // thời gian hiện tại (giây)
    const buffer = 60; // số giây đệm
    console.log("now", now)
    console.log("exp", exp)
    console.log("now + buffer - exp", now + buffer - exp)

      if (now + buffer >= exp) {
          console.log("Token sắp hết hạn, gọi refresh...");
          clearInterval(intervalId); // ngừng kiểm tra để tránh gọi nhiều lần
          refreshToken(); // gọi API refresh
      } else {
          console.log(`Kiểm tra token: còn ${exp - now} giây`);
      }
  }, checkInterval);
}

function refreshToken() {
  chrome.storage.local.get("username", (username) => {
    chrome.storage.local.get("password", (password) => {
      const apiData = {
        "email": username.username,
        "password": password.password
      };

      fetch('http://localhost:9119/e-commerce/v1.0/user/login', {
        method: 'POST',
        headers: {
            'accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(apiData)
      })
      .then(res => res.json())
      .then(data => {
          const newToken = data.data.result.token
          if (newToken) {

              chrome.storage.local.set({ token: data.data.result.token }, () => {
                console.log("Token đã được lưu vào chrome.storage.local!");
              });

              let payload = decodeJWT(newToken)
              startTokenWatcher(payload.exp); // tiếp tục theo dõi token mới
              console.log("Đã refresh token.");
          } else {
              console.error("Không nhận được token mới khi refresh.");
          }
      })
      .catch(err => {
          console.error("Lỗi khi refresh token:", err);
          // Chuyển hướng login nếu cần
      });
    })
  })

}

const loginBtn = document.getElementById('login-btn');
const logoutBtn = document.getElementById('logout-btn');


console.log("running")

logoutBtn.addEventListener('click', () => {
  const loginView = document.getElementById('login-view');
  const userView = document.getElementById('user-view');

  chrome.storage.local.remove("token", () => {
    console.log("Token đã bị xóa khỏi chrome.storage.local.");
  });

  chrome.storage.local.remove("username", () => {
    console.log("username đã bị xóa khỏi chrome.storage.local.");
  });

  chrome.storage.local.remove("password", () => {
    console.log("password đã bị xóa khỏi chrome.storage.local.");
  });
  
  loginView.style.display = 'block'
  userView.style.display = 'none'
})

loginBtn.addEventListener('click', () => {
  // Views
  const loginView = document.getElementById('login-view');
  const userView = document.getElementById('user-view');

  // Login Form Elements
  const loginBtn = document.getElementById('login-btn');
  const usernameInput = document.getElementById('username');
  const passwordInput = document.getElementById('password');
  const rememberMeCheckbox = document.getElementById('remember-me');
  const loginError = document.getElementById('login-error');

  // User View Elements
  const userDisplayName = document.getElementById('user-display-name');
  const logoutBtn = document.getElementById('logout-btn');

  const username = usernameInput.value;
  const password = passwordInput.value;

  // Basic validation
  if (!username || !password) {
    loginError.textContent = 'Vui lòng nhập đầy đủ thông tin.';
    return;
  }

  loginError.textContent = ''; // Clear previous errors


  // Gọi API
  const apiData = {
    "email": username,
    "password": password
  };
  fetch('http://localhost:9119/e-commerce/v1.0/user/login', {
      method: 'POST',
      headers: {
          'accept': 'application/json',
          'Content-Type': 'application/json'
      },
      body: JSON.stringify(apiData)
  })
  .then(response => {
      if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
      }
      return response.json();
  })
  .then(data => {
    console.log(data)
    
    const token = data.data.result.token;
    const payload = decodeJWT(token);
    console.log('Payload:', payload);
    userDisplayName.textContent = payload.email;

    loginView.style.display = 'none'
    userView.style.display = 'block'

    chrome.storage.local.set({ token: data.data.result.token }, () => {
      console.log("Token đã được lưu vào chrome.storage.local!");
    });

    chrome.storage.local.set({ username: username }, () => {
      console.log("username đã được lưu vào chrome.storage.local!");
    });

    chrome.storage.local.set({ password: password }, () => {
      console.log("password đã được lưu vào chrome.storage.local!");
    });
    startTokenWatcher(payload.exp)
  })
  .catch(error => {
      console.error('API Error:', error);
      loginError.textContent = 'Thông tin đăng nhập không chính xác!';
  });

});

chrome.storage.local.get("token", (result) => {
  if(result.token){
    console.log("result", result)
    const loginView = document.getElementById('login-view');
    const userView = document.getElementById('user-view');
    const userDisplayName = document.getElementById('user-display-name');
    
    const token = result.token;
    const payload = decodeJWT(token);
    console.log('Payload:', payload);
    userDisplayName.textContent = payload.email;

    loginView.style.display = 'none'
    userView.style.display = 'block'
    startTokenWatcher(payload.exp)
  }
  else{
    const loginView = document.getElementById('login-view');
    const userView = document.getElementById('user-view');

    loginView.style.display = 'block'
    userView.style.display = 'none'
  }
});

chrome.storage.local.get("username", (result) => {
  if(result.username){
    console.log("result", result)
  }
});