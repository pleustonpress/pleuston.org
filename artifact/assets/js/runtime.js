// Task ID: qa60100 & github issue #4
document.getElementById('search-form').addEventListener('submit', function(event) {
    event.preventDefault();
    // trim the query and redirect to search page
    var query = document.getElementById('query').value.trim();
    if (query) {
        window.location.href = 'https://blog.pleuston.org/search/?q=' + query;
    }else {
        window.location.href = 'https://blog.pleuston.org/search/';
    }
});

// https://github.com/pleustonpress/pleuston.org/issues/7
document.addEventListener('DOMContentLoaded', function() {
    var addToFavoritButton = document.getElementById('header-favourites');
    var EmailButton = document.getElementById('header-email');
    var instagramButton = document.getElementById('header-instagram');
    instagramButton.addEventListener('click', function(event) {
        event.preventDefault();
        // open instagram page
        window.location.href = 'https://www.instagram.com/';
    });
    EmailButton.addEventListener('click', function(event) {
        event.preventDefault();
        // open email client
        window.location.href ='mailto:help@pleuston.org';
    });
    addToFavoritButton.addEventListener('click', function(event) {
        event.preventDefault(); 

        var url = window.location.href; 
        var title = document.title; 

        if (window.sidebar && window.sidebar.addPanel) { // Firefox <23
            window.sidebar.addPanel(title, url, '');
        } else if (window.external && ('AddFavorite' in window.external)) { // IE
            window.external.AddFavorite(url, title);
        } else {
            alert('Use the Ctrl+D shortcut to add this page to your favorites.');
        }
    });
});

