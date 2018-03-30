function main() {

    setTimeout(function(){console.log("Ready")}, 10 * 1000)
}

// $(document).ready(main);

function trawl() {
    var username = $(".username").val()
    if (! username) {
        console.log("Please enter a username")
        $('.username').addClass("missing-username");
    } else {
        $('.username').removeClass("missing-username");
        console.log("Trawling Last.fm data for username: " + username)
    }
}