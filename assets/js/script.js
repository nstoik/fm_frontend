// App initialization code goes here

const axios = require('axios');
// import 'axios'

$(document).ready(() => {
  // Sidebar init
  $('#sidebar').mCustomScrollbar({
    theme: 'minimal',
  });
  // Sidebar management
  $('#sidebarCollapse').on('click', () => {
    $('#sidebar, #content').toggleClass('active');
    $('.collapse.in').toggleClass('in');
    $('a[aria-expanded=true]').attr('aria-expanded', 'false');
  });

  // Login form submitted. Get JWT
  // eslint-disable-next-line no-unused-vars
  $('#loginForm').submit((event) => {
    const username = $('#loginForm #username').val();
    const password = $('#loginForm #password').val();
    const content = { username, password };
    const url = `http://${window.location.hostname}:5000/auth/login`;
    const config = {
      headers: {
        'Content-Type': 'application/json',
      },
    };
    axios.post(url, content, config)
      .then((response) => {
        localStorage.setItem('refresh_token', response.data.refresh_token);
        localStorage.setItem('access_token', response.data.access_token);
      })
      .catch((error) => {
        // eslint-disable-next-line no-console
        console.log(error);
      });
  });

  // Logout. Remove JWT
  // eslint-disable-next-line no-unused-vars
  $('#logoutButton').on('click', (event) => {
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('access_token');
  });
});
