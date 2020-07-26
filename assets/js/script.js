// App initialization code goes here

const axios = require('axios')
//import 'axios'

$(document).ready(function () {
    // Sidebar init
    $("#sidebar").mCustomScrollbar({
        theme: "minimal"
    });
    // Sidebar management
    $('#sidebarCollapse').on('click', function () {
        $('#sidebar, #content').toggleClass('active');
        $('.collapse.in').toggleClass('in');
        $('a[aria-expanded=true]').attr('aria-expanded', 'false');
    });

    // Login form submitted. Get JWT
    $('#loginForm').submit(function(event) {
        var username = $('#loginForm #username').val()
        var password = $('#loginForm #password').val()
        var content = {'username': username, 'password': password}
        var url = 'http://' + window.location.hostname + ':5000/auth/login'
        var config = {
            headers: {
                'Content-Type': 'application/json',
            }
          }
        axios.post(url, content, config)
        .then(function (response) {
            localStorage.setItem('refresh_token', response.data['refresh_token'])
            localStorage.setItem('access_token', response.data['access_token'])
        })
        .catch(function (error) {
            console.log(error)
        });   
    });

    // Logout. Remove JWT
    $('#logoutButton').on('click', function(event) {
        localStorage.removeItem('refresh_token')
        localStorage.removeItem('access_token')
    });

});